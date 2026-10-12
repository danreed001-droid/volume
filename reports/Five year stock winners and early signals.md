# AI Suppliers Won; Volume Spikes Flagged Them Early

From October 2021 to October 2026 the biggest US stock winners were mostly not the famous AI names. They were the suppliers behind the AI data-center build-out:
- **Celestica (+3,769%)**, **Sterling Infrastructure (+2,149%)** and **Comfort Systems (+2,142%)**
- **Micron (+1,422%)** and **Bloom Energy (+1,313%)**
- Powell, Credo, Modine, Lumentum and Vertiv

All of these made roughly 10–38x. NVIDIA made about 11x and Palantir about 9x, while SPY returned about +91% over the same window ([yfinance](https://finance.yahoo.com)).

The cause was nearly always the same. A measurable demand shock (AI capex, electricity demand, memory pricing, GLP-1 drugs) showed up in **an earnings report or contract that guided far above consensus**. The stock then made a single "ignition day": in the large-cap sample, a **median ~20% one-day gain on ~4.8x its 50-day average volume**, usually closing at a new 52-week high.

That signature is exactly what a volume-spike scanner sees, so the user's tool is pointed at the right phenomenon. As written, though, it cannot tell an ignition from noise. It ignores price direction. It cannot compute 52-week highs or 200-day averages from its 9-month history. And it never looks at NYSE stocks outside the S&P 500, which is where Celestica, the #1 name, trades.

The honest caveats are severe:
- Only about 4% of US stocks account for all net market wealth creation.
- Observable traits explain about 2% of which stocks become decade-scale winners.
- High-volume breakouts fail more often than quiet ones.
- Even the true winners fell 35–60% at least once after igniting.

The realistic goal is a scanner that puts real ignitions on a short watchlist within one to three days, plus a playbook of small, many, rule-based positions that survive the frequent false signals.

## Data-center suppliers beat the AI headliners by 2–4x

The five-year leaderboard rewards whoever sold the "picks and shovels." The table below combines the large-cap and small/mid-cap screens. All figures are computed from Yahoo Finance daily data through the 2026-10-09 close ([yfinance](https://finance.yahoo.com)).

The two research passes used slightly different start dates (Oct 1 vs Oct 11, 2021), so Celestica shows +3,769% or +3,815%, and SPY +91% or +79%, depending on the start. Rankings are unaffected. Anything after roughly June 2026 rests on the price data alone and could not be checked against press coverage.

| Group | Names (5-yr return) | What they sold |
|---|---|---|
| AI hardware and connectivity | **CLS +3,769%**, CRDO +1,759% (since Jan 2022 IPO), LITE +1,190%, DELL +1,110%, SMCI +1,032%, NVDA +1,013%, ANET +818%, AVGO +702% | Servers, switches, optics, cables, GPUs and custom chips |
| Memory and storage | **MU +1,422%**, STX +1,005%, WDC +840%, SNDK +4,294% (since Feb 2025 spin) | HBM/DRAM and NAND during a shortage |
| Data-center construction and cooling | **STRL +2,149%**, **FIX +2,142%**, POWL +2,210%, MOD +1,421%, IESC +1,179%, VRT +996% | Site work, mechanical/electrical, switchgear, cooling |
| Power | BE +1,313%, VST +901%, GEV +669% (since spin), CEG +637% (since spin) | Fuel cells, nuclear, turbines |
| Software, consumer and other | PLTR +788%, LLY +428%, CRS +1,026%, ATI +1,008% | AI software, GLP-1 drugs, aerospace alloys |

Sources: [yfinance large-cap screen](https://finance.yahoo.com); [yfinance small/mid-cap screen](https://finance.yahoo.com/quote/FIX/history).

Several of these were small or mid caps in 2021 that *became* large caps: CLS, STRL, FIX, BE, LITE, CRDO and POWL. That matters for the scanner, because a universe limited to today's index members would have missed them early.

Start date matters as much as stock selection. Stocks that crashed hardest in 2022 look mediocre on a five-year basis but were the largest winners from the low:
- **Carvana: +13% over five years, but +8,466%** from its December 2022 low, after a −99% collapse.
- **AppLovin: +217% over five years, but +2,879%** from its low, after −92%.
- **Palantir: +3,384%** from its low, after −78%.
- **Robinhood: +1,482%** from its low, after −84%.

Source for all four: [yfinance](https://finance.yahoo.com).

The small-cap screen found even larger trough-to-peak moves: Rigetti ~150x, Sezzle ~139x, GeneDx ~135x, Carvana ~129x and D-Wave ~108x. Several were negative or barely positive point-to-point because they first fell 90% or more ([yfinance](https://finance.yahoo.com/quote/CVNA/history)).

So "which stocks shot up" has two answers:
- **Compounders** rose steadily from reasonable starting points.
- **Trough rockets** were nearly bankrupt or ignored in late 2022 and then re-rated violently.

## Guidance shocks tied to a capex cycle drove the durable moves

Almost every winner's move began with a **quantified surprise about future demand**, not a story.

**NVIDIA** guided its next quarter to about **$11B against roughly $7.2B consensus** in May 2023 and rose 24% the next day ([StreetBeat](https://news.streetbeat.com/article/32562219); [Nasdaq](https://www.nasdaq.com/articles/why-nvidia-surged-36.3-in-may)).

**Broadcom** re-rated in December 2024. Its CEO sized the AI chip and networking opportunity at **$60–90B for fiscal 2027**, and the market cap crossed $1 trillion ([Investing.com/Reuters](https://investing.com/news/stock-market-news/broadcom-rallies-on-forecast-for-booming-ai-chip-demand-3771047)).

**Celestica** beat the top of its own guidance and raised its 2023 outlook. The shares rallied "on high volume" ([Celestica IR](https://corporate.celestica.com/node/14826); [Globe and Mail](https://arc-dev.theglobeandmail.com/investing/markets/inside-the-market/article-tuesdays-tsx-breakouts-with-strong-earnings-growth-and-ai-exposure)).

**Powell Industries** reported in August 2023 that backlog had **nearly tripled to a record $1.3B**, with gross margin up 810 basis points. That was before the data-center narrative had even attached to it ([SEC 8-K](https://www.sec.gov/Archives/edgar/data/80420/000008042023000036/ex99-1q32023earningsrelease.htm)).

**Credo** guided to $115–125M against a much smaller base and rose 48% in a day ([Barchart](https://www.barchart.com/story/news/29876050/why-credo-technology-group-rocketed-nearly-50-today)).

The non-earnings ignitions were structural events, and they were just as quantifiable:
- **Vistra** bought 4,000 MW of nuclear capacity ([POWER Magazine](https://www.powermag.com/vistra-expands-nuclear-portfolio-in-3-4-billion-deal-for-energy-harbor/)).
- **Constellation** signed a 20-year Microsoft deal to restart Three Mile Island and rose 22% ([Nasdaq](https://www.nasdaq.com/articles/why-constellation-energy-stock-surged-more-30-september)).
- **Bloom Energy** signed an up-to-1 GW fuel-cell agreement with AEP that one analyst called "literally 10x" expectations ([Barchart](https://www.barchart.com/story/news/29606224/why-bloom-energy-stock-rocketed-48-on-friday)).
- **Carvana** guided to positive EBITDA, then cut more than $1.2B of debt while roughly half its float was sold short ([CNBC](https://www.cnbc.com/2023/06/08/carvana-shares-surge-after-company-boosts-second-quarter-guidance.html); [Investing.com](https://investing.com/news/stock-market-news/carvana-enters-deal-with-noteholders-to-cut-debt-by-12-billion-3128760)).
- **Turnarounds** ignited on first profits: Sezzle's Q1 2024 net income exceeded all of 2023 ([Nasdaq](https://www.nasdaq.com/press-release/sezzle-reports-first-quarter-2024-results-2024-05-08)), and Root's revenue rose 173% against a much lower consensus ([Barchart](https://www.barchart.com/story/news/25296547/up-675-ytd-what-s-behind-the-breakout-in-root-stock)).

Two further patterns matter for timing.

**Skepticism coexisted with the early move.** Palantir still carried Hold and Sell ratings after its May 2023 ignition ([Benzinga](https://benzinga.com/news/earnings/23/05/32273478/palantir-delivers-another-profitable-quarter-touts-new-ai-platform-shares-surge)). TD Cowen called Broadcom's market-size claim "difficult to prove/disprove" ([FXStreet](https://www.fxstreet.com/news/broadcom-is-the-newest-trillion-dollar-company-202412131520)). A big gap on fresh news is therefore not proof that the information is already priced in.

**S&P 500 inclusion acted as a later accelerant.** APP closed up 11.6% and HOOD up 15.8% on the session after their September 2025 addition was announced ([Yahoo Finance](https://finance.yahoo.com/news/robinhood-applovin-join-p-500-173000838.html)). A Goldman study found new additions beat the equal-weight index by about 4 points on announcement day, but there is no permanent value effect ([Sherwood](https://www.sherwood.news/markets/robinhood-applovin-vault-higher-as-the-inclusion-effect-is-in-full-force); [Barchart](https://www.barchart.com/story/news/28519135/palantir-stock-will-join-the-sp-500-in-september-history-says-it-could-soar-afterward)).

What separated compounders from round-trips was the *kind* of demand:
- **Theme names collapsed.** All 16 theme stocks checked (quantum, small nuclear reactors, space, eVTOL, speculative AI software, crypto miners turned AI hosts) sit **47–87% below their peaks**. Several were pre-revenue at ignition: Oklo had no revenue, and AST SpaceMobile reported $0.5M in its quarter ([Barchart](https://www.barchart.com/story/news/29410919/why-oklo-stock-skyrocketed-178-in-october); [SpaceNews](https://spacenews.com/?p=423957)).
- **Theme rallies reversed on single headlines.** Quantum names fell 32–46% in one day after Jensen Huang said practical quantum computing was decades away ([Nasdaq](https://www.nasdaq.com/articles/quantum-computing-stock-rally-over-so-soon)).
- **Backlog-and-earnings compounders mostly held.** About 10 of 15 sit within ~40% of their peaks.
- **Earnings alone were not enough.** Consumer names with real earnings (Celsius, Duolingo, Cava, Hims) still fell 55–72% from their peaks when growth slowed against high multiples ([yfinance](https://finance.yahoo.com/quote/CELH/history)).

The durable recipe was revenue already present and accelerating, a multi-year backlog, and demand tied to a measurable capex cycle, confirmed again every quarter.

## Winners ignited on 10–60% gaps at 3–15x volume, often more than once

The large-cap analysis identified 23 ignition days. Measured against the 50-day average volume ([yfinance](https://finance.yahoo.com)):
- Volume ranged from **2.1x (Eli Lilly) to 14.8x (Dell)**, with a **median near 4.8x**.
- The median one-day gain was about 20%.
- **16 of 23 closed at a new 52-week high.**
- Fourteen were within 10% of their high the day before.
- Fifteen had six-month relative strength above the S&P 500.

Small caps were more extreme. Typical ignition days gained 20–75% on **5–85x** average volume: Root traded 85x, GeneDx 35x and AST SpaceMobile 22x ([yfinance](https://finance.yahoo.com/quote/ASTS/history)).

These are precisely the days a volume-ratio scanner ranks near the top. A sample of the clearest cases:

| Ticker | Ignition date | One-day move | Volume vs 50-day | New 52w high? | Trigger |
|---|---|---|---|---|---|
| NVDA | 2023-05-25 | +24% | 3.6x | Yes | Q2 guide ~$11B vs ~$7.2B consensus |
| PLTR | 2023-05-09 | +23% | 7.5x | No (−32%) | Second GAAP-profitable quarter, AIP demand |
| CLS | 2023-07-28 | +15% | 7.0x | Yes | Beat-and-raise |
| VRT | 2023-08-02 | +29% | 6.8x | Yes | Q2 2023 results |
| APP | 2023-08-10 | +27% | 8.2x | No (−27%) | AXON 2.0 ramp |
| DELL | 2024-03-01 | +32% | **14.8x** | Yes | Q4 FY24 results |
| BE | 2024-11-15 | +59% | 10.7x | Yes | AEP 1 GW agreement |
| CRDO | 2024-12-03 | +48% | 6.8x | Yes | Guide $115–125M |
| SNDK | 2025-09-04 | +18% | 4.3x | Yes | NAND undersupply through 2026 |

Source: [yfinance](https://finance.yahoo.com), with catalysts sourced in the section above.

Two patterns should shape the scanner's design.

**Ignitions cluster by theme.** NVIDIA's May 2023 report produced same-week high-volume breakouts in Broadcom (+11.5%, 3.9x) and Vertiv (+14%, 8x, new high) ([yfinance](https://finance.yahoo.com)). Ignition dates bunch into waves:
- the AI wave of February–August 2023
- the power re-rating of 2024
- the post-election wave of November–December 2024
- the memory supercycle of April–September 2025

When one leader posts a blowout, its suppliers are the next candidates.

**The first ignition is frequently not the one that pays.** Micron's December 2023 ignition was only +15% a year later, after a −58% drawdown, and Dell's was +10% after −60%. Both then delivered their real moves in a second leg ([yfinance](https://finance.yahoo.com)). In small caps, many first gaps went nowhere over the next 60 sessions:
- Powell −13%
- Sterling −1%
- Sezzle about 0%
- Hims −16%

The big trends came from **repeated** qualifying gaps on successive earnings reports. Powell, AppLovin, Credo and Sezzle each had three to six ([yfinance](https://finance.yahoo.com/quote/ASTS/history)). "Second or third consecutive earnings gap-up" is a better filter than "first spike."

## Base rates make most signals fail, and hindsight hides it

Everything above was selected by looking backward, so the evidence for prediction is weaker than the case studies suggest.

**Most stocks lose.** Most US common stocks since 1926 have lifetime returns below Treasury bills. **The best-performing 4% explain the entire net gain of the market**, and 83 firms (0.3%) produced half of $47 trillion in excess wealth ([ASU W.P. Carey](https://news.wpcarey.asu.edu/20180917-do-stocks-outperform-treasury-bills); [The Idea Farm](https://theideafarm.com/markets/extreme-stock-market-performers-part-iv-can-observable-characteristics-forecast-outcomes/)). A secondary estimate puts the 10-year 10x rate at **0.7–2% of Russell 3000 stocks** ([QuantifiedStrategies](https://www.quantifiedstrategies.com/whats-the-probability-of-a-10x-stock/)). A five-year 10x is rarer still.

**Traits explain almost nothing in advance.** Bessembinder tested observable characteristics directly against decade-scale outcomes. They explained **about 2% of the variation** in subsequent decade returns ([The Idea Farm](https://theideafarm.com/markets/extreme-stock-market-performers-part-iv-can-observable-characteristics-forecast-outcomes/)). Even a scanner that triples the hit rate leaves most flagged names failing.

**The well-replicated signals predict modest averages, not multi-baggers.** Those signals are:
- **Momentum:** about 5.5% a year after publication, half its in-sample level ([ETF.com](https://www.etf.com/sections/index-investor-corner/swedroe-momentum-really-dead)).
- **Nearness to the 52-week high:** it beats raw momentum and does not reverse ([SUFE summary of George & Hwang 2004](https://academicnewsletter.sufe.edu.cn/info/361244)).
- **The high-volume return premium:** unusually high-volume stocks tend to rise over the following month ([Gervais, Kaniel & Mingelgrin](https://ideas.repec.org/a/bla/jfinan/v56y2001i3p877-919.html)).
- **Earnings-day volume combined with surprise:** post-announcement drift rises with unexplained earnings-day volume ([Garfinkel & Sokobin](https://www.biz.uiowa.edu/faculty/jgarfinkel/pubs/drift_JAR.pdf)).

Each is worth a few percent a year in portfolio averages.

**The classic earnings-drift edge has largely disappeared in liquid stocks.** Martineau finds post-earnings drift in non-microcap US stocks "completely disappeared" by 2006 ([Martineau](https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf)). Later work shows surviving drift is insignificant once microcaps are excluded ([UCLA Anderson Review](https://anderson-review.ucla.edu/is-post-earnings-announcement-drift-a-thing-again/)). On S&P 500 and Nasdaq large caps, the scanner should not expect the gap itself to keep drifting. Any edge comes from the minority of gaps that start multi-quarter re-ratings.

**Volume alone makes breakouts less reliable, not more.** In Bulkowski's study of about 8,000 chart patterns, up-breakouts on above-average volume gained slightly more (37.6% vs 35.8%). But they **failed nearly three times as often (14% vs 5%)** and **pulled back to the breakout level about three times as often (57% vs 18%)** ([Bulkowski](https://thepatternsite.com/VolumeStudy.html)).

**The practitioner playbooks are hindsight samples.** O'Neil's CAN SLIM, Minervini's trend template and Mayer's *100 Baggers* all study winners after the fact, with no control group of lookalikes that failed ([AAII](https://www.aaii.com/files/journal/pdf/9874_william-oneil-can-slim-approach-to-selecting-growth-stocks.pdf); [Livewire](https://www.livewiremarkets.com/wires/100-baggers-common-traits)). No independent test of the Minervini template was found, and no rigorous hit rates exist for pocket pivots, VCPs or episodic pivots.

**This study shares the same flaw.** The 23 ignitions above were chosen *because* they worked. Nobody counted how many other 20% gaps on 5x volume in 2023–2025 led nowhere. The research never backtested the false-positive rate. That number is the single most important unknown, and the user's own data can produce it.

**Real failures look identical at ignition.** Super Micro's January 2024 guidance raise produced a +36% day on 7.3x volume at a new high, exactly the winning signature. Within eight months the stock was down **85%**: a short-seller report, then its auditor resigned ([KOB/AP](https://kob.com/news/business-money/super-micro-computers-shares-plunge-after-accounting-firm-resigns)). It remains about 65% below that peak ([yfinance](https://finance.yahoo.com)).

## Eight scanner upgrades turn volume spikes into ignition candidates

`scripts/scan_volume.py` currently has four limitations:
- It downloads volume only, with `period="9mo"`.
- It ranks purely by `latest / mean(prior N)`.
- Its "fresh volume high" test checks the prior-100 maximum, which already implies the prior-50 test.
- It draws from S&P 500 constituents, Nasdaq-listed symbols and ten ETFs.

As a result it ranks a −30% crash day the same as a +30% breakout. It cannot test trend or 52-week-high conditions, which need about 252–300 sessions. And it misses NYSE and NYSE American stocks outside the S&P 500. That gap covered **Celestica, the best stock of the period**, and plausibly several of the industrial compounders while they were still mid caps, although current index membership was not verified for every name.

The upgrades below are ordered by expected value per hour of work. Thresholds are sourced where a source exists and otherwise marked as judgment calls to tune by backtest.

| # | Upgrade | Rule (daily OHLCV, yfinance) | Why |
|---|---|---|---|
| 1 | **Widen the universe** | Add Nasdaq Trader's `otherlisted.txt` (NYSE/NYSE American/Arca common stocks); keep ADV ≥100k and add close ≥ $5 and 50-day dollar volume ≥ ~$5–20M (judgment) | The top winner and several compounders were NYSE-listed non-S&P names |
| 2 | **Pull OHLC, 2 years, adjusted** | `period="2y"`, `auto_adjust=True`, keep Open/High/Low/Close/Volume for all tickers | Needed for 200-day MA slope, 52-week high and gap math |
| 3 | **Direction and close quality** | Up day; close-location value (C−L)/(H−L) ≥ 0.6 (judgment); report down-day spikes separately as distribution | Removes dumps and intraday fades |
| 4 | **Gap / episodic-pivot flag** | Open ≥ 1.08 × prior close and volume ≥ 3x the 50-day average, close ≥ open or in the upper half of the range | Matches the EP definition of an 8–10%+ gap on 2–4x+ volume ([TradingSim](https://tradingsim.com/blog/episodic-pivot-power-earnings-gap-buyable-gap-up-explained/)) and the ignition sample |
| 5 | **Trend and 52-week gate** | C > SMA50 > SMA150 > SMA200; SMA200 rising over 21 sessions; C ≥ 0.75 × 52-week high and ≥ 1.25 × 52-week low; extra flag when close is a new 252-day high | Trend template ([actionalerts](https://actionalerts.substack.com/p/using-mark-minervinis-trend-template)) and the 52-week-high effect; 16 of 23 ignitions closed at a new high |
| 6 | **Relative-strength rank** | RS = 0.4·r63 + 0.2·r(63–126) + 0.2·r(126–189) + 0.2·r(189–252), percentile ≥ 80; flag RS-line (C/SPY) 252-day high before price | IBD-style approximation ([TradingView](https://www.tradingview.com/script/lsLzfQqs-RS-Rating-Multi-Timeframe)); 15 of 23 ignitions had RS > 1 |
| 7 | **Repeat-ignition and group memory** | Store each day's flags; boost names with ≥2 qualifying gaps in 12 months; boost names whose industry peers flagged within 5 sessions | Second and third gaps, and sympathy clusters, carried the big trends |
| 8 | **Calendar and baseline hygiene** | Use a median baseline alongside the mean; down-weight monthly opex, triple-witching/S&P rebalance Fridays, Russell reconstitution and index-add effective dates | The June 2026 Russell close set a record 4.59B shares on the Nasdaq Closing Cross ([Mondo Visione](https://mondovisione.com/news/record-trading-volume-on-the-nasdaq-closing-cross-during-the-june-2026-russell-u-2026626/)), which is mechanical, not conviction |

Two further flags are cheap once the data is in hand.

**A pocket-pivot flag** marks an up day whose volume exceeds the largest down-day volume of the prior 10 sessions, near the 10- or 50-day average ([LuxAlgo](https://www.luxalgo.com/library/concept/pocket-pivot/)). It catches quieter accumulation before the gap.

**A turnaround lane** catches a different kind of ignition. Palantir, AppLovin, Vistra and Carvana all ignited 20–72% *below* their 52-week highs, so the trend gate rejects them. Run them as a separate list, gated instead on 3-month relative strength and a ≥15% gap on ≥5x volume. Expect higher volatility and lower reliability there.

Ranking should change too. Use the volume ratio only as a qualifier and sort on a composite: setup flags, RS percentile, proximity to the 52-week high, then volume ratio. The core logic is about twenty lines of pandas:

```python
d = ohlcv  # DataFrame: Open High Low Close Volume, 2y, auto_adjust=True
v50 = d.Volume.shift(1).rolling(50).mean()
vr = d.Volume / v50
clv = (d.Close - d.Low) / (d.High - d.Low).replace(0, float("nan"))
gap = d.Open / d.Close.shift(1) - 1
sma = {n: d.Close.rolling(n).mean() for n in (50, 150, 200)}
hi52 = d.Close.shift(1).rolling(252).max()
lo52 = d.Close.rolling(252).min()
trend_ok = ((d.Close > sma[50]) & (sma[50] > sma[150]) & (sma[150] > sma[200])
            & (sma[200] > sma[200].shift(21))
            & (d.Close >= 0.75 * hi52) & (d.Close >= 1.25 * lo52))
up_quality = (d.Close > d.Close.shift(1)) & (clv >= 0.6)
ignition = up_quality & (vr >= 3) & (gap >= 0.08)
breakout = up_quality & (vr >= 1.5) & (d.Close > hi52)
```

Before trusting any of this, the scanner should **backtest itself**. Run the flags daily over 2015–2026 on the widened universe, including delisted tickers where obtainable, since yfinance drops many. For each flag type, record:
- forward 20-, 60-, 120- and 250-day returns versus SPY
- the share of flags reaching +50% and +100%
- the maximum adverse excursion

That converts the anecdotes in this report into the user's own base rates. It also settles the question the research could not: of all the days that looked like NVIDIA's May 2023 or Dell's March 2024, how many led anywhere? Assume any edge found will be about half as large live: published anomalies lose about 50% after publication ([arXiv survey of McLean & Pontiff](https://arxiv.org/pdf/2209.13623)).

## A survivable playbook trades many small bets and re-enters second legs

The evidence points to a playbook built around one fact: **most flags fail, and the few winners will still fall 35–60% at some point.**

Nearly every AI and power winner bottomed near 2025-04-04 in the DeepSeek-plus-tariff selloff. Vertiv fell 61%, Credo 61%, AppLovin 57%, Celestica 54%, Constellation 51% and Arista 50%. Many show further 40–60% drawdowns from mid-2026 peaks that were still open at the last close ([yfinance](https://finance.yahoo.com)). Only Eli Lilly and GE Vernova held their post-ignition drawdowns to about −38% or better. **A fixed −20% stop would have shaken a holder out of almost every winner**, usually in Q1 2025.

The trader therefore has to choose a style and not blend them.

**The swing-momentum style** fits the scanner's daily cadence:
- **Entry.** Buy the ignition day's close or the next day's opening range.
- **Stop.** Place it at the gap-day low, or 3–4% below it ([TradingSim](https://tradingsim.com/blog/episodic-pivot-power-earnings-gap-buyable-gap-up-explained/)).
- **Profit-taking.** Take one-third to one-half off around +20% or after three to five strong days.
- **Trailing.** Trail the rest on the 10- or 20-day moving average.
- **Sizing.** Size so a stop-out costs about 0.5–1% of equity (judgment). Expect many small losses, because high-volume breakouts often pull back to the breakout level ([Bulkowski](https://thepatternsite.com/VolumeStudy.html)).
- **What it captures.** The early leg. Repeated re-entries capture more of a multi-year trend.

**The compounder style** uses the scanner to find candidates, then holds through volatility:
- **Admission.** Admit only names showing revenue acceleration, a growing backlog or rising margins at ignition. FIX, POWL, STRL, CRDO and SEZL all did.
- **Sizing.** Hold small starting positions, sized to survive a 50–60% drawdown.
- **Adding.** Add on the second and third qualifying earnings gaps.
- **Exit.** Exit on a broken fundamental thesis (guidance cut, auditor or accounting event, lost customer) rather than on price alone.

**Both styles share five rules.**

1. **Hold many positions, sized small and roughly equal.** Return skew means concentrated portfolios usually underperform even when the expected value is fine ([ASU W.P. Carey](https://news.wpcarey.asu.edu/20180917-do-stocks-outperform-treasury-bills)).
2. **Re-enter rather than give up.** Micron and Dell paid on their *second* ignition, so a stopped-out name that re-ignites goes straight back on the list.
3. **Respect regime.** Momentum crashes in panic rebounds. Past losers returned +163% against +8% for winners in March–May 2009 ([Daniel & Moskowitz](https://www.nber.org/system/files/working_papers/w20439/w20439.pdf)). Cut new-entry size after large index drawdowns and volatility spikes.
4. **Watch group breadth for the exit.** Theme peaks clustered across whole groups and broke on single headlines. Quantum and nuclear names peaked together on 2025-10-07 to 10-15 ([yfinance](https://finance.yahoo.com/quote/OKLO/history)). The research suggests (untested) that exiting when several peers post high-volume down days together would have avoided most of the 50–80% round-trips. The scanner's down-day spike list is the natural input.
5. **Treat short interest and options data as tie-breakers only.** High short interest is at best a weak *bearish* signal ([Asquith, Pathak & Ritter](https://www.nber.org/system/files/working_papers/w10434/w10434.pdf)), and public option volume predicts little beyond the next day ([Kang, Kim & Lee](https://acfr.aut.ac.nz/__data/assets/pdf_file/0003/56424/38716-C-Kang-option_July2016_CMK_v3.pdf)).

## Conclusion

The biggest change in understanding is where the edge sits. It does not come from forecasting which company becomes the next Celestica; Bessembinder's roughly 2% explanatory power says that is close to impossible. It comes from **reacting fast to public, quantified demand shocks** and then **managing the many that fail**.

Over this period those shocks were unusually legible:
- guidance 50% above consensus
- tripled backlogs
- gigawatt-scale contracts
- whole supply chains igniting within days of one leader's report

A volume scanner is a good instrument for that, because the market announces these events with 3–15x volume. The user's current tool hears the noise but cannot yet tell its direction or context.

The next leaderboard will probably not be AI suppliers again. The process transfers, though: watch for the theme where a leader posts a quantified guidance shock, then scan its suppliers for repeat gaps.

The most valuable next step is not another indicator. It is running the upgraded flags back through 2015–2026 to measure the false-positive rate. That number, not the list of past winners, should set the position size.
