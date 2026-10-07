#!/usr/bin/env python3
"""
study_weekly_hits.py
====================
Weekly hit-rate report for NIBII's momentum ranking: of the 20 stocks it
ranks highest each Friday (6-1 month strength, beating SPY -- the dashboard's
top 5 + ranks 6-20), how many went up over the next week?

Two starting points, because the model decides on Friday's close but trades
on Monday's close:
  from Friday   Friday close -> next Friday close
  from Monday   Monday close (the trade) -> next Monday close
SPY is measured the same two ways. For each week the winners' and losers'
average, median and most common (rounded to the nearest 1%) returns are
also reported, for the top 20 and for the top 5 alone.

Uses the plain ranking, not Boost's news-gap swaps or the Auto mix. Prices
are split-adjusted closes (no dividends) from NIBII's long-history cache;
S&P 500 stocks count only from their join date. Today's index lists, so
companies that later collapsed are missing.

USAGE
-----
    python scripts/study_weekly_hits.py --nibii-dir ../NIBII
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from datetime import date

import numpy as np

TOP, TOP5 = 20, 5


def mode_count(xs):
    """Most common value (ties -> the smaller)."""
    c = Counter(xs)
    best = max(c.values())
    return min(v for v, n in c.items() if n == best)


def mode_pct(rets):
    """Most common return, rounded to the nearest 1%."""
    return mode_count([int(round(r * 100)) for r in rets]) / 100 if len(rets) else float("nan")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nibii-dir", required=True)
    parser.add_argument("--since", default="2000-01-01")
    parser.add_argument("-o", "--output", default="reports/weekly_hits.md")
    args = parser.parse_args()
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), args.output)

    nibii = os.path.abspath(args.nibii_dir)
    sys.path[:0] = [nibii, os.path.join(nibii, "scripts")]
    os.chdir(nibii)
    import backtest_long_history as blh
    from momentum_scan import blocked_dates
    from mtl.momentum import last_sessions_of_weeks, score_table
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

    fridays = [f for f in last_sessions_of_weeks(cal) if f >= args.since]
    weeks = []
    print(f"Ranking {len(fridays)} Fridays...", file=sys.stderr)
    for n, f in enumerate(fridays):
        k = idx[f]
        # this Friday, next Friday, Monday (next session) and the Monday after
        later = [x for x in fridays[n + 1:n + 2]]
        if not later or k + 1 >= len(cal):
            continue
        nf = later[0]
        mon = cal[k + 1]
        nmon_i = idx[nf] + 1
        if nmon_i >= len(cal):
            continue
        nmon = cal[nmon_i]
        rows = score_table(prices, cal, k, 126, 21, eligible=eligible)
        top = [t for t, _, ok in rows if ok][:TOP]
        if len(top) < TOP:
            continue

        def rets(names, a, b):
            out = []
            for t in names:
                pa, pb = prices[t].get(a), prices[t].get(b)
                if pa and pb:
                    out.append(pb / pa - 1)
            return np.array(out)
        w = dict(friday=f, top=top,
                 fri=rets(top, f, nf), mon=rets(top, mon, nmon),
                 fri5=rets(top[:TOP5], f, nf), mon5=rets(top[:TOP5], mon, nmon),
                 spy_fri=prices["SPY"][nf] / prices["SPY"][f] - 1,
                 spy_mon=prices["SPY"][nmon] / prices["SPY"][mon] - 1)
        weeks.append(w)

    def summary(ws, key, size):
        ups = [int((w[key] > 0).sum()) for w in ws]
        allr = np.concatenate([w[key] for w in ws])
        win, lose = allr[allr > 0], allr[allr <= 0]
        avg_w = [w[key][w[key] > 0].mean() for w in ws if (w[key] > 0).any()]
        avg_l = [w[key][w[key] <= 0].mean() for w in ws if (w[key] <= 0).any()]
        return dict(avg_up=np.mean(ups), med_up=np.median(ups), mode_up=mode_count(ups), size=size,
                    pct_majority=np.mean([u > size / 2 for u in ups]),
                    win_avg=win.mean(), win_med=np.median(win), win_mode=mode_pct(win),
                    lose_avg=lose.mean(), lose_med=np.median(lose), lose_mode=mode_pct(lose),
                    wk_win_avg=np.mean(avg_w), wk_lose_avg=np.mean(avg_l),
                    avg_all=allr.mean(), hit=len(win) / len(allr))

    def spy_summary(ws, key):
        r = np.array([w[key] for w in ws])
        win, lose = r[r > 0], r[r <= 0]
        return dict(up=(r > 0).mean(), win_avg=win.mean(), win_med=np.median(win), win_mode=mode_pct(win),
                    lose_avg=lose.mean(), lose_med=np.median(lose), lose_mode=mode_pct(lose), avg_all=r.mean())

    def block(ws, title):
        L = [f"## {title} ({len(ws):,} weeks, {ws[0]['friday']} to {ws[-1]['friday']})", "",
             "### How many went up the next week", "",
             "| Group | Measured from | Avg up | Median up | Most common | Weeks with a majority up | Share of all picks up |",
             "|---|---|---:|---:|---:|---:|---:|"]
        for label, key, size in (("Top 20", "fri", 20), ("Top 20", "mon", 20), ("Top 5", "fri5", 5), ("Top 5", "mon5", 5)):
            s = summary(ws, key, size)
            frm = "Friday close" if key.startswith("fri") else "Monday close"
            L.append(f"| {label} | {frm} | {s['avg_up']:.1f} of {size} | {s['med_up']:.0f} | {s['mode_up']} | "
                     f"{s['pct_majority']:.0%} | {s['hit']:.0%} |")
        for key, frm in (("spy_fri", "Friday close"), ("spy_mon", "Monday close")):
            s = spy_summary(ws, key)
            L.append(f"| SPY | {frm} | up in {s['up']:.0%} of weeks | | | | |")
        L += ["", "### Size of the wins and losses (one week)", "",
              "| Group | Measured from | Avg winner | Median winner | Most common winner | Avg loser | Median loser | Most common loser | Avg of all |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
        for label, key, size in (("Top 20", "fri", 20), ("Top 20", "mon", 20), ("Top 5", "fri5", 5), ("Top 5", "mon5", 5)):
            s = summary(ws, key, size)
            frm = "Friday close" if key.startswith("fri") else "Monday close"
            L.append(f"| {label} | {frm} | {s['win_avg']:+.1%} | {s['win_med']:+.1%} | {s['win_mode']:+.0%} | "
                     f"{s['lose_avg']:+.1%} | {s['lose_med']:+.1%} | {s['lose_mode']:+.0%} | {s['avg_all']:+.2%} |")
        for key, frm in (("spy_fri", "Friday close"), ("spy_mon", "Monday close")):
            s = spy_summary(ws, key)
            L.append(f"| SPY | {frm} | {s['win_avg']:+.1%} | {s['win_med']:+.1%} | {s['win_mode']:+.0%} | "
                     f"{s['lose_avg']:+.1%} | {s['lose_med']:+.1%} | {s['lose_mode']:+.0%} | {s['avg_all']:+.2%} |")
        return L + [""]

    recent = [w for w in weeks if w["friday"] >= "2010-01-01"]
    lines = [
        f"# Weekly Wins of the Top-20 Picks — {date.today().isoformat()}",
        "",
        "Each Friday the model ranks the S&P 500 (from join date) + Nasdaq-100 by 6-month return skipping the "
        "latest month, keeping only stocks beating SPY; these are its 20 best (the dashboard's top 5 + ranks 6-20). "
        "*From Friday* = Friday close to next Friday close (the signal); *from Monday* = Monday close to next "
        "Monday close (when the trade happens). Plain ranking, without Boost's news swaps or the Auto mix. "
        "Split-adjusted prices, no dividends; today's index lists (survivorship bias). "
        "'Most common' returns are rounded to the nearest 1%.",
        "",
        *block(weeks, f"Since {weeks[0]['friday'][:4]}"),
        *block(recent, "Since 2010 (the dashboard's record)"),
        "## By year (top 20, from Monday — the weeks you actually trade)", "",
        "| Year | Weeks | Avg up of 20 | Most common | Avg winner | Avg loser | Avg pick | SPY up weeks | SPY avg week |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    by_year = {}
    for w in weeks:
        by_year.setdefault(w["friday"][:4], []).append(w)
    for y, ws in sorted(by_year.items()):
        s, q = summary(ws, "mon", 20), spy_summary(ws, "spy_mon")
        lines.append(f"| {y} | {len(ws)} | {s['avg_up']:.1f} | {s['mode_up']} | {s['win_avg']:+.1%} | {s['lose_avg']:+.1%} | "
                     f"{s['avg_all']:+.2%} | {q['up']:.0%} | {q['avg_all']:+.2%} |")
    lines += ["", "## Last 12 weeks", "",
              "| Friday | Top 20 up (from Fri) | Top 20 up (from Mon) | Top 5 up (Mon) | Avg winner (Mon) | Avg loser (Mon) | SPY from Fri | SPY from Mon |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for w in weeks[-12:]:
        m = w["mon"]
        aw = m[m > 0].mean() if (m > 0).any() else float("nan")
        al = m[m <= 0].mean() if (m <= 0).any() else float("nan")
        fmt = lambda x: "—" if np.isnan(x) else f"{x:+.1%}"  # noqa: E731
        lines.append(f"| {w['friday']} | {(w['fri'] > 0).sum()} | {(m > 0).sum()} | {(w['mon5'] > 0).sum()} of 5 | "
                     f"{fmt(aw)} | {fmt(al)} | {w['spy_fri']:+.1%} | {w['spy_mon']:+.1%} |")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
