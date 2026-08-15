#!/usr/bin/env python3
"""Scan the S&P 500, Nasdaq Composite, and a fixed ETF watchlist for the
biggest volume spikes: tickers whose most recent session's volume is
highest relative to their trailing 50-session and 100-session average.

Requires real internet access (Yahoo Finance + Nasdaq Trader symbol
directory). Intended to run on GitHub Actions, not in a sandboxed
environment with restricted egress.
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import urllib.request
from datetime import date

import pandas as pd
import requests
import yfinance as yf

import plot_vsa2d

WINDOWS = (50, 100)
TOP_N = int(os.environ.get("TOP_N", "25"))
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "150"))
# Minimum trailing-average daily volume (shares) required to qualify for the
# ranking. Filters out illiquid names (e.g. SPAC units trading a few hundred
# shares/day) where a tiny absolute move produces a meaningless huge ratio.
MIN_AVG_VOLUME = int(os.environ.get("MIN_AVG_VOLUME", "100000"))
HISTORY_PERIOD = "9mo"  # comfortably covers 100+ trading sessions
# How many chart-worthy tickers to pull full OHLCV history for (fresh-volume-
# high tickers are always included on top of this; see build_chart_set).
CHART_TOP_N = int(os.environ.get("CHART_TOP_N", "10"))
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/plain,text/html,application/xhtml+xml,*/*;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs",
}

NASDAQ_LISTED_FILENAME = "nasdaqlisted.txt"
NASDAQ_LISTED_HTTPS_URL = f"https://www.nasdaqtrader.com/dynamic/SymDirectory/{NASDAQ_LISTED_FILENAME}"
NASDAQ_LISTED_FTP_URL = f"ftp://ftp.nasdaqtrader.com/symboldirectory/{NASDAQ_LISTED_FILENAME}"
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


def _parse_symbol_directory(text: str, source: str) -> pd.DataFrame:
    lines = [ln for ln in text.strip().splitlines() if ln.strip()]
    if not lines:
        raise ValueError(f"Empty response from {source}")

    header = [h.strip() for h in lines[0].split("|")]
    if header[0].lower() != "symbol":
        raise ValueError(
            f"{source} did not return the expected symbol directory "
            f"(first line was: {lines[0][:200]!r})"
        )

    ncols = len(header)
    rows = []
    skipped = 0
    # Skip the header and any trailing footer line(s) (e.g. "File Creation
    # Time: ...") or other malformed rows that don't match the header width.
    for ln in lines[1:]:
        fields = [f.strip() for f in ln.split("|")]
        if len(fields) == ncols:
            rows.append(fields)
        else:
            skipped += 1
    if skipped:
        print(f"  {source}: skipped {skipped} malformed line(s)", file=sys.stderr)
    print(f"  {source}: columns = {header}, rows = {len(rows)}", file=sys.stderr)
    return pd.DataFrame(rows, columns=header)


def _fetch_symbol_directory(https_url: str, ftp_url: str) -> pd.DataFrame:
    try:
        resp = requests.get(https_url, headers=REQUEST_HEADERS, timeout=30)
        resp.raise_for_status()
        return _parse_symbol_directory(resp.text, https_url)
    except Exception as exc:  # noqa: BLE001
        print(f"  {https_url} failed ({exc}); falling back to FTP", file=sys.stderr)

    with urllib.request.urlopen(ftp_url, timeout=30) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    return _parse_symbol_directory(text, ftp_url)


def fetch_nasdaq_composite() -> list[str]:
    nasdaq_df = _fetch_symbol_directory(NASDAQ_LISTED_HTTPS_URL, NASDAQ_LISTED_FTP_URL)
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


def download_ohlcv(tickers: list[str]) -> dict[str, list[dict]]:
    """Download full daily OHLCV history (not just Volume) for a small set of
    chart-worthy tickers, for the price/volume report. Uses auto_adjust so
    Close reflects splits/dividends the same way the Colab notebook's
    `t.history()` calls do."""
    ohlcv: dict[str, list[dict]] = {}
    if not tickers:
        return ohlcv
    chunks = [tickers[i : i + CHUNK_SIZE] for i in range(0, len(tickers), CHUNK_SIZE)]
    for idx, chunk in enumerate(chunks, start=1):
        print(f"  OHLCV chunk {idx}/{len(chunks)} ({len(chunk)} tickers)", file=sys.stderr)
        for attempt in range(3):
            try:
                data = yf.download(
                    tickers=chunk,
                    period=HISTORY_PERIOD,
                    interval="1d",
                    group_by="ticker",
                    threads=True,
                    progress=False,
                    auto_adjust=True,
                )
                break
            except Exception as exc:  # noqa: BLE001
                print(f"    retry {attempt + 1} after error: {exc}", file=sys.stderr)
                time.sleep(5 * (attempt + 1))
        else:
            continue

        for ticker in chunk:
            try:
                df = data[ticker] if len(chunk) > 1 else data
                df = df.dropna(subset=["Close"])
            except (KeyError, TypeError):
                continue
            if df.empty:
                continue
            rows = [
                {
                    "t": ts.strftime("%Y-%m-%d"),
                    "o": None if pd.isna(row["Open"]) else round(float(row["Open"]), 6),
                    "h": None if pd.isna(row["High"]) else round(float(row["High"]), 6),
                    "l": None if pd.isna(row["Low"]) else round(float(row["Low"]), 6),
                    "c": round(float(row["Close"]), 6),
                    "v": None if pd.isna(row["Volume"]) else int(row["Volume"]),
                }
                for ts, row in df.iterrows()
            ]
            ohlcv[ticker] = rows
        time.sleep(1)
    return ohlcv


def build_chart_set(
    universes: dict[str, list[str]],
    volumes: dict[str, pd.Series],
    top_n: int,
) -> dict[str, dict]:
    """Pick the tickers worth putting a 3D chart in front of a human for:
    every "fresh volume high" (the genuine breakouts) plus the top
    `CHART_TOP_N` from each universe/window ranking (the headline spikes),
    deduped, in a stable order. Returns {ticker: {"category", "note"}}."""
    flagged: dict[str, dict] = {}

    for uni_name, tickers in universes.items():
        breakout_df = find_volume_breakouts(tickers, volumes, top_n)
        for row in breakout_df.itertuples(index=False):
            flagged.setdefault(row.Ticker, {
                "category": f"{uni_name} — Fresh Volume High",
                "note": f"{row.Ratio:.2f}x 100d max",
            })
        for window in WINDOWS:
            rank_df = rank_universe(tickers, volumes, window, CHART_TOP_N)
            for row in rank_df.itertuples(index=False):
                flagged.setdefault(row.Ticker, {
                    "category": f"{uni_name} — Top Volume Spike",
                    "note": f"{row.Ratio:.2f}x {window}d avg",
                })
    return flagged


def rank_universe(tickers: list[str], volumes: dict[str, pd.Series], window: int, top_n: int) -> pd.DataFrame:
    """Rank by how far the most recent session's volume exceeds the trailing
    `window`-session average (computed from the sessions *before* today, so
    today's spike isn't diluting its own baseline)."""
    rows = []
    for t in tickers:
        vol = volumes.get(t)
        if vol is None or len(vol) < window + 1:
            continue
        latest = vol.iloc[-1]
        baseline = vol.iloc[-(window + 1) : -1].mean()
        if baseline < MIN_AVG_VOLUME:
            continue
        rows.append({
            "Ticker": t,
            "LatestVolume": latest,
            "AvgVolume": baseline,
            "Ratio": latest / baseline,
        })
    if not rows:
        return pd.DataFrame(columns=["Ticker", "LatestVolume", "AvgVolume", "Ratio"])
    df = pd.DataFrame(rows).sort_values("Ratio", ascending=False).head(top_n)
    for col in ("LatestVolume", "AvgVolume"):
        df[col] = df[col].round(0).astype("int64")
    df["Ratio"] = df["Ratio"].round(2)
    return df.reset_index(drop=True)


def format_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No data available._\n"
    lines = [
        "| # | Ticker | Latest Volume | Avg Volume | vs Avg |",
        "|---|--------|---------------:|-----------:|-------:|",
    ]
    for i, row in enumerate(df.itertuples(index=False), start=1):
        lines.append(
            f"| {i} | {row.Ticker} | {row.LatestVolume:,} | {row.AvgVolume:,} | {row.Ratio:.2f}x |"
        )
    return "\n".join(lines) + "\n"


def find_volume_breakouts(tickers: list[str], volumes: dict[str, pd.Series], top_n: int) -> pd.DataFrame:
    """Tickers whose most recent session's volume is higher than every one
    of the trailing 50 sessions AND every one of the trailing 100 sessions
    (a fresh volume high on both timeframes at once)."""
    rows = []
    for t in tickers:
        vol = volumes.get(t)
        if vol is None or len(vol) < 101:
            continue
        latest = vol.iloc[-1]
        prior_50 = vol.iloc[-51:-1]
        prior_100 = vol.iloc[-101:-1]
        if prior_50.mean() < MIN_AVG_VOLUME:
            continue
        max_50, max_100 = prior_50.max(), prior_100.max()
        if latest > max_50 and latest > max_100:
            rows.append({
                "Ticker": t,
                "LatestVolume": latest,
                "Max50": max_50,
                "Max100": max_100,
                "Ratio": latest / max_100,
            })
    if not rows:
        return pd.DataFrame(columns=["Ticker", "LatestVolume", "Max50", "Max100", "Ratio"])
    df = pd.DataFrame(rows).sort_values("Ratio", ascending=False).head(top_n)
    for col in ("LatestVolume", "Max50", "Max100"):
        df[col] = df[col].round(0).astype("int64")
    df["Ratio"] = df["Ratio"].round(2)
    return df.reset_index(drop=True)


def format_breakout_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_None qualified._\n"
    lines = [
        "| # | Ticker | Latest Volume | Prior 50d Max | Prior 100d Max | vs 100d Max |",
        "|---|--------|---------------:|---------------:|----------------:|------------:|",
    ]
    for i, row in enumerate(df.itertuples(index=False), start=1):
        lines.append(
            f"| {i} | {row.Ticker} | {row.LatestVolume:,} | {row.Max50:,} | "
            f"{row.Max100:,} | {row.Ratio:.2f}x |"
        )
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
        f"ETFs = {len(etfs)}. Ranked by the most recent session's volume relative to the "
        f"trailing 50/100-session average (biggest volume spikes first). Tickers averaging "
        f"under {MIN_AVG_VOLUME:,} shares/day are excluded to filter out illiquid noise.",
        "",
    ]
    for uni_name, tickers in universes.items():
        report_lines.append(f"## {uni_name}")
        shown = min(TOP_N, len(tickers))
        for window in WINDOWS:
            report_lines.append(
                f"### Top {shown} — latest session volume vs {window}-session average"
            )
            df = rank_universe(tickers, volumes, window, TOP_N)
            report_lines.append(format_table(df))

        report_lines.append(
            "### Fresh volume highs — latest session above every one of the "
            "trailing 50 AND 100 sessions"
        )
        breakout_df = find_volume_breakouts(tickers, volumes, TOP_N)
        report_lines.append(format_breakout_table(breakout_df))
    report = "\n".join(report_lines)

    os.makedirs("reports", exist_ok=True)
    dated_path = f"reports/volume_report_{today}.md"
    with open(dated_path, "w") as f:
        f.write(report)
    with open("reports/latest.md", "w") as f:
        f.write(report)

    print(f"Wrote {dated_path} and reports/latest.md", file=sys.stderr)

    # --- price/volume charts (Colab "Multi-Chart Price + Volume Viewer" logic) ---
    # Chart every fresh-volume-high plus each universe's top volume-spike
    # names. These are exactly the tickers the markdown report calls out, so
    # the ranking work above is reused rather than re-scanned.
    print("Building chart ticker set...", file=sys.stderr)
    flagged = build_chart_set(universes, volumes, TOP_N)
    print(f"  {len(flagged)} tickers flagged for charts", file=sys.stderr)

    print(f"Downloading OHLCV history for {len(flagged)} chart tickers...", file=sys.stderr)
    ohlcv = download_ohlcv(sorted(flagged))
    print(f"  got OHLCV for {len(ohlcv)} tickers", file=sys.stderr)

    data_path = f"reports/volume_data_{today}.json"
    bundle = {"report_date": today, "flagged": flagged, "ohlcv": ohlcv}
    with open(data_path, "w") as f:
        json.dump(bundle, f)
    with open("reports/volume_data_latest.json", "w") as f:
        json.dump(bundle, f)

    html = plot_vsa2d.build_report_html(today, flagged, ohlcv)
    html_path = f"reports/volume_2d_{today}.html"
    with open(html_path, "w") as f:
        f.write(html)
    with open("reports/volume_2d_latest.html", "w") as f:
        f.write(html)

    print(f"Wrote {html_path}, reports/volume_2d_latest.html, and {data_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
