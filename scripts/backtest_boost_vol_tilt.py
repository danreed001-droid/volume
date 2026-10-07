#!/usr/bin/env python3
"""
backtest_boost_vol_tilt.py
==========================
Does tilting NIBII's Auto + News boost toward its more VOLATILE candidates
help? (study_big_winners.py found that 60%+ winners were mostly high-
volatility stocks -- but so were the big losers.)

Variants, all on the same Boost pipeline (backtest_long_history.build(boost=True):
6-1 month strength, beat SPY, top 5, keep while top 10, news-gap boost, Auto
mix with the best-of sleeve), 2000-2026:

  pool 10 / pool 20   among the best 10 (20) by strength, buy the most
                      volatile first (63-day volatility)
  tilt 0.5 / tilt 1   rank buys by strength x volatility^0.5 (^1)
  weight by vol       same picks, each holding weighted by its volatility
  only 40%+ vol       skip a buy whose volatility is under 40% a year; the
                      next-best stock that passes is taken

Needs a NIBII checkout whose mtl/momentum.py has the experimental
`vol_tilt`, `vol_pool` and weighting='vol' options (local experiment, see
the report). Survivorship bias (today's index lists) flatters every line,
and most of all volatile stocks, whose failures are the ones missing.

USAGE
-----
    python scripts/backtest_boost_vol_tilt.py --nibii-dir ../NIBII
"""
from __future__ import annotations

import argparse
import functools
import math
import os
import sys
from datetime import date

PERIODS = [("2000-01-01", "2009-12-31"), ("2010-01-01", "2019-12-31"), ("2020-01-01", "2026-12-31")]
CRASHES = [("Dot-com", "2000-03-24", "2002-10-09"), ("2008", "2007-10-09", "2009-03-09"),
           ("COVID", "2020-02-19", "2020-03-23"), ("2022", "2022-01-03", "2022-10-12"), ("2025", "2025-02-19", "2025-04-08")]


def stats(curve, a="0000", b="9999"):
    v = [x for d, x in curve if a <= d <= b]
    if len(v) < 2:
        return None, None, None
    total = v[-1] / v[0] - 1
    years = (len(v) - 1) / 252
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
    return (1 + total) ** (1 / years) - 1, dd, worst


def crash(curve, a, b):
    v = [x for d, x in curve if a <= d <= b]
    return f"{v[-1] / v[0] - 1:+.0%}" if len(v) > 1 else "—"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nibii-dir", required=True)
    parser.add_argument("-o", "--output", default="reports/boost_vol_tilt.md")
    args = parser.parse_args()
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), args.output)

    nibii = os.path.abspath(args.nibii_dir)
    sys.path[:0] = [nibii, os.path.join(nibii, "scripts")]
    os.chdir(nibii)
    import backtest_long_history as blh
    import mtl.momentum as mm

    if "vol_pool" not in mm.run_momentum.__code__.co_varnames:
        sys.exit("this NIBII checkout's run_momentum has no vol_tilt / vol_pool options")

    # 63-day volatility per ticker, indexed like the calendar, for the "only 40%+ vol" filter
    D = blh.load()
    cal = [b[0] for b in D["bench"]["SPY"]]
    vol63 = {}
    for t, bs in D["bars"].items():
        px = dict((b[0], b[4]) for b in bs)
        closes = [px.get(d) for d in cal]
        out, rets = [None] * len(cal), []
        for k in range(1, len(cal)):
            a, b = closes[k - 1], closes[k]
            rets.append(math.log(b / a) if a and b else None)
            w = [r for r in rets[-63:] if r is not None]
            if len(w) >= 40:
                m = sum(w) / len(w)
                out[k] = (sum((x - m) ** 2 for x in w) / (len(w) - 1)) ** 0.5 * math.sqrt(252)
        vol63[t] = out

    def vol_at_least(th):
        return lambda t, k: (vol63.get(t) or [None] * (k + 1))[k] is not None and vol63[t][k] >= th

    variants = [
        ("Boost (today)", {}),
        ("Pool 10: most volatile of the best 10", dict(vol_pool=10)),
        ("Pool 20: most volatile of the best 20", dict(vol_pool=20)),
        ("Tilt 0.5: strength x vol^0.5", dict(vol_tilt=0.5)),
        ("Tilt 1: strength x vol", dict(vol_tilt=1.0)),
        ("Same picks, weighted by volatility", dict(weighting="vol")),
        ("Only buy 40%+ volatility", dict(buy_when=vol_at_least(0.40))),
        ("Only buy 30%+ volatility", dict(buy_when=vol_at_least(0.30))),
    ]
    original = blh.run_momentum
    results = []
    for label, extra in variants:
        print(f"  {label}", file=sys.stderr)
        blh.run_momentum = functools.partial(original, **extra)
        try:
            curves, _, _ = blh.build(boost=True)
        finally:
            blh.run_momentum = original
        results.append((label, curves["Current setup (auto mix)"], curves["Top 5 in stock"]))
    spy = curves["SPY"]

    lines = [
        f"# Boost: Favoring the More Volatile Picks — {date.today().isoformat()}",
        "",
        "NIBII's Auto + News boost with its stock picks tilted toward higher 63-day volatility, "
        "2000-2026 (`backtest_long_history.build(boost=True)`, same costs and Monday trading). "
        "Survivorship bias flatters every line — volatile stocks most, since the ones that collapsed are missing.",
        "",
        "## Full period",
        "",
        "| Variant | Per year | Worst drop | Worst year | Top 5 alone per year | Top 5 alone worst drop |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, c, t5 in results:
        a, dd, wy = stats(c)
        a5, dd5, _ = stats(t5)
        lines.append(f"| {label} | {a:+.1%} | {dd:.0%} | {wy:+.0%} | {a5:+.1%} | {dd5:.0%} |")
    a, dd, wy = stats(spy)
    lines.append(f"| SPY | {a:+.1%} | {dd:.0%} | {wy:+.0%} | | |")
    lines += ["", "## By decade (per year) — does any edge hold in each?", "",
              "| Variant | " + " | ".join(f"{p[0][:4]}-{p[1][2:4]}" for p in PERIODS) + " |",
              "|---|" + "---:|" * len(PERIODS)]
    for label, c, _ in results:
        lines.append(f"| {label} | " + " | ".join(f"{stats(c, a_, b_)[0]:+.1%}" for a_, b_ in PERIODS) + " |")
    lines += ["", "## Crashes", "", "| Variant | " + " | ".join(x[0] for x in CRASHES) + " |",
              "|---|" + "---:|" * len(CRASHES)]
    for label, c, _ in results:
        lines.append(f"| {label} | " + " | ".join(crash(c, a_, b_) for _, a_, b_ in CRASHES) + " |")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
