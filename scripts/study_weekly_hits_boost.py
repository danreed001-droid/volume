#!/usr/bin/env python3
"""
study_weekly_hits_boost.py
==========================
The weekly hit-rate report (study_weekly_hits.py) for the stocks Boost
actually HOLDS: NIBII's Auto + News boost rule (top 5 by 6-1 month strength,
keep while top 10, plus any stock that gapped up 12%+ on news in the last 4
weeks replacing the weakest holding), run exactly as
backtest_long_history.build(boost=True) runs it, 2000-2026.

Each week's 5 holdings are measured two ways:
  from Friday   the signal Friday's close -> the next signal Friday's close
  from Monday   the trade Monday's close  -> the next trade Monday's close
next to the plain model's 5 holdings (same rule without the news boost) and
SPY. A separate section follows the news-boosted stocks themselves: each
week a boosted stock was held vs the stock it displaced from the plain list.

Stock picks only -- the Auto mix's sleeve share is not included. Split-
adjusted closes, no dividends; today's index lists (survivorship bias).

USAGE
-----
    python scripts/study_weekly_hits_boost.py --nibii-dir ../NIBII
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from study_weekly_hits import mode_count, mode_pct  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nibii-dir", required=True)
    parser.add_argument("-o", "--output", default="reports/weekly_hits_boost.md")
    args = parser.parse_args()
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), args.output)

    nibii = os.path.abspath(args.nibii_dir)
    sys.path[:0] = [nibii, os.path.join(nibii, "scripts")]
    os.chdir(nibii)
    import backtest_long_history as blh
    from momentum_scan import blocked_dates
    from mtl.momentum import run_momentum
    from mtl.news import booster, news_gap_days
    from mtl.universe import load_added, load_sp500

    D = blh.load()
    bars = D["bars"]
    sp, added = load_sp500(), load_added()
    prices = {t: {b[0]: b[4] for b in bs} for t, bs in bars.items() if bs}
    prices["SPY"] = {b[0]: b[4] for b in D["bench"]["SPY"]}
    cal = [b[0] for b in D["bench"]["SPY"]]
    idx = {d: i for i, d in enumerate(cal)}
    blocked = {t: blocked_dates(bs) for t, bs in bars.items()}

    def eligible(t, d):
        return d not in blocked.get(t, ()) and (t not in sp or added.get(t, "0000") <= d)

    kw = dict(look=126, skip=21, top_n=5, eligible=eligible, exec_next="close")
    print("Running plain and Boost rules...", file=sys.stderr)
    plain = run_momentum(prices, cal, blh.START, **kw)
    gaps = {t: news_gap_days(bs) for t, bs in bars.items() if bs}
    boost = run_momentum(prices, cal, blh.START, prefer=booster(gaps, cal), prefer_mode="force",
                         prefer_rank=None, prefer_pool="all", **kw)

    def held_by_week(run):
        """{trade Monday: holdings} - picks are dated by the trading session."""
        return {d: h for d, h in run["picks"]}

    hb, hp = held_by_week(boost), held_by_week(plain)
    mondays = sorted(set(hb) & set(hp))

    def ret(t, a, b):
        pa, pb = prices.get(t, {}).get(a), prices.get(t, {}).get(b)
        return pb / pa - 1 if pa and pb else None

    weeks = []
    for m, m2 in zip(mondays, mondays[1:]):
        f, f2 = cal[idx[m] - 1], cal[idx[m2] - 1]          # the signal Fridays
        w = dict(monday=m, friday=f, boost=hb[m], plain=hp[m],
                 boosted=[t for t in hb[m] if t not in hp[m]], displaced=[t for t in hp[m] if t not in hb[m]])
        for key in ("boost", "plain"):
            w[key + "_fri"] = np.array([x for x in (ret(t, f, f2) for t in w[key]) if x is not None])
            w[key + "_mon"] = np.array([x for x in (ret(t, m, m2) for t in w[key]) if x is not None])
        w["boosted_mon"] = [x for x in (ret(t, m, m2) for t in w["boosted"]) if x is not None]
        w["displaced_mon"] = [x for x in (ret(t, m, m2) for t in w["displaced"]) if x is not None]
        w["spy_fri"], w["spy_mon"] = ret("SPY", f, f2), ret("SPY", m, m2)
        if len(w["boost_mon"]) and len(w["plain_mon"]):
            weeks.append(w)

    def counts(ws, key):
        ups = [int((w[key] > 0).sum()) for w in ws]
        allr = np.concatenate([w[key] for w in ws])
        win, lose = allr[allr > 0], allr[allr <= 0]
        return dict(avg_up=np.mean(ups), med_up=np.median(ups), mode_up=mode_count(ups),
                    maj=np.mean([u >= 3 for u in ups]), hit=len(win) / len(allr),
                    win_avg=win.mean(), win_med=np.median(win), win_mode=mode_pct(win),
                    lose_avg=lose.mean(), lose_med=np.median(lose), lose_mode=mode_pct(lose),
                    avg=allr.mean(), week_avg=np.mean([w[key].mean() for w in ws]))

    def spy(ws, key):
        r = np.array([w[key] for w in ws if w[key] is not None])
        win, lose = r[r > 0], r[r <= 0]
        return dict(up=(r > 0).mean(), win_avg=win.mean(), win_med=np.median(win), win_mode=mode_pct(win),
                    lose_avg=lose.mean(), lose_med=np.median(lose), lose_mode=mode_pct(lose), avg=r.mean())

    def block(ws, title):
        L = [f"## {title} ({len(ws):,} weeks, trades {ws[0]['monday']} to {ws[-1]['monday']})", "",
             "### How many of the 5 holdings went up the next week", "",
             "| Holdings | Measured from | Avg up | Median up | Most common | Weeks with 3+ of 5 up | Share of all holdings up |",
             "|---|---|---:|---:|---:|---:|---:|"]
        for label, k in (("Boost", "boost"), ("Plain model (no news boost)", "plain")):
            for frm, sfx in (("Friday close", "_fri"), ("Monday close", "_mon")):
                s = counts(ws, k + sfx)
                L.append(f"| {label} | {frm} | {s['avg_up']:.2f} of 5 | {s['med_up']:.0f} | {s['mode_up']} | "
                         f"{s['maj']:.0%} | {s['hit']:.0%} |")
        for frm, k in (("Friday close", "spy_fri"), ("Monday close", "spy_mon")):
            L.append(f"| SPY | {frm} | up in {spy(ws, k)['up']:.0%} of weeks | | | | |")
        L += ["", "### Size of the wins and losses (one week)", "",
              "| Holdings | Measured from | Avg winner | Median winner | Most common winner | Avg loser | Median loser | Most common loser | Avg week (5 equal) |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
        for label, k in (("Boost", "boost"), ("Plain model", "plain")):
            for frm, sfx in (("Friday close", "_fri"), ("Monday close", "_mon")):
                s = counts(ws, k + sfx)
                L.append(f"| {label} | {frm} | {s['win_avg']:+.1%} | {s['win_med']:+.1%} | {s['win_mode']:+.0%} | "
                         f"{s['lose_avg']:+.1%} | {s['lose_med']:+.1%} | {s['lose_mode']:+.0%} | {s['week_avg']:+.2%} |")
        for frm, k in (("Friday close", "spy_fri"), ("Monday close", "spy_mon")):
            s = spy(ws, k)
            L.append(f"| SPY | {frm} | {s['win_avg']:+.1%} | {s['win_med']:+.1%} | {s['win_mode']:+.0%} | "
                     f"{s['lose_avg']:+.1%} | {s['lose_med']:+.1%} | {s['lose_mode']:+.0%} | {s['avg']:+.2%} |")
        return L + [""]

    recent = [w for w in weeks if w["monday"] >= "2010-01-01"]
    bw = [x for w in weeks for x in w["boosted_mon"]]
    dw = [x for w in weeks for x in w["displaced_mon"]]
    diff_weeks = [w for w in weeks if w["boosted"]]
    lines = [
        f"# Weekly Wins of Boost's Holdings — {date.today().isoformat()}",
        "",
        "Boost's 5 stock holdings each week (NIBII's Auto + News boost rule, run as in "
        "`backtest_long_history.build(boost=True)`), next to the plain model's 5 and SPY. *From Friday* = "
        "signal Friday close to the next signal Friday; *from Monday* = the trade Monday's close to the next "
        "trade Monday. Stock picks only (the Auto mix's sleeve share isn't included). Split-adjusted prices, "
        "no dividends; today's index lists (survivorship bias). 'Most common' returns are rounded to the nearest 1%.",
        "",
        *block(weeks, f"Since {weeks[0]['monday'][:4]}"),
        *block(recent, "Since 2010"),
        "## The news-boosted stocks themselves (from Monday)", "",
        f"Boost's list differed from the plain model's in {len(diff_weeks):,} of {len(weeks):,} weeks.", "",
        "| Group | Stock-weeks | Share up | Avg week | Median week | Avg winner | Avg loser |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, arr in (("Boosted in (held by Boost, not the plain model)", np.array(bw)),
                       ("Displaced (held by the plain model instead)", np.array(dw))):
        lines.append(f"| {label} | {len(arr):,} | {(arr > 0).mean():.0%} | {arr.mean():+.2%} | {np.median(arr):+.2%} | "
                     f"{arr[arr > 0].mean():+.1%} | {arr[arr <= 0].mean():+.1%} |")
    lines += ["", "## By year (from Monday)", "",
              "| Year | Weeks | Boost avg up of 5 | Boost avg week | Plain avg up of 5 | Plain avg week | SPY up weeks | SPY avg week |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
    by_year = {}
    for w in weeks:
        by_year.setdefault(w["monday"][:4], []).append(w)
    for y, ws in sorted(by_year.items()):
        b, p, s = counts(ws, "boost_mon"), counts(ws, "plain_mon"), spy(ws, "spy_mon")
        lines.append(f"| {y} | {len(ws)} | {b['avg_up']:.2f} | {b['week_avg']:+.2%} | {p['avg_up']:.2f} | {p['week_avg']:+.2%} | "
                     f"{s['up']:.0%} | {s['avg']:+.2%} |")
    lines += ["", "## Last 12 weeks (from Monday)", "",
              "| Trade Monday | Boost holdings | Up of 5 | Avg winner | Avg loser | Avg week | Plain avg week | SPY |",
              "|---|---|---:|---:|---:|---:|---:|---:|"]
    for w in weeks[-12:]:
        r = w["boost_mon"]
        aw = f"{r[r > 0].mean():+.1%}" if (r > 0).any() else "—"
        al = f"{r[r <= 0].mean():+.1%}" if (r <= 0).any() else "—"
        names = ", ".join(t + ("*" if t in w["boosted"] else "") for t in w["boost"])
        lines.append(f"| {w['monday']} | {names} | {(r > 0).sum()} | {aw} | {al} | {r.mean():+.1%} | "
                     f"{w['plain_mon'].mean():+.1%} | {w['spy_mon']:+.1%} |")
    lines += ["", "\\* = in Boost's list because of a news gap (not in the plain model's 5 that week)."]
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
