#!/usr/bin/env python3
"""
backtest_boost_mix.py
=====================
NIBII's "Auto + News boost" momentum plan mixed with this repo's quality-dip
portfolio (70/30 and others), at 1x to 2x leverage.

- Boost curve: built by NIBII's own scripts/backtest_long_history.py
  (build(boost=True)), from a local NIBII checkout (--nibii-dir).
- Quality-dip curve: "Quality dips, hold 3y" from
  .cache/backtest/portfolio_curves.csv (run backtest_quality_dip.py first).
- Mixing and leverage use NIBII's scripts/backtest_leverage.run: weekly
  rebalance, anything above 100% of the account is borrowed at a margin
  rate charged daily; the account is wiped out if equity hits zero.

The mix can only start in 2011 (quality data begins ~2010), which misses
2000-02 and 2008. So Boost alone is also run from 2000 at each leverage
level -- that's the real stress test for "how much leverage is safe".

USAGE
-----
    python scripts/backtest_boost_mix.py --nibii-dir ../NIBII
"""
from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

MIX_START = "2011-01-03"
RATES = (0.06, 0.08)
LEVERAGE = (1.0, 1.25, 1.5, 2.0)
MIXES = [("Boost alone", 1.0, 0.0), ("70/30 Boost/quality", 0.7, 0.3),
         ("50/50 Boost/quality", 0.5, 0.5), ("Quality dips alone", 0.0, 1.0)]
CRASHES = [("Dot-com Mar 2000-Oct 2002", "2000-03-24", "2002-10-09"),
           ("2008 crisis Oct 2007-Mar 2009", "2007-10-09", "2009-03-09"),
           ("COVID Feb-Mar 2020", "2020-02-19", "2020-03-23"),
           ("2022 bear market", "2022-01-03", "2022-10-12"),
           ("Feb-Apr 2025", "2025-02-19", "2025-04-08")]


def stats(curve: list[list]) -> dict:
    v = [x for _, x in curve]
    total = v[-1] / v[0] - 1
    years = (len(v) - 1) / 252
    peak, dd = v[0], 0.0
    for x in v:
        peak = max(peak, x)
        dd = min(dd, x / peak - 1)
    ye: dict[str, float] = {}
    for d, x in curve:
        ye[d[:4]] = x
    prev, worst_year = v[0], 0.0
    for y in sorted(ye):
        worst_year = min(worst_year, ye[y] / prev - 1)
        prev = ye[y]
    annual = (1 + total) ** (1 / years) - 1 if total > -1 else -1.0
    return {"annual": annual, "maxDD": dd, "worst_year": worst_year, "final": 10000 * (1 + total)}


def crash(curve: list[list], a: str, b: str) -> str:
    v = [x for d, x in curve if a <= d <= b]
    return f"{v[-1] / v[0] - 1:+.0%}" if len(v) > 1 else "—"


def table(title: str, rows: list[tuple[str, list[list]]], crashes: list[tuple[str, str, str]]) -> list[str]:
    out = [f"### {title}", "",
           "| Plan | Per year | Worst drop | Worst calendar year | $10k became | " + " | ".join(c[0] for c in crashes) + " |",
           "|---|---:|---:|---:|---:|" + "---:|" * len(crashes)]
    for label, c in rows:
        s = stats(c)
        out.append(f"| {label} | {s['annual']:+.0%} | {s['maxDD']:.0%} | {s['worst_year']:+.0%} | "
                   f"${s['final']:,.0f} | " + " | ".join(crash(c, a, b) for _, a, b in crashes) + " |")
    return out + [""]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nibii-dir", required=True, help="local NIBII checkout")
    parser.add_argument("--cache-dir", default=".cache/backtest")
    parser.add_argument("-o", "--output", default="reports/boost_mix_backtest.md")
    args = parser.parse_args()

    nibii = os.path.abspath(args.nibii_dir)
    sys.path[:0] = [nibii, os.path.join(nibii, "scripts")]
    os.chdir(nibii)  # NIBII scripts resolve their data/ cache relative to the repo
    import backtest_long_history as blh
    from backtest_leverage import run

    print("Building NIBII Auto + News boost curve...", file=sys.stderr)
    boost_curves, calendar, _ = blh.build(boost=True)
    boost = boost_curves["Current setup (auto mix)"]
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    q = pd.read_csv(os.path.join(args.cache_dir, "portfolio_curves.csv"), index_col=0, parse_dates=True)
    q = q["Quality dips, hold 3y"].dropna()
    quality = {d.strftime("%Y-%m-%d"): float(v) for d, v in q.items()}

    boost_mix = [[d, v] for d, v in boost if d >= MIX_START and d in quality]
    mix_cal = [d for d, _ in boost_mix]
    boost_all = [[d, v] for d, v in boost]
    full_cal = [d for d, _ in boost_all]
    flat = {d: 1.0 for d in full_cal}  # "other" leg unused when its weight is 0

    lines = [
        "# Boost + Quality Dips Mix, with Leverage",
        "",
        "NIBII's **Auto + News boost** plan mixed with this repo's **quality dips (hold 3y)** portfolio. "
        "Weights are rebalanced weekly; anything above 100% of the account is borrowed at the margin "
        "rate shown, charged daily (NIBII's `backtest_leverage.run`). Same universe for both: today's "
        "S&P 500 (from each stock's join date) + Nasdaq-100, so survivorship bias flatters all of it.",
        "",
    ]
    for rate in RATES:
        lines += [f"## Borrowing at {rate:.0%} a year", ""]
        rows = []
        for name, wb, wq in MIXES:
            for lev in LEVERAGE:
                rows.append((f"{name} x{lev:g}", run(boost_mix, quality, wb * lev, wq * lev, mix_cal, rate)))
        lines += table(f"Since {MIX_START} (quality data starts ~2010)", rows, CRASHES[2:])
        rows = [(f"Boost alone x{lev:g}", run(boost_all, flat, lev, 0.0, full_cal, rate)) for lev in LEVERAGE]
        rows.append(("SPY", [[d, v] for d, v in boost_curves["SPY"]]))
        lines += table(f"Boost alone since {full_cal[0]} (includes the dot-com crash and 2008)", rows, CRASHES)

    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"Wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
