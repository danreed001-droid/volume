# Biggest US Large-Cap Winners, Oct 2021 – Oct 2026, and the Early Signals Behind Them

**Method and data note (read first).** All returns, drawdowns, gap and volume figures below come from my own calculations on Yahoo Finance daily data, pulled with `yfinance` (split- and dividend-adjusted, `auto_adjust=True`). The script is in the scratchpad.
- **Universe:** the current S&P 500 list, scraped from [Wikipedia's S&P 500 constituents page](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies), plus about 90 extra candidates: Nasdaq-100 and AI/power/crypto names, IPOs and spin-offs. That is 530 tickers.
- **Window:** start close is **2021-10-11**; end close is **2026-10-09**, the last trading day before today, 2026-10-12.
- **Volume ratio ("vr"):** the day's volume divided by the average of the prior 50 sessions.
- **"New 52w high":** the close exceeds the highest close of the prior 252 sessions.
- **Source label:** price-derived figures are cited as [yfinance/Yahoo Finance](https://finance.yahoo.com).
- **Verification limit:** my training knowledge ends around mid-2026. I could not cross-check figures for **~July–Oct 2026** (late-2026 peaks, open drawdowns, the last closes) against press coverage, so they rest on yfinance alone. They are flagged "(2026 data, unverified vs press)".
- **Survivorship:** using today's S&P 500 list means stocks that left the index are missing. That does not affect who the winners were, but anything that soared and was later removed would be absent.

Benchmarks over the same window: SPY **+91%** total return and QQQ **+116%**. Their max drawdowns were −24% (trough 2022-10-12) and −35% (trough 2022-11-03) — [yfinance](https://finance.yahoo.com).

---

## Q1. Which large caps had the largest % gains over Oct 2021–Oct 2026, and over shorter windows (from the 2022 bear-market low)?

### Takeaway
The 5-year leaderboard is dominated by **AI-infrastructure "picks and shovels"** rather than just the famous AI names:
- **Hardware and memory:** Celestica, Micron, Dell, Seagate, Western Digital, SanDisk, Lumentum, Arista and Super Micro.
- **Data-center construction, power and cooling:** Comfort Systems, Sterling, Vertiv, Bloom Energy, Vistra, Constellation and GE Vernova.

NVIDIA (~+1,000%) and Palantir (~+790%) are top-15 but not #1. Measured from the 2022 lows, the list tilts toward stocks that had crashed 75–99%: Carvana, Palantir, AppLovin and Robinhood.

### Cited Findings

**A. 5-year price return, close 2021-10-11 → close 2026-10-09 (names listed at the start)** — [yfinance](https://finance.yahoo.com)

| Rank | Ticker | 5-yr return | Max drawdown in window (peak→trough) | Theme |
|---|---|---|---|---|
| 1 | CLS (Celestica; NYSE-listed Canadian firm, not S&P 500) | **+3,769%** | −54% (Feb–Apr 2025) | AI server/switch EMS for hyperscalers |
| 2 | STRL (Sterling Infrastructure) | +2,149% | −54% (Jun–Sep 2026, open; 2026 data, unverified vs press) | Data-center site work |
| 3 | FIX (Comfort Systems USA) | +2,142% | −46% (Jan–Apr 2025) | Data-center mechanical/HVAC |
| 4 | MU (Micron) | +1,422% | −58% (Jun 2024–Apr 2025) | HBM/DRAM memory supercycle |
| 5 | BE (Bloom Energy) | +1,313% | −76% (Nov 2021–Feb 2024) | On-site fuel-cell power for data centers |
| 6 | LITE (Lumentum) | +1,190% | −66% (Jan 2022–Oct 2023) | Optical components for AI networks |
| 7 | DELL | +1,110% | −60% (May 2024–Apr 2025) | AI servers |
| 8 | SMCI (Super Micro) | +1,032% | **−85%** (Mar 2024–Nov 2024, still ~65% below its 2024 ATH) | AI servers |
| 9 | NVDA | **+1,013%** | −66% (Nov 2021–Oct 2022) | AI GPUs |
| 10 | STX (Seagate) | +1,005% | −57% (Jan–Nov 2022) | AI-driven HDD/storage demand |
| 11 | VRT (Vertiv) | +996% | −70% (Nov 2021–Jun 2022) | Data-center power/cooling |
| 12 | VST (Vistra) | +901% | −49% (Jan–Apr 2025) | Power demand, nuclear |
| 13 | WDC (Western Digital) | +840% | −55% (2022) | Storage |
| 14 | ANET (Arista) | +818% | −50% (Jan–Apr 2025) | AI Ethernet networking |
| 15 | PLTR (Palantir) | **+788%** | −78% (Nov 2021–Dec 2022) | AI software (AIP) / profitability inflection |
| 16 | CIEN (Ciena) | +759% | −50% | Optical networking |
| 17 | FLEX | +755% | −40% | EMS / data-center power |
| 18 | AVGO (Broadcom) | +702% | −41% (Dec 2024–Apr 2025) | Custom AI ASICs + networking (plus the VMware deal) |
| 19 | MPC (Marathon Petroleum) | +688% | −45% | Refining margins + buybacks (non-AI) |
| 20 | HWM (Howmet) | +627% | −24% | Aerospace engines |
| — | EME +588%, PWR +541%, KLAC +531%, LRCX +507%, AMD +481%, **LLY +428%**, GE +387%, APH +386% | | | |

**B. Notable names commonly cited as "winners" that did *not* top the 5-year table** — [yfinance](https://finance.yahoo.com)
- APP (AppLovin) is only **+217%** on 5 years. It fell −92% from Nov 2021 to Dec 2022, then rose about **+2,879%** off the Dec-2022 low. Its 2025-12-22 ATH close of ~$734 was followed by a −63% drawdown to Oct 2026 (2026 data, unverified vs press).
- HOOD +159% on 5 years. It fell −84% into the June 2022 low, then rose +1,482% from that low.
- AXON +152% on 5 years. It is −60% from its Aug-2025 ATH (open drawdown, 2026 data, unverified vs press).
- MSTR +111%; COIN −30%; NFLX +12%; TSLA +45%; META +123%; CVNA +13% on 5 years, but **+8,466% off its Dec-2022 low** after a −99% crash.

**C. Spin-offs and IPOs that became large caps (no full 5-year history)**, return from first trading close to 2026-10-09 — [yfinance](https://finance.yahoo.com)
- SNDK (SanDisk, spun from WDC Feb 2025): **+4,294%**. ATH close $2,335 on 2026-06-25, then a −56% drawdown to late July 2026 (2026 data, unverified vs press).
- CRDO (Credo, IPO Jan 2022): +1,759%.
- TLN (Talen, relisted 2023): +714%.
- GEV (GE Vernova, spun 2024-04-02): **+669%**.
- CEG (Constellation, spun Jan 2022): **+637%**.
- ALAB (Astera Labs, IPO Mar 2024): +452%.

**D. Largest gains from the 2022 bear-market closing low to 2026-10-09** — [yfinance](https://finance.yahoo.com)

| Ticker | 2022 low date | Gain from low | 5-yr max drawdown |
|---|---|---|---|
| CVNA | 2022-12-27 | **+8,466%** | −99% |
| CLS | 2022-09-26 | +4,274% | −54% |
| PLTR | 2022-12-27 | +3,384% | −78% |
| APP | 2022-12-27 | +2,879% | −92% |
| VRT | 2022-06-30 | +2,867% | −70% |
| STRL | 2022-09-27 | +2,363% | −54% |
| CRDO | 2022-05-11 | +2,361% | −62% |
| FIX | 2022-06-17 | +2,214% | −46% |
| BE | 2022-05-11 | +2,212% | −76% |
| LITE | 2022-12-28 | +2,133% | −66% |
| MU | 2022-09-26 | +2,046% | −58% |
| NVDA | 2022-10-14 | +1,950% | −66% |
| DELL | 2022-10-12 | +1,783% | −60% |
| STX / WDC | Nov / Dec 2022 | +1,696% / +1,648% | −57% / −55% |
| HOOD | 2022-06-16 | +1,482% | −84% |

- Prices on 2021-10-11 for reference (split-adjusted): NVDA $20.60, PLTR $23.53, LLY $223.30, APP $87.41, SPY $406.57. Closes on 2026-10-09: NVDA $229.28, PLTR $209.05, LLY $1,179.27, APP $277.04, SPY $779 — [yfinance](https://finance.yahoo.com).
- SanDisk's huge run is corroborated in press: Goldman Sachs raised its SNDK target to $700 in Jan 2026 after a ~1,100%+ six-month surge ([LongPort](https://longportapp.cn/news/274356328)). One aggregator cites "~3,314% over the past year" ([Whale Alert story](https://whale-alert.io/stories/c3b001a9d8355b/SanDisk-shares-surge-3314-over-past-year-as-NAND-shortage-and-AI-demand-push-revenue-margins-and-NAND-prices-higher)), which is low-quality but directionally consistent with yfinance.

### Inferences
- The "obvious" AI winners (NVDA, AVGO, PLTR) made **8–11x**. Less glamorous suppliers to the AI build-out made **10–38x**. Several of them were small or mid caps in 2021 that *became* large caps: CLS, STRL, FIX, BE, LITE, CRDO, SNDK.
- Starting point matters enormously. Names that crashed hardest in 2022 (CVNA, APP, PLTR, HOOD) look modest on 5 years but were the biggest winners from the low. A trader buying in 2023 got far more than a holder from Oct 2021.
- Many leaders show sharp **open drawdowns of 40–60% from mid-2026 peaks**: SNDK, STRL, BE, CRDO, WDC, CLS, VRT, APP and AXON. That suggests a meaningful AI/memory-trade correction in summer 2026 (2026 data, unverified vs press).

### Gaps
- I did not verify current S&P 500 or Nasdaq-100 membership for STRL, BE, LITE, CRDO, CIEN, FLEX or SNDK. CLS is Canadian and not in the S&P 500.
- I did not compute market caps, so "large cap" status is inferred from index lists and price levels.
- The universe misses companies that were never in the S&P 500 or my extras list (e.g., some ADRs). A small/mid-cap that became large but isn't listed could be missing.
- Late-2026 figures could not be verified against press reports.

---

## Q2. For each winner, what was the thesis/catalyst, when did the move start, and what was observable at ignition?

### Takeaway
Nearly every winner had a single identifiable **"ignition day"**: an earnings report or corporate event that produced a **+10% to +60% one-day gain on 3–15x average volume**, usually a gap-up. In 16 of 23 cases the stock closed at a **new 52-week high** that day. The fundamental trigger was almost always a **guidance raise far above consensus**, or a structural event that re-rated the business (a nuclear acquisition, a debt restructuring, a hyperscaler deal).

### Cited Findings (per name)

All ignition-day stats are from [yfinance](https://finance.yahoo.com) unless another source is cited. Columns: day return / opening gap / volume vs 50-day average / whether it closed at a new 52w high.

**1. NVIDIA (NVDA): AI GPU / data-center capex**
- **Ignition: 2023-05-25**, the day after Q1 FY24 results: **+24.4% close, +26% gap, 3.6x volume, new 52w high.**
- NVDA had already rallied off its Oct-2022 low. It was −4% from its 52w high the day before, with 6-month relative strength of 1.90x vs SPY. An earlier warning shot came on 2023-02-23 (+14%, 2.35x volume).
- Catalyst: Nvidia guided Q2 revenue to about **$11B ±2% vs ~$7.2B consensus**, its first forecast of that kind. Q1 revenue was $7.19B vs $6.52B expected ([StreetBeat](https://news.streetbeat.com/article/32562219); [Nasdaq/Motley Fool](https://www.nasdaq.com/articles/why-nvidia-surged-36.3-in-may)). Shares rose 36.3% in May 2023 ([Nasdaq](https://www.nasdaq.com/articles/why-nvidia-surged-36.3-in-may)).
- Results: +653% from the pre-ignition close to 2026-10-09 (SPY +98%). The stock was +249% one year after ignition.
- Pain: −27% (Jun–Aug 2024) and −37% (Jan–Apr 2025, DeepSeek/tariffs).

**2. Palantir (PLTR): AIP / commercial AI plus GAAP profitability inflection**
- **Ignition: 2023-05-09** (Q1 2023 results): **+23.4%, +19% gap, 7.5x volume.** It was *not* at a 52w high; the stock was −32% from it, in a long base.
- An earlier tell came on 2023-02-14 (+21%, 6.35x volume) on its first-ever GAAP-profitable quarter (Q4 2022).
- Catalyst: Q1 2023 revenue was $525M (+18%) vs ~$505.6M expected. It was the second straight GAAP-profitable quarter. Management said it expected to stay profitable every quarter through 2023 and called AIP demand "unprecedented" ([SiliconANGLE](https://siliconangle.com/2023/05/08/palantir-share-surge-earnings-revenue-beat-second-quarter-profit/); [Benzinga](https://benzinga.com/news/earnings/23/05/32273478/palantir-delivers-another-profitable-quarter-touts-new-ai-platform-shares-surge)). Analysts were still skeptical: Jefferies kept Hold and Deutsche Bank kept Sell, raising its target only to $7 ([Benzinga](https://benzinga.com/news/earnings/23/05/32273478/palantir-delivers-another-profitable-quarter-touts-new-ai-platform-shares-surge)).
- Follow-on catalysts:
  - 2024-02-06: +30.8%, 8.1x volume, new 52w high.
  - **S&P 500 inclusion**, announced 2024-09-06 and effective 2024-09-23. The stock rose as much as 13% to a 52w high on the next trading day ([Daizy](https://daizy.com/blog/palantir-stock-jumps-on-announcement-it-will-be-added-to-the-s-p-500); [Nasdaq](https://www.nasdaq.com/articles/palantir-join-sp-500-how-will-it-impact-stock)).
  - 2024-11-05: +23.5% (election week).
  - 2025-02-04: +24%.
- Results: **+2,601%** from the pre-ignition close ($7.74) to $209.05. It closed at an ATH on 2026-10-09.
- Pain: −30% (Aug–Sep 2023), −41% (Feb–Apr 2025) and **−48% (Nov 2025–Jun 2026)**.

**3. Broadcom (AVGO): custom AI accelerators (XPUs) plus AI networking**
- **First ignition: 2023-05-26**, the day after NVDA's report, a sympathy move: +11.5%, 3.9x volume, new 52w high.
- **Main re-rating: 2024-12-13** (FQ4 2024 results): **+24.4%, +18% gap, 6.0x volume, new 52w high.** The stock rose another +11% the next session on 5x volume.
- Catalyst: CEO Hock Tan put the AI XPU plus networking serviceable market at **$60–90B for FY2027**, from three hyperscale customers each planning 1M-XPU clusters. FY2024 AI revenue was $12.2B. Market cap crossed $1T as shares rose ~21–24% ([Investing.com/Reuters](https://investing.com/news/stock-market-news/broadcom-rallies-on-forecast-for-booming-ai-chip-demand-3771047); [FXStreet](https://www.fxstreet.com/news/broadcom-is-the-newest-trillion-dollar-company-202412131520)).
- Results: +418% from the May-2023 ignition.
- Pain: −41% (Dec 2024–Apr 2025); −29% (Dec 2025–Mar 2026); −29% from the Jun-2026 ATH (open; 2026 data, unverified vs press).

**4. Vistra (VST): nuclear acquisition, then AI power-demand re-rating**
- **Ignition: 2023-03-06**: **+13.9%, 5.3x volume**, not at a 52w high (−20% from it).
- Catalyst: Vistra agreed to buy Energy Harbor for **$3.4B**, adding about 4,000 MW of nuclear capacity ([POWER Magazine](https://www.powermag.com/vistra-expands-nuclear-portfolio-in-3-4-billion-deal-for-energy-harbor/); [Benzinga](https://www.benzinga.com/trading-ideas/movers/23/03/31223267/why-is-vistra-stock-trading-higher-today)). The deal closed 2024-03-01 ([Vistra IR](https://investor.vistracorp.com/2024-03-01-Vistra-Completes-Energy-Harbor-Acquisition?asPDF=1)).
- **Acceleration: Feb 27 – Mar 6, 2024** (Q4 2023 results plus the deal close). There were six straight sessions of 2.0–2.7x volume, almost all at new 52w highs, taking the stock from $47.66 to $59.70.
- Results: +211% from the Feb-2024 acceleration. ATH close was $216.66 on 2025-09-22.
- Pain: **−35%** (May–Jul 2024); **−49%** (Jan–Apr 2025); **−38%** from the Sep-2025 ATH to May 2026 (still open).

**5. Constellation Energy (CEG): nuclear fleet re-rated as AI baseload power**
- **Ignition: 2024-02-27** (Q4 2023 results): **+16.9%, 3.0x volume, new 52w high.** The stock was −1% from its high beforehand, a classic breakout.
- **Second catalyst: 2024-09-20**: **+22.3%, +12.8% gap, 4.6x volume, new 52w high.** Constellation signed a **20-year PPA with Microsoft to restart Three Mile Island Unit 1**, the largest PPA in its history ([Barchart](https://barchart.com/story/news/28641887/constellation-energy-to-restart-three-mile-island-nuclear-reactor); [Nasdaq](https://www.nasdaq.com/articles/why-constellation-energy-stock-surged-more-30-september)). Shares rose 32% in Sep 2024.
- Third catalyst: 2025-01-10, +25%, 4.7x volume (Calpine deal; date from yfinance, catalyst not press-verified here).
- Results: +128% from Feb-2024 ignition, and +637% since the Jan-2022 spin.
- Pain: −28% (mid-2024); −51% (Jan–Apr 2025); −41% from the Oct-2025 ATH (2026 data, unverified vs press).

**6. Micron (MU): HBM/DRAM memory supercycle**
- **Ignition: 2023-12-21** (FQ1 2024 results): **+8.6%, +8% gap, 4.25x volume, new 52w high.**
- Follow-through on 2024-03-21: +14.1%, +17.8% gap, 5.6x volume, new 52w high.
- But MU then fell **−58% (Jun 2024–Apr 2025)**, and was only +15% one year after ignition. The real move came in 2025–26: 2025-12-18 brought +10.2%, 2.65x volume, RS 1.5x.
- Results: +1,220% from the Dec-2023 ignition. ATH close was $1,213 on 2026-06-25.
- NAND/DRAM price hikes by Micron, SanDisk and WDC were reported in Sep–Nov 2025 ([TrendForce](https://www.trendforce.com/news/?p=45538); [TechRadar](https://www.techradar.com/pro/black-friday-storage-blood-bath-incoming-micron-sandisk-set-to-dramatically-increase-nand-and-dram-prices-with-a-direct-impact-expected-on-ssd-and-ram-prices-within-weeks)).
- Takeaway: MU is an example of **two ignitions**, with a painful round trip between them.

**7. SanDisk (SNDK): NAND shortage, AI storage**
- **Ignition: 2025-09-04**: **+17.9%, 4.3x volume, new high.**
- Followed by 2025-09-11 (+14%, 3.7x volume) and 2025-09-29 (+16.9%, 3.0x volume).
- Catalyst: at the Sept 2025 Goldman Sachs Communacopia conference, SanDisk said the NAND market would stay undersupplied through 2026, alongside industry-wide price hikes ([TrendForce](https://www.trendforce.com/news/?p=45538)). Later, NAND prices were reported up about 60% in Q1 2026. FQ3 2026 revenue was $5.95B (+251% y/y) with ~78% non-GAAP gross margin ([Motley Fool](https://www.fool.com/investing/2026/06/26/the-memory-shortage-is-minting-winners-3-stocks-no/); [Finterra/Observer-Reporter](https://stocks.observer-reporter.com/observerreporter/article/finterra-2026-3-31-deep-dive-sandisk-sndk-and-the-2026-nand-flash-shortage)).
- Results: +2,884% from the pre-ignition close ($53) to $1,582. Peak was $2,335 (+4,305%).
- Pain: −31% (Nov–Dec 2025); **−56% (Jun 25 – Jul 29, 2026)** (2026 data, unverified vs press).

**8. Seagate (STX) and Western Digital (WDC): HDD demand from AI data storage**
- STX **ignition 2025-04-30** (earnings): +11.6%, 3.0x volume, from a base −26% below its high.
  - Results: +873% to 2026-10-09; +736% one year later.
  - Later legs: 2025-10-29 (+19%, new high) and 2026-01-28 (+19%, 3.9x volume).
- WDC **ignition 2025-07-31**: +10.2%, 3.8x volume, closing at a new 52w high (the prior day was right at the high).
  - Results: +458%, with a peak +948%.
  - Pain: −47% open drawdown from the Jun-2026 ATH (2026 data, unverified vs press).
- Catalyst detail for these specific earnings days was not press-verified in this pass. The thematic cause, a memory/storage shortage, is supported by the sources in #7.

**9. Super Micro Computer (SMCI): AI servers. A boom, then a bust from accounting issues**
- **Ignition: 2023-05-03**: **+28.3%, 5.3x volume, new 52w high.** RS was 1.68x into the event. An earlier 2022-05-04 tell came at +31%, 9.4x volume.
- **Blow-off catalyst: Jan 18, 2024 preliminary raise.** Quarterly sales guidance went to **$3.6–3.65B from $2.7–2.9B**. Shares rose about 36% the next day ([Barchart](https://www.barchart.com/story/news/23821208/is-it-too-late-to-buy-super-micro-computer-stock)). yfinance shows 2024-01-19 at +35.9% on 7.3x volume, at a new high. On Jan 29 it raised FY revenue guidance to $14.3–14.7B from $10–11B ([CNBC](https://www.cnbc.com/2024/01/30/super-micro-shares-pop-after-earnings-beat-rosy-revenue-forecast-.html)).
- Peak: ATH close on **2024-03-13**, at **+1,038%** from the pre-ignition close.
- Collapse: **−85% by 2024-11-14**. Hindenburg published a short report alleging accounting manipulation in Aug 2024. **EY resigned** as auditor in Oct 2024, and shares fell more than 30% that day. A special committee review in Dec 2024 found EY's conclusions "not supported," and shares rose over 20% ([KOB/AP](https://kob.com/news/business-money/super-micro-computers-shares-plunge-after-accounting-firm-resigns); [ClickOrlando/AP](https://www.clickorlando.com/business/2024/12/02/super-micros-shares-jump-after-server-maker-says-review-finds-no-evidence-of-misconduct/)).
- It is still ~65% below its 2024 ATH ($41.86 vs $118.81) — [yfinance](https://finance.yahoo.com).

**10. Celestica (CLS): hyperscaler AI switch/server manufacturing. #1 five-year return**
- **Ignition: 2023-07-28** (Q2 2023 results): **+15.0%, 7.0x volume, a new 52w high on the breakout day (0% from the high beforehand).** Six-month RS was 1.20x.
- Catalyst: Q2 revenue ($1.94B, +13%) and adjusted EPS ($0.55) both came in above the high end of guidance. The 2023 revenue outlook was raised to ≥$7.85B and adjusted EPS to $2.25 ([Celestica IR](https://corporate.celestica.com/node/14826)). The Globe and Mail noted the shares rallied "on high volume" ([Globe and Mail](https://arc-dev.theglobeandmail.com/investing/markets/inside-the-market/article-tuesdays-tsx-breakouts-with-strong-earnings-growth-and-ai-exposure)).
- Later legs: 2024-10-24 (+18%), 2025-01-30 (+13.6%) and 2025-07-29 (+16.5%, 4.3x volume, RS ~2x).
- Results: **+1,911%** from ignition, with a peak of +2,523% (Jun 2026).
- Pain: −35% (2024), **−54% (Feb–Apr 2025)**, −29%, and −41% open (2026 data, unverified vs press).

**11. Vertiv (VRT): data-center power and liquid cooling**
- **Ignition: 2023-04-26** (Q1 2023 results): **+11.1%, +17% gap, 4.8x volume**, from a base −26% below its high. Follow-through came on 2023-05-25 (NVDA sympathy, +14%, 8x volume, new high).
- The defining day was **2023-08-02** (Q2 2023 results): **+29.3%, +24% gap, 6.8x volume, new high, RS 2.09x.**
- Specific Q1/Q2 2023 guidance figures were *not* verified in my search (gap). Later coverage confirms the stock's AI cooling and data-center narrative ([Nasdaq/Motley Fool](https://www.nasdaq.com/articles/meet-artificial-intelligence-ai-infrastructure-stock-has-crushed-nvidia-and-broadcom-270)).
- Results: +1,893% from ignition; +639% one year later.
- Pain: −37% (mid-2024); **−61% (Jan–Apr 2025)**; −41% open from the May-2026 ATH (2026 data, unverified vs press).

**12. AppLovin (APP): AXON 2.0 AI ad engine; software margins inflect**
- **Ignition: 2023-08-10** (Q2 2023 results): **+26.5%, +30% gap, 8.2x volume.** It was not at a 52w high (−27%), but RS was 2.12x. An earlier tell came on 2023-02-09 (+27%, 4.2x volume).
- Catalyst: AXON 2.0 rollout and record software-platform revenue and margins. Q3 revenue was guided to $780–800M. BofA said AXON 2.0 could "catalyze a multiyear growth story" ([Barchart](https://www.barchart.com/story/news/21873636/why-is-applovin-app-stock-rocketing-higher-today); [Investing.com](https://investing.com/news/stock-market-news/applovin-stock-jumps-22-following-q2-beat-432SI-3150503)). Some coverage was skeptical about valuation and free cash flow ([CMC Markets](https://www.cmcmarkets.com/en/optox/app-stock-earnings-review-applovins-adtech-pivot-pays-off)).
- Later legs:
  - 2024-11-07: **+46.3%**, 4.25x volume, new high, RS 2.84x ([NBC/CNBC](https://www.nbcmiami.com/news/business/money-report/applovin-top-tech-stock-of-the-year-soars-another-45-on-earnings-beat/3466479/?amp=1)).
  - 2025-02-13: +24%.
  - **S&P 500 inclusion**, announced 2025-09-05 and effective 2025-09-22. APP closed +11.6% at $547.04 on 2025-09-08 ([Yahoo Finance](https://finance.yahoo.com/news/robinhood-applovin-join-p-500-173000838.html); [Sherwood](https://www.sherwood.news/markets/robinhood-applovin-vault-higher-as-the-inclusion-effect-is-in-full-force)).
- Results: +842% from ignition; the 2025-12-22 peak was +2,394%.
- Pain: **−57% (Feb–Apr 2025)**, −28% (Oct–Nov 2025), and **−63% from the Dec-2025 ATH to 2026-10-02 (open; 2026 data, unverified vs press)**.

**13. Eli Lilly (LLY): GLP-1 obesity drugs (Mounjaro/Zepbound)**
- **Ignition: 2022-04-28**, SURMOUNT-1 topline: tirzepatide gave up to **22.5% weight loss at 72 weeks** (15 mg, efficacy estimand) vs 2.4% for placebo. 63% of the 15 mg arm lost ≥20% of body weight ([Lilly IR](https://investor.lilly.com/node/47141)).
- The price reaction was **modest: +4.3%, 2.1x volume**, not a 52w high (−9% from it). RS was already 1.25x.
- This was a *slow-burn* ignition. The stock had already been outperforming during the 2022 bear market (its 2022 low was in Feb), and it made new highs through 2022–23. 2023-04-27 was a new high on 1.6x volume. 2023-08-08 (Q2 2023) brought **+14.9%, 5.98x volume, new 52w high**, the biggest volume event.
- Results: +330% from the SURMOUNT-1 date.
- Pain: only one >25% drawdown, **−34% (Aug 2024–Aug 2025)**. It had the lowest max drawdown (−34%) of the top winners.

**14. Arista Networks (ANET): AI Ethernet back-end networks**
- **Ignition: 2023-08-01** (Q2 2023 results): **+19.7%, +14% gap, 4.6x volume, new 52w high.**
- Follow-through on 2023-10-31 (+14%, 4.6x volume, new high) and 2025-08-06 (+17.5%).
- Results: +459%; it closed at an ATH on 2026-10-09.
- Pain: **−50% (Jan–Apr 2025)**; −28% (Oct 2025–Mar 2026).
- Catalyst specifics were not press-verified in this pass (gap).

**15. Dell Technologies (DELL): AI servers**
- **Ignition: 2024-03-01** (Q4 FY24 results released Feb 29): **+31.6%, +31.7% gap, 14.8x volume (the highest ratio in this study), new 52w high.** The stock was at its high beforehand, with RS 1.48x. An earlier tell came on 2023-09-01 (+21%, 8x volume, new high).
- The March 2024 catalyst text was not confirmed by my search (gap). The 2026 leg *is* sourced: on 2026-05-29, Dell rose ~32% after Q1 FY27 revenue of $43.8B, AI server sales up 757% y/y, $24.4B of new AI orders, and FY guidance raised to $165–169B ([SentiSense](https://app.sentisense.ai/stories/dell-stock-surges-32-percent-on-blowout-ai-server-sales-and-raised-outlook-05292026); yfinance shows +32.8% on 5.2x volume).
- Results: +543% from the 2024 ignition, but only **+10% one year later**, after a **−60% drawdown (May 2024–Apr 2025)**.

**16. Comfort Systems (FIX) and Sterling Infrastructure (STRL): data-center construction (mechanical, site work)**
- FIX **ignition 2023-02-23**: +9.8%, 2.3x volume, new 52w high, RS 1.24x.
  - Biggest volume days: 2025-07-25 (+22.4%, 3.6x volume) and 2025-10-24 (+19%).
  - Results: +1,303% from ignition. Pain: −46% (Jan–Apr 2025).
- STRL **ignition 2023-08-08**: **+22.3%, 4.7x volume, new 52w high, RS 1.52x.**
  - 2026-05-05 brought **+52.2%, +37% gap, 4.9x volume** (2026 data, unverified vs press).
  - Results: +730% from ignition.
  - Pain: −48% (Jan–Apr 2025) and **−54% from the Jun-2026 ATH (open)**.
- Catalyst specifics for these earnings days were not press-verified (gap).

**17. GE Vernova (GEV): gas turbines, grid and electrification for power demand**
- **Move start: the 2024-04-02 spin-off from GE.** It drifted down 12% in the first week (to $122.18 on 2024-04-05), then broke out on 2024-04-23 (+8.2%, earnings).
- High-volume days came later: 2025-07-23 (+14.6%, new high) and 2025-12-10 (+15.6%, 3.7x volume).
- Results: **+610%** from the pre-spin reference close, and +669% from its first close.
- Pain: only −38% (Jan–Mar 2025).

**18. Carvana (CVNA): near-bankruptcy turnaround**
- **Ignition: 2023-06-08**: **+56% close, 10.2x volume.** The stock was −72% from its 52w high, but 3-month RS was 2.6x.
- Catalyst: raised Q2 guidance to about **$50M of positive adjusted EBITDA**. Bloomberg reported shares up as much as 55% intraday ([Bloomberg](https://www.bloomberg.com/news/articles/2023-06-08/carvana-cvna-shares-soar-on-forecast-of-improved-financial-results); [CNBC](https://www.cnbc.com/2023/06/08/carvana-shares-surge-after-company-boosts-second-quarter-guidance.html)). The debt deal cutting more than $1.2B of debt came on 2023-07-19: yfinance shows +40% on 3.65x volume, a new high, 3-month RS 5.75x ([ABC15](https://www.abc15.com/news/business/carvana-shares-soar-as-company-announces-debt-restructuring-deal-q2-earnings)).
- Results: +1,952% from ignition.
- Pain was enormous: **seven drawdowns of more than 25%**, including −53% (Sep–Nov 2023), −43% (2025) and −41% (2026, open).

**19. Robinhood (HOOD): retail-trading/crypto boom, product expansion, profitability**
- **Ignition: 2024-11-06** (election-week crypto rally): **+19.6%, 3.65x volume, new 52w high**, RS 1.24x.
- Later: S&P 500 inclusion, announced 2025-09-05. HOOD closed +15.8% at a record $117.28 on 2025-09-08 ([Yahoo Finance](https://finance.yahoo.com/news/robinhood-applovin-join-p-500-173000838.html)).
- Results: +337% from ignition, with a peak of +511%.
- Pain: −48% (Feb–Apr 2025); **−57% from the Oct-2025 ATH to Mar 2026**.

**20. Other AI-infrastructure ignitions**, all [yfinance](https://finance.yahoo.com), catalyst text not press-verified:
- LITE 2024-11-08: +13.9%, 4.8x volume, new high. +1,398% since.
- CRDO 2024-12-03: **+47.9%, 6.8x volume, new high**. +353% since, with −61%, −54% and −50% drawdowns.
- BE 2024-11-15: **+59.2%, +58% gap, 10.65x volume, new high**. +2,012% since.

### Inferences
- **The ignition was nearly always an earnings release** with guidance far above consensus. NVDA's guide was ~50% above the Street; SMCI raised its quarterly guide ~30%; AVGO quantified a $60–90B market.
- The exceptions were corporate actions: VST's acquisition, CEG's PPA, CVNA's restructuring, the GEV spin, and S&P 500 inclusion for PLTR, APP and HOOD.
- In the ignition sample, the **median one-day gain was ~20%** and **median volume ~4.8x the 50-day average**. Range: 2.1x (LLY) to 14.8x (DELL) — [yfinance](https://finance.yahoo.com).
- **16 of 23** ignitions closed at a new 52-week high. Most of the rest still had strong 6-month relative strength (APP 2.1x, CVNA 2.0x).
- The main exceptions to "breakout plus RS" were bottom-fishing turnarounds (PLTR, VST, VRT, STX, BE). These ignited from deep bases 20–32% below their highs and needed follow-through to confirm.
- **Sympathy moves were tradable signals.** NVDA's 2023-05-25 report triggered same-week high-volume breakouts in AVGO (+11.5%, 3.9x) and VRT (+14%, 8x, new high), so the leader's report flagged the supply chain.
- **The first ignition was not always the best entry.** MU and DELL went nowhere for a year (MU +15% and DELL +10% one year later, with −58% and −60% drawdowns) before their second leg.

### Gaps
- I did not verify analyst estimate-revision data (FactSet/Zacks consensus changes) around each ignition; that needs paid data.
- Insider buying around ignition dates was not researched. There is no evidence either way.
- Press-verified catalyst text is missing for VRT (Apr/Aug 2023), ANET (Aug 2023), DELL (Mar 2024), MU (Dec 2023), STX/WDC (2025), FIX/STRL, LITE, CRDO, BE, CEG (Jan 2025) and GEV (2025). Their price and volume stats are from yfinance only.
- SMCI's 2023-05-03 catalyst (fiscal Q3 2023 results/outlook) was not press-verified.

---

## Q3. How much pain did holders have to sit through?

### Takeaway
Even the best performers routinely suffered **35–60% drawdowns after the move began**, most commonly in **Jan–Apr 2025** (the DeepSeek AI-capex scare plus the April 2025 tariff crash). Many also show **40–60% drawdowns from mid-2026 peaks** that were still open at 2026-10-09. Only LLY and GEV avoided a drawdown worse than about −38% after ignition.

### Cited Findings
- **The 2025 cluster** — [yfinance](https://finance.yahoo.com): almost every AI/power winner bottomed on or near 2025-04-04. Drawdowns:
  - VRT −61%, CRDO −61%, APP −57%, CLS −54%, CEG −51%, LITE −51%, ANET −50%, VST −49%.
  - HOOD −48%, STRL −48%, FIX −46%, AVGO −41%, PLTR −41%, NVDA −37%.
  - MU's −58% and DELL's −60% ran from mid-2024 to Apr 2025.
- **Idiosyncratic busts:** SMCI −85% after the auditor resignation ([KOB/AP](https://kob.com/news/business-money/super-micro-computers-shares-plunge-after-accounting-firm-resigns)). CVNA had seven drawdowns of more than 25%; AXON is −60% from its Aug-2025 ATH (open).
- **Open drawdowns at 2026-10-09** (2026 data, unverified vs press): APP −63%, HOOD −57% (low Mar 2026), SNDK −56% (Jun–Jul 2026), STRL −54%, BE −53%, CRDO −50%, WDC −47%, VRT −41%, CLS −41%, CEG −41%, MU −39%, VST −38%, AVGO −29%.
- **Pre-ignition pain for holders since Oct 2021:** PLTR −78%, APP −92%, HOOD −84%, CVNA −99%, NVDA −66% and VRT −70% in 2022 — [yfinance](https://finance.yahoo.com).

### Inferences
- Holding these winners required tolerating at least one roughly 50% drawdown, usually 12–24 months after ignition. A trader using a fixed −20% stop would have been shaken out of almost every name, typically in Q1 2025.
- The Jan–Apr 2025 drawdown was a **market-wide, theme-wide** event, not stock-specific. Leaders that held up best and recovered fastest (PLTR, HOOD, CLS, STX) made new highs within months. Relative strength *during* the correction looks like a useful signal of which leaders would lead next.

### Gaps
- I could not confirm the causes of the summer-2026 drawdowns (Jun–Sep 2026) from press sources; they are visible only in yfinance data.

---

## Q4. Common patterns across the winners (what an alert trader could have caught)

### Takeaway
The repeatable signature was: **(1)** a structural theme with a quantifiable demand shock (AI capex, power, memory pricing, GLP-1); **(2)** a stock already showing relative strength or basing near highs; **(3)** an earnings or corporate event producing a **10–60% gap-up on 3–15x volume**, typically closing at a new 52-week high; **(4)** follow-through at subsequent earnings; and often **(5)** S&P 500 inclusion as a later accelerant. Clusters of winners moved together, so one leader's blowout (NVDA, May 2023) was a signal for its whole supply chain.

### Cited Findings
- **Themes by count** among the ~25 names studied:
  - AI compute/networking/servers: NVDA, AVGO, ANET, DELL, SMCI, CLS, CRDO, LITE, CIEN.
  - AI memory/storage: MU, SNDK, STX, WDC.
  - Data-center physical build: VRT, FIX, STRL, PWR, EME.
  - Power generation: VST, CEG, GEV, BE, TLN.
  - AI software: PLTR, APP.
  - GLP-1: LLY.
  - Fintech/crypto and turnarounds: HOOD, CVNA.
- **Ignition timing clusters:**
  - Feb–Aug 2023: the NVDA-led AI wave (NVDA, PLTR, SMCI, VRT, ANET, APP, CLS, STRL, CVNA).
  - Feb–Mar 2024 / Sep 2024: power (VST, CEG) and DELL.
  - Nov–Dec 2024: post-election/AI wave 2 (HOOD, LITE, BE, CRDO, AVGO).
  - Apr–Sep 2025: the memory/storage supercycle (STX, WDC, SNDK, then MU's second leg).
  — [yfinance](https://finance.yahoo.com)
- **Pre-ignition setup** (23 ignitions, [yfinance](https://finance.yahoo.com)):
  - Median distance from the 52w high the day before was about −6%. Fourteen of 23 were within 10% of their high.
  - Six-month RS vs SPY exceeded 1.0 in 15 of 23 cases (NVDA 1.90, APP 2.12, CVNA 2.03, CRDO 1.65, STRL 1.52, DELL 1.48).
  - Several broke out of long bases: PLTR, VST and APP were 270–365 days from their prior 52w high.
- **Index inclusion as a secondary signal:**
  - PLTR (and DELL) were added in Sep 2024; PLTR rose up to 13% on the next trading day ([Nasdaq](https://www.nasdaq.com/articles/palantir-join-sp-500-how-will-it-impact-stock); [Kavout](https://kavout.com/market-lens/palantir-and-dell-join-the-sp-500-what-investors-need-to-know)).
  - APP, HOOD and EME were added in Sep 2025; APP rose +11.6% and HOOD +15.8% on the first session ([Yahoo Finance](https://finance.yahoo.com/news/robinhood-applovin-join-p-500-173000838.html)).
  - A Goldman Sachs study cited by Sherwood found that since 2021, stocks newly added to the S&P 500 beat the equal-weight index by about 4 percentage points on announcement day ([Sherwood](https://www.sherwood.news/markets/robinhood-applovin-vault-higher-as-the-inclusion-effect-is-in-full-force)).
  - Academic work cited by Barchart (NY Fed 2011) finds no permanent value effect from inclusion ([Barchart](https://www.barchart.com/story/news/28519135/palantir-stock-will-join-the-sp-500-in-september-history-says-it-could-soar-afterward)).
- **Skepticism at ignition was common:** Palantir still had Hold/Sell ratings after its May-2023 report ([Benzinga](https://benzinga.com/news/earnings/23/05/32273478/palantir-delivers-another-profitable-quarter-touts-new-ai-platform-shares-surge)); AppLovin got valuation pushback after Aug 2023 ([Seeking Alpha](https://seekingalpha.com/article/4629451-applovin-q2-2023-earnings-stock-rally-ytd-may-elevate-expectation-hold)); TD Cowen called Broadcom's $60–90B claim "difficult to prove/disprove" ([FXStreet](https://www.fxstreet.com/news/broadcom-is-the-newest-trillion-dollar-company-202412131520)).

### Inferences
- **Practical screen implied by the data:**
  - A large cap or fast-growing mid-cap gaps up ≥10% on ≥3x 50-day volume after earnings with a guidance raise.
  - It closes at or near a 52-week high, with 3- to 6-month RS vs SPY above 1.2.
  - It sits in a theme where a leader just posted a similar event.
  - That combination flagged nearly all the winners here within days of the start of their main advance.
- **False positives exist** and need management:
  - SMCI's big-volume gaps preceded an −85% collapse.
  - MU's and DELL's first ignitions led to roughly 60% drawdowns before working.
  - CRDO and BE had repeated −50% swings.
  - So the signal identifies *candidates*; position sizing and re-entry on later ignitions (second-leg breakouts) mattered as much as the first signal.
- **Analyst skepticism at ignition** (Hold/Sell ratings, valuation worries) coexisted with the early moves. Upward estimate revisions likely followed the guidance raises, but I did not quantify this.
- **Turnaround winners** (CVNA, PLTR, APP, HOOD) produced the largest percentage gains from lows. But they ignited from deep drawdowns, not 52-week highs, and they had the most violent subsequent drawdowns.

### Gaps
- I have no quantitative estimate-revision history or insider-transaction data. The "analyst revisions" and "insider buying" signals asked about remain unverified.
- I did not backtest the base rate: how many stocks showed the same gap-plus-volume pattern and *failed*. Without it, the hit rate of the pattern is unknown.
- I did not assess options or short-interest signals.
