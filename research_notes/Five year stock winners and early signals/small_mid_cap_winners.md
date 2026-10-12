# US Small- and Mid-Cap Multi-Baggers, Oct 2021 – Oct 2026: Catalysts, Ignition Events, Survivorship

**Method note (read first).** All price and volume figures are my own calculations from Yahoo Finance daily data pulled with Python `yfinance` on 2026-10-12 (window 2021-10-01 to 2026-10-09 close). Prices are split-adjusted. Splits that affect raw prices: CVNA 5-for-1 (2026-05-08), SMCI 10-for-1 (2024-10-01), CELH 3-for-1 (2023-11-15), DAVE 1-for-32 reverse (2023-01-06), NUTX two reverse splits (2024), APLD 1-for-6 reverse (2022). Use the **multiples** (trough-to-peak and trough-to-now). Raw dollar levels are adjusted. "Vol x" means that day's volume divided by the prior 50-day average volume. "Ignition" days are those after the trough with a ≥12% one-day gain on ≥3x average volume (scripts: `scratchpad/winners.py`, `scratchpad/ignite.py`). Citation for computed figures: [Yahoo Finance historical data via yfinance](https://finance.yahoo.com/quote/CVNA/history) (swap the ticker in the URL). **Anything dated after about June 2026 (the 2026 peaks, the mid-2026 drawdowns, current prices) comes only from this data pull. I could not confirm it in news sources, so treat it as UNVERIFIED.** For context, SPY returned +79% over the window and closed near an all-time high on 2026-10-06. IWM returned +25% and was 9% below its 2026-08-14 high. ARKK returned -19%. These are computed figures.

## Which small/mid caps produced the biggest multi-bag moves in the window?

### Takeaway
The biggest and most durable 5-year multi-baggers were not the meme or theme names. They were small/mid-cap industrials and AI "picks-and-shovels" names with surging backlogs and earnings: CLS +3,815%, FIX +2,217%, POWL +2,210%, STRL +2,144%, CRDO +1,759%, MOD +1,421%, BE +1,419%, LITE +1,192%, IESC +1,179%, CRS +1,026%, ATI +1,008%, SMCI +1,021% point-to-point. The most explosive trough-to-peak moves (50x to 150x) came from distressed or speculative names bought at the 2022–2024 lows: CVNA ~129x, SEZL ~139x, RGTI ~150x, WGS ~135x, QBTS ~108x, DAVE ~97x, APP ~79x. Several of these later gave back 60–80%.

### Cited Findings
**Master table (computed from yfinance; "5y" = Oct 1 2021 close to Oct 9 2026 close)**

| Ticker | 5y return | Trough (date) → Peak (date) | Trough→Peak | Trough→Now | Now vs peak | Bucket |
|---|---|---|---|---|---|---|
| CLS (Celestica) | +3,815% | 2022-09-26 → 2026-06-02 | 57x | 44x | -23% | AI hardware/EMS |
| FIX (Comfort Systems) | +2,217% | 2021-10-01 → 2026-06-22 | 28x | 23x | -17% | Data-center MEP contractor |
| POWL (Powell Ind.) | +2,210% | 2022-04-11 → 2026-05-11 | 51x | 30x | -40% | Electrical gear/backlog |
| STRL (Sterling Infra.) | +2,144% | 2022-09-27 → 2026-06-04 | 48x | 25x | -48% | Data-center site work |
| CRDO (Credo) | +1,759% | 2023-05-04 → 2026-06-22 | 41x | 30x | -28% | AI connectivity (AECs) |
| MOD (Modine) | +1,421% | 2022-04-27 → 2026-06-02 | 40x | 24x | -41% | Data-center cooling |
| BE (Bloom Energy) | +1,419% | 2024-02-23 → 2026-06-22 | 40x | 33x | -19% | On-site power for AI |
| LITE (Lumentum) | +1,192% | 2023-10-27 → 2026-10-06 | 31x | 31x | -3% | AI optics |
| IESC (IES Holdings) | +1,179% | 2022-05-03 → 2026-08-17 | 31x | 24x | -25% | Electrical contractor |
| CRS (Carpenter Tech) | +1,026% | 2022-07-06 → 2026-07-06 | 24x | 15x | -38% | Aerospace alloys |
| SMCI (Super Micro) | +1,021% | 2022-04-12 → 2024-03-13 | 34x | 12x | -65% | AI servers |
| ATI | +1,008% | 2021-12-01 → 2026-08-17 | 16x | 14x | -17% | Aerospace alloys |
| NBIS (Nebius) | +1,005%* | 2024-10-23 → 2026-06-18 | 17x | 13x | -23% | AI neocloud (*relisted 2024) |
| VRT (Vertiv) | +889% | 2022-06-30 → 2026-05-14 | 46x | 30x | -35% | Data-center power/cooling |
| VST (Vistra) | +858% | 2021-10-01 → 2025-09-22 | 13x | 10x | -26% | Power/nuclear IPP |
| SEZL (Sezzle) | +852% | 2023-10-27 → 2026-07-15 | 139x | 95x | -32% | BNPL, profitable fintech |
| AGX (Argan) | +780% | 2022-10-20 → 2026-06-30 | 25x | 12x | -51% | Power-plant EPC |
| PLTR | +759% | 2022-12-27 → 2026-10-09 | 35x | 35x | 0% | (large cap, context only) |
| ALAB (Astera Labs) | +452%* | 2024-08-07 → 2026-06-30 | 13x | 9x | -29% | AI connectivity (*IPO Mar 2024) |
| APLD (Applied Digital) | +388% | 2022-07-13 → 2026-05-28 | 56x | 27x | -52% | AI data-center hosting |
| ASTS (AST SpaceMobile) | +384% | 2024-04-02 → 2026-05-28 | 66x | 25x | -62% | Space (direct-to-cell) |
| IONQ | +334% | 2022-12-27 → 2025-10-13 | 26x | 13x | -51% | Quantum |
| RKLB (Rocket Lab) | +327% | 2024-04-15 → 2026-05-27 | 43x | 19x | -55% | Space |
| HIMS | +324% | 2022-05-11 → 2025-02-19 | 22x | 10x | -55% | Telehealth/GLP-1 |
| APP (AppLovin) | +270% | 2022-12-27 → 2025-12-22 | 79x | 30x | -62% | AI ad-tech |
| OKLO | +253%* | 2024-09-03 → 2025-10-14 | 31x | 6x | -80% | Nuclear SMR (*SPAC price base) |
| LEU (Centrus) | +245% | 2022-05-12 → 2025-10-15 | 23x | 8x | -67% | Nuclear fuel |
| CVNA (Carvana) | +5% | 2022-12-27 → 2026-01-22 | 129x | 86x | -33% | Distressed turnaround |
| RGTI (Rigetti) | +44% | 2023-05-03 → 2025-10-15 | 150x | 37x | -75% | Quantum |
| QBTS (D-Wave) | +49% | 2023-05-12 → 2025-10-15 | 108x | 35x | -67% | Quantum |
| WGS (GeneDx) | -73% | 2023-11-13 → 2025-11-25 | 135x | 54x | -60% | Genomic testing turnaround |
| DAVE | +16% | 2023-05-19 → 2026-07-16 | 97x | 81x | -17% | Fintech turnaround |
| ROOT | -47% | 2023-03-13 → 2025-03-24 | 51x | 14x | -72% | Insurtech turnaround |
| NUTX (Nutex) | -97% | 2024-07-09 → 2026-10-05 | 52x | 48x | -8% | Micro-cap healthcare |
| CELH (Celsius) | -9% | 2022-01-27 → 2024-03-13 | 7x | 2x | -70% | Consumer growth |
| DUOL | -7% | 2022-05-11 → 2025-05-14 | 8.6x | 2.4x | -72% | Consumer software |
| CAVA | +23%* | 2023-10-03 → 2024-12-06 | 5x | 1.8x | -64% | Restaurant (*IPO Jun 2023) |
| TEM (Tempus) | +76%* | 2024-06-25 → 2025-10-08 | 4.1x | 2.8x | -31% | AI diagnostics (*IPO 2024) |
| JOBY | -46% | 2022-12-27 → 2025-08-04 | 6.4x | 1.7x | -73% | eVTOL |

All rows are computed from [Yahoo Finance data via yfinance](https://finance.yahoo.com/quote/FIX/history).

- Of the user's suggested candidates, the following were **not** strong 5-year winners: JOBY (-46%), ROOT (-47%), DUOL (-7%), CELH (-9%), CAVA (+23% vs. IPO-week price), TEM (+76% vs. first price), CVNA (+5% point-to-point, despite a ~129x move off the low). Their returns come almost entirely from buying the trough. — [Yahoo Finance data via yfinance](https://finance.yahoo.com/quote/JOBY/history)
- CELH's big multi-bag run (2019–2021) mostly happened before the window. Within the window it went ~7x from the Jan 2022 low to the Mar 2024 peak, then fell 78%. — [Yahoo Finance data via yfinance](https://finance.yahoo.com/quote/CELH/history)
- Carvana collapsed below $4 (pre-split) at end-2022 and recovered to ~$40 after its 2023 debt exchange. — [IFR](https://www.ifre.com/ifr-awards/1443705/americas-restructuring-carvanas-us5.5bn-debt-exchange). My data puts the Jan 2026 peak at ~$478 pre-split equivalent ($95.69 adjusted × 5).

### Inferences
- Two different kinds of "winner" exist. (1) **Compounders**: industrial/AI-infrastructure small caps (FIX, POWL, STRL, CLS, CRDO, IESC, MOD, ATI, CRS) produced 10–38x point-to-point and held most of the gain. (2) **Trough rockets**: distressed or theme names (CVNA, SEZL, RGTI, QBTS, WGS, DAVE, ROOT) produced 50–150x from capitulation lows, but their 5-year point-to-point returns were often mediocre or negative, because they first fell 90%+ in 2021–22.
- Point-to-point 5-year leaders were dominated by "AI-capex derivative" industrials rather than AI software or pure-play theme stocks.

### Gaps
- I did not systematically screen the whole Russell 2000/S&P 400 universe. The list comes from a candidate set of ~75 tickers, so some unlisted micro-cap multi-baggers may be missing.
- Market caps at the start of the window were not pulled. "Small/mid cap" status at ignition is based on general knowledge (most names were under $5B at their trough). Exceptions: SMCI and APP were roughly $1–3B at their troughs, and PLTR was large-cap throughout.
- All 2026 peaks and the mid-2026 drawdowns are unverified by news sources.

## What were the catalysts and the ignition events/dates?

### Takeaway
Most ignitions were a **fundamental surprise announced on a scheduled earnings date or a contract press release**. They produced a one-day gain of +20–75% on **5–85x average volume**, usually after the stock had already doubled off a capitulation low and was emerging from a base. Typical triggers: guidance raises, record backlog, a first profitable quarter, or a marquee customer (AT&T/Verizon, AEP, PepsiCo, hyperscalers). In theme stocks, the trigger was often **someone else's news** (Google/Amazon nuclear deals, Google's Willow chip) that re-rated the whole group.

### Cited Findings
**Ignition-day volume data (computed; return = close-to-close, gap = open vs. prior close)** — [Yahoo Finance data via yfinance](https://finance.yahoo.com/quote/ASTS/history)

| Ticker | Ignition date | Event | 1-day / gap | Vol x 50d avg | Price vs trough at ignition | Next 60 trading days |
|---|---|---|---|---|---|---|
| CVNA | 2023-05-05 | Q1'23 report: guided to positive adj. EBITDA | +24% / +39% gap | 6.4x | 2.4x | +479% |
| CVNA | 2023-07-19 | Debt exchange, ~48–54% of float short | (squeeze) | n/a | — | — |
| SEZL | 2023-12-22 | (post Nasdaq uplisting run) | +40% | 11.3x | 3.0x | +169% |
| SEZL | 2024-05-09 | Q1'24: GAAP NI beat all of 2023, guidance raised | +76% / +45% gap | 10.7x | 9.6x | ~0% |
| SEZL | 2024-11-08 | Q3'24 | +72% / +40% gap | 6.9x | 53x | -41% |
| CRDO | 2024-05-30 | FQ4'24 results | +27% | 6.2x | 3.5x | +37% |
| CRDO | 2024-12-03 | FQ2'25: rev +64%, guide $115–125M | +48% / +35% gap | 6.8x | 9.6x | -23% |
| ASTS | 2024-05-16 | AT&T definitive agreement + Q1 | +69% / +31% gap | 22.5x | 2.0x | +420% |
| ASTS | 2024-05-29 | Verizon $100M deal | +69% | 17.3x | 4.5x | +264% |
| ROOT | 2024-02-22 | Q4'23: revenue +173%, big beat | +53% / +34% gap | 85x | 3.8x | +393% |
| HIMS | 2024-02-27 | Q4'23 earnings | +31% / +20% gap | 12.3x | 4.3x | +20% |
| HIMS | 2024-05-20 | Launch of compounded semaglutide at $199/mo | +28% | 11.9x | 6.0x | -16% |
| WGS | 2024-04-30 | Q1'24: rev +51%, exome/genome +96%, guidance raised | +55% / +30% gap | 34.7x | 13.8x | +96% |
| DAVE | 2024-03-05 | Q4'23 earnings | +64% / +25% gap | 10.6x | 7.9x | +32% |
| POWL | 2023-08-02 | FQ3'23: backlog ~3x to record $1.3B | +40% / +21% gap | 9.3x | 4.5x | -13% |
| POWL | 2024-01-31 | FQ1'24 earnings | +45% / +23% gap | 8.8x | 6.3x | +26% |
| APP | 2023-05-11 / 2023-08-10 | AXON 2.0 ad engine ramp | +24% / +26% | 6.2x / 8.2x | 2.4x / 4.0x | +37% / +6% |
| APP | 2024-11-07 | Q3'24: rev +39%, software +66%, e-commerce pilot | +46% / +36% gap | 4.2x | 26.5x | +54% |
| SMCI | 2023-05-03 | AI server demand (pre-ChatGPT capex wave) | +28% | 5.3x | 3.8x | +147% |
| OKLO | 2024-10-15/16 | Google–Kairos SMR deal, then Amazon SMR deals | +16%, +42% | 11.7x, 14.1x | 2.1x–3.0x | +96% / +38% |
| RKLB | 2024-11-13 | Q3'24: rev +55%, backlog $1.05B, first Neutron contract | +28% / +31% gap | 8.8x | 5.3x | +47% |
| BE | 2024-11-15 | Up to 1 GW fuel-cell agreement with AEP | +59% / +58% gap | 10.6x | 2.5x | +20% |
| IONQ | 2024-09-27 | (theme bid begins) | +20% | 10.4x | 3.1x | +326% |
| QUBT | 2024-11-13 | Quantum theme mania | +93% | 54x | 6.3x | +211% |
| CELH | 2022-05-11 | Q1'22 earnings (PepsiCo deal followed Aug 1 2022) | +15% | 5.0x | 1.2x | +114% |
| CAVA | 2023-12-12 / 2024-08-23 | Q2'24 earnings beat | +20% | 12.8x / 8.7x | 1.3x / 4.1x | +62% / +12% |
| STRL | 2023-08-08 | Q2'23 earnings (E-Infrastructure) | +22% | 4.7x | 3.6x | -1% |
| FIX | 2025-07-25 | Q2'25 earnings | +22% / +18% gap | 3.6x | 9.3x | +21% |

- **Carvana:** Q1 2023 adjusted EBITDA margin was -0.9%, but the "best first quarter in company history" came with guidance to positive adjusted EBITDA in Q2 2023, and the stock "soared" on May 5, 2023. — [Nasdaq/Motley Fool](https://www.nasdaq.com/articles/up-157-in-2023:-has-carvana-really-made-any-progress); [Motley Fool](https://www.fool.com/investing/2023/05/05/why-carvana-stock-soared-today); [Carvana IR](https://investors.carvana.com/news-releases/2023/05-04-2023-211057697)
- **Carvana squeeze:** The July 2023 debt deal eliminated >83% of 2025/2027 unsecured notes and was paired with a ~$350M equity raise. Short interest was ~54% of float per Ortex (as of Jul 18) or ~48% per S3, and traders called the move a short squeeze. — [Investing.com](https://investing.com/news/stock-market-news/carvana-enters-deal-with-noteholders-to-cut-debt-by-12-billion-3128760); [IFR](https://www.ifre.com/ifr-awards/1443705/americas-restructuring-carvanas-us5.5bn-debt-exchange)
- **Sezzle:** The Q1 2024 release (May 8, 2024) said Q1 GAAP net income exceeded all of 2023 and raised FY24 net income guidance from $20M to $30M. — [Nasdaq press release](https://www.nasdaq.com/press-release/sezzle-reports-first-quarter-2024-results-2024-05-08). In May 2025 the stock rose ~42% on Q1'25 revenue of $104.9M vs. $64.8M est., and the 2025 revenue growth guide went to 60–65% from 25–30%. — [Motley Fool](https://www.fool.com/investing/2025/05/09/why-sezzle-stock-blasted-higher-this-week)
- **AST SpaceMobile:** The AT&T definitive agreement (revenue share through 2030) was announced May 15, 2024. Shares closed up >68% on May 16 at $4.03, despite Q1 revenue of only $0.5M. The Verizon deal two weeks later sent shares higher again. — [SpaceNews](https://spacenews.com/?p=423957); [Satellite Today](https://www.satellitetoday.com/connectivity/2024/05/16/att-signs-commercial-agreement-with-ast-spacemobile-for-satellite-to-cell-service)
- **Root:** The Q4 2023 report (late Feb 2024) showed revenue +173% to $194.8M vs. $127M consensus, and an adjusted loss of $1.68 vs. $2.49 expected. KBW upgraded the stock, and it was up 675% YTD by early April 2024. — [Barchart](https://www.barchart.com/story/news/25296547/up-675-ytd-what-s-behind-the-breakout-in-root-stock). Full-year 2024 net income was $29.2M vs. a 2023 loss of $147.4M. — [Stock Track/iTiger](https://itiger.com/news/1148811308). I found no source attributing the Feb 2024 move to a short squeeze, but the 85x volume ratio is consistent with forced covering (my inference).
- **Hims & Hers:** It launched compounded semaglutide at $199/month on May 20, 2024, and the stock rose roughly 29–38% depending on the source. The FDA later declared the shortage resolved (Feb 2025), forcing it to largely stop. — [Quartz](https://qz.com/hims-hers-ozempic-1851488227); [MarketBeat](https://www.marketbeat.com/articles/hims-and-hers-health-soars-on-generic-glp-1-rollout-plans/); [NBC LA/CNBC](https://www.nbclosangeles.com/news/business/money-report/hims-hers-shares-rise-as-company-adds-new-weight-loss-medications-to-platform/3667659/?amp=1)
- **Credo:** The stock rose ~48% on Dec 3, 2024. Revenue grew 63.6% to $72.0M and next-quarter guidance was $115–125M. The product is active electrical cables (AECs) for AI data centers. — [Barchart/Motley Fool](https://www.barchart.com/story/news/29876050/why-credo-technology-group-rocketed-nearly-50-today)
- **Powell:** In fiscal Q3 2023 (Aug 1, 2023), backlog nearly tripled to a record $1.3B. Orders were $505M (+$303M y/y), revenue +42%, gross margin +810 bp to 22.2%, and net income more than doubled. The drivers were LNG and petrochemical orders, which predate the data-center narrative. — [SEC 8-K](https://www.sec.gov/Archives/edgar/data/80420/000008042023000036/ex99-1q32023earningsrelease.htm)
- **GeneDx:** In Q1 2024 (Apr 29, 2024), revenue grew 51% to $61.5M vs. $49.5M consensus. Exome/genome revenue rose 96%, adjusted gross margin was 61% vs. 33% a year earlier, and guidance was raised with a path to 2025 profitability. Shares were up 34% intraday the next morning. — [GeneDx IR](https://genedx.gcs-web.com/news-releases/news-release-details/genedx-reports-first-quarter-2024-financial-results-and-business); [360dx](https://www.360dx.com/node/91916)
- **Oklo:** The stock rose 177.6% in October 2024 on Alphabet's Kairos SMR deal and Amazon's SMR deals. It received a DOE approval for its Aurora fuel facility safety report the day before. It was pre-revenue, and shares fell in early Nov 2024 after FERC rejected the Talen–Amazon arrangement. — [Barchart/Motley Fool](https://www.barchart.com/story/news/29410919/why-oklo-stock-skyrocketed-178-in-october); [Benzinga](https://benzinga.com/z/41607219)
- **Rocket Lab:** Q3 2024 (Nov 12, 2024) revenue was ~$105M (+55%), backlog $1.05B (+80%), plus a first multi-launch Neutron contract. The stock rose ~40% that week. — [Satellite Today](https://www.satellitetoday.com/launch/2024/11/13/rocket-lab-signs-first-neutron-launch-contract-posts-55-growth-in-q3); [Motley Fool](https://www.fool.com/investing/2024/11/15/heres-why-rocket-lab-stock-shot-up-423-this-week)
- **Bloom Energy:** The stock rose ~48% on Nov 15, 2024 on an agreement to supply up to 1 GW of fuel cells to AEP for data centers. That was "literally 10x" what Piper expected, although Evercore noted it was an option, not a firm order. The rally came a week after a weak earnings report. — [Barchart/Motley Fool](https://www.barchart.com/story/news/29606224/why-bloom-energy-stock-rocketed-48-on-friday); [Utility Dive](https://www.utilitydive.com/news/aep-bloom-energy-fuel-cell-data-center/733150/); [TipRanks](https://www.tipranks.com/news/the-fly/american-electric-deal-a-big-win-for-bloom-energy-says-evercore-isi)
- **AppLovin:** Q3 2024 revenue grew 39% to $1.2B and software grew 66% (driven by the AXON engine). The e-commerce pilot "exceeded expectations." Nov 7, 2024 was the stock's best day ever (+46%). — [Motley Fool](https://www.fool.com/investing/2024/11/08/why-applovin-stock-soared-45-this-week)
- **Celsius:** On Aug 1, 2022, PepsiCo invested $550M for ~8.5% (convertible preferred at $75/share) plus a long-term US distribution deal. The stock closed +11%. — [CNBC](https://www.cnbc.com/2022/08/01/pepsico-takes-550-million-stake-in-energy-drink-maker-celsius-.html); [SEC 8-K exhibit](https://www.sec.gov/Archives/edgar/data/1341766/000182912622014925/celsiusholdings_ex99-2.htm)
- **Dave:** I found no news article for the March 5, 2024 (+64%, 10.6x volume) reaction. In the Q4 2024 report (Mar 2025), revenue grew 38% to $100.9M, net income was $16.8M, and adjusted EBITDA rose 234%. — [SEC 8-K](https://www.sec.gov/Archives/edgar/data/1841408/000119312525044114/d916251dex991.htm)
- **Sterling / Comfort Systems:** Sterling's E-Infrastructure (data-center site development) is its main growth driver. In Q3 2025, data-center revenue rose more than 125% y/y, and signed backlog was $2.6B (+64%). FIX does mechanical/electrical/cooling for data centers. — [Zacks](https://www.zacks.com/stock/news/2536796/sterling-vs.-comfort-systems:-which-stock-wins-on-data-center-growth); [MarketBeat](https://www.marketbeat.com/articles/3-infrastructure-stocks-fueling-the-data-center-building-boom-pwr-strl-fix/)

### Inferences
- **Observable "at ignition" signals, in order of frequency in this sample:**
  1. A scheduled earnings report with a guidance raise or an inflection: first GAAP profit (SEZL, ROOT, DAVE), positive EBITDA guidance (CVNA), a gross-margin step-up (WGS), or a backlog step-change (POWL, RKLB, STRL).
  2. A gap of ≥15–45% on ≥5x volume (often 10–85x for small floats).
  3. A marquee-counterparty contract (ASTS/AT&T, BE/AEP, CELH/PepsiCo).
  4. High short interest, which amplified the move (CVNA ~48–54% of float; ROOT's 85x volume).
- **The stock had usually already doubled before the "obvious" ignition day.** The median "price vs. trough at ignition" in the table is ~3–5x. The capitulation low itself was rarely accompanied by a fundamental signal. The real tradeable signal came after the first leg off the bottom.
- **The first high-volume gap was not reliable on its own.** Many first gaps were followed by flat or negative 60-day returns: SEZL May 2024 ~0%, CRDO Jun 2023 -6%, STRL Aug 2023 -1%, POWL Aug 2023 -13%, HIMS May 2024 -16%, QBTS May 2023 -24% to -48%, RGTI Aug 2023 -54% to -63%. The bigger trend came from **repeated** gap-ups on successive earnings reports (POWL, APP, CRDO, SEZL each had 3–6 qualifying days). This suggests "second or third consecutive earnings gap-up with rising estimates" is a better filter than the first spike.
- In theme names (OKLO, IONQ, QUBT, RGTI, QBTS), ignition was driven by **sector news from mega-caps** (Google/Amazon nuclear deals Oct 2024; Google Willow Dec 2024) rather than company fundamentals, with clustered high-volume days across the whole group.

### Gaps
- I could not find dated news for several computed ignition days: SEZL 2023-12-22, CAVA 2023-12-12, IONQ 2024-09-27, NUTX 2024-08-12/2025-04-01, DAVE 2024-03-05. The catalysts for these are unconfirmed.
- No short-interest time series was pulled. Short-interest figures are cited only for CVNA.
- Some ignition dates fall on the day after an after-hours release. The listed date is the first full trading-day reaction.

## What fraction of "theme spikes" held vs. collapsed? What distinguished the ones that held?

### Takeaway
In this sample, **essentially none of the pure-theme spikes held their peaks**. All 16 quantum/nuclear/space/eVTOL/speculative-AI/crypto-to-AI names I checked sit 47–87% below their highs as of Oct 9, 2026. Most peaked on 2025-10-13 to 10-15 (quantum and nuclear) or in late May/June 2026 (space, AI hosting). The fundamentally driven compounders mostly sit 3–50% below their peaks and still hold 10–40x gains from their troughs. Real revenue/earnings growth was necessary but not sufficient: consumer growth names with real earnings (CELH, DUOL, CAVA, ELF, HIMS) also fell 50–78% when growth decelerated or the narrative broke.

### Cited Findings
**Theme-name survivorship (computed; "now vs peak" as of 2026-10-09)** — [Yahoo Finance data via yfinance](https://finance.yahoo.com/quote/OKLO/history)
- **Quantum:** IONQ -51% (peak 2025-10-13), RGTI -75%, QBTS -67% (both peaked 2025-10-15), QUBT -71% (peak 2024-12-18). Even so, from their 2023–24 lows they are still up 13–37x.
- **Nuclear/SMR:** OKLO -80% (peak 2025-10-14), SMR -87%, LEU -67% (both 2025-10-15), NNE -73% (2025-10-07). SMR is -28% over the full 5 years.
- **Space:** RKLB -55% (peak 2026-05-27), ASTS -62% (2026-05-28), LUNR -71%.
- **eVTOL:** JOBY -73% (peak 2025-08-04; -46% over 5 years), ACHR -64% (-41% over 5 years).
- **Speculative AI software:** SOUN -78% (peak 2024-12-26; -28% over 5 years).
- **Crypto-miners turned AI hosts:** IREN -54%, CIFR -54%, APLD -52%, CORZ -47%.
- **Compounders, by contrast:** FIX -17%, ATI -17%, DAVE -17%, BE -19%, CLS -23%, IESC -25%, CRDO -28%, SEZL -32%, LITE -3%. STRL (-48%), AGX (-51%) and POWL (-40%) are bigger exceptions, all after June 2026 peaks (unverified).
- **News context for 2026:** Quantum stocks sold off starting Jan 2026 (IONQ/RGTI/QBTS -11%/-18%/-19% that month) and fell further into summer. IONQ went from $69.28 (Jun 1) to $41.72 (Aug 4), and D-Wave was 66% below its 52-week high of $46.75. — [Yahoo Finance](https://finance.yahoo.com/news/quantum-stocks-february-2026-outlook-200000944.html); [Investing.com](https://www.investing.com/news/stock-market-news/quantum-computing-stocks-outlook-ionq-rigetti-and-dwave-after-a-brutal-selloff-93CH-4798766); [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/d-wave-quantum-crashed-2026-111512486.html). As of late Sept 2026, NuScale was -48% YTD and Oklo -51% YTD. — [Motley Fool](https://www.fool.com/investing/2026/09/27/nuclear-stocks-have-crashed-in-2026-heres-the-1-th/). Quantum stocks fell harder than tech overall during 2026 tech sell-offs, and IonQ traded at nearly 52x forward sales. — [Motley Fool](https://www.fool.com/investing/2026/09/01/perdiction-if-a-september-sell-off-hits-speculativ/)
- **First quantum round-trip:** The Dec 2024 Google Willow rally (D-Wave +1,096% since November) reversed on Jan 8, 2025 after Jensen Huang said practical quantum was decades away. In a single day RGTI fell -32%, QUBT -46% and QBTS -32%. — [TipRanks/Nasdaq](https://www.nasdaq.com/articles/quantum-computing-stock-rally-over-so-soon); [Motley Fool](https://www.fool.com/investing/2025/02/06/why-quantum-computing-stocks-rigetti-computing-d-w/)
- **Oklo** was pre-revenue at its Oct 2024 ignition. — [Barchart](https://www.barchart.com/story/news/29410919/why-oklo-stock-skyrocketed-178-in-october)
- **ASTS** had Q1 2024 revenue of only $0.5M at ignition. — [SpaceNews](https://spacenews.com/?p=423957)
- **Consumer/fundamental names that still round-tripped:** CELH -70%, DUOL -72%, CAVA -64%, ELF -50%, HIMS -55%, ROOT -72%, UPST -73%, SMCI -65% from peaks. — [Yahoo Finance data via yfinance](https://finance.yahoo.com/quote/CELH/history). HIMS's GLP-1 driver was regulatory and later removed when the FDA declared the shortage over. — [NBC LA/CNBC](https://www.nbclosangeles.com/news/business/money-report/hims-hers-shares-rise-as-company-adds-new-weight-loss-medications-to-platform/3667659/?amp=1)

### Inferences
- **Fraction that held:** about 0 of 16 pure-theme names held within 45% of their peak. About 10 of 15 "backlog/earnings compounders" are within ~40% of their peak. For theme stocks, surviving gains depended entirely on entry timing. A 5-year holder of JOBY, ACHR, SOUN or SMR lost money, and RGTI/QBTS holders roughly lagged SPY (+44%/+49% vs. +79%).
- **What distinguished holders:**
  - Revenue already present and accelerating, with operating leverage. FIX, POWL, STRL, CRDO and SEZL all showed rising margins and GAAP profits at ignition.
  - A multi-year backlog (POWL $1.3B, RKLB $1.05B, STRL $2.6B).
  - Demand tied to a measurable capex cycle (data-center build-out) rather than a future technology milestone.
  - Recurring confirmation every quarter.
  - Theme names were pre-revenue or tiny-revenue (OKLO, ASTS at $0.5M/qtr, quantum names), so their valuations rested on deal headlines and peer sympathy and reversed on the next negative headline (Huang comment, FERC ruling).
- **Necessary but not sufficient:** Consumer names with real earnings (CELH, DUOL, CAVA, ELF) still fell 50–78% when growth decelerated from very high multiples. The best holders combined earnings growth with a still-reasonable multiple and an expanding addressable market.
- **Survivorship warning:** Lists of "biggest winners" built from trough-to-peak multiples hugely overstate what was capturable. For a theme stock, peak-to-now drawdowns of 55–87% mean that late entrants and buy-and-holders often captured little.

### Gaps
- Theme-group drawdowns since June 2026 are computed from data only. I found no news explaining the broad May–June 2026 peak and subsequent 40–60% declines in space/AI-hosting/industrial small caps (STRL -48%, AGX -51%, POWL -40%, RKLB -55%, ASTS -62%) while SPY sat at highs. This needs verification.
- The tally is not a random sample. It is biased toward names that had big moves (survivorship in the candidate list itself). Theme stocks that never spiked are excluded.

## Common patterns

### Takeaway
The repeatable pattern was:
1. A capitulation low, usually in the 2022 bear market (May–Dec 2022 for most names).
2. A first leg up of 2–4x with little news.
3. A scheduled earnings report or marquee contract producing a +20–75% gap on 5–85x average volume. The best ones repeated this on subsequent reports.
4. A sector narrative (AI data-center capex, power demand, GLP-1, nuclear, quantum, space) that drew institutional and retail flows.
5. For theme names, a blow-off peak clustered across the group and a 50–87% round-trip.

### Cited Findings
- **Trough clustering:** 18 of the 39 names in the master table made their lows between 2022-04 and 2022-12 (CLS, POWL, STRL, MOD, IESC, CRS, SMCI, VRT, AGX, PLTR, APLD, IONQ, HIMS, APP, LEU, CVNA, DUOL, JOBY). Many speculative names in the wider screen bottomed in the same week of 2022-12-21 to 12-29 (CVNA, APP, IONQ, JOBY, PLTR, ACHR, SOUN, IREN, CIFR, COIN, MSTR). Others bottomed in May–Oct 2023 (RGTI, QBTS, CRDO, SEZL, DAVE, LITE) or in early to mid 2024 (RKLB, ASTS, OKLO, BE, SMR, NUTX). — [Yahoo Finance data via yfinance](https://finance.yahoo.com/quote/IWM/history)
- **Peak clustering:** quantum and nuclear peaked together on 2025-10-07 to 10-15 (IONQ, RGTI, QBTS, OKLO, SMR, LEU, NNE). Space, AI hosting and data-center industrials peaked in late May–June 2026 (RKLB 5/27, ASTS 5/28, APLD 5/28, POWL 5/11, STRL 6/4, CLS 6/2, MOD 6/2, CRDO 6/22, BE 6/22, FIX 6/22, NBIS 6/18, CIFR 6/18). — [Yahoo Finance data via yfinance](https://finance.yahoo.com/quote/RKLB/history)
- **High short interest** amplified turnarounds. CVNA's 48–54% of float short coincided with its July 2023 restructuring rally. — [Investing.com](https://investing.com/news/stock-market-news/carvana-enters-deal-with-noteholders-to-cut-debt-by-12-billion-3128760)
- **Big-tech sector catalysts** lifted whole groups: Alphabet/Amazon SMR deals for nuclear in Oct 2024 ([Barchart](https://www.barchart.com/story/news/29410919/why-oklo-stock-skyrocketed-178-in-october)), and Google Willow for quantum in Dec 2024 ([Nasdaq](https://www.nasdaq.com/articles/quantum-computing-stock-rally-over-so-soon)).
- **Mega-cap customer contracts** produced the largest single-day moves at the smallest market caps: ASTS +68% on AT&T ([SpaceNews](https://spacenews.com/?p=423957)), BE +48% on AEP ([Barchart](https://www.barchart.com/story/news/29606224/why-bloom-energy-stock-rocketed-48-on-friday)).
- **Profitability inflections** coincided with ignition for turnarounds: SEZL Q1'24 net income exceeded all of 2023 ([Nasdaq](https://www.nasdaq.com/press-release/sezzle-reports-first-quarter-2024-results-2024-05-08)), ROOT turned profitable in 2024 ([iTiger](https://itiger.com/news/1148811308)), and CVNA guided to positive EBITDA ([Motley Fool](https://www.fool.com/investing/2023/05/05/why-carvana-stock-soared-today)).

### Inferences
- **Signals a trader could have screened for in real time:**
  - A ≥15% earnings gap on ≥5x 50-day average volume after the stock is already 2x off a 52-week low.
  - Guidance raised well above consensus (CRDO, SEZL 2025, APP).
  - Backlog or orders up ≥50% y/y (POWL, RKLB, STRL).
  - A first GAAP profit or a positive EBITDA guide (SEZL, ROOT, DAVE, CVNA).
  - Short interest ≥20–30% of float.
  - Group-wide sympathy moves when a mega-cap validates a theme.
  The best winners showed several of these at once and repeated them across 2–4 consecutive quarters.
- **Risk-management pattern:** Theme spikes ended with clustered group-wide peaks and a single external negative headline (Huang's quantum comment, FERC's Talen ruling, FDA ending the GLP-1 shortage). Distribution was visible as high-volume down days across the group. Exits keyed to group breadth would likely have saved most of the 50–80% drawdowns (an inference, not tested).
- Fundamental compounders also suffered 40–85% intra-trend drawdowns (SMCI -85% after its accounting issues, STRL -54%, POWL -47%, CRDO -50%). Holding winners required tolerance for deep pullbacks even when fundamentals held.

### Gaps
- I did not backtest the screening rule on non-winners (base rate of false positives), so its predictive value is unquantified.
- SMCI's accounting controversy (Aug 2024) and other company-specific crash causes were not separately sourced in this pass.
