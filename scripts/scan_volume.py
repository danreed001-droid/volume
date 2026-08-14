#!/usr/bin/env python3
"""Scan the S&P 500, Nasdaq Composite, and a fixed ETF watchlist for highest
trailing average daily volume over the last 50 and 100 trading sessions.

Requires real internet access (Yahoo Finance + Nasdaq Trader symbol
directory). Intended to run on GitHub Actions, not in a sandboxed
environment with restricted egress.
"""
from __future__ import annotations

import io
import os
import sys
import time
from datetime import date

import pandas as pd
import requests
import yfinance as yf

WINDOWS = (50, 100)
TOP_N = int(os.environ.get("TOP_N", "25"))
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "150"))
HISTORY_PERIOD = "9mo"  # comfortably covers 100+ trading sessions
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (volume-scanner)"}

NASDAQ_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/SymDirectory/nasdaqlisted.txt"
SP500_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Fixed ETF watchlist (not the full ETF universe) per user request.
FIXED_ETFS = ["XLE", "XLF", "GLD", "TLT", "XLB", "SPY", "EEM", "QQQ", "SLV", "XLRE"]


def _clean_symbol(sym: str) -> str:
    """Normalize exchange symbol formats to what yfinance expects."""
    return sym.strip().replace(".", "-").replace("$", "-P")


def _valid_ticker(sym: str) -> bool:
    if not sym or len(sym) > 6:
        return False
    return all(c.isalnum() or c == "-" for c in sym)


def fetch_sp500() -> list[str]:
    resp = requests.get(SP500_WIKI_URL, headers=REQUEST_HEADERS, timeout=30)
    resp.raise_for_status()
    tables = pd.read_html(io.StringIO(resp.text))
    df = tables[0]
    return sorted({_clean_symbol(s) for s in df["Symbol"].astype(str) if _valid_ticker(_clean_symbol(s))})


def _fetch_symbol_directory(url: str) -> pd.DataFrame:
    resp = requests.get(url, headers=REQUEST_HEADERS, timeout=30)
    resp.raise_for_status()
    lines = resp.text.strip().splitlines()
    # Last line is a "File Creation Time" footer, not data.
    lines = [ln for ln in lines if not ln.startswith("File Creation Time")]
    return pd.read_csv(io.StringIO("\n".join(lines)), sep="|")


def fetch_nasdaq_composite() -> list[str]:
    nasdaq_df = _fetch_symbol_directory(NASDAQ_LISTED_URL)
    nasdaq_common = nasdaq_df[
        (nasdaq_df["Test Issue"] == "N") & (nasdaq_df["ETF"] == "N")
    ]["Symbol"]
    return sorted({_clean_symbol(s) for s in nasdaq_common.astype(str) if _valid_ticker(_clean_symbol(s))})


def download_volumes(tickers: list[str]) -> dict[str, pd.Series]:
    """Download daily volume history for tickers, chunked to stay polite to Yahoo."""
    volumes: dict[str, pd.Series] = {}
    chunks = [tickers[i : i + CHUNK_SIZE] for i in range(0, len(tickers), CHUNK_SIZE)]
    for idx, chunk in enumerate(chunks, start=1):
        print(f"  chunk {idx}/{len(chunks)} ({len(chunk)} tickers)", file=sys.stderr)
        for attempt in range(3):
            try:
                data = yf.download(
                    tickers=chunk,
                    period=HISTORY_PERIOD,
                    interval="1d",
                    group_by="ticker",
                    threads=True,
                    progress=False,
                    auto_adjust=False,
                )
                break
            except Exception as exc:  # noqa: BLE001
                print(f"    retry {attempt + 1} after error: {exc}", file=sys.stderr)
                time.sleep(5 * (attempt + 1))
        else:
            continue

        for ticker in chunk:
            try:
                if len(chunk) == 1:
                    vol = data["Volume"]
                else:
                    vol = data[ticker]["Volume"]
            except (KeyError, TypeError):
                continue
            vol = vol.dropna()
            if not vol.empty:
                volumes[ticker] = vol
        time.sleep(1)  # be polite between chunks
    return volumes


def rank_universe(tickers: list[str], volumes: dict[str, pd.Series], window: int, top_n: int) -> pd.DataFrame:
    rows = []
    for t in tickers:
        vol = volumes.get(t)
        if vol is None or len(vol) < window:
            continue
        avg = vol.tail(window).mean()
        rows.append({"Ticker": t, "AvgVolume": avg})
    df = pd.DataFrame(rows).sort_values("AvgVolume", ascending=False).head(top_n)
    df["AvgVolume"] = df["AvgVolume"].round(0).astype("int64")
    return df.reset_index(drop=True)


def format_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No data available._\n"
    lines = ["| # | Ticker | Avg Daily Volume |", "|---|--------|------------------:|"]
    for i, row in enumerate(df.itertuples(index=False), start=1):
        lines.append(f"| {i} | {row.Ticker} | {row.AvgVolume:,} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    print("Fetching ticker universes...", file=sys.stderr)
    sp500 = fetch_sp500()
    nasdaq_composite = fetch_nasdaq_composite()
    etfs = sorted({_clean_symbol(s) for s in FIXED_ETFS})
    universes = {
        "S&P 500": sp500,
        "Nasdaq Composite": nasdaq_composite,
        "ETFs": etfs,
    }
    print(
        f"  S&P 500: {len(sp500)} | Nasdaq Composite: {len(nasdaq_composite)} | ETFs: {len(etfs)}",
        file=sys.stderr,
    )

    all_tickers = sorted(set(sp500) | set(nasdaq_composite) | set(etfs))
    print(f"Downloading volume history for {len(all_tickers)} unique tickers...", file=sys.stderr)
    volumes = download_volumes(all_tickers)
    print(f"  got data for {len(volumes)} tickers", file=sys.stderr)

    today = date.today().isoformat()
    report_lines = [
        f"# Volume Scan — {today}",
        "",
        f"Universe sizes: S&P 500 = {len(sp500)}, Nasdaq Composite = {len(nasdaq_composite)}, "
        f"ETFs = {len(etfs)}. Ranked by trailing average daily volume (shares/day).",
        "",
    ]
    for uni_name, tickers in universes.items():
        report_lines.append(f"## {uni_name}")
        shown = min(TOP_N, len(tickers))
        for window in WINDOWS:
            report_lines.append(f"### Top {shown} by avg volume — trailing {window} sessions")
            df = rank_universe(tickers, volumes, window, TOP_N)
            report_lines.append(format_table(df))
    report = "\n".join(report_lines)

    os.makedirs("reports", exist_ok=True)
    dated_path = f"reports/volume_report_{today}.md"
    with open(dated_path, "w") as f:
        f.write(report)
    with open("reports/latest.md", "w") as f:
        f.write(report)

    print(f"Wrote {dated_path} and reports/latest.md", file=sys.stderr)


if __name__ == "__main__":
    main()
