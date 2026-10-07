#!/usr/bin/env python3
"""
backtest_gated_robustness.py
============================
Robustness check for trend-gated leverage on NIBII's Auto + News boost
(backtest_boost_leverage_ideas.py): is "lever up in an uptrend, cut back
otherwise" a real effect, or a lucky fit to SPY's 200-day average?

The same rule (hi x Boost while the signal says uptrend at the Friday close,
lo x otherwise; borrowed money at 6%) is run with several unrelated trend
signals. If most of them beat plain 1x Boost, the effect is real. Then the
SPY 200-day version is compared with 1x year by year, to see whether the
gain is spread out or comes from one or two years.

USAGE
-----
    python scripts/backtest_gated_robustness.py --nibii-dir ../NIBII
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date

import backtest_boost_leverage_ideas as li

LEVELS = [(1.5, 0.6), (1.25, 0.6)]


def sma_flags(series: dict[str, float], days: int) -> dict[str, bool]:
    out, win, tot = {}, [], 0.0
    for d in sorted(series):
        v = series[d]
        win.append(v)
        tot += v
        if len(win) > days:
            tot -= win.pop(0)
        out[d] = v > tot / len(win)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nibii-dir", required=True)
    parser.add_argument("-o", "--output", default="reports/gated_leverage_robustness.md")
    parser.add_argument("--levels", default=",".join(f"{h:g}:{l:g}" for h, l in LEVELS),
                        help="hi:lo pairs, e.g. 1:0.6,1:0.4 for no-margin versions")
    args = parser.parse_args()
    levels = [tuple(float(x) for x in pair.split(":")) for pair in args.levels.split(",")]
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(repo, args.output)

    nibii = os.path.abspath(args.nibii_dir)
    sys.path[:0] = [nibii, os.path.join(nibii, "scripts")]
    os.chdir(nibii)
    import backtest_long_history as blh
    from mtl.momentum import last_sessions_of_weeks

    print("Building Auto + News boost curve...", file=sys.stderr)
    curves, cal, downs = blh.build(boost=True)
    boost = dict(curves["Current setup (auto mix)"])
    spy_all = dict(curves["SPY"])
    qqq_all = dict(curves["QQQ (Nasdaq-100)"])
    # benchmark history before the backtest start, so long averages are warm on day one
    for b in ("SPY", "QQQ"):
        hist = {r[0]: r[4] for r in blh.load()["bench"][b]}
        (spy_all if b == "SPY" else qqq_all).update({d: v for d, v in hist.items() if d not in boost})
    cal = [d for d in cal if d in boost and d in spy_all]
    fridays = set(last_sessions_of_weeks(cal))

    import yfinance as yf
    vx = yf.download("^VIX", start="1999-01-01", progress=False, auto_adjust=False)["Close"].squeeze()
    vix_raw = {ts.strftime("%Y-%m-%d"): float(v) for ts, v in vx.dropna().items()}
    vix, last = {}, 20.0
    for d in cal:
        last = vix_raw.get(d, last)
        vix[d] = last

    spy_sorted = sorted(spy_all)
    pos = {d: i for i, d in enumerate(spy_sorted)}
    signals: dict[str, dict[str, bool]] = {}
    for n in (100, 150, 200, 250):
        signals[f"SPY > {n}-day avg"] = sma_flags(spy_all, n)
    signals["QQQ > 200-day avg"] = sma_flags(qqq_all, 200)
    # SPY 10-month average, checked on month-end closes (the classic monthly trend rule)
    month_end = {}
    for d in spy_sorted:
        month_end[d[:7]] = d
    me = sorted(month_end.values())
    me_flags, state = {}, True
    for i, d in enumerate(me):
        if i >= 9:
            state = spy_all[d] > sum(spy_all[x] for x in me[i - 9:i + 1]) / 10
        me_flags[d] = state
    cur, f10 = True, {}
    for d in spy_sorted:
        cur = me_flags.get(d, cur)
        f10[d] = cur
    signals["SPY > 10-month avg (monthly)"] = f10
    signals["SPY up over 12 months"] = {d: spy_all[d] > spy_all[spy_sorted[max(0, pos[d] - 252)]] for d in spy_sorted}
    signals["VIX below 25"] = {d: vix[d] < 25 for d in cal}
    signals["NIBII Auto: <2 holdings in downtrend"] = {d: downs(d) < 2 for d in cal if d in fridays}

    base = li.simulate(cal, boost, spy_all, vix, fridays, {}, 1.0)
    spans = [(cal[0], cal[-1]), ("2011-01-03", cal[-1])]

    def row(label, c, a, b):
        ann, dd, wy = li.stats(c, a, b)
        return ann, dd, wy, f"| {label} | {ann:+.1%} | {dd:.0%} | {wy:+.0%} |"

    lines = [
        f"# Gated Leverage Robustness — {date.today().isoformat()}",
        "",
        "Rule: hold *hi* x NIBII's Auto + News boost while the signal says uptrend at the Friday close, "
        "*lo* x otherwise (rest in cash); borrowed money pays 6% a year. Each signal is tested against "
        "plain 1x Boost. Survivorship bias (today's index lists) flatters every line equally.",
        "",
    ]
    curves_by = {}
    for hi, lo in levels:
        for a, b in spans:
            ann0, dd0, wy0, r0 = row("Boost 1x (no gating)", base, a, b)
            lines += [f"## {hi:g}x in uptrend / {lo:g}x otherwise — {a[:4]} to {b[:4]}", "",
                      "| Signal | Per year | Worst drop | Worst year | Weeks in uptrend | Beats 1x on |",
                      "|---|---:|---:|---:|---:|---|", r0[:-1] + " | — | — |"]
            wins = 0
            for name, flags in signals.items():
                up = {}
                cur = True
                for d in cal:
                    cur = flags.get(d, cur)
                    up[d] = cur
                key = (name, hi, lo)
                if key not in curves_by:
                    curves_by[key] = li.simulate(cal, boost, spy_all, vix, fridays, {}, hi, lo, up=up)
                c = curves_by[key]
                ann, dd, wy, _ = row(name, c, a, b)
                wk = [up[d] for d in cal if d in fridays and a <= d <= b]
                beats = [lbl for lbl, ok in (("return", ann > ann0), ("worst drop", dd >= dd0),
                                              ("worst year", wy >= wy0)) if ok]
                wins += ann > ann0
                lines.append(f"| {name} | {ann:+.1%} | {dd:.0%} | {wy:+.0%} | {sum(wk) / len(wk):.0%} | "
                             f"{', '.join(beats) or 'nothing'} |")
            lines += ["", f"**{wins} of {len(signals)} signals beat plain 1x on return.**", ""]

    # year by year: SPY 200-day, 1.5 / 0.6 vs 1x
    gated = curves_by[("SPY > 200-day avg", *levels[0])]

    def yearly(c):
        ye, prev, out = {}, c[0][1], {}
        for d, x in c:
            ye[d[:4]] = x
        for y in sorted(ye):
            out[y] = ye[y] / prev - 1
            prev = ye[y]
        return out
    yb, yg = yearly(base), yearly(gated)
    lines += [f"## Year by year — SPY 200-day, {levels[0][0]:g}x / {levels[0][1]:g}x vs plain 1x", "",
              "| Year | Boost 1x | Gated | Difference |", "|---|---:|---:|---:|"]
    better = 0
    for y in sorted(yb):
        diff = yg[y] - yb[y]
        better += diff > 0
        lines.append(f"| {y} | {yb[y]:+.0%} | {yg[y]:+.0%} | {diff:+.0%} |")
    lines += ["", f"Gated did better in **{better} of {len(yb)}** years.", ""]

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
