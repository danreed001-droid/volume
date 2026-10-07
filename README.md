# Volume Scanner

Scans the **S&P 500**, **Nasdaq Composite**, and a fixed **ETF watchlist**
for the biggest volume spikes: tickers whose most recent session's volume
is highest relative to their trailing **50-session** and **100-session**
average (i.e. unusual activity today, not just perpetually high-volume
names like SPY/NVDA).

## How it works

- `scripts/scan_volume.py` builds the three ticker universes:
  - S&P 500 — scraped from the Wikipedia constituents table.
  - Nasdaq Composite — all non-test, non-ETF common symbols from Nasdaq
    Trader's official symbol directory.
  - ETFs — a fixed watchlist: `XLE, XLF, GLD, TLT, XLB, SPY, EEM, QQQ, SLV,
    XLRE` (edit `FIXED_ETFS` in the script to change it).
- Pulls ~9 months of daily volume history per ticker from Yahoo Finance
  (`yfinance`), in chunks, with basic retry/backoff.
- For each ticker, computes the 50-session and 100-session average volume
  from the sessions *before* the latest one, then ranks by
  `latest_volume / trailing_average` (highest ratio first).
- Tickers averaging under `MIN_AVG_VOLUME` shares/day (default 100,000) are
  excluded, since illiquid names (e.g. SPAC units trading a few hundred
  shares/day) produce meaningless huge ratios off tiny absolute moves.
- Each universe also gets a **"Fresh volume highs"** section: tickers whose
  latest session's volume beat every single session in the trailing 50 days
  *and* every one in the trailing 100 days — a genuine volume breakout,
  not just "above average."
- Writes a Markdown report to `reports/volume_report_<date>.md` and updates
  `reports/latest.md`.

## Schedule

`.github/workflows/volume-scan.yml` runs this every **weekday at 22:00 UTC**
(after the US market close) via GitHub Actions and commits the updated
report back to the repo. It also supports manual runs via the "Run
workflow" button (`workflow_dispatch`).

**Note:** scheduled (`cron`) workflows on GitHub only fire from the
repository's default branch. This branch (`claude/volume-tickers-sp500-nasdaq-e9tusw`)
is currently the repo's default branch (the repo had no commits before this
change), so the schedule is active as-is.

## Configuration

Environment variables (set in the workflow file or when running locally):

- `TOP_N` — how many tickers to list per universe/window (default `25`).
- `CHUNK_SIZE` — how many tickers to request from Yahoo Finance per batch
  (default `150`). Lower this if you hit rate-limiting (HTTP 429) errors.
- `MIN_AVG_VOLUME` — minimum trailing-average daily volume (shares) required
  to qualify for the ranking (default `100000`).

## Running locally

```bash
pip install -r requirements.txt
python scripts/scan_volume.py
```

Requires normal internet access to `en.wikipedia.org`, `nasdaqtrader.com`,
and Yahoo Finance.

## Known limitations

- Yahoo Finance's unofficial API can rate-limit large scans. The S&P 500 +
  Nasdaq Composite combined is still ~3,500-4,000 tickers, so if runs start
  failing partway through, reduce `CHUNK_SIZE` and/or increase the delay
  between chunks in `scan_volume.py`.

## Dual-timeframe watchlist report

A second, separate report: for a curated ~650-ticker watchlist (S&P 500 +
a themed VSA watchlist + ETFs/FX/crypto), it plots an **hourly chart (last
50 candles)** and a **daily chart (last 365 days)** side by side for every
ticker, with click-to-filter chips for each group and click-to-sort
columns. It's a compact scanning tool, not a scoring/ranking model like the
volume scan above.

- `scripts/watchlists.py` — the ticker universes and group definitions:
  - `SP500` — the same S&P 500 constituent list format as the main scan.
  - `SC_ETFS` / `SC_FX` / `SC_CRYPTO` — a small fixed ETF/FX/crypto
    watchlist.
  - `VSA_ASSETS` — 15 hand-curated themed groups (Tech & AI, Finance &
    Value, Aero & Defense, Biotech & Pharma, Cybersecurity, Nuclear &
    Power, etc.), each a short list of representative tickers.
  - `GROUPS` — all of the above merged into one dict keyed by group name,
    used to build the report's filter chips. A ticker can belong to more
    than one group (e.g. `AAPL` is both `S&P 500` and `TECH & AI`) — its
    row shows every group it's in, and it appears whenever any of its
    groups is selected.
- `scripts/dual_timeframe_scan.py` — the report generator:
  - Fetches both timeframes with `yfinance`, in chunks of 150 tickers
    (`--chunk-size` to change), with 3 retries and backoff per chunk —
    matching `scan_volume.py`'s conventions.
  - If a ticker fails on both timeframes it's skipped (not fatal to the
    run); if it fails on only one, its row still renders with the other
    chart and a "—" placeholder. The report footer states how many of the
    requested tickers actually rendered vs. were skipped, and why
    (delisted, renamed, or a transient fetch failure — not a bug in the
    report).
  - Charts are rendered as small inline SVG candlesticks rather than full
    interactive Plotly charts (like `plot_vsa2d.py` uses) — at ~650 rows x
    2 charts each, embedding a Plotly figure per chart would make the file
    enormous; SVG keeps it a single lightweight, fast-loading HTML file.
  - Each ticker's two charts are scaled independently to their own
    high/low range (not a shared/comparable price axis across tickers) —
    the point is to eyeball each ticker's own recent shape, not compare
    absolute price levels between tickers.
  - No company-name lookup — at this scale, an extra API call per ticker
    just for display names isn't worth it, so rows show ticker symbols
    only.
  - Sticky header row and sticky rank (`#`) column so you can keep your
    place while scrolling a ~650-row table on a small screen.

Run it locally:

```bash
python scripts/dual_timeframe_scan.py -o reports/dual_timeframe_latest.html
```

Or, for a fast offline smoke test with synthetic data (no network calls,
no yfinance rate limits):

```bash
python scripts/dual_timeframe_scan.py --demo --limit 24 -o /tmp/demo.html
```

It runs automatically as a second step in `.github/workflows/volume-scan.yml`,
right after the main volume scan, writing to
`reports/dual_timeframe_latest.html`. That step is marked
`continue-on-error: true` so a bad day for this scan never blocks the
primary volume scan's report from being committed.

## Quality dip scan

`scripts/quality_dip_scan.py` looks for financially strong companies whose
stock is trading near its 52-week low -- e.g. MSFT around $340 in mid-2026.
It writes `reports/quality_dip_latest.md` and shows up as the "Quality Dips"
tab on the dashboard.

- **Universe:** the S&P 500 plus the themed stock groups in
  `scripts/watchlists.py` (ETFs, FX, crypto and futures are skipped).
- **Price screen:** last close within `DIP_MAX_ABOVE_LOW` (default 15%)
  of the 52-week low, using one chunked `yf.download()`.
- **Quality screen** (`yf.Ticker(t).info`, run only on price-screen
  survivors). Every check must pass:
  - market cap >= `MIN_MARKET_CAP` (default $10B)
  - revenue growth >= `MIN_REVENUE_GROWTH` (default 5% YoY)
  - net margin >= `MIN_PROFIT_MARGIN` (default 10%)
  - positive free cash flow
  - net cash, or net debt <= `MAX_NET_DEBT_TO_EBITDA` (default 1.5x)
    EBITDA. A strict cash > debt test isn't used because Yahoo's
    `totalDebt` includes lease liabilities.
- Names failing exactly one check are listed as **close calls** (up to
  `TOP_N`). Missing data counts as a fail, so banks and insurers usually
  miss on FCF, which Yahoo doesn't report for them.

Run it locally (takes about 3-4 minutes):

```bash
python scripts/quality_dip_scan.py
```

### Backtest

`scripts/backtest_quality_dip.py` replays the same screen at every month-end
since 2005 and measures each signal's 1-year and 3-year total return against
SPY. It writes `reports/quality_dip_backtest.md`, which shows up as the
"Quality Dips Backtest" dashboard tab. It's a one-off research run, not part
of the scheduled workflow.

- **Financials:** SEC EDGAR XBRL 10-K data, which starts around 2009-2011.
  Each signal uses only the latest 10-K *filed* by that date, so nothing
  from the future leaks in.
- **Universe:** today's S&P 500 (with index join dates) and Nasdaq-100 from
  the NIBII repo's `data/` lists, plus this repo's watchlist. An S&P 500
  stock only counts from the date it joined the index.
- **Survivorship bias:** companies that collapsed and left the index are
  missing, so results are flattered.

```bash
SEC_USER_AGENT="Your Name you@example.com" python scripts/backtest_quality_dip.py
```

### Boost mix + leverage

`scripts/backtest_boost_mix.py` mixes NIBII's "Auto + News boost" momentum
plan with the quality-dip portfolio (100/0, 70/30, 50/50, 0/100) at 1x to
2x leverage. The margin rate is 6% or 8%, and weights are rebalanced weekly
using NIBII's `backtest_leverage.run`. Boost alone is also run from 2000 so
the dot-com crash and 2008 are included. It needs a local NIBII checkout
and a prior run of `backtest_quality_dip.py`. Output:
`reports/boost_mix_backtest.md`.

```bash
python scripts/backtest_boost_mix.py --nibii-dir ../NIBII
```

### Levering Boost: trend-gated leverage and put hedges

`scripts/backtest_boost_leverage_ideas.py` tests ways to lever NIBII's
"Auto + News boost" without the losses constant leverage suffers in
2000-02 and 2008:

- **Trend-gated leverage:** L x Boost while SPY is above its 200-day
  average at the Friday close, a lower level (1x, 0.6x or cash) otherwise.
- **SPY put hedge:** 3-month 10%-out-of-the-money SPY puts on the levered
  exposure, rolled monthly. They're priced with Black-Scholes at VIX + 4
  points.

It skips buying calls on the picks: NIBII's `backtest_options_only.py`
already shows that loses money over 2000-2026. Output:
`reports/boost_leverage_ideas.md`.

```bash
python scripts/backtest_boost_leverage_ideas.py --nibii-dir ../NIBII
```
