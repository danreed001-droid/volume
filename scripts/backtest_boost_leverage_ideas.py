#!/usr/bin/env python3
"""
backtest_boost_leverage_ideas.py
================================
Ways to lever NIBII's "Auto + News boost" plan without the 2000-02 / 2008
wipeouts that constant leverage suffers (see backtest_boost_mix.py).

NIBII's own options tests (scripts/backtest_options_only.py) already show
that BUYING calls on the top-5 signals loses money over 2000-2026 in every
variant -- time decay and the 2000-02 / 2008 bear markets eat them. So the
ideas here keep the stock-based Boost curve and change only how much of it
is held, plus an optional SPY put hedge:

  constant Lx         L x Boost every week, borrowed part pays RATE
  trend-gated         L x Boost while SPY closed above its 200-day average
                      at the Friday close, else `low` x (1x, 0.6x or 0x)
  + put hedge         also hold 3-month SPY puts 10% out of the money on the
                      whole levered exposure, bought monthly, sold and rolled
                      at the next month's first session. Priced with
                      Black-Scholes at VIX + 4 points (out-of-the-money puts
                      trade above VIX -- skew), 2% paid each way. Puts pay off
                      on SPY falls only; Boost can fall more than SPY.

Leverage is set at the Friday close and applied from the next session
(weekly, like the Boost signal itself). Borrowed money pays RATE a year,
charged daily. Survivorship bias (today's index lists) flatters every line.

USAGE
-----
    python scripts/backtest_boost_leverage_ideas.py --nibii-dir ../NIBII
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from datetime import date

RATE = 0.06          # margin rate on borrowed money
CASH_RATE = 0.0      # cash earns nothing (conservative, matches NIBII)
OPT_RATE = 0.04      # risk-free rate for option pricing
PUT_OTM = 0.90       # strike = 90% of SPY
PUT_DAYS = 91        # ~3-month puts
SKEW_PTS = 0.04      # added to VIX for 10% OTM puts
SPREAD = 0.02
SMA_DAYS = 200
CRASHES = [("Dot-com", "2000-03-24", "2002-10-09"), ("2008", "2007-10-09", "2009-03-09"),
           ("Flash 2011", "2011-04-29", "2011-10-03"), ("Q4 2018", "2018-09-20", "2018-12-24"),
           ("COVID", "2020-02-19", "2020-03-23"), ("2022", "2022-01-03", "2022-10-12"),
           ("2025", "2025-02-19", "2025-04-08")]


def _ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_put(s: float, k: float, t: float, vol: float, r: float) -> float:
    if t <= 0:
        return max(0.0, k - s)
    v = vol * math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / v
    return k * math.exp(-r * t) * _ncdf(-(d1 - v)) - s * _ncdf(-d1)


def simulate(cal, boost, spy, vix, fridays, sma, lev_hi, lev_lo=None, hedge=False):
    """Daily NAV curve [[date, nav]]. lev_lo=None -> constant lev_hi."""
    nav, lev = 1.0, lev_hi
    put = None  # dict(k, exp_idx, qty, value)
    out = [[cal[0], nav]]
    month = cal[0][:7]
    for i in range(1, len(cal)):
        d, p = cal[i], cal[i - 1]
        rb = boost[d] / boost[p] - 1
        borrowed = max(0.0, lev - 1)
        cash = max(0.0, 1 - lev)
        nav *= 1 + lev * rb - borrowed * RATE / 252 + cash * CASH_RATE / 252
        if put:
            t = max(0.0, (put["exp"] - i) / 252)
            new_val = put["qty"] * bs_put(spy[d], put["k"], t, vix[d] / 100 + SKEW_PTS, OPT_RATE)
            nav += new_val - put["value"]
            put["value"] = new_val
        if nav <= 0:
            out.append([d, 1e-9])
            break
        # monthly put roll at the first session of a new month
        if hedge and d[:7] != month:
            if put:
                nav -= put["value"] * SPREAD        # sell at bid
                put = None
            k = spy[d] * PUT_OTM
            price = bs_put(spy[d], k, PUT_DAYS / 365, vix[d] / 100 + SKEW_PTS, OPT_RATE)
            qty = lev * nav / spy[d]                 # puts on the full levered exposure
            cost = qty * price * (1 + SPREAD)
            nav -= cost - qty * price               # pay the ask; mark at mid
            put = {"k": k, "exp": i + int(PUT_DAYS * 252 / 365), "qty": qty, "value": qty * price}
        month = d[:7]
        # weekly leverage decision at the Friday close, applied from next session
        if lev_lo is not None and d in fridays:
            lev = lev_hi if spy[d] > sma[d] else lev_lo
        out.append([d, nav])
    return out


def stats(curve, a, b):
    v = [x for d, x in curve if a <= d <= b]
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
    annual = (1 + total) ** (1 / years) - 1 if total > -1 else -1.0
    return annual, dd, worst


def crash(curve, a, b):
    v = [x for d, x in curve if a <= d <= b]
    return f"{v[-1] / v[0] - 1:+.0%}" if len(v) > 1 else "—"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nibii-dir", required=True)
    parser.add_argument("-o", "--output", default="reports/boost_leverage_ideas.md")
    args = parser.parse_args()
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(repo, args.output)

    nibii = os.path.abspath(args.nibii_dir)
    sys.path[:0] = [nibii, os.path.join(nibii, "scripts")]
    os.chdir(nibii)
    import backtest_long_history as blh
    from mtl.momentum import last_sessions_of_weeks

    print("Building Auto + News boost curve...", file=sys.stderr)
    curves, cal, _ = blh.build(boost=True)
    boost = dict(curves["Current setup (auto mix)"])
    spy_curve = curves["SPY"]
    spy = dict(spy_curve)

    import yfinance as yf
    vx = yf.download("^VIX", start="1999-01-01", progress=False, auto_adjust=False)["Close"].squeeze()
    vix_raw = {ts.strftime("%Y-%m-%d"): float(v) for ts, v in vx.dropna().items()}

    cal = [d for d in cal if d in boost and d in spy]
    vix, last = {}, 20.0
    for d in cal:
        last = vix_raw.get(d, last)
        vix[d] = last
    # 200-day SMA of SPY over the full benchmark history (starts before the backtest)
    all_spy = [(d, v) for d, v in sorted(dict(curves["SPY"]).items())]
    sma, window, total = {}, [], 0.0
    for d, v in all_spy:
        window.append(v)
        total += v
        if len(window) > SMA_DAYS:
            total -= window.pop(0)
        sma[d] = total / len(window)
    fridays = set(last_sessions_of_weeks(cal))

    plans = [
        ("Boost 1x (today)", dict(lev_hi=1.0)),
        ("Boost 1.5x constant", dict(lev_hi=1.5)),
        ("Boost 2x constant", dict(lev_hi=2.0)),
        ("1.5x in uptrend, 1x otherwise", dict(lev_hi=1.5, lev_lo=1.0)),
        ("2x in uptrend, 1x otherwise", dict(lev_hi=2.0, lev_lo=1.0)),
        ("1.5x in uptrend, 0.6x otherwise", dict(lev_hi=1.5, lev_lo=0.6)),
        ("1.25x in uptrend, 0.6x otherwise", dict(lev_hi=1.25, lev_lo=0.6)),
        ("2x in uptrend, 0.6x otherwise", dict(lev_hi=2.0, lev_lo=0.6)),
        ("2x in uptrend, cash otherwise", dict(lev_hi=2.0, lev_lo=0.0)),
        ("1x + SPY put hedge", dict(lev_hi=1.0, hedge=True)),
        ("2x constant + SPY put hedge", dict(lev_hi=2.0, hedge=True)),
        ("1.5x in uptrend / 0.6x + put hedge", dict(lev_hi=1.5, lev_lo=0.6, hedge=True)),
        ("2x in uptrend / 0.6x + put hedge", dict(lev_hi=2.0, lev_lo=0.6, hedge=True)),
    ]
    results = []
    for label, kw in plans:
        print(f"  {label}", file=sys.stderr)
        results.append((label, simulate(cal, boost, spy, vix, fridays, sma, **kw)))
    results.append(("SPY buy & hold", [[d, spy[d]] for d in cal]))

    spans = [(cal[0], cal[-1]), ("2011-01-03", cal[-1])]
    lines = [
        f"# Levering Auto + News Boost — {date.today().isoformat()}",
        "",
        "Built on NIBII's Auto + News boost curve (`backtest_long_history.build(boost=True)`). "
        f"Leverage is decided at the Friday close; 'uptrend' = SPY above its {SMA_DAYS}-day average. "
        f"Borrowed money pays {RATE:.0%} a year. Put hedge = 3-month SPY puts {1 - PUT_OTM:.0%} out of the "
        f"money on the full levered exposure, rolled monthly, Black-Scholes at VIX + {SKEW_PTS * 100:.0f} points, "
        f"{SPREAD:.0%} paid each way. Survivorship bias (today's index lists) flatters every line.",
        "",
    ]
    for a, b in spans:
        lines += [f"## {a} to {b}", "",
                  "| Plan | Per year | Worst drop | Worst year | " + " | ".join(c[0] for c in CRASHES) + " |",
                  "|---|---:|---:|---:|" + "---:|" * len(CRASHES)]
        for label, c in results:
            ann, dd, wy = stats(c, a, b)
            lines.append(f"| {label} | {ann:+.0%} | {dd:.0%} | {wy:+.0%} | "
                         + " | ".join(crash(c, x, y) if x >= a else "—" for _, x, y in CRASHES) + " |")
        lines.append("")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
