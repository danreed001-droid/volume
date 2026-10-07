#!/usr/bin/env python3
"""
backtest_volume_spike.py
========================
"Stocks with stories go up": is a volume spike -- often the first sign of a
new story -- a buy signal, and does it improve NIBII's Auto + News boost?

Part 1, event study (2000-2025, S&P 500 from its join date + Nasdaq-100):
every session where a stock traded VOL_X+ times its average volume of the
previous 50 sessions, split by what the price did that day, plus controls.
Forward total return from that close over 1 / 3 / 6 / 12 months, against
SPY over the same window. After an event, the same stock is not counted
again in the same group for 21 sessions.

Part 2, inside Boost (backtest_long_history.build(boost=True), 2000-2026):
NIBII's news-gap boost lets a stock that gapped up 12%+ on news in the last
4 weeks replace the weakest top-5 holding. Here the trigger is swapped for
(or combined with) a volume-spike-up day: volume VOL_X+ x average, close up
5%+, closing in the upper 40% of the day's range.

Data: NIBII's cached prices (data/.long_hist.pkl) and volumes
(data/.volume.pkl, from scripts/study_big_moves.py). Today's index lists,
so failed companies are missing (survivorship bias).

USAGE
-----
    python scripts/backtest_volume_spike.py --nibii-dir ../NIBII
"""
from __future__ import annotations

import argparse
import os
import pickle
import sys
from datetime import date

import numpy as np

VOL_X = 3.0
HORIZONS = {"1m": 21, "3m": 63, "6m": 126, "12m": 252}
COOLDOWN = 21
EVENT_END = "2025-10-01"   # leave room for 12-month forward returns


def spike_days(bars, vols, vol_x=VOL_X, min_up=0.05, min_where=0.6):
    """Dates where volume >= vol_x x the prior 50-session average, the close
    is up min_up+ and sits in the upper part of the day's range."""
    out = []
    v = [vols.get(b[0]) for b in bars]
    for j in range(51, len(bars)):
        prior = [x for x in v[j - 50:j] if x]
        if not v[j] or len(prior) < 40:
            continue
        d, o, h, lo, c = bars[j][:5]
        pc = bars[j - 1][4]
        if not pc or h <= lo:
            continue
        if v[j] >= vol_x * (sum(prior) / len(prior)) and c / pc - 1 >= min_up and (c - lo) / (h - lo) >= min_where:
            out.append(d[:10])
    return out


def event_study(bars, vols, spy, added, news_gap_days):
    """{group: [(fwd returns dict, spy fwd dict)]}"""
    groups: dict[str, list] = {}
    spy_d = [b[0] for b in spy]
    spy_c = np.array([b[4] for b in spy])
    spy_i = {d: i for i, d in enumerate(spy_d)}

    def add(group, t, j, closes, dates, last):
        if j - last.get((group, t), -10 ** 9) < COOLDOWN:
            return
        i0 = spy_i.get(dates[j])
        if i0 is None:
            return
        fwd, sfwd = {}, {}
        for h, n in HORIZONS.items():
            if j + n < len(closes) and i0 + n < len(spy_c):
                fwd[h] = closes[j + n] / closes[j] - 1
                sfwd[h] = spy_c[i0 + n] / spy_c[i0] - 1
        if "12m" in fwd:
            groups.setdefault(group, []).append((fwd, sfwd))
            last[(group, t)] = j

    for t, bs in bars.items():
        vmap = vols.get(t) or {}
        if not bs or not vmap:
            continue
        dates = [b[0][:10] for b in bs]
        closes = np.array([b[4] for b in bs])
        vol = np.array([vmap.get(d) or np.nan for d in dates])
        gaps = set(news_gap_days(bs))
        last: dict = {}
        joined = added.get(t, "0000")
        for j in range(51, len(bs)):
            d = dates[j]
            if d < "2000-01-01" or d > EVENT_END or d < joined:
                continue
            prior = vol[j - 50:j]
            prior = prior[~np.isnan(prior)]
            if len(prior) < 40 or np.isnan(vol[j]) or closes[j - 1] <= 0:
                continue
            ratio = vol[j] / prior.mean()
            _, o, h, lo, c = bs[j][:5]
            r = c / closes[j - 1] - 1
            where = (c - lo) / (h - lo) if h > lo else 0.5
            if ratio >= VOL_X:
                if r >= 0.05 and where >= 0.6:
                    add("Volume spike + up 5%+, strong close", t, j, closes, dates, last)
                elif r >= 0.05:
                    add("Volume spike + up 5%+, weak close", t, j, closes, dates, last)
                elif r <= -0.05:
                    add("Volume spike + down 5%+", t, j, closes, dates, last)
                else:
                    add("Volume spike, price moved under 5%", t, j, closes, dates, last)
                if ratio >= 5 and r >= 0.08:
                    add("Huge spike: 5x volume + up 8%+", t, j, closes, dates, last)
            elif r >= 0.05 and ratio < 1.5:
                add("Control: up 5%+ on normal volume", t, j, closes, dates, last)
            if d in gaps:
                add("NIBII news gap (12%+ gap that held)", t, j, closes, dates, last)
            if j % 63 == 0:
                add("Control: random stock-day (every 63rd)", t, j, closes, dates, last)
    return groups


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nibii-dir", required=True)
    parser.add_argument("-o", "--output", default="reports/volume_spike_study.md")
    args = parser.parse_args()
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), args.output)

    nibii = os.path.abspath(args.nibii_dir)
    sys.path[:0] = [nibii, os.path.join(nibii, "scripts")]
    os.chdir(nibii)
    import backtest_long_history as blh
    from mtl.news import news_gap_days
    from mtl.universe import load_added

    D = blh.load()
    with open(os.path.join(nibii, "data", ".volume.pkl"), "rb") as fh:
        vols = pickle.load(fh)
    added = load_added()

    print("Event study...", file=sys.stderr)
    groups = event_study(D["bars"], vols, D["bench"]["SPY"], added, news_gap_days)
    lines = [
        f"# Volume Spikes as a Story Signal — {date.today().isoformat()}",
        "",
        f"A *volume spike* = a session trading {VOL_X:g}x+ its average volume of the previous 50 sessions. "
        "Forward total return from that day's close, vs SPY over the same window. Events 2000 to "
        f"{EVENT_END[:7]}, S&P 500 (from join date) + Nasdaq-100, one event per stock per group per month. "
        "Today's index lists, so companies that later collapsed are missing.",
        "",
        "## Part 1: what happened after each kind of day",
        "",
        "| Day type | Events | Avg 3m vs SPY | Avg 6m vs SPY | Avg 12m | Avg 12m vs SPY | Median 12m vs SPY | % beat SPY (12m) | % up 60%+ (12m) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    order = ["Volume spike + up 5%+, strong close", "Volume spike + up 5%+, weak close", "Huge spike: 5x volume + up 8%+",
             "Volume spike + down 5%+", "Volume spike, price moved under 5%", "NIBII news gap (12%+ gap that held)",
             "Control: up 5%+ on normal volume", "Control: random stock-day (every 63rd)"]
    for g in order:
        ev = groups.get(g, [])
        if not ev:
            continue
        ex = {h: np.array([f[h] - s[h] for f, s in ev]) for h in HORIZONS}
        f12 = np.array([f["12m"] for f, _ in ev])
        lines.append(f"| {g} | {len(ev):,} | {ex['3m'].mean():+.1%} | {ex['6m'].mean():+.1%} | {f12.mean():+.1%} | "
                     f"{ex['12m'].mean():+.1%} | {np.median(ex['12m']):+.1%} | {(ex['12m'] > 0).mean():.0%} | "
                     f"{(f12 >= 0.6).mean():.1%} |")

    # Part 2: inside Boost
    print("Boost variants...", file=sys.stderr)
    blh.load = lambda: D                       # same objects every build -> stable ticker lookup
    ticker_of = {id(bs): t for t, bs in D["bars"].items()}
    original = blh.news_gap_days

    def spikes(bs, **kw):
        return spike_days(bs, vols.get(ticker_of.get(id(bs)), {}), **kw)

    variants = [
        ("Boost (today): news gap 12%+", original),
        ("Volume spike (3x, up 5%+) instead of news gap", lambda bs: spikes(bs)),
        ("Bigger spike (5x, up 8%+) instead of news gap", lambda bs: spikes(bs, vol_x=5.0, min_up=0.08)),
        ("News gap OR volume spike (3x, up 5%+)", lambda bs: sorted(set(original(bs)) | set(spikes(bs)))),
        ("News gap only when volume was 3x+", lambda bs: sorted(set(original(bs)) & set(spikes(bs, min_up=0.0, min_where=0.0)))),
    ]
    rows = []
    for label, fn in variants:
        print(f"  {label}", file=sys.stderr)
        blh.news_gap_days = fn
        try:
            curves, _, _ = blh.build(boost=True)
        finally:
            blh.news_gap_days = original
        rows.append((label, curves["Current setup (auto mix)"], curves["Top 5 in stock"]))
    base_curves, _, _ = blh.build(boost=False)
    rows.append(("No boost at all (plain Auto)", base_curves["Current setup (auto mix)"], base_curves["Top 5 in stock"]))

    def stats(c, a="0000", b="9999"):
        v = [x for d, x in c if a <= d <= b]
        total = v[-1] / v[0] - 1
        peak, dd = v[0], 0.0
        for x in v:
            peak = max(peak, x)
            dd = min(dd, x / peak - 1)
        return (1 + total) ** (252 / (len(v) - 1)) - 1, dd

    periods = [("2000-01-01", "2009-12-31"), ("2010-01-01", "2019-12-31"), ("2020-01-01", "2026-12-31")]
    lines += ["", "## Part 2: as Boost's story trigger (2000-2026, Auto mix on top)", "",
              "| Trigger | Per year | Worst drop | 2000-09 | 2010-19 | 2020-26 | Top 5 alone per year |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for label, c, t5 in rows:
        a, dd = stats(c)
        lines.append(f"| {label} | {a:+.1%} | {dd:.0%} | " + " | ".join(f"{stats(c, x, y)[0]:+.1%}" for x, y in periods)
                     + f" | {stats(t5)[0]:+.1%} |")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
