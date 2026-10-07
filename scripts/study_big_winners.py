#!/usr/bin/env python3
"""
study_big_winners.py
====================
What did stocks that went on to gain 60%+ over the next 12 months have in
common *before* the run, compared with every other stock at the same time?

Observations: every stock at every month-end since 2005 (S&P 500 from its
join date + Nasdaq-100 + watchlist, prices from backtest_quality_dip.py's
cache). Outcome: total return over the next 12 months >= WINNER (60%).
For each trait measured at the month-end (price trend, volatility, distance
from highs/lows, big up-days, financials from the latest 10-K filed by then,
sector, market regime), the report shows how often stocks with that trait
became big winners vs the base rate ("lift" = 2.0x means twice as likely).

Observations overlap (the same stock in consecutive months, many stocks in
the same rally), so treat lifts as descriptive, not as independent tests.
Today's index lists only, so companies that collapsed are missing.

USAGE
-----
    python scripts/backtest_quality_dip.py ...   # once, to fill .cache/backtest
    python scripts/study_big_winners.py --nibii-dir ../NIBII
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import date

import numpy as np
import pandas as pd

WINNER = 0.60
LOSER = -0.40   # the other side of the same coin: fell 40%+ over the next 12 months


def latest_10k(records: list[dict], when: str) -> dict | None:
    known = [r for r in records if r["filed"] <= when]
    return max(known, key=lambda r: r["end"]) if known else None


def build(prices: pd.DataFrame, fundamentals: dict, added: dict, sectors: dict) -> pd.DataFrame:
    spy = prices["SPY"]
    daily_ret = prices.pct_change(fill_method=None)
    vol63 = daily_ret.rolling(63, min_periods=50).std() * np.sqrt(252)
    hi252 = prices.rolling(252, min_periods=240).max()
    lo252 = prices.rolling(252, min_periods=240).min()
    sma200 = prices.rolling(200, min_periods=190).mean()
    big_day = (daily_ret >= 0.10).astype(float).rolling(63, min_periods=1).max()  # a +10% day in the last 3 months

    month_ends = prices.groupby(prices.index.to_period("M")).tail(1).index
    pos = {d: i for i, d in enumerate(prices.index)}
    rows = []
    stocks = [t for t in prices.columns if t != "SPY"]
    for m, d in enumerate(month_ends):
        i = pos[d]
        if i < 252 or m + 12 >= len(month_ends):
            continue
        fwd_d = month_ends[m + 12]
        p0, p12 = prices.iloc[i], prices.loc[fwd_d]
        p_6, p_1 = prices.iloc[i - 126], prices.iloc[i - 21]
        mom = p_1 / p_6 - 1
        spy_mom = spy.iloc[i - 21] / spy.iloc[i - 126] - 1
        ds = d.strftime("%Y-%m-%d")
        eligible = [t for t in stocks if not (pd.isna(p0[t]) or pd.isna(p12[t]) or pd.isna(mom[t]))
                    and (t not in added or added[t] <= ds)]
        if len(eligible) < 50:
            continue
        rank = mom[eligible].rank(ascending=False)
        spy_up = spy.iloc[i] > spy.iloc[i - 200:i].mean()
        for t in eligible:
            f = latest_10k(fundamentals.get(t, []), ds)
            rev_g = margin = fcf_pos = net_cash = None
            if f and f.get("revenue") and f["revenue"] > 0:
                if f.get("prior_revenue") and f["prior_revenue"] > 0:
                    rev_g = f["revenue"] / f["prior_revenue"] - 1
                if f.get("net_income") is not None:
                    margin = f["net_income"] / f["revenue"]
                if f.get("ocf") is not None:
                    fcf_pos = f["ocf"] - (f.get("capex") or 0) > 0
                if f.get("cash") is not None:
                    net_cash = f["cash"] >= (f.get("debt") or 0)
            rows.append(dict(
                date=ds, ticker=t, fwd=p12[t] / p0[t] - 1,
                mom6_1=mom[t], mom_rank=rank[t], n=len(eligible), beat_spy=mom[t] > spy_mom,
                ret1m=p0[t] / prices.iloc[i - 21][t] - 1,
                vol=vol63.iloc[i][t], off_high=p0[t] / hi252.iloc[i][t] - 1, above_low=p0[t] / lo252.iloc[i][t] - 1,
                above_sma=p0[t] > sma200.iloc[i][t], big_day=bool(big_day.iloc[i][t]),
                rev_g=rev_g, margin=margin, fcf_pos=fcf_pos, net_cash=net_cash,
                sector=sectors.get(t, "Other"), spy_up=spy_up))
    df = pd.DataFrame(rows)
    df["winner"] = df["fwd"] >= WINNER
    df["loser"] = df["fwd"] <= LOSER
    return df


def lift_table(df: pd.DataFrame, title: str, groups: list[tuple[str, pd.Series]]) -> list[str]:
    base = df["winner"].mean()
    out = [f"### {title}", "", "| Group | Share of stock-months | Became 60%+ winners | Lift | Fell 40%+ | Avg 12-month return |",
           "|---|---:|---:|---:|---:|---:|"]
    for label, mask in groups:
        g = df[mask]
        if len(g) < 200:
            continue
        out.append(f"| {label} | {len(g) / len(df):.0%} | {g['winner'].mean():.1%} | "
                   f"{g['winner'].mean() / base:.1f}x | {g['loser'].mean():.1%} | {g['fwd'].mean():+.0%} |")
    return out + [""]


def deciles(df: pd.DataFrame, col: str, title: str, fmt: str) -> list[str]:
    d = df.dropna(subset=[col]).copy()
    d["q"] = pd.qcut(d[col], 10, labels=False, duplicates="drop")
    base = df["winner"].mean()
    out = [f"### {title}", "", "| Decile (low → high) | Range | Became 60%+ winners | Lift | Fell 40%+ | Median 12-month return |",
           "|---|---|---:|---:|---:|---:|"]
    for q, g in d.groupby("q"):
        out.append(f"| {q + 1} | {fmt.format(g[col].min())} to {fmt.format(g[col].max())} | "
                   f"{g['winner'].mean():.1%} | {g['winner'].mean() / base:.1f}x | {g['loser'].mean():.1%} | {g['fwd'].median():+.0%} |")
    return out + [""]


def profile(df: pd.DataFrame) -> list[str]:
    w, r = df[df["winner"]], df[~df["winner"]]
    rows = [("6-1 month return", "mom6_1", "{:+.0%}"), ("Momentum rank (1 = strongest)", "mom_rank", "{:.0f}"),
            ("Last month's return", "ret1m", "{:+.1%}"), ("Volatility (annualized)", "vol", "{:.0%}"),
            ("Distance from 52-week high", "off_high", "{:+.0%}"), ("Above 52-week low", "above_low", "{:+.0%}"),
            ("Revenue growth (last 10-K)", "rev_g", "{:+.0%}"), ("Net margin (last 10-K)", "margin", "{:+.0%}")]
    out = ["| Trait (median) | 60%+ winners | Everyone else |", "|---|---:|---:|"]
    for label, col, fmt in rows:
        out.append(f"| {label} | {fmt.format(w[col].median())} | {fmt.format(r[col].median())} |")
    for label, col in (("Beat SPY over 6-1 months", "beat_spy"), ("Above 200-day average", "above_sma"),
                       ("Had a +10% day in last 3 months", "big_day"), ("Positive free cash flow", "fcf_pos"),
                       ("Net cash", "net_cash"), ("SPY in uptrend (above 200-day)", "spy_up")):
        out.append(f"| {label} | {w[col].dropna().astype(float).mean():.0%} | {r[col].dropna().astype(float).mean():.0%} |")
    return out + [""]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nibii-dir", required=True)
    parser.add_argument("--cache-dir", default=".cache/backtest")
    parser.add_argument("-o", "--output", default="reports/big_winners_study.md")
    args = parser.parse_args()

    prices = pd.read_pickle(os.path.join(args.cache_dir, "prices.pkl"))
    with open(os.path.join(args.cache_dir, "fundamentals.json")) as fh:
        fundamentals = json.load(fh)
    added, sectors = {}, {}
    with open(os.path.join(args.nibii_dir, "data", "sp500.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            sectors[r["symbol"]] = r["sector"]
            if r.get("added"):
                added[r["symbol"]] = r["added"]
    with open(os.path.join(args.nibii_dir, "data", "ndx100.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            sectors.setdefault(r["symbol"], r["industry"])

    print("Building stock-month table...", file=sys.stderr)
    df = build(prices, fundamentals, added, sectors)
    base = df["winner"].mean()
    winners = df[df["winner"]]

    top = df["mom_rank"]
    lines = [
        f"# What 60%+ Winners Had in Common — {date.today().isoformat()}",
        "",
        f"Every stock at every month-end from {df['date'].min()[:7]} to {df['date'].max()[:7]} "
        f"({len(df):,} stock-months, {df['ticker'].nunique()} stocks). A *winner* gained {WINNER:.0%}+ "
        f"(dividends included) over the next 12 months; 'fell 40%+' is the mirror image ({df['loser'].mean():.1%} of all). "
        f"Winners: **{len(winners):,} stock-months, {base:.1%} of all** "
        f"— the base rate. Lift = how much more often than the base rate a group became winners. "
        f"Observations overlap and the lists are today's index members, so read this as a description, not proof.",
        "",
        "## Winners vs everyone else, at the start",
        "",
        *profile(df),
        "## Which traits raised the odds",
        "",
        *lift_table(df, "Momentum (6-month return skipping the last month, ranked across all stocks)", [
            ("Top 5", top <= 5), ("Ranks 6-20", (top > 5) & (top <= 20)), ("Ranks 21-50", (top > 20) & (top <= 50)),
            ("Top 10% of stocks", top <= df["n"] * 0.1), ("Bottom 10% of stocks", top > df["n"] * 0.9),
            ("Beat SPY", df["beat_spy"]), ("Lagged SPY", ~df["beat_spy"])]),
        *lift_table(df, "Volatility and recent moves", [
            ("Had a +10% day in the last 3 months", df["big_day"]), ("No +10% day", ~df["big_day"]),
            ("Volatility above 50%", df["vol"] > 0.5), ("Volatility below 25%", df["vol"] < 0.25),
            ("Within 5% of 52-week high", df["off_high"] >= -0.05), ("30%+ below 52-week high", df["off_high"] <= -0.30),
            ("Above 200-day average", df["above_sma"]), ("Below 200-day average", ~df["above_sma"])]),
        *lift_table(df, "Financials (latest 10-K filed by then)", [
            ("Revenue growth 25%+", df["rev_g"] >= 0.25), ("Revenue growth 10-25%", (df["rev_g"] >= 0.10) & (df["rev_g"] < 0.25)),
            ("Revenue growth under 5%", df["rev_g"] < 0.05), ("Net margin 20%+", df["margin"] >= 0.20),
            ("Net margin negative", df["margin"] < 0), ("Positive free cash flow", df["fcf_pos"] == True),  # noqa: E712
            ("Negative free cash flow", df["fcf_pos"] == False), ("Net cash", df["net_cash"] == True),  # noqa: E712
            ("Net debt", df["net_cash"] == False)]),  # noqa: E712
        *lift_table(df, "Combinations", [
            ("Top 10% momentum + revenue growth 25%+", (top <= df["n"] * 0.1) & (df["rev_g"] >= 0.25)),
            ("Top 10% momentum + volatility above 50%", (top <= df["n"] * 0.1) & (df["vol"] > 0.5)),
            ("Top 10% momentum + +10% day in last 3 months", (top <= df["n"] * 0.1) & df["big_day"]),
            ("Revenue growth 25%+ + volatility above 50%", (df["rev_g"] >= 0.25) & (df["vol"] > 0.5)),
            ("Top 10% momentum + low volatility (<25%)", (top <= df["n"] * 0.1) & (df["vol"] < 0.25))]),
        *lift_table(df, "Market backdrop", [("SPY above its 200-day average", df["spy_up"]),
                                            ("SPY below its 200-day average", ~df["spy_up"])]),
        *deciles(df, "vol", "By volatility decile", "{:.0%}"),
        *deciles(df, "mom6_1", "By 6-1 month return decile", "{:+.0%}"),
        "### By sector", "",
        "| Sector | Stock-months | Became 60%+ winners | Lift |", "|---|---:|---:|---:|",
    ]
    for sec, g in sorted(df.groupby("sector"), key=lambda x: -x[1]["winner"].mean()):
        if len(g) >= 500:
            lines.append(f"| {sec} | {len(g):,} | {g['winner'].mean():.1%} | {g['winner'].mean() / base:.1f}x |")
    lines += ["", "### Winners by start year", "", "| Year | Stock-months | Became 60%+ winners |", "|---|---:|---:|"]
    for y, g in df.groupby(df["date"].str[:4]):
        lines.append(f"| {y} | {len(g):,} | {g['winner'].mean():.1%} |")
    lines += ["", "### Most frequent big winners", "", "| Ticker | Months it was the start of a 60%+ year |", "|---|---:|"]
    for t, n in winners["ticker"].value_counts().head(15).items():
        lines.append(f"| {t} | {n} |")

    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"Wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
