#!/usr/bin/env python3
"""
backtest_gaps_and_midcaps.py
============================
Two ideas for bigger returns on top of NIBII's Auto + News boost, 2000-2026.

1. A NEWS-GAP PORTFOLIO on its own. NIBII's news gap (mtl/news.py: opened
   AND closed 12%+ above the prior close, closing in the upper 40% of the
   day's range) beat SPY by ~31% on average over the next 12 months
   (backtest_volume_spike.py). Here every gap is bought at the NEXT
   session's close and held HOLD sessions, two ways:
     - equal weight across every open position (fully invested whenever
       anything is held, cash otherwise)
     - 10 slots: each new gap gets 1/10 of the account if a slot is free,
       the rest stays in cash
   Plus 70/30 and 50/50 mixes with Boost, rebalanced weekly.
   Universe: S&P 500 (from each stock's join date) + Nasdaq-100.

2. A WIDER UNIVERSE for Boost: the same rule with today's S&P 400 mid-caps
   added. Each mid-cap counts only from the latest date Wikipedia's S&P 400
   change log shows it being added (names with no logged addition are
   assumed to have been members throughout -- some hindsight).

Both use today's index lists, so companies that later collapsed are
missing (survivorship bias). It flatters mid-caps more than large caps.

USAGE
-----
    python scripts/backtest_gaps_and_midcaps.py --nibii-dir ../NIBII
"""
from __future__ import annotations

import argparse
import io
import os
import pickle
import sys
from datetime import date

import numpy as np

COST = 0.001        # per side, a little above NIBII's 0.05% for these jumpier names
SLOTS = 10
SP400_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"
PERIODS = [("2000-01-01", "2009-12-31"), ("2010-01-01", "2019-12-31"), ("2020-01-01", "2026-12-31")]


def stats(curve, a="0000", b="9999"):
    v = [x for d, x in curve if a <= d <= b]
    total = v[-1] / v[0] - 1
    peak, dd = v[0], 0.0
    for x in v:
        peak = max(peak, x)
        dd = min(dd, x / peak - 1)
    ye, prev, worst = {}, v[0], 0.0
    for d, x in curve:
        if a <= d <= b:
            ye[d[:4]] = x
    for y in sorted(ye):
        worst = min(worst, ye[y] / prev - 1)
        prev = ye[y]
    return (1 + total) ** (252 / (len(v) - 1)) - 1, dd, worst


def gap_portfolios(bars, cal, start, eligible, news_gap_days, hold):
    """(equal-weight curve, 10-slot curve, average positions held) as [[date, value]]."""
    idx = {d: i for i, d in enumerate(cal)}
    n = len(cal)
    closes = {}
    for t, bs in bars.items():
        arr = np.full(n, np.nan)
        for b in bs:
            i = idx.get(b[0][:10])
            if i is not None:
                arr[i] = b[4]
        # carry the last close over missing sessions
        last = np.nan
        for i in range(n):
            if np.isnan(arr[i]):
                arr[i] = last
            else:
                last = arr[i]
        closes[t] = arr
    entries = []   # (entry index, exit index, ticker)
    for t, bs in bars.items():
        for d in news_gap_days(bs):
            i = idx.get(d)
            if i is None or i + 1 >= n or cal[i] < start or not eligible(t, cal[i]):
                continue
            entries.append((i + 1, min(i + 1 + hold, n - 1), t))
    entries.sort()

    s0 = idx[next(d for d in cal if d >= start)]
    # equal weight across open positions
    ew, val, open_count = [], 1.0, []
    by_day = {}
    for e, x, t in entries:
        for k in range(e + 1, x + 1):
            by_day.setdefault(k, []).append(t)
    starts = {}
    for e, x, t in entries:
        starts.setdefault(e, []).append(t)
    ends = {}
    for e, x, t in entries:
        ends.setdefault(x, []).append(t)
    for k in range(s0, n):
        held = by_day.get(k, [])
        if held:
            r = [closes[t][k] / closes[t][k - 1] - 1 for t in held
                 if closes[t][k - 1] > 0 and not np.isnan(closes[t][k])]
            if r:
                val *= 1 + float(np.mean(r))
        # trading cost on the share of the book that turned over today
        live = len(by_day.get(k, [])) or 1
        turned = len(starts.get(k, [])) + len(ends.get(k, []))
        val *= 1 - COST * min(1.0, turned / live)
        ew.append([cal[k], val])
        open_count.append(len(held))

    # 10 slots
    slots, cash, sl = {}, 1.0, []
    pending = {}
    for e, x, t in entries:
        pending.setdefault(e, []).append((x, t))
    for k in range(s0, n):
        for key in list(slots):
            t, x = key
            p0, p1 = closes[t][k - 1], closes[t][k]
            if p0 > 0 and not np.isnan(p1):
                slots[key] *= p1 / p0
            if k >= x:
                cash += slots.pop(key) * (1 - COST)
        nav = cash + sum(slots.values())
        for x, t in pending.get(k, []):
            if len(slots) < SLOTS and (t, x) not in slots and cash > 0:
                amt = min(cash, nav / SLOTS)
                cash -= amt
                slots[(t, x)] = amt * (1 - COST)
        sl.append([cal[k], cash + sum(slots.values())])
    return ew, sl, float(np.mean(open_count)), len(entries)


def mix(a, b, wa, cal):
    """Weekly-rebalanced wa in curve a, 1-wa in curve b (both [[date, value]])."""
    from mtl.momentum import last_sessions_of_weeks
    weeks = set(last_sessions_of_weeks(cal))
    bd = dict(b)
    out, prev, x, y = [], None, wa, 1 - wa
    for d, v in a:
        if d not in bd:
            continue
        if prev:
            x *= v / prev[0]
            y *= bd[d] / prev[1]
        out.append([d, x + y])
        if d in weeks:
            x, y = (x + y) * wa, (x + y) * (1 - wa)
        prev = (v, bd[d])
    return out


def sp400_with_dates():
    """{ticker: date added or '0000'} for today's S&P 400, Yahoo symbols."""
    import pandas as pd
    import requests
    html = requests.get(SP400_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=60).text
    tables = pd.read_html(io.StringIO(html))
    members = {s.replace(".", "-") for s in tables[0]["Symbol"].astype(str)}
    ch = tables[1]
    ch.columns = ["date", "add_t", "add_s", "rem_t", "rem_s", "reason"]
    added = {}
    for _, r in ch.iterrows():
        t = str(r["add_t"]).replace(".", "-")
        try:
            d = pd.to_datetime(r["date"]).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            continue
        if t in members and d > added.get(t, "0000"):
            added[t] = d
    return {t: added.get(t, "0000") for t in members}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nibii-dir", required=True)
    parser.add_argument("--cache", default="/tmp/midcap_bars.pkl", help="where mid-cap prices are cached")
    parser.add_argument("-o", "--output", default="reports/gaps_and_midcaps.md")
    args = parser.parse_args()
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), args.output)

    nibii = os.path.abspath(args.nibii_dir)
    sys.path[:0] = [nibii, os.path.join(nibii, "scripts")]
    os.chdir(nibii)
    import backtest_long_history as blh
    from mtl.news import news_gap_days
    from mtl.universe import load_added, load_sp500

    D = blh.load()
    cal = [b[0] for b in D["bench"]["SPY"]]
    sp, added = load_sp500(), load_added()

    def eligible(t, d):
        return t not in sp or added.get(t, "0000") <= d

    print("Boost baseline...", file=sys.stderr)
    base, _, _ = blh.build(boost=True)
    boost = base["Current setup (auto mix)"]
    spy = base["SPY"]

    lines = [f"# News-Gap Portfolio and Mid-Caps for Boost — {date.today().isoformat()}", "",
             "Both tests use today's index lists (survivorship bias: companies that later collapsed are missing).", "",
             "## 1. A news-gap portfolio on its own", "",
             "Every NIBII news gap (opened and closed 12%+ up, closing near the day's high) bought at the next "
             f"session's close, held 6 or 12 months; {COST:.1%} cost each way. S&P 500 (from join date) + Nasdaq-100.", "",
             "| Portfolio | Per year | Worst drop | Worst year | 2000-09 | 2010-19 | 2020-26 |",
             "|---|---:|---:|---:|---:|---:|---:|"]

    def row(label, c):
        a, dd, wy = stats(c)
        return (f"| {label} | {a:+.1%} | {dd:.0%} | {wy:+.0%} | "
                + " | ".join(f"{stats(c, x, y)[0]:+.1%}" for x, y in PERIODS) + " |")

    start = boost[0][0]
    notes = []
    curves = {}
    for hold, label in ((126, "6 months"), (252, "12 months")):
        print(f"Gap portfolios, hold {label}...", file=sys.stderr)
        ew, sl, avg_open, n_ev = gap_portfolios(D["bars"], cal, start, eligible, news_gap_days, hold)
        curves[hold] = (ew, sl)
        lines.append(row(f"Gaps, hold {label}, equal weight", ew))
        lines.append(row(f"Gaps, hold {label}, 10 slots", sl))
        notes.append(f"Hold {label}: {n_ev:,} gaps since {start[:4]}, {avg_open:.1f} positions open on an average day.")
    lines.append(row("Boost (today)", boost))
    ew12 = curves[252][0]
    lines.append(row("70% Boost / 30% gaps (12m, equal weight)", mix(boost, ew12, 0.7, cal)))
    lines.append(row("50% Boost / 50% gaps (12m, equal weight)", mix(boost, ew12, 0.5, cal)))
    lines.append(row("SPY", spy))
    lines += ["", *[f"- {x}" for x in notes], ""]

    # 2. mid-caps
    print("Mid-cap universe...", file=sys.stderr)
    mids = sp400_with_dates()
    new = sorted(t for t in mids if t not in D["bars"])
    if os.path.exists(args.cache):
        with open(args.cache, "rb") as fh:
            mid_bars = pickle.load(fh)
    else:
        mid_bars = blh.fetch(new, start=blh.FROM)
        with open(args.cache, "wb") as fh:
            pickle.dump(mid_bars, fh)
    mid_bars = {t: bs for t, bs in mid_bars.items() if bs}
    D2 = dict(D, bars={**D["bars"], **mid_bars})
    sp2 = dict(sp, **{t: ("", "") for t in mid_bars})
    added2 = dict(added, **{t: mids[t] for t in mid_bars})
    orig = (blh.load, blh.load_sp500, blh.load_added)
    blh.load, blh.load_sp500, blh.load_added = (lambda: D2), (lambda: sp2), (lambda: added2)
    try:
        print("Boost with mid-caps...", file=sys.stderr)
        wide, _, _ = blh.build(boost=True)
    finally:
        blh.load, blh.load_sp500, blh.load_added = orig
    dated = sum(1 for t in mid_bars if mids[t] != "0000")
    lines += ["## 2. Boost with S&P 400 mid-caps added", "",
              f"{len(mid_bars)} of today's S&P 400 had prices ({dated} with a logged join date; the rest assumed "
              "members throughout). Same Boost rule, costs and Monday trading.", "",
              "| Universe | Per year | Worst drop | Worst year | 2000-09 | 2010-19 | 2020-26 |",
              "|---|---:|---:|---:|---:|---:|---:|",
              row("S&P 500 + Nasdaq-100 (today)", boost),
              row("+ S&P 400 mid-caps", wide["Current setup (auto mix)"]),
              row("Top 5 alone, today's universe", base["Top 5 in stock"]),
              row("Top 5 alone, + mid-caps", wide["Top 5 in stock"]), ""]
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
