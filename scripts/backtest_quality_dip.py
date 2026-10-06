#!/usr/bin/env python3
"""
backtest_quality_dip.py
=======================
Historical check of the quality_dip_scan.py idea: when a stock qualified
(near its 52-week low AND financially strong), how did it do afterwards?

Signals are evaluated at every month-end:
  - near low:  month-end close within DIP_MAX_ABOVE_LOW of the trailing
               252-session closing low (same price screen as the live scan)
  - quality:   using only the latest 10-K the company had *filed* by that
               date (no look-ahead), the same checks as the live scan --
               revenue growth, net margin, positive FCF, net cash or net
               debt <= MAX_NET_DEBT_TO_EBITDA x EBITDA. The market-cap check
               is skipped: $10B meant something very different in 2010.
After a signal, the same ticker is ignored for COOLDOWN_MONTHS so one long
slide isn't counted as a dozen separate buys.

Each signal's forward 1y and 3y total return (dividend-adjusted) is compared
with SPY over the same window. Three groups are reported:
  A. every near-low signal (prices only, ~20 years)
  B. near-low + passed quality (from when SEC XBRL financials exist, ~2010)
  C. near-low + FAILED quality (same period as B -- the "MOS-style" control)

Data sources: Yahoo Finance (prices) and SEC EDGAR companyfacts (financials).
SEC requires a contact in the User-Agent, read from the SEC_USER_AGENT
environment variable, e.g. SEC_USER_AGENT="Your Name you@example.com".

Universe: this repo's live-scan universe plus the S&P 500 (with index join
dates) and Nasdaq-100 lists maintained in the NIBII repo
(github.com/danreed001-droid/NIBII, data/sp500.csv + data/ndx100.csv). As in
NIBII's own backtests, an S&P 500 stock only produces signals from the date
it joined the index -- otherwise today's list smuggles in hindsight (stocks
get added after big runs).

Known biases (also printed in the report):
  - Survivorship: the universe is still *today's* index lists, so companies
    that collapsed and were dropped are missing. This flatters every group,
    group A the most.
  - XBRL tag coverage varies by company; missing data counts as failing
    quality, so banks/insurers rarely qualify.

USAGE
-----
    SEC_USER_AGENT="Name email@example.com" python scripts/backtest_quality_dip.py
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import time
from datetime import date, datetime

import pandas as pd
import requests

import quality_dip_scan as qds

START = "2004-01-01"  # one year of lookback before the first 2005 signals
DIP_MAX_ABOVE_LOW = qds.DIP_MAX_ABOVE_LOW
MIN_REVENUE_GROWTH = qds.MIN_REVENUE_GROWTH
MIN_PROFIT_MARGIN = qds.MIN_PROFIT_MARGIN
MAX_NET_DEBT_TO_EBITDA = qds.MAX_NET_DEBT_TO_EBITDA
COOLDOWN_MONTHS = int(os.environ.get("COOLDOWN_MONTHS", "12"))
HORIZONS = {"1y": 12, "3y": 36}  # months forward
BENCHMARK = "SPY"
PORTFOLIO_SINCE = "2011-01-03"  # first full year with point-in-time quality data

NIBII_RAW = "https://raw.githubusercontent.com/danreed001-droid/NIBII/main/data/{name}"

SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"

# XBRL tags, in order of preference. Companies switch tags over the years
# (e.g. SalesRevenueNet -> RevenueFromContractWithCustomer... after ASC 606),
# so for each fiscal year the first tag that has a value wins.
REVENUE_TAGS = [
    "RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet",
    "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet",
    "SalesRevenueServicesNet", "RevenuesNetOfInterestExpense",
]
NET_INCOME_TAGS = ["NetIncomeLoss", "ProfitLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]
OCF_TAGS = ["NetCashProvidedByUsedInOperatingActivities",
            "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"]
CAPEX_TAGS = ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets",
              "PaymentsForCapitalImprovements"]
OP_INCOME_TAGS = ["OperatingIncomeLoss"]
DA_TAGS = ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
           "DepreciationAmortizationAndAccretionNet", "Depreciation"]
CASH_TAGS = ["CashAndCashEquivalentsAtCarryingValue",
             "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", "Cash"]
SHORT_INVEST_TAGS = ["ShortTermInvestments", "MarketableSecuritiesCurrent", "AvailableForSaleSecuritiesCurrent"]
# Total long-term debt (incl. current portion) if reported; otherwise the
# non-current + current pieces are summed.
LTD_TOTAL_TAGS = ["LongTermDebt", "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities"]
LTD_NONCURRENT_TAGS = ["LongTermDebtNoncurrent", "LongTermDebtAndCapitalLeaseObligations"]
LTD_CURRENT_TAGS = ["LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligationsCurrent"]
SHORT_DEBT_TAGS = ["ShortTermBorrowings", "CommercialPaper", "DebtCurrent"]


# ─────────────────────────────────────────────────────────────────────────
# Universe (NIBII index lists)
# ─────────────────────────────────────────────────────────────────────────
def _nibii_csv(name: str, nibii_dir: str | None) -> list[dict]:
    if nibii_dir:
        with open(os.path.join(nibii_dir, "data", name), newline="") as fh:
            return list(csv.DictReader(fh))
    resp = requests.get(NIBII_RAW.format(name=name), timeout=30)
    resp.raise_for_status()
    return list(csv.DictReader(io.StringIO(resp.text)))


def load_universe(nibii_dir: str | None) -> tuple[list[str], dict[str, str]]:
    """(tickers, {ticker: date it joined the S&P 500})."""
    sp500 = _nibii_csv("sp500.csv", nibii_dir)
    ndx = _nibii_csv("ndx100.csv", nibii_dir)
    added = {r["symbol"]: r["added"] for r in sp500 if r.get("added")}
    tickers = set(qds.stock_universe()) | {r["symbol"] for r in sp500} | {r["symbol"] for r in ndx}
    return sorted(tickers), added


# ─────────────────────────────────────────────────────────────────────────
# Prices
# ─────────────────────────────────────────────────────────────────────────
def load_prices(tickers: list[str], cache_dir: str) -> pd.DataFrame:
    """Daily dividend/split-adjusted closes, one column per ticker. Cached;
    only tickers missing from the cache are downloaded."""
    path = os.path.join(cache_dir, "prices.pkl")
    cached = pd.read_pickle(path) if os.path.exists(path) else pd.DataFrame()
    todo = [t for t in tickers if t not in cached.columns]
    if not todo:
        return cached[[t for t in tickers if t in cached.columns]]
    import yfinance as yf

    frames = [cached] if not cached.empty else []
    for idx, chunk in enumerate(qds._chunks(todo, qds.CHUNK_SIZE), start=1):
        print(f"  [prices] chunk {idx} ({len(chunk)} tickers)", file=sys.stderr)
        for attempt in range(3):
            try:
                data = yf.download(tickers=chunk, start=START, interval="1d", group_by="ticker",
                                   threads=True, progress=False, auto_adjust=True)
                break
            except Exception as exc:  # noqa: BLE001
                print(f"    retry {attempt + 1}: {exc}", file=sys.stderr)
                time.sleep(5 * (attempt + 1))
        else:
            continue
        for t in chunk:
            try:
                s = (data[t] if len(chunk) > 1 else data)["Close"].dropna()
            except (KeyError, TypeError):
                continue
            if not s.empty:
                frames.append(s.rename(t))
        time.sleep(1)
    prices = pd.concat(frames, axis=1).sort_index()
    prices.to_pickle(path)
    return prices[[t for t in tickers if t in prices.columns]]


# ─────────────────────────────────────────────────────────────────────────
# SEC fundamentals
# ─────────────────────────────────────────────────────────────────────────
def _sec_get(url: str, user_agent: str) -> requests.Response:
    for attempt in range(4):
        resp = requests.get(url, headers={"User-Agent": user_agent}, timeout=60)
        if resp.status_code in (429, 503):
            time.sleep(2 ** attempt)
            continue
        return resp
    return resp


def _annual_series(facts: dict, tags: list[str], instant: bool) -> dict[str, tuple[float, str]]:
    """{period_end: (value, first_filed_date)} from 10-K facts, merging tags
    in preference order. Duration facts must span ~1 year. The *earliest*
    filing of each period is kept, so later restatements can't leak into the
    past."""
    out: dict[str, tuple[float, str]] = {}
    for tag in tags:
        units = facts.get(tag, {}).get("units", {}).get("USD", [])
        per_tag: dict[str, tuple[float, str]] = {}
        for f in units:
            if not str(f.get("form", "")).startswith("10-K"):
                continue
            if not instant:
                if "start" not in f:
                    continue
                days = (datetime.fromisoformat(f["end"]) - datetime.fromisoformat(f["start"])).days
                if not 350 <= days <= 380:
                    continue
            prev = per_tag.get(f["end"])
            if prev is None or f["filed"] < prev[1]:
                per_tag[f["end"]] = (float(f["val"]), f["filed"])
        for end, v in per_tag.items():
            out.setdefault(end, v)
    return out


def extract_annuals(companyfacts: dict) -> list[dict]:
    """One record per fiscal year: the metrics the quality checks need,
    plus 'filed' (when the market could first have known them)."""
    facts = companyfacts.get("facts", {}).get("us-gaap", {})
    rev = _annual_series(facts, REVENUE_TAGS, False)
    ni = _annual_series(facts, NET_INCOME_TAGS, False)
    ocf = _annual_series(facts, OCF_TAGS, False)
    capex = _annual_series(facts, CAPEX_TAGS, False)
    opi = _annual_series(facts, OP_INCOME_TAGS, False)
    da = _annual_series(facts, DA_TAGS, False)
    cash = _annual_series(facts, CASH_TAGS, True)
    sti = _annual_series(facts, SHORT_INVEST_TAGS, True)
    ltd_total = _annual_series(facts, LTD_TOTAL_TAGS, True)
    ltd_nc = _annual_series(facts, LTD_NONCURRENT_TAGS, True)
    ltd_c = _annual_series(facts, LTD_CURRENT_TAGS, True)
    std = _annual_series(facts, SHORT_DEBT_TAGS, True)

    def v(series, end):
        return series[end][0] if end in series else None

    records = []
    ends = sorted(rev)
    for i, end in enumerate(ends):
        prior = [e for e in ends[:i] if 340 <= (datetime.fromisoformat(end) - datetime.fromisoformat(e)).days <= 390]
        if end in ltd_total:
            debt = ltd_total[end][0]
        else:
            debt = (v(ltd_nc, end) or 0.0) + (v(ltd_c, end) or 0.0)
        debt += v(std, end) or 0.0
        records.append({
            "end": end,
            # Filed date of the 10-K that first reported this year's revenue.
            "filed": rev[end][1],
            "revenue": rev[end][0],
            "prior_revenue": rev[prior[-1]][0] if prior else None,
            "net_income": v(ni, end),
            "ocf": v(ocf, end),
            "capex": v(capex, end),
            "op_income": v(opi, end),
            "da": v(da, end),
            "cash": (v(cash, end) or 0.0) + (v(sti, end) or 0.0) if end in cash else None,
            "debt": debt,
        })
    return records


def load_fundamentals(tickers: list[str], cache_dir: str, user_agent: str) -> dict[str, list[dict]]:
    path = os.path.join(cache_dir, "fundamentals.json")
    cached: dict[str, list[dict]] = {}
    if os.path.exists(path):
        with open(path) as fh:
            cached = json.load(fh)

    todo = [t for t in tickers if t not in cached]
    if todo:
        cik_map = {row["ticker"].upper(): int(row["cik_str"])
                   for row in _sec_get(SEC_TICKERS_URL, user_agent).json().values()}
        for i, t in enumerate(todo, start=1):
            cik = cik_map.get(t) or cik_map.get(t.replace("-", "."))
            if cik is None:
                cached[t] = []
                continue
            resp = _sec_get(SEC_FACTS_URL.format(cik=cik), user_agent)
            cached[t] = extract_annuals(resp.json()) if resp.ok else []
            if i % 50 == 0:
                print(f"  [sec] {i}/{len(todo)}", file=sys.stderr)
                with open(path, "w") as fh:
                    json.dump(cached, fh)
            time.sleep(0.12)  # SEC fair-access limit is 10 requests/second
        with open(path, "w") as fh:
            json.dump(cached, fh)
    return cached


def quality_at(records: list[dict], when: pd.Timestamp) -> bool | None:
    """Did the latest 10-K filed on or before `when` pass every quality
    check? None if no 10-K had been filed yet (no XBRL data that early)."""
    known = [r for r in records if r["filed"] <= when.strftime("%Y-%m-%d")]
    if not known:
        return None
    r = max(known, key=lambda x: x["end"])
    rev, prior = r["revenue"], r["prior_revenue"]
    if not rev or rev <= 0 or not prior or prior <= 0 or rev / prior - 1 < MIN_REVENUE_GROWTH:
        return False
    if r["net_income"] is None or r["net_income"] / rev < MIN_PROFIT_MARGIN:
        return False
    if r["ocf"] is None or r["ocf"] - (r["capex"] or 0.0) <= 0:
        return False
    if r["cash"] is None:
        return False
    net_debt = r["debt"] - r["cash"]
    if net_debt > 0:
        if r["op_income"] is None or r["da"] is None:
            return False
        ebitda = r["op_income"] + r["da"]
        if ebitda <= 0 or net_debt / ebitda > MAX_NET_DEBT_TO_EBITDA:
            return False
    return True


# ─────────────────────────────────────────────────────────────────────────
# Signals + forward returns
# ─────────────────────────────────────────────────────────────────────────
def build_signals(prices: pd.DataFrame, fundamentals: dict[str, list[dict]],
                  added: dict[str, str]) -> pd.DataFrame:
    trailing_low = prices.rolling(252, min_periods=240).min()
    month_ends = prices.groupby(prices.index.to_period("M")).tail(1).index
    monthly = prices.loc[month_ends]
    monthly_low = trailing_low.loc[month_ends]
    bench = monthly[BENCHMARK]

    rows = []
    for t in prices.columns:
        if t == BENCHMARK:
            continue
        last_signal_idx = -10**9
        closes, lows = monthly[t].values, monthly_low[t].values
        joined = pd.Timestamp(added[t]) if t in added else None
        for i, when in enumerate(month_ends):
            if joined is not None and when.tz_localize(None) < joined:
                continue
            c, lo = closes[i], lows[i]
            if pd.isna(c) or pd.isna(lo) or lo <= 0 or c / lo - 1 > DIP_MAX_ABOVE_LOW:
                continue
            if i - last_signal_idx < COOLDOWN_MONTHS:
                continue
            last_signal_idx = i
            row = {"ticker": t, "date": when, "quality": quality_at(fundamentals.get(t, []), when)}
            for label, m in HORIZONS.items():
                j = i + m
                if j < len(month_ends) and not pd.isna(closes[j]):
                    row[label] = closes[j] / c - 1
                    row[f"{label}_spy"] = bench.iloc[j] / bench.iloc[i] - 1
            rows.append(row)
    return pd.DataFrame(rows)


def portfolio_curve(signals: pd.DataFrame, prices: pd.DataFrame, months_held: int) -> pd.Series:
    """Daily value of a portfolio that buys every quality signal at its
    month-end close and holds it for `months_held` months, equal-weight
    across whatever is held (rebalanced daily). Cash (0%) when nothing is
    held. Starts at the first quality signal."""
    q = signals[signals["quality"] == True]  # noqa: E712
    month_ends = prices.groupby(prices.index.to_period("M")).tail(1).index
    pos = {d: i for i, d in enumerate(month_ends)}
    rets = prices.pct_change(fill_method=None)
    held = pd.DataFrame(False, index=prices.index, columns=prices.columns)
    for _, r in q.iterrows():
        i = pos[pd.Timestamp(r["date"])]
        start = month_ends[i]
        end = month_ends[min(i + months_held, len(month_ends) - 1)]
        # held from the session after the buy close through the sell close
        held.loc[(held.index > start) & (held.index <= end), r["ticker"]] = True
    day_ret = rets.where(held).mean(axis=1).fillna(0.0)
    first = month_ends[pos[pd.Timestamp(q["date"].min())]]
    return (1 + day_ret[day_ret.index > first]).cumprod()


def curve_stats(values: pd.Series) -> dict:
    """Same definitions as NIBII's mtl.backtest.curve_stats: total, annual
    (252 sessions a year) and worst peak-to-trough drop."""
    total = values.iloc[-1] / values.iloc[0] - 1
    years = (len(values) - 1) / 252
    return {"total": total, "annual": (1 + total) ** (1 / years) - 1,
            "maxDD": (values / values.cummax() - 1).min()}


def portfolio_section(signals: pd.DataFrame, prices: pd.DataFrame, since: str, cache_dir: str) -> list[str]:
    spy = prices[BENCHMARK].dropna()
    curves = {f"Quality dips, hold {m // 12}y": portfolio_curve(signals, prices, m) for m in (12, 36)}
    curves["SPY"] = spy
    lines = [
        f"Since {since}. Every quality signal bought at its month-end close, equal weight, held 1 or 3 years.",
        "",
        "| Portfolio | Total | Per year | Worst drop | $10k became |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, c in curves.items():
        c = c[c.index >= since]
        st = curve_stats(c)
        lines.append(f"| {name} | {st['total']:+,.0%} | {st['annual']:+.1%} | {st['maxDD']:.0%} | "
                     f"${10000 * (1 + st['total']):,.0f} |")
    years = sorted({d.year for d in spy.index if d >= pd.Timestamp(since)})
    lines += ["", "| Year | " + " | ".join(curves) + " |", "|---|" + "---:|" * len(curves)]
    for y in years:
        cells = []
        for c in curves.values():
            c = c[c.index >= since]
            yr = c[c.index.year == y]
            prev = c[c.index.year < y]
            base = prev.iloc[-1] if not prev.empty else yr.iloc[0]
            cells.append(f"{yr.iloc[-1] / base - 1:+.0%}")
        lines.append(f"| {y} | " + " | ".join(cells) + " |")
    pd.DataFrame(curves).to_csv(os.path.join(cache_dir, "portfolio_curves.csv"))
    return lines


def results_header() -> list[str]:
    lines = [
        "| Group | Horizon | Signals | Avg return | Median return | % positive | Avg SPY same window | Avg excess vs SPY | % beat SPY |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    return lines


def group_rows(name: str, df: pd.DataFrame) -> list[str]:
    out = []
    for label in HORIZONS:
        if label not in df:
            continue
        d = df.dropna(subset=[label])
        if d.empty:
            continue
        excess = d[label] - d[f"{label}_spy"]
        out.append(
            f"| {name} | {label} | {len(d):,} | {d[label].mean():+.1%} | {d[label].median():+.1%} | "
            f"{(d[label] > 0).mean():.0%} | {d[f'{label}_spy'].mean():+.1%} | {excess.mean():+.1%} | "
            f"{(excess > 0).mean():.0%} |"
        )
    return out


def by_year(df: pd.DataFrame, label: str) -> list[str]:
    lines = [
        f"| Signal year | Quality signals | Avg {label} | vs SPY | Failed-quality signals | Avg {label} | vs SPY |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    d = df.dropna(subset=[label]).copy()
    d["year"] = d["date"].dt.year
    d["excess"] = d[label] - d[f"{label}_spy"]
    for year, g in d.groupby("year"):
        q, f = g[g["quality"] == True], g[g["quality"] == False]  # noqa: E712
        if q.empty and f.empty:
            continue

        def cells(x):
            return ("0", "—", "—") if x.empty else (f"{len(x)}", f"{x[label].mean():+.1%}", f"{x['excess'].mean():+.1%}")
        lines.append(f"| {year} | " + " | ".join(cells(q)) + " | " + " | ".join(cells(f)) + " |")
    return lines


def examples(df: pd.DataFrame, label: str, n: int = 10) -> list[str]:
    d = df[(df["quality"] == True)].dropna(subset=[label]).sort_values(label)  # noqa: E712
    lines = [f"| Ticker | Signal date | {label} return | SPY same window |", "|---|---|---:|---:|"]
    for _, r in pd.concat([d.tail(n).iloc[::-1], d.head(n)]).iterrows():
        lines.append(f"| {r['ticker']} | {r['date']:%Y-%m-%d} | {r[label]:+.1%} | {r[f'{label}_spy']:+.1%} |")
    return lines


def build_report(df: pd.DataFrame, n_tickers: int, n_with_fund: int, portfolio: list[str]) -> str:
    first_q = df[df["quality"].notna()]["date"].min()
    a = df
    b = df[df["quality"] == True]  # noqa: E712
    c = df[df["quality"] == False]  # noqa: E712
    a_same = df[df["quality"].notna()]
    return "\n".join([
        f"# Quality Dip Backtest — {date.today().isoformat()}",
        "",
        f"Month-end signals from {df['date'].min():%Y-%m} to {df['date'].max():%Y-%m} across {n_tickers} stocks "
        f"({n_with_fund} with SEC financials): today's S&P 500 and Nasdaq-100 (lists from the NIBII repo) plus "
        f"this repo's watchlist. S&P 500 stocks only count from the date they joined the index. A signal = month-end close within {DIP_MAX_ABOVE_LOW:.0%} of the "
        f"trailing 52-week low; a *quality* signal also passed revenue growth ≥ {MIN_REVENUE_GROWTH:.0%}, net "
        f"margin ≥ {MIN_PROFIT_MARGIN:.0%}, positive FCF, and net cash or net debt ≤ "
        f"{MAX_NET_DEBT_TO_EBITDA:g}x EBITDA, using only the latest 10-K filed by that date. "
        f"After a signal, that ticker is skipped for {COOLDOWN_MONTHS} months. Returns include dividends.",
        "",
        "## Results",
        "",
        *results_header(),
        *group_rows(f"A. All near-low signals ({df['date'].min():%Y}+)", a),
        *group_rows(f"A'. All near-low signals ({first_q:%Y}+)", a_same),
        *group_rows(f"B. Near low + quality ({first_q:%Y}+)", b),
        *group_rows(f"C. Near low, failed quality ({first_q:%Y}+)", c),
        "",
        "Compare B with C to see whether the quality checks help. A' covers the same years as B and C, "
        "so it's the fair price-only comparison.",
        "",
        "## As a portfolio",
        "",
        *portfolio,
        "",
        "## By signal year (3-year forward returns)",
        "",
        *by_year(df, "3y"),
        "",
        "## Best and worst quality signals (3-year forward return)",
        "",
        *examples(df, "3y"),
        "",
        "## Caveats",
        "",
        "- **Survivorship bias:** the universe is *today's* S&P 500 / Nasdaq-100 + watchlist. Companies that collapsed and "
        "left the index aren't here, so every group looks better than it would have in real time — the "
        "price-only group (A) most of all, since failing companies are exactly the ones that sit near lows.",
        "- Financials come from SEC XBRL filings, which start around 2009–2011, so quality results cover fewer years.",
        "- Missing XBRL data counts as failing quality, so banks/insurers and companies with unusual tags rarely qualify.",
        "- Signals overlap in time (many stocks dip together in a crash), so they are not independent bets. "
        "Not financial advice.",
        "",
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-o", "--output", default="reports/quality_dip_backtest.md")
    parser.add_argument("--nibii-dir", help="local NIBII checkout for data/sp500.csv + data/ndx100.csv "
                        "(default: fetch them from GitHub)")
    parser.add_argument("--cache-dir", default=".cache/backtest",
                        help="where downloaded prices/financials are cached between runs")
    args = parser.parse_args()

    user_agent = os.environ.get("SEC_USER_AGENT")
    if not user_agent:
        sys.exit('Set SEC_USER_AGENT, e.g. SEC_USER_AGENT="Your Name you@example.com" (SEC requires a contact).')
    os.makedirs(args.cache_dir, exist_ok=True)

    tickers, added = load_universe(args.nibii_dir)
    print(f"Loading prices for {len(tickers)} stocks + {BENCHMARK}...", file=sys.stderr)
    prices = load_prices(tickers + [BENCHMARK], args.cache_dir)
    print("Loading SEC financials...", file=sys.stderr)
    fundamentals = load_fundamentals([t for t in tickers if t in prices.columns], args.cache_dir, user_agent)

    signals = build_signals(prices, fundamentals, added)
    signals.to_csv(os.path.join(args.cache_dir, "signals.csv"), index=False)
    n_with_fund = sum(1 for t in prices.columns if fundamentals.get(t))
    portfolio = portfolio_section(signals, prices, PORTFOLIO_SINCE, args.cache_dir)
    report = build_report(signals, prices.shape[1] - 1, n_with_fund, portfolio)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(f"Wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
