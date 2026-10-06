#!/usr/bin/env python3
"""
quality_dip_scan.py
===================
"Quality on sale" scanner: large, profitable, growing companies with a
healthy balance sheet whose share price is sitting near its 52-week low --
the same setup as buying MSFT around $340 in mid-2026 (near the yearly low,
revenue growing ~18%, ~40% net margin, more cash than it needs).

Two stages, so the slow per-ticker fundamentals lookups only run on names
that already pass the cheap price screen:

  1. Price screen -- one chunked yf.download() of 1y daily closes for the
     stock universe (S&P 500 + the themed VSA watchlist from watchlists.py).
     Keep tickers trading within DIP_MAX_ABOVE_LOW of their 52-week low.
  2. Fundamentals screen -- yf.Ticker(t).info for each survivor, checked
     against the quality thresholds below. Names failing exactly one check
     are listed separately as "close calls" so a near-miss isn't invisible.

Being near a low is not a buy signal on its own -- a stock can be cheap
because the business is getting worse (see MOS). That's why every
fundamentals check here must pass, not just the price screen.

USAGE
-----
    python scripts/quality_dip_scan.py                 # writes reports/quality_dip_latest.md
    python scripts/quality_dip_scan.py -o /tmp/x.md
"""
from __future__ import annotations

import argparse
import math
import os
import sys
import time
from datetime import date

import watchlists as wl

CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "150"))
TOP_N = int(os.environ.get("TOP_N", "25"))  # cap on the "close calls" table
# Price screen: last close at most this far above the 52-week low (0.15 = 15%).
DIP_MAX_ABOVE_LOW = float(os.environ.get("DIP_MAX_ABOVE_LOW", "0.15"))
# Fundamentals screen (all must pass).
MIN_MARKET_CAP = float(os.environ.get("MIN_MARKET_CAP", "10e9"))        # large, established companies
MIN_REVENUE_GROWTH = float(os.environ.get("MIN_REVENUE_GROWTH", "0.05"))  # year-over-year, latest quarter
MIN_PROFIT_MARGIN = float(os.environ.get("MIN_PROFIT_MARGIN", "0.10"))    # net margin
# Net debt / EBITDA. Net cash (negative net debt) always passes. Measured
# against EBITDA rather than requiring cash > debt because Yahoo's totalDebt
# includes lease liabilities -- on a strict cash-vs-debt test even MSFT fails.
MAX_NET_DEBT_TO_EBITDA = float(os.environ.get("MAX_NET_DEBT_TO_EBITDA", "1.5"))

HISTORY_PERIOD = "1y"


def _chunks(items: list[str], size: int) -> list[list[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def stock_universe() -> list[str]:
    """S&P 500 plus the themed VSA watchlist, minus ETFs/FX/crypto/futures
    (no fundamentals to screen)."""
    non_stock_groups = {"ETFs", "CRYPTO & FX", "COMMODITIES"}
    tickers = set(wl.SP500)
    for group, members in wl.VSA_ASSETS.items():
        if group not in non_stock_groups:
            tickers.update(members)
    return sorted(tickers)


# ─────────────────────────────────────────────────────────────────────────
# Stage 1 -- price screen
# ─────────────────────────────────────────────────────────────────────────
def price_screen(tickers: list[str]) -> dict[str, dict]:
    """Return {ticker: {close, low, high, above_low, off_high}} for tickers
    within DIP_MAX_ABOVE_LOW of their 52-week low. Lows/highs use daily
    closes, so they can differ slightly from Yahoo's intraday 52w range."""
    import yfinance as yf

    hits: dict[str, dict] = {}
    chunks = _chunks(tickers, CHUNK_SIZE)
    for idx, chunk in enumerate(chunks, start=1):
        print(f"  [price] chunk {idx}/{len(chunks)} ({len(chunk)} tickers)", file=sys.stderr)
        data = None
        for attempt in range(3):
            try:
                data = yf.download(
                    tickers=chunk, period=HISTORY_PERIOD, interval="1d",
                    group_by="ticker", threads=True, progress=False, auto_adjust=True,
                )
                break
            except Exception as exc:  # noqa: BLE001 -- chunk-level network hiccup, not fatal
                print(f"    [price] retry {attempt + 1} after error: {exc}", file=sys.stderr)
                time.sleep(5 * (attempt + 1))
        if data is None:
            continue
        for ticker in chunk:
            try:
                closes = (data[ticker] if len(chunk) > 1 else data)["Close"].dropna()
            except (KeyError, TypeError):
                continue
            if len(closes) < 100:  # too little history for a meaningful 52w range
                continue
            close, low, high = float(closes.iloc[-1]), float(closes.min()), float(closes.max())
            if low <= 0:
                continue
            above_low = close / low - 1
            if above_low <= DIP_MAX_ABOVE_LOW:
                hits[ticker] = {
                    "close": close, "low": low, "high": high,
                    "above_low": above_low, "off_high": close / high - 1,
                }
        time.sleep(1)
    return hits


# ─────────────────────────────────────────────────────────────────────────
# Stage 2 -- fundamentals screen
# ─────────────────────────────────────────────────────────────────────────
def _num(info: dict, key: str) -> float | None:
    v = info.get(key)
    if isinstance(v, (int, float)) and not math.isnan(v):
        return float(v)
    return None


def fetch_fundamentals(ticker: str) -> dict | None:
    import yfinance as yf

    for attempt in range(3):
        try:
            info = yf.Ticker(ticker).info or {}
            break
        except Exception as exc:  # noqa: BLE001
            print(f"    [fundamentals] {ticker} retry {attempt + 1}: {exc}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    else:
        return None
    cash, debt, ebitda = _num(info, "totalCash"), _num(info, "totalDebt"), _num(info, "ebitda")
    net_debt = (debt or 0.0) - (cash or 0.0) if (cash is not None or debt is not None) else None
    return {
        "name": info.get("shortName") or ticker,
        "sector": info.get("sector") or "—",
        "market_cap": _num(info, "marketCap"),
        "revenue_growth": _num(info, "revenueGrowth"),
        "profit_margin": _num(info, "profitMargins"),
        "fcf": _num(info, "freeCashflow"),
        "net_debt": net_debt,
        "ebitda": ebitda,
        "forward_pe": _num(info, "forwardPE"),
    }


def failed_checks(f: dict) -> list[str]:
    """Names of the quality checks this company fails. Missing data counts
    as a failure -- the scan only vouches for what it can see."""
    fails = []
    if f["market_cap"] is None or f["market_cap"] < MIN_MARKET_CAP:
        fails.append("size")
    if f["revenue_growth"] is None or f["revenue_growth"] < MIN_REVENUE_GROWTH:
        fails.append("growth")
    if f["profit_margin"] is None or f["profit_margin"] < MIN_PROFIT_MARGIN:
        fails.append("margin")
    if f["fcf"] is None or f["fcf"] <= 0:
        fails.append("FCF")
    nd, ebitda = f["net_debt"], f["ebitda"]
    if nd is None:
        fails.append("balance sheet")
    elif nd > 0 and (ebitda is None or ebitda <= 0 or nd / ebitda > MAX_NET_DEBT_TO_EBITDA):
        fails.append("balance sheet")
    return fails


# ─────────────────────────────────────────────────────────────────────────
# Report
# ─────────────────────────────────────────────────────────────────────────
def _pct(v: float | None) -> str:
    return "—" if v is None else f"{v * 100:+.1f}%"


def _bn(v: float | None) -> str:
    return "—" if v is None else f"${v / 1e9:,.1f}B"


def _leverage(f: dict) -> str:
    nd, ebitda = f["net_debt"], f["ebitda"]
    if nd is None:
        return "—"
    if nd <= 0:
        return f"net cash {_bn(-nd)}"
    if ebitda and ebitda > 0:
        return f"{nd / ebitda:.1f}x"
    return "n/a"


def format_table(rows: list[tuple[str, dict, dict, list[str]]], show_fails: bool) -> str:
    if not rows:
        return "_None today._\n"
    header = "| # | Ticker | Name | Sector | Price | Above 52w low | Off 52w high | Rev growth | Net margin | FCF (ttm) | Net debt/EBITDA | Fwd P/E |"
    align = "|---|--------|------|--------|------:|------:|------:|------:|------:|------:|------:|------:|"
    if show_fails:
        header += " Fails |"
        align += "-------|"
    lines = [header, align]
    for i, (t, p, f, fails) in enumerate(rows, start=1):
        pe = "—" if f["forward_pe"] is None else f"{f['forward_pe']:.1f}"
        line = (
            f"| {i} | {t} | {f['name']} | {f['sector']} | ${p['close']:,.2f} | {_pct(p['above_low'])} | "
            f"{_pct(p['off_high'])} | {_pct(f['revenue_growth'])} | {_pct(f['profit_margin'])} | "
            f"{_bn(f['fcf'])} | {_leverage(f)} | {pe} |"
        )
        if show_fails:
            line += f" {', '.join(fails)} |"
        lines.append(line)
    return "\n".join(lines) + "\n"


def build_report(universe_size: int, price_hits: dict[str, dict],
                 results: list[tuple[str, dict, dict, list[str]]]) -> str:
    passes = [r for r in results if not r[3]]
    close_calls = [r for r in results if len(r[3]) == 1][:TOP_N]
    today = date.today().isoformat()
    return "\n".join([
        f"# Quality Dip Scan — {today}",
        "",
        f"Stocks trading within {DIP_MAX_ABOVE_LOW:.0%} of their 52-week low that still look "
        f"financially strong: market cap ≥ ${MIN_MARKET_CAP / 1e9:,.0f}B, revenue growth ≥ "
        f"{MIN_REVENUE_GROWTH:.0%}, net margin ≥ {MIN_PROFIT_MARGIN:.0%}, positive free cash flow, "
        f"and net cash or net debt ≤ {MAX_NET_DEBT_TO_EBITDA:g}x EBITDA.",
        "",
        f"Universe: {universe_size} stocks (S&P 500 + themed watchlist). "
        f"{len(price_hits)} passed the price screen; {len(passes)} passed every quality check.",
        "",
        "_Near a low is not a buy signal by itself — check why the stock fell before buying. "
        "Fundamentals are Yahoo Finance snapshots (latest quarter / trailing 12 months). Not financial advice._",
        "",
        "## Quality dips — pass every check (closest to 52-week low first)",
        format_table(passes, show_fails=False),
        f"## Close calls — fail exactly one check (closest {TOP_N} to their low)",
        format_table(close_calls, show_fails=True),
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-o", "--output", default="reports/quality_dip_latest.md")
    args = parser.parse_args()

    universe = stock_universe()
    print(f"Price screen: {len(universe)} stocks, keeping those within "
          f"{DIP_MAX_ABOVE_LOW:.0%} of their 52-week low...", file=sys.stderr)
    price_hits = price_screen(universe)
    print(f"  {len(price_hits)} near their lows", file=sys.stderr)

    print("Fetching fundamentals for price-screen survivors...", file=sys.stderr)
    results = []
    for i, ticker in enumerate(sorted(price_hits), start=1):
        f = fetch_fundamentals(ticker)
        if f is None:
            print(f"    [{i}/{len(price_hits)}] {ticker}: no fundamentals, skipped", file=sys.stderr)
            continue
        results.append((ticker, price_hits[ticker], f, failed_checks(f)))
        time.sleep(0.3)  # be polite -- one quoteSummary request per ticker
    results.sort(key=lambda r: r[1]["above_low"])

    report = build_report(len(universe), price_hits, results)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(f"Wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
