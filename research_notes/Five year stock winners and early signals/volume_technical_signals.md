# Volume- and Price-Based Technical Signals That Precede Large, Sustained Stock Advances

Note on sourcing: most practitioner definitions (pocket pivot, VCP, episodic pivot, IBD RS rating, breakout volume) are only available here from **secondary sources** (TradingView scripts, LuxAlgo, Tradezella, TradingSim). The original books and Stockbee posts were not retrieved. Academic evidence (George-Hwang, Gervais-Kaniel-Mingelgrin, Garfinkel-Sokobin, Asquith-Pathak-Ritter) is better sourced. Bulkowski's own site is a primary source for breakout statistics.

## What exact rules (with numbers) would best upgrade a raw volume-spike scanner into a "potential big winner early" scanner?

### Takeaway
The most consistently documented upgrades fall into three groups. (1) Require the spike to be an **up day with a strong close** in a stock that is **already in a Stage 2 / trend-template uptrend and near its 52-week high**. (2) Add **pattern-specific volume signatures**: pocket pivots (up-day volume greater than the largest down-day volume of the prior 10 sessions), breakouts on roughly 1.4–2x the 50-day average volume after a tight, low-volume base (VCP), and catalyst gap-ups of 8–10% or more on 2–4x+ volume (episodic pivot / power earnings gap). (3) Rank by **IBD-style relative strength**, with extra weight when the RS line makes a new high before price does. Each of these can be computed from daily yfinance OHLCV.

### Cited Findings

**Episodic pivot / power earnings gap / buyable gap-up**
- Episodic pivot (Stockbee / Qullamaggie) criteria: the gap "needs to be considerable: 8-10% or more", and volume should be a multiple of average daily volume "like 2x, 3x, 4x or more", appearing early (pre-market or the first 30 minutes). The catalyst must be significant (earnings beat, FDA news, upgrade, and similar). Check whether the stock was "consolidating in a constructive range" or already over-extended before the gap. The article treats the O'Neil power earnings gap as essentially the same setup. — [TradingSim](https://tradingsim.com/blog/episodic-pivot-power-earnings-gap-buyable-gap-up-explained/)
- Entry and stop: an opening-range "low risk entry at the low of the day". For Morales's buyable gap-up, allow "a good 3-4% on the downside" below the gap-day intraday low. Qullamaggie trails with the 10- or 20-day MA, and O'Neil and Qullamaggie both take "1/3 to 1/2" of profits at a 20% gain or 3–5 days into the move. — [TradingSim](https://tradingsim.com/blog/episodic-pivot-power-earnings-gap-buyable-gap-up-explained/)
- "EP 9 Million" variant: flags any stock trading at least 9M shares in a day, far above its normal volume, with a minimum price (e.g. above $3). — [Tradezella](https://www.tradezella.com/strategies/episode-pivot-strategy). A community TradingView script implements it as volume > 9M, volume > prior bar, and price > +4%. This is a third-party interpretation. — [TradingView script](https://vn.tradingview.com/script/vPiS8SMM)
- Buyable gap-up (Morales/Kacher) as described by IBKR: a gap up in price on substantial volume, then a later pullback on decreasing volume back toward the gap level. — [Interactive Brokers Campus](https://www.interactivebrokers.com/campus/?p=214153)

**Pocket pivot (Morales & Kacher)**
- Volume rule: an up day whose volume exceeds the **largest down-day volume of the prior 10 sessions**. It should occur in or emerging from a constructive base, typically near support at the 10- or 50-day MA, in an uptrend, and not extended. Up days that wedge higher on quiet volume, or that fire inside downtrends, are "improper". — [LuxAlgo](https://www.luxalgo.com/library/concept/pocket-pivot/)
- Only the volume signature is precisely defined; base and fundamental criteria must be judged separately. The source is "Trade Like an O'Neil Disciple". — [TradingView open-source Pocket Pivots script](https://www.tradingview.com/script/Y8HdDerB-Pocket-Pivots)

**Breakout volume threshold (O'Neil/IBD tradition)**
- Breakout-day volume should exceed the 50-day average by 40%+ (i.e. ≥1.4x). Some traders require 100% (2x). The buy point is the handle high plus about $0.10, and volume should contract in the handle. — [Tapeboard glossary](https://tapeboard.com/glossary/what-is-a-cup-and-handle-pattern); [StockAlarm](https://pro.stockalarm.io/blog/cup-and-handle-pattern-guide). No primary IBD page confirming 40% was found.

**VCP / volume dry-up (Minervini)**
- A base with typically 2–4 (sometimes 5–6) contractions, each shallower than the last, e.g. about 20% → about 10% → about 5%. Volume shrinks along with price, with a clear dry-up near the end. The pivot is the high of the final tight area, the entry is through it on volume expansion, and the stop goes under the last contraction low. The pattern is meant to sit inside a trend-template uptrend. — [LuxAlgo VCP](https://www.luxalgo.com/library/concept/volatility-contraction-pattern/)
- Rule-of-thumb contraction ranges: 20–35%, 10–20%, 5–15%, 3–8%, with breakout volume ≥50% above average. These are not confirmed as Minervini's own numbers. — [skills.cat Minervini page](https://skills.cat/skills/copyleftdev/sk1llz/minervini-swing-trading)

**Trend template / Stage 2**
- Minervini trend template: price > 150 and 200 DMA; 150 > 200 DMA; 200 DMA rising for at least 1 month; 50 > 150 and 200; price > 50 DMA; price ≥25% (30% in "Trade Like a Stock Market Wizard") above the 52-week low; price within 25% of the 52-week high; IBD RS rating ≥70 (preferably 80s–90s). — [actionalerts Substack](https://actionalerts.substack.com/p/using-mark-minervinis-trend-template); [TradingView trend-template scripts](https://www.tradingview.com/scripts/trend-template/)
- Weinstein Stage 2 breakout: the 30-week MA turns up, and price closes above Stage 1 resistance. Volume thresholds differ by source. One gives ≥2x the recent average ([MQL5](https://www.mql5.com/en/articles/22746)). A forum post citing the book gives "two times the four week average or greater on the breakout week, or three times average daily volume on a breakout day" ([stageanalysis.net](https://www.stageanalysis.net/forum/printthread.php?tid=14)). Another uses ≥1.5x the 20-week median ([TradingView DIVISLAB](https://in.tradingview.com/chart/DIVISLAB/jofJTfN1-DIVISLAB-Stage-2-Breakout/)).

**Relative strength**
- IBD-style RS approximation: weighted 12-month performance = 40% on the last 63 trading days plus 20% on each of the three prior 63-day quarters. This is then percentile-ranked 1–99 across the universe. IBD's real formula is proprietary. — [TradingView RS Rating script](https://www.tradingview.com/script/lsLzfQqs-RS-Rating-Multi-Timeframe)
- RS line (price / index) "blue dot": shown when the RS line hits a new 52-week high. Special emphasis goes to cases where the RS line makes its high **before** price does. — [TradingView ChillLax RS Line script](https://www.tradingview.com/script/11Di8Fti-ChillLax-Relative-Strength-Line-with-NewHigh-NewLow-Blue-Dot)

### Inferences
Below is a proposed concrete daily rule set, built from the sources above. Thresholds are the sourced ones where available; where marked, they are my choices.
1. **Liquidity/universe**: keep the 100k ADV filter. Consider adding close ≥ $5–10 and 50-day dollar volume ≥ about $5–20M (my choice; the EP sources use a > $3 minimum).
2. **Volume quality**: today's volume ≥1.4x the 50-day average (IBD) and ideally ≥2x. Also require an up day (close > prior close) and a close in the upper part of the day's range: close location value (C−L)/(H−L) ≥ 0.5–0.7 (my threshold; the CLV concept underlies the A/D line). Drop down-day spikes, or keep them only as a distribution warning.
3. **Trend gate (Stage 2 / trend template)**: C > SMA50 > SMA150 > SMA200; SMA200 today > SMA200 21 sessions ago; C ≥ 1.25–1.30 × 52-week low; C ≥ 0.75 × 52-week high.
4. **RS gate**: RS score = 0.4·r63 + 0.2·r126_63 + 0.2·r189_126 + 0.2·r252_189, percentile-ranked within the universe ≥ 70 (ideally ≥ 80–90). Flag when the RS line (C / SPY) reaches a 252-day high, with a bonus if price has not yet reached its 252-day high.
5. **Setup flags** (each scored separately):
   - *Breakout*: close > max(high of prior N days, N = 20–65 or 252 for a 52-week high) with volume ≥1.4–2x the 50-day average.
   - *Pocket pivot*: up day, volume > max(volume on down days in the prior 10 sessions), close ≥ SMA10 or SMA50 and within about 5% of it (my "not extended" proxy).
   - *Episodic pivot / gap*: open ≥ 1.08 × prior close (8%+ gap), volume ≥ 3x the 50-day average (or ≥ 9M shares), and close ≥ open or close in the upper half of the range (the gap "held" intraday). Prior 60–120 sessions range-bound (my proxy for "constructive range / not extended").
   - *VCP / dry-up*: in the 10 sessions before the breakout, average volume ≤ 0.5–0.7 × the 50-day average (my threshold). The 10-day true-range % is the lowest of the last N, or the successive pullback depths decline.
6. **Ranking**: score = setup flags + RS percentile + volume ratio + proximity to the 52-week high (George-Hwang), instead of ranking by raw volume ratio alone.

### Gaps
- No primary Morales/Kacher, Minervini, Weinstein, IBD, or Stockbee text was retrieved. Thresholds come from secondary implementations, and some (VCP contraction depths, Weinstein's 2x) conflict across sources.
- No published, quantified hit rate for pocket pivots, VCPs, or episodic pivots was found. The evidence for them is anecdotal (e.g. APPS +1,170% after an EP, per [TradingSim](https://tradingsim.com/blog/episodic-pivot-power-earnings-gap-buyable-gap-up-explained/)).
- No source gave a specific OBV or A/D-line divergence rule with tested results.

## What filters remove the most noise?

### Takeaway
The biggest noise sources are calendar-driven volume: index reconstitutions and rebalances (Russell in late June, S&P quarterly rebalances on triple-witching Fridays) and options expiry. Those days produce record volumes driven by closing auctions, not conviction buying. Bulkowski's data also shows that "above-average volume" alone *raises* breakout failure and throwback rates, so up-day, close-location, trend, and RS filters matter more than the volume multiple itself.

### Cited Findings
- The Russell reconstitution of 26 June 2026 produced Nasdaq's busiest-ever Closing Cross: 4.59B shares and $334.03B, versus 2.51B shares and $102.46B in 2025. — [Mondo Visione / Nasdaq](https://mondovisione.com/news/record-trading-volume-on-the-nasdaq-closing-cross-during-the-june-2026-russell-u-2026626/); [TradeInformer](https://tradeinformer.com/institutional-trading/nasdaq-closing-cross-handles-record-334-billion-during-russell-rebalance)
- The Russell recon is "typically the biggest close of the year", even though it doesn't coincide with a triple witch, unlike S&P rebalances. — [Nasdaq](https://www.nasdaq.com/articles/russell-recon-big-day-small-cap-companies)
- On the June 2024 recon day, volume across all Reg NMS securities was 65% above the June average and more than 220% higher in the final 30 minutes (including the closing auction). — [BMLL](https://www.bmlltech.com/news/market-insight/into-the-close-unpacking-u-s-closing-auction-dynamics-and-the-impact-of-the-russell-reconstitution)
- 18 June 2026 options expiry was reportedly a record (about $8.3T notional), 8 days before the recon (single source, unverified). — [France Épargne](https://www.france-epargne.fr/news/triple-witching-record-et-russell-semestriel-la-microstructure-des-marches-reprend-la-main)
- Bulkowski (about 8,000 rectangles and double/triple tops/bottoms, Jul 1991–May 2011; breakout volume vs the prior 31 calendar days): up-breakouts on above-average volume gained 37.6% vs 35.8% on below-average volume. But 10%-failure rates were **14% vs 5%**, throwbacks **57% vs 18%**, and pullbacks 47% vs 17%. His revised study says the performance gain for high-volume up-breakouts is "meager", while throwbacks and failures "increase substantially". — [Bulkowski Volume Study](https://thepatternsite.com/VolumeStudy.html)
- Weak-volume or flat-volume breakouts are treated as suspect, and a handle with rising volume signals that sellers are in control. — [StockAlarm](https://pro.stockalarm.io/blog/cup-and-handle-pattern-guide)
- Pocket pivots that fire inside downtrends, or that wedge up on quiet volume, are discarded. — [LuxAlgo](https://www.luxalgo.com/library/concept/pocket-pivot/)

### Inferences
- **Calendar mask**: exclude or down-weight volume spikes on (a) the 3rd Friday of each month (monthly opex), especially Mar/Jun/Sep/Dec (triple witching plus S&P quarterly rebalance); (b) the Russell reconstitution day (last Friday of June historically; check FTSE Russell's schedule, as it is moving to semi-annual); (c) S&P index-add effective dates. A simple approach is to compute volume ratios using a *median* rather than a mean baseline, and to skip "fresh volume high" flags on those dates.
- **Close-based filters** (up day, close in the upper part of the range, gap held) remove down-day dumps and news blips that fade intraday.
- **Trend/RS gates** remove spikes in Stage 4 / downtrending names, where pocket-pivot-style signals are explicitly considered improper.
- Given Bulkowski's finding, use the volume multiple as a *qualifier*, not the ranking key. Then require a follow-through check (e.g. holds above the breakout level or the gap-day low for 3–5 sessions), and expect many throwbacks: stops below the breakout-day low or pivot are commonly used.
- Adding ETFs and index constituents increases rebalance noise. Consider evaluating ETFs separately.

### Gaps
- No quantitative study was found on how much opex or rebalance days contaminate single-stock "volume high" signals.
- No gap-and-go vs gap-fill rate statistics were found for earnings gaps.
- Exact 2026+ Russell schedule changes (semi-annual recon) were not verified here.

## What evidence exists for each signal's hit rate?

### Takeaway
Academic evidence supports three ingredients: **proximity to the 52-week high** (George and Hwang 2004), **abnormal volume shocks** (the high-volume return premium), and **unexplained earnings-day volume combined with earnings surprise** (PEAD studies). Practitioner patterns (pocket pivot, VCP, EP) have no rigorous published hit rates in what I found. Bulkowski's breakout data shows that high-volume breakouts fail and throw back more often. Short interest and option signals are weak or short-lived as long signals.

### Cited Findings
- **52-week high**: nearness to the 52-week high "dominates and improves upon the forecasting power of past returns" (individual and industry), explains a large portion of momentum profits, and its predictions "do not reverse in the long run". Sample 1963–2001; *Journal of Finance* 2004, 59(5):2145–2176. — [CXO Advisory summary](https://www.cxoadvisory.com/1284/technical-trading/the-52-week-high-as-a-momentum-indicator-for-individual-stocks/); [SUFE academic newsletter](https://academicnewsletter.sufe.edu.cn/info/361244). International-index evidence is mixed (Du). — [NAU](https://experts.nau.edu/en/publications/the-52-week-high-and-momentum-investing-in-international-stock-in/)
- **High-volume return premium**: stocks with unusually high (low) volume over a day or week tend to appreciate (depreciate) over the following month. The proposed explanation is visibility. — [Gervais, Kaniel & Mingelgrin, JF 2001 (Wharton WP)](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9901.pdf). This is not universal: in China, both high- and low-volume portfolios underperformed. — [PKU HSBC Business School](https://english.phbs.pku.edu.cn/info/3351/20251.htm)
- **Earnings volume + drift**: returns after the announcement increase with the *unexplained* component of earnings-date volume (opinion divergence). — [Garfinkel & Sokobin, JAR 2006](https://www.biz.uiowa.edu/faculty/jgarfinkel/pubs/drift_JAR.pdf). The high-volume premium and PEAD are complementary, with each adding predictive power for analyst-followed firms. — [Lerman, Livnat & Mendenhall](https://archive.nyu.edu/handle/2451/27578). In Europe, surprise and abnormal volume both predict abnormal returns, more strongly under high information uncertainty. — [Gerard, EFMA](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2011-Braga/papers/0361.pdf)
- **Breakouts (Bulkowski)**: up-breakouts gained 37.6% (above-average volume) vs 35.8% (below), measured to the ultimate high before a 20% reversal. Failure (<10% move) was 14% vs 5%, and throwbacks 57% vs 18%. — [Bulkowski](https://thepatternsite.com/VolumeStudy.html). Rectangle-top up-breakouts have a 15% break-even failure rate and 66% throwback/pullback rate, not split by volume. — [Bulkowski rectangle tops](https://www.thepatternsite.com/recttops.html)
- **Short interest**: equal-weighted high-short-interest portfolios generally underperform, but value-weighted ones do not. Results are period-dependent (1988–94 strong, 1995–2002 not on Nasdaq). This makes high short interest a weak bearish signal, not a bullish one. — [Asquith, Pathak & Ritter, NBER w10434](https://www.nber.org/system/files/working_papers/w10434/w10434.pdf). Short-interest-ratio predictability lasts about 12 months, while put/call open-interest predictability fades after the first month (Chan, Kot & Ni, as cited). — [Kang, Kim & Lee 2016](https://acfr.aut.ac.nz/__data/assets/pdf_file/0003/56424/38716-C-Kang-option_July2016_CMK_v3.pdf)
- **Options volume**: per a secondhand summary of Pan & Poteshman (2006), *publicly* observable option volume predicts at most next-day returns, while non-public signed data predicts more persistently. Unsigned OTM call (put) volume predicts positive (negative) future returns. — [Kang, Kim & Lee 2016](https://acfr.aut.ac.nz/__data/assets/pdf_file/0003/56424/38716-C-Kang-option_July2016_CMK_v3.pdf); [CXO Advisory](https://cxoadvisory.com/equity-options/using-otm-equity-options-volume-to-predict-stock-returns)

### Inferences
- The best-evidenced combination for "early big winner" candidates is: a stock near or at a 52-week high, plus an abnormal volume shock on an up day, plus (ideally) an earnings catalyst with a surprise. This is close to what the power earnings gap / EP and IBD breakout rules encode.
- Expect low per-signal hit rates with large right-tail payoffs. Bulkowski's failure and throwback rates imply stop placement and re-entry rules matter. Stops at the low of the breakout or gap day (EP), 3–4% below the gap-day low (Morales), or under the last VCP contraction low are the conventions found.
- Options and short-interest data are secondary at best, and yfinance's short-interest fields are infrequent snapshots (bi-monthly FINRA reporting). Use them as tie-breakers, not triggers.
- The user should backtest each flag on their own universe: forward 20/60/120/250-day returns, % reaching +50% / +100%, and maximum adverse excursion, conditioned on the calendar mask.

### Gaps
- No rigorous backtest of pocket pivots, VCPs, RS-line-new-high-before-price, or episodic pivots was found. Quantified Strategies / Alpha Architect material on OBV, A/D, and up/down volume ratio was not retrieved in this pass.
- Pan & Poteshman's original paper was not retrieved, so the options findings are secondhand.
- No source quantified the follow-through rate (e.g. % of 8%+ earnings gaps that hold the gap-day low after 20 days).
