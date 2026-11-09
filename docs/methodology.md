# Methodology

This document explains how each series in the repository was built, in the order the pieces fit together. Column definitions are in [`data/README.md`](../data/README.md); sources are in [`sources.md`](sources.md); caveats are summarized in [`limitations.md`](limitations.md).

Contents

1. [Definitions and approach](#1-definitions-and-approach)
2. [Retail prices and the bundled series](#2-retail-prices-and-the-bundled-series)
3. [Wires-company charges, residential, 2002–2025](#3-wires-company-charges-residential-20022025)
4. [Wires-company charges, all classes and business, 2002–2025](#4-wires-company-charges-all-classes-and-business-20022025)
5. [Transmission versus distribution, 2002–2025](#5-transmission-versus-distribution-20022025)
6. [Regulated era, 1992–2001](#6-regulated-era-19922001)
7. [Statewide series](#7-statewide-series)
8. [Source anomalies found along the way](#8-source-anomalies-found-along-the-way)
9. [Series breaks](#9-series-breaks)

## 1. Definitions and approach

**Question.** Did falling ERCOT wholesale prices reach Texas retail bills? Answering it needs a retail price that can be split into what the wires companies charge and what is left for energy and retail service.

**Components.** For each year and customer class the price is split into:

| Component | Meaning |
|---|---|
| Transmission | The wires company's bill from ERCOT for transmission service, allocated to the class. |
| Distribution + other | The wires company's remaining own retail charges (distribution, metering, riders). |
| Transition charges | Securitization (transition bond) charges and other stranded-cost items such as competition transition charges, excess mitigation credits and retail clawback credits. Can be negative. |
| Storm bonds and state fee | Storm-restoration bond charges and riders, and the state System Benefit Fund fee. |
| Energy + retail | Everything left after the wires companies' charges: the competitive provider's energy cost, margin and retail costs. |

**Two eras.**
- **Through 2001** (regulated monopolies): the price is the bundled revenue per kWh of the investor-owned utilities in the ERCOT region. Transmission and distribution are *estimates* built from each utility's cost of service (Section 6). Generation + retail is the remainder.
- **From 2002** (retail choice): the price is competitive retail providers' revenue per kWh. The wires companies' charges are measured from filings (Sections 3–5) and weighted by kWh across Oncor, CenterPoint, AEP Texas and TNMP. Energy + retail is the retail price minus those charges.

**Business** means all customer classes minus residential: commercial, industrial, lighting and other.

**Grades.** Line items and rows carry a certainty grade: **A** (reported in a filed source as used), **B** (computed by a method checked against reported values), **C** (weak: an assumption, a proportional scaling or a press-reported figure). Rows carry the lowest grade among their inputs. Cells are left blank rather than interpolated unless a labelled imputation is described below.

**Units.** Nominal cents per kWh unless a column says otherwise. Real-dollar charts use CPI-U annual averages scaled to 2025.

## 2. Retail prices and the bundled series

- **Source:** EIA Form 861, files `Sales_Ult_Cust` (annual, 1990–2025) and the historical series. Price = revenue ÷ MWh by ownership group and customer class.
- **Groups:** `iou` (investor-owned utilities outside the competitive area), `pub` (ERCOT-area municipal utilities and co-ops), `comp` (competitive retail providers, from 2002), plus the investor-owned utilities in the ERCOT region before 2002.
- **Filtering for consistency:** entities with fewer than 500 residential customers are excluded from utility-level series. From 2012 EIA's full-form data drops small co-ops and municipals, so the public-power groups are filtered in 2019 to the utilities that also file the full form in 2018 or 2020.
- **Delivery-only data.** EIA reports delivery revenue (wires charges) separately only from 2020. For 2012–2018 EIA's Operational Data gives all-class delivery totals only, and for 2002–2011 delivery revenue is blank. Everything earlier comes from FERC Form 1 and SEC filings (Section 3).
- **What EIA's delivery series contains is not uniform across utilities.** For Oncor and CenterPoint it excludes the bond companies' charges, like FERC Form 1 (CenterPoint's Form 1 equals EIA's figure to the dollar). For AEP Texas it includes them, because AEP consolidates its bond companies: AEP's 10-K residential cents per kWh is within about 2% of EIA's in 2020–2025, and it fell 0.28¢ in 2020 when the TF2 bonds retired. EIA's AEP delivery therefore carries 0.2–0.9¢ of securitization charges that the others do not. A residual "energy + retail" built directly from EIA delivery data would be biased for these reasons; this repository rebuilds delivery line by line instead.

## 3. Wires-company charges, residential, 2002–2025

Output: `data/utility_level/wires_residential_components_2002_2025.csv` (one row per utility-year), with line-item detail in `wires_residential_components_line_items.csv`. Delivery revenue before the component split, 2002–2019, is in `wires_residential_delivery_revenue_2002_2019.csv`.

### 3.1 Volumes and reported revenue

| Utility | Years | Source |
|---|---|---|
| Oncor, CenterPoint | 2002–2025 | FERC Form 1 p.300, account 440 Residential Sales (via PUDL) |
| TNMP | 2002–06 | Form 1 p.304, Texas unbundled residential schedule |
| TNMP | 2007–19 | PNM Resources 10-K operating statistics |
| TNMP | 2020–25 | EIA-861 (2025: EIA-861 2025 release) |
| AEP Texas Central, North | 2002, 2005, 2008–18 (North also 2003–04) | AEP earnings monitoring reports (EMRs) filed annually at the PUCT under 16 TAC §25.73: residential revenue by rider, billed MWh and customers. 2005 and 2011 exist only as scans; values were read from the page images |
| AEP Central, North | 2002–17 (volumes only) | PUCT retail-market Market Share Data workbook: all retail providers' residential MWh and customers by TDU area. Used where no EMR volumes exist |
| AEP Central, North | 2020–25 | EIA-861 `Delivery_Companies` |
| AEP Texas combined | 2015–18 | Sum of the Central and North EMRs |
| AEP Texas combined | 2019–25 | AEP Texas Inc. EMRs (merged company only). Check: versus EIA-861 Central+North revenue −0.3% to −0.4% (2020–21, 2023–24), −2.2% in 2022; versus AEP 10-K −0.1% (2019), −0.2% (2025) |

The market-share workbook agrees with other volume sources: Oncor identical to Form 1 (2003–16); CenterPoint and TNMP within about 1–2%; AEP Central+North versus the AEP 10-K 0.0% (2015), −2.3% (2016), −1.5% (2017).

### 3.2 Delivery = reported revenue minus the non-delivery items inside it

- **Oncor:** Form 1 as reported. Form 1 excludes bond charges (in 2010 Oncor's 10-K revenue minus Form 1 equals its transition-charge revenue) and the excess-mitigation and clawback credits (no step in Form 1 cents per kWh when they ended in 2003 and 2005).
- **CenterPoint:** Form 1 minus the competition transition charge (CTC) and storm ADFIT credits. Form 1 excludes bond charges and the excess mitigation credit (no step when it ended in April 2005). The CTC (Sept 13, 2005–2008, about 0.07¢) and the storm ADFIT credits are *assumed* to be booked inside Form 1; that assumption is unverified. The CTC started Sept 13, 2005 according to CenterPoint Houston's 10-K; the archived PUCT summary printed before that date shows $0, so the March 2006 rate (0.08¢) is carried back to Sept 13, 2005.
- **TNMP:** reported revenue minus the CTC (2007–2020) and storm riders.
- **AEP, years with an earnings monitoring report:** taken from the EMR's "Revenues, Sales, and Customer Data" workpapers. Each rider has its own workpaper marked "Included in WP1" (base revenue) or "Not Included". Delivery = WP1 base revenue (including TCRF, DCRF, AMS, EECRF, rate-case, merger-savings and rate-reduction riders) minus the transition, CTC/true-up, excess-mitigation and SBF riders included in it, plus nuclear decommissioning where billed separately.
  - 2019: the TCRF workpaper is labelled "Not Included" but is already in WP1, so it is not added again (it is "Included" in every other year with a separate TCRF workpaper; 2019 WP1 is in line with 2018's; and WP1 + transition + storm reproduces the 10-K within 0.1%).
  - 2021: the COVID-19 Electricity Relief Program rider ($3.4M residential, "Not Included") is a state public-benefit levy like the SBF and is placed in the `sbf` columns.
- **AEP Central and North as separate divisions, 2020–2024:** EIA-861 reported revenue minus residential bond charges and ADFIT credits. 2025 division rows and TNMP 2025 come from the EIA-861 2025 release.
- **AEP years without an earnings report** (Central 2003–04 and both divisions 2006–07): delivery is imputed (Section 3.5). The two divisions separately in 2019 are left blank; use the merged AEP Texas row.

### 3.3 Bond charges: residential allocation factor × all-class collections

Each financing order fixes the share of the bond revenue requirement allocated to the residential class:

| Series | Residential share |
|---|---|
| CenterPoint TC1 | 35.58% |
| CenterPoint TC2 | 40.04% |
| CenterPoint TC3 | 18.34% |
| CenterPoint TC5 | 40.61% |
| CenterPoint SRC1 | 64.92% |
| CenterPoint SRC2 | 55.46% |
| Oncor | 41.27% |
| AEP TF1 | 37.07% |
| AEP TF2 | 37.92% |
| AEP TF3 | 39.29% |
| AEP Restoration | 52.52% |

All-class collections come from, in order of preference:
1. **Issuer 10-K income statements:** CenterPoint TC1 2002–12, TC2 2005–07, Oncor 2003–16, AEP TF1 2002.
2. **Monthly servicer remittances** (SEC 8-K and 10-D exhibits): CenterPoint TC2 2009–19, TC5, SRC2; AEP TF2, TF3, Restoration.
3. **Scheduled debt service** from the prospectus amortization table × coupons + fees: AEP TF1 2003–15, CenterPoint TC3, SRC1, TC2 2008.

Collections by series and year are in `data/source_extracts/securitization_collections_by_series.csv`. Checks:
- CenterPoint's summed series total 2004–2019 is within 0.9% of its 10-K "bond companies" revenue. Individual years differ by up to ±10% because of remittance timing (2019 is +21%).
- Scheduled-debt-service estimates were within about ±5% where actuals exist.
- AEP Central bond dollars (factor × collections) versus PUCT TC rates × market-share kWh: −11% to +7% by year, typically −4% to −7% (2004–2017). Billed amounts in the EMRs run 4–10% above factor × collections (median 1.076) but equal PUCT bond rate × residential kWh within about 2% in 10 of 12 report years. Where an EMR exists, the billed amount is used.
- CenterPoint TC1 in 2013: the bonds retired and the issuer filed no FY2013 10-K, so this year uses the PUCT residential rate × kWh.
- Oncor 2016 bond revenue ($21.6M) is derived from the 10-K statement that it fell $98M from 2015.

### 3.4 Riders: PUCT rate × residential kWh

The PUCT's "Summary of Non-Bypassable Charges" lists every TDU's residential rider rates. 62 archived copies were recovered from the Wayback Machine, giving 43 distinct versions from Sept 2003 to Mar 2021. Rates were read by hand from the documents' layout text; each is a step function by the document's own version date. Rates are averaged over each year by day. For $/customer-month riders they are multiplied by residential customers instead. For AEP Central and North in 2019, residential kWh by division is unknown (the 2019 EMR covers the merged company only), so cents per kWh comes from the PUCT rates directly.

Deregulation transition items were large:

| Utility | Period | Securitized transition charges (¢/kWh) |
|---|---|---|
| CenterPoint | 2006–2019 | 0.37–0.67 |
| AEP Central | 2007–2019 | 1.1–1.5 (2002–2006: about 0.4–0.5) |
| Oncor | 2004–2015 | about 0.15 |

They were partly offset in the early years by credits:

| Credit | Rate | Period |
|---|---|---|
| CenterPoint EMC | −0.49¢ | 2002 to Apr 2005 |
| Oncor EMC | −0.23¢ | 2002–2003 |
| Oncor clawback | $2.73/customer-month (about −0.22¢) | 2004–2005 |
| AEP Central negative CTC | −1.07¢, then −0.56¢ | Feb 2007 (first published; possibly earlier) – 2008 |
| AEP Central retail clawback refund | about −0.72¢ for the year (~$60M residential: payments from Oct 12 plus a one-time December bill credit of about $58 per 1,000 kWh) | Oct–Dec 2006 |
| AEP North interim credit (retail clawback, Docket 31461), then CTC | −1.9¢, then +0.08¢ | Sept 2006–Feb 2007, then July 2007–May 2008 |

### 3.5 Assumptions, gaps and imputed values

**Before Sept 2003** (no archived PUCT summary): the EMC rates (all three utilities) and SBF rates first seen in Sept 2003 are carried back to Jan 2002. For CenterPoint this is supported by its 10-K (the EMC was a fixed ~$238M a year refund from Jan 2002). AEP Central's 2002–2004 bond cents per kWh comes from TF1 collections over EMR or market-share kWh.

**After Mar 2021** (last PUCT summary): small TDU-billed storm items not observed after Aug 2021 are omitted (CenterPoint and AEP ADFIT credits ≤0.015¢, TNMP's 0.014¢ storm factor). Bond charges after 2021 are fully covered by SEC servicer data.

**Not handled:** nuclear decommissioning charges are left in delivery (PUCT lists them separately only for some utilities); CenterPoint's SRC3 bonds (issued late 2025) are omitted. No straight-line interpolation is used.

**Imputed cells** (AEP, years without an earnings report) are filled in the normal columns and marked by four extra columns per component: `*_status` (`imputed`), `*_certainty` (0–100), `*_error_band_cents` (± ¢/kWh) and `*_imputation_method`. `min_certainty_of_imputed` is the lowest score in the row. To treat low-confidence cells as missing, drop cells below a chosen certainty. Scale: 85+ = the method reproduces observed values within about 2% in most test years; 70–80 = validated against observed years, error band ≤ about 0.06¢; 60–65 = validated but with a known bias or timing assumption; 55 or lower = weakest. Merged AEP Texas scores are kWh-weighted over the divisions (an observed division counts as 100), rounded to 5.

| Utility | Year | Component | Value (¢/kWh) | Certainty | ± ¢/kWh | Method |
|---|---|---|---|---|---|---|
| AEP Central | 2003 | delivery | 2.19 | 65 | 0.05 | AEP North observed × Central/North ratio 0.6875 (mean of 2002 = 0.682 and 2005 = 0.693; base rates of both unchanged Sept 2003–Feb 2006). Cross-check: rate model adjusted for its same-year North error, within 0.03¢ |
| AEP Central | 2004 | delivery | 2.25 | 70 | 0.05 | Same ratio; cross-check within 0.04¢ |
| AEP Central | 2006, 2007 | delivery | 2.32, 2.40 | 70, 65 | 0.06 | Rate-based model: PUCT base rates, merger/rate-reduction credits and TCRF × PUCT market-share monthly customers and kWh. Test errors versus AEP reports −0.03 to +0.06¢ (2005, 2008–10). Omits nuclear decommissioning and the rate-case surcharge (about 0.01–0.04¢ low). 2007: mid-year rate change and an assumed end date (Sept 2007) for the merger/rate-reduction credits |
| AEP North | 2006, 2007 | delivery | 3.33, 3.41 | 60, 55 | 0.10 | Same model. Test errors −0.05 to +0.02¢ (2005, 2008–10) but +0.09/+0.13¢ in 2003–04 (from the kWh source; dollars within 0.3%) |
| AEP Texas merged | 2003, 2004, 2006, 2007 | delivery | 2.36, 2.42, 2.48, 2.56 | 70, 75, 70, 65 | 0.04–0.07 | Sum of the divisions. Merged model test errors −0.04¢ (2005), +0.00¢ (2008) |
| AEP Central | 2002 | bond charges | 0.46 | 65 | 0.016 | Residential factor × TF1 issuer revenue × 1.076 (median billed/estimate ratio in report years, range 1.04–1.10) |
| AEP Central | 2003 | bond charges | 0.42 | 70 | 0.021 | PUCT TC1 rate × residential kWh; rate known Sept–Dec, carried back to Jan |
| AEP Central | 2004 | bond charges | 0.41 | 85 | 0.008 | PUCT TC1 rate × residential kWh |
| AEP Central | 2006 | bond charges | 0.60 | 70 | 0.036 | PUCT TC1 + TC2 rate × kWh. TC2 billing assumed from 2006-10-15 at the Feb 2007 rate: TF2 was issued Oct 2006 (AEP 10-K 2006) and remitted Nov–Dec 2006, but the PUCT summary shows TC2 only from Feb 2007 |
| AEP Central | 2007 | bond charges | 1.16 | 80 | 0.035 | PUCT TC1 + TC2 rate × kWh (TC2 for 1 Jan–11 Feb carried back) |
| AEP Central | 2006 | transition_other (retail clawback refunds) | −0.72 | 50 | 0.16 | December bill credit: $58 per 1,000 kWh × Dec 2006 residential kWh = $31.0M (certainty 60). Plus 89% of the $33M paid Oct 12–Dec 1 = $29.2M (certainty 50: residential share and pass-through assumed). Source: Corpus Christi *Caller-Times*, Dec. 2006 |

Merged AEP Texas bond charges and the clawback refund in these years are AEP Central's divided by merged kWh, with the same certainty.

### 3.6 Checks

- AEP EMRs: residential delivery + transition + storm revenue versus AEP 10-K residential revenue: −1.2% (2017), −0.1% (2018), −0.1% (2019). EMR MWh versus market share within about ±2.5% (2003–2017); 2002 is 6–7% lower in the EMR because January 2002 is pilot data only.
- Overlap with EIA delivery (2020–2022): CenterPoint matches exactly; Oncor runs 0.6% low (Form 1 versus EIA); TNMP within ±0.02¢; AEP runs 0.03–0.09¢ high, mainly because the 10-K kWh is 1–2% below EIA's. See `data/validation/eia_overlap_check_2020_2022.csv`.
- Full list of checks: `data/validation/residential_components_checks.csv`.

## 4. Wires-company charges, all classes and business, 2002–2025

Output: `data/utility_level/wires_all_class_components_2002_2025.csv`, with line items in `wires_all_class_components_line_items.csv`. Business (C&I) = (all-class − residential) ÷ (all-class kWh − residential kWh); the file includes it as `ci_*`.

**Delivery** for Oncor and CenterPoint is FERC Form 1 p.300 "sales to ultimate consumers" (accounts 440–445). This equals EIA's "Revenues from delivery customers" (Operational Data 2012–19) and EIA's `Delivery_Companies` totals (2020–25): the two match to the dollar in 24 of 28 utility-years, and the other four are Oncor within −0.35%. It excludes the bond companies and third-party transmission revenue (account 456.1 from 2006). Delivery for TNMP:

| Years | Source | Grade |
|---|---|---|
| 2002–06 | Form 1 p.304, sum of Texas Unbundled Delivery schedules 6.1.1.1–6.1.1.6 (New Mexico bundled schedules excluded) | A |
| 2007–11 | PNMR 10-K residential + commercial + industrial revenue × 1.0229 (the 2012–19 ratio of EIA delivery revenue to R+C+I, range 1.019–1.029; lighting sits in "Other") | B |
| 2012–19 | EIA Operational Data "Revenues from delivery customers" | A |
| 2020–25 | EIA `Delivery_Companies` | A |

**Bond and storm charges:** all-class collections per series (Section 3.3). **SBF:** PUCT per-kWh rate × all-class kWh until Aug 2013 (B); it was a uniform per-kWh fee, and AEP's all-class SBF ÷ all-class MWh is within 2% of the residential rate in every report year.

**Other transition charges:**

| Utility | Item | Years | Method | Grade |
|---|---|---|---|---|
| Oncor | Excess mitigation credits | 2002–03 | Total from the 10-K: $389M + $26M interest. 2003 = $176M; 2002 = the remainder, $239M | C (year split) |
| Oncor | Retail clawback | 2004–05 | Residential-only credit ($2.73/customer-month), so all-class = residential | B |
| Oncor | TC2-R refund | 2016–17 | Residential ÷ the bond residential factor, 0.4127 | C |
| CenterPoint | Excess mitigation credits | 2002–05 | 10-K: "approximately $238 million per year" from Jan 2002; 2005 prorated to April 29 | B, 2005 C |
| CenterPoint | CTC + rate-case-expense rider | Sept 13, 2005–2008 | Residential (rate × kWh) ÷ the TC2 residential factor, 0.4004: about $42–46M a year | C |
| CenterPoint | Storm ADFIT credits | 2011–21 | Residential ÷ the SRC1 factor, 0.6492 | C |
| TNMP | CTC (Dec 2006–2020) | | Residential × 1.8 (±15%). The 10-K's $87.3M true-up balance collected over 14 years implies about $160–200M from all classes; $184M used. Applying the residential per-kWh rate to all kWh would overstate it because larger customers pay CTC per kW | C |
| TNMP | Storm riders | | Residential × all kWh ÷ residential kWh | C |

**AEP Texas Central and North.** In report years (Central 2002, 2005, 2008–18; North 2002–05, 2008–18; merged 2019–25) all-class amounts are each schedule's "Total" column, read the same way as the residential column. 2005 and 2011 exist only as scans; their totals were read from the page images and each Totals line was checked so that the six class totals add to column 7. 2002 reports cover about Feb–Dec and are scaled to full-year MWh from the market-share workbook (×1.031 Central, ×1.057 North; B). Central bond charges in years without a report are all-class collections (TF1 scheduled debt service; TF2 from Oct 2006 remittances); in report years these match AEP's billed bond charges within −1.9% to +4.4%, mostly ±1% (12 years), so no correction is applied. For years without a report (Central 2003–04 and 2006–07; North 2006–07):

| Item | Method | Grade |
|---|---|---|
| MWh | PUCT Market Share Data, total MWh (within about 2% of AEP's own MWh in report years, except North 2003–05 at −3 to −5% and the 2010–11 outliers) | B |
| Delivery 2006–07 | Form 1 account 456 ÷ 1.019 (Central) or 1.018 (North), the mean ratio of account 456 to report-year all-class delivery over 2008–16 (range 0.99–1.06). Account 456 is usable only from 2006, when wholesale transmission moved to 456.1 and generation sales had ended | C |
| Delivery, Central 2003–04 | **Blank.** No report exists, and account 456 then still included wholesale transmission and generation sales. The merged AEP rows for 2003–04 are therefore blank too (the statewide all-class series imputes them; see Section 7) | – |
| EMC, Central 2003–04 | Residential × 2.40, the all/residential EMC ratio in the 2002 and 2005 reports (2.39, 2.41) | C |
| Clawback, Central 2006 | −$68M: $33M paid to retailers Oct 12–Dec 1 plus $35M of December bill credits (*Caller-Times*, Dec 2006). The PUCT ruling was "almost $65M" | C |
| CTC and true-up expense, Central 2007 | Residential × 2.585, the all/residential CTC ratio in the 2008 report | C |
| North interim clawback credit (Sept 2006–Feb 2007) | Residential ÷ 0.89 (the residential share of Central's 2006 clawback) | C |
| North CTC, Jul–Dec 2007 | Residential × 1.664, the 2008 report ratio | C |

Division rows 2020–25 come from EIA-861 `Delivery_Companies` (all classes), less AEP Central's all-class bond and storm-bond collections, because EIA's AEP figure includes them. Merged "AEP Texas (Central+North)" is the sum of the divisions for 2002–18 and the merged report for 2019–25. Merged report delivery + bonds + storm + SBF equals EIA's Central+North within −1.0% to +0.8% (2020–25).

**Checks and grades.** 62 rows are A, 36 B and 44 C; most C grades come from one small rider (CenterPoint storm ADFIT credits, the TNMP CTC and the Oncor bond refund). Our delivery revenue on EIA's own basis matches EIA's 2020–2025 file within $13M (Oncor 2021, −0.3%) and the 2012–2018 file within $0.5M except Oncor 2015 ($4.4M, −0.14%). Business cents per kWh matches EIA's within 0.02¢ except CenterPoint 2020–24 (ours 0.09–0.19¢ higher, because EIA leaves out CenterPoint's bond charges). Details: `data/validation/all_class_checks.csv`.

**Notes on definitions.**
- *kWh denominator:* retail kWh billed by the wires company. In the 2002–17 overlap, the market-share workbook matches Oncor's Form 1 within 0.3%, CenterPoint within 0.6% (except 2002 and 2017), AEP within about 2% (except Central 2011 −16% and North 2011 −7%, where the workbook appears to be missing data) and TNMP erratically (−11% to +21% in 2002–04 and 2013–15).
- *Transmission-voltage customers* are included in every utility's totals. AEP Central has 3.9–5.5 TWh a year of them (about 20% of its MWh). AEP North's all-class cents per kWh falls to 1.94¢ in 2025 as oil-field load grew from 2023.
- *Partial years and mergers:* AEP's 2002 report covers about Feb–Dec (scaled); Oncor's 2009 Form 1 class relabelling (most industrial revenue moved to commercial) does not affect totals; Sharyland's distribution moved into Oncor in 2017 (Oncor MWh rises 11% in 2018); AEP's divisions are reported separately through 2018 and merged from 2019.
- *2002–04 credits* are net for all classes: CenterPoint about −$238M a year, Oncor −$239M and −$176M, AEP Central about −$15M a year.
- Before 2006, about $60M a year (about 3%) of Oncor's 10-K distribution revenue, net of bond charges, is booked outside Form 1 accounts 440–445. It is excluded here, as it is from EIA's later figures.

## 5. Transmission versus distribution, 2002–2025

Output: `data/utility_level/wires_residential_transmission_split_2002_2025.csv` (Oncor, CenterPoint, AEP Central and North through 2019, merged AEP, TNMP).

```
res_tx_cents     = tdu_wholesale_tx_cost × res_tx_alloc_factor ÷ residential kWh
dist_other_cents = delivery_cents − res_tx_cents
```

**Cost.** Each year's final ERCOT transmission charge matrix gives the TDU's prior-year average 4CP load (`tdu_4cp_kw`), the billed postage-stamp rate (`ercot_postage_stamp_rate`) and total ERCOT TCOS. `tdu_wholesale_tx_cost_matrix_kusd` = 4CP × rate.

*The billed rate is the sum of every transmission service provider's access fee,* not total TCOS divided by the TOTAL-row 4CP on the matrix's Parameters sheet. The TOTAL row double-counts aggregated load entities (aggregators and their members), so dividing by it understates the rate. Each TDU's column total on the matrix's `$TotalTrans` sheet equals 4CP × the sum of access fees to the dollar (verified for Oncor, CenterPoint, AEP and TNMP in 2009, 2014, 2019, 2023, 2024 and 2025; for example Oncor 2024: $1,975.2M on the sheet versus $1,786.8M by the TOTAL-row method).

| Year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| TOTAL-row rate ($/kW-yr) | 52.48 | 52.01 | 58.41 | 62.50 | 62.94 | 60.39 | 67.21 |
| Billed rate (sum of access fees) | 54.57 | 54.28 | 58.50 | 64.29 | 67.30 | 66.76 | 68.55 |
| Understatement by the TOTAL-row method | 4.0% | 4.4% | 0.2% | 2.9% | 6.9% | 10.5% | 2.0% |

*Mid-year TCOS updates.* Transmission service providers file interim TCOS updates that take effect after the matrix is set. For every provider whose TCOS differs between matrix *y* and matrix *y+1*, the approval date of the new docket was taken (PUC "Notice of Approval" or "Order" on Interchange; 309 dockets), and the TDU's load-ratio share of the change from that date to Dec 31 was added (`in_year_tcos_updates_kusd`). `tdu_wholesale_tx_cost_kusd` is the time-weighted total. It adds 0–8% a year, largest in 2013–14 (the CREZ lines). Limits: it assumes each update takes effect on approval and misses a second update by the same provider in one year; 2025 is on a matrix basis only; 2018 is slightly negative (tax-cut reductions).

**Residential allocation factor.** The residential share of the 4CP transmission allocator from the governing base-rate case, read from Rider TCRF or the TCRF workbook in each TDU's semi-annual TCRF petitions (165 petitions; rule 16 TAC §25.193). TCRF riders existed for all five TDUs from 2002. Each factor is day-weighted within its change year.

| Utility | Factor and effective date | Source |
|---|---|---|
| Oncor | 0.47028, 2002 | Docket 22350 (unbundled cost of service, UCOS) |
| | 0.443564, Sept 17, 2009 | Docket 35717 |
| | 0.468539, July 1, 2011 | Docket 38929 (transmission then moved out of base rates into TCRF) |
| | 0.470021, Nov 27, 2017 | Docket 46957 |
| | 0.458807, Sept 2023 | Docket 53601 (order Apr 6, 2023); first used in the Sept 2023 TCRF (petition 55075) |
| CenterPoint | 0.417858, 2002 | Docket 22355 |
| | 0.456, Oct 2006 | Docket 32093; date from the CEHE 10-K |
| | 0.471426, Sept 2011 | Docket 38339; "implemented in September 2011" (10-K) |
| | 0.476096, Sept 2020 | Docket 49421 (order Mar 9, 2020); first used in the Sept 2020 TCRF (petition 50890) |
| | 0.489238, Sept 2025 | Docket 56211 (order Mar 13, 2025); first used in the Sept 2025 TCRF (petition 58178) |
| AEP Central | 0.442622, 2002 | Docket 22352 |
| | 0.463085, Oct 2005 | Docket 28840 |
| | 0.472086, July 2008 | Docket 33309 |
| AEP North | 0.452331, 2002 | Docket 22354 |
| | 0.465534, June 2007 | Docket 33310 |
| TNMP | 0.5258, 2002 | Docket 22349 |
| | 0.45931, Sept 2009 | Docket 36025 |
| | 0.495956, Mar 2011 | Docket 38480 |
| | 0.45129, Jan 1, 2019 | Docket 48401, effective Jan 1, 2019 (stated in petition 50891) |
| | 0.416446, Sept 2020 | the Sept 2020 TCRF is the first to use the new allocators (petition 50891) |
| Merged AEP 2020–25 | 0.4708 (Central and North, cost-weighted) to Feb 2021; 0.47309 from Mar 2021; 0.48203 from Sept 2022; 0.48477 from Mar 2025 | Docket 49494 consolidated the TCRF (order Apr 3, 2020); first uses in petitions 51554, 53653 and 57356 |

Where a rate-case effective date was not stated, the first TCRF update that used the new factor was used, or the date was bracketed between consecutive PUCT rate summaries. Those change years are graded B, and the source is in `alloc_source`. Merged AEP 2002–19 cost-weights the two divisions; division rows stop in 2019 because the 2020+ matrices list AEP Texas as one load.

**Residential kWh and `delivery_cents`** come from `wires_residential_components_2002_2025.csv`. Delivery excludes bond, storm and SBF charges, so `dist_other` is distribution plus non-transmission riders. AEP rows whose delivery was imputed (2003–04, 2006–07) carry grade C.

**Checks.**
- *Oncor third-party transmission versus its 10-K:* the 10-K's "wholesale transmission service expense" (fees paid to other providers) versus the model (Oncor's share × (ERCOT TCOS − Oncor's own TCOS), time-weighted) is within −0.6% to −5.8% for 2010–2016; the largest gap is 2013 (−5.8%), when CREZ updates came in several steps.
- *CenterPoint year-over-year change in "transmission costs billed by transmission providers"* (10-K, $M) versus the model: 2014 +168 / +172; 2015 +47 / +47; 2018 −32 / −36; 2019 +57 / +57; 2009 +18 / +30; 2010 +28 / +22; 2016 +55 / +72; 2017 +56 / +66.
- *Billed residential transmission, 2005–2010* (base-rate transmission charge plus Rider TCRF, from the PUCT summaries) versus cost: mean ratio Oncor 1.03 (0.94–1.17), AEP Central 1.00, AEP North 0.90, TNMP 0.82 (TNMP's base transmission charge stayed at its 2002 level until 2009). After 2010 the summary's columns stop lining up, so the check stops there.
- Transmission is 14–42% of delivery in every year; only CenterPoint 2003 and AEP North 2003 are below 15% (14.4%) and are flagged in `notes`. ERCOT TCOS was $0.90B in 2002, $2.0B in 2013, $3.6B in 2019 and $5.4B in 2025.

**Business transmission.** Business transmission for 2002–2025 is each wires company's wholesale transmission cost × (1 − residential allocation factor) ÷ (all-class kWh − residential kWh). Class allocators sum to one, so the business share is the complement of the residential factor. This lumps lighting and other small classes in with commercial and industrial and does not distinguish secondary, primary and transmission-voltage customers.

## 6. Regulated era, 1992–2001

Output: `data/utility_level/regulated_residential_functional_split_1990_2001.csv` (TU Electric, Houston Lighting & Power, Central Power & Light, West Texas Utilities, TNMP), with every Form 1 component of the revenue requirement in `data/source_extracts/ferc1_functional_revenue_requirement_1992_2001.csv`. Every transmission and distribution row is graded C: it is a cost-of-service estimate, not a billed amount.

- `bundled_cents` is EIA-861 residential revenue ÷ MWh for the Texas operations, matched by EIA utility ID. The 1999–2001 retail-pilot "Part C" rows are dropped. `transition_cents` and `storm_cents` are zero.
- **1990–91:** no functional split; only the bundled price.
- **1994–2001:** FERC Form 1 via PUDL. **1992–93:** EIA's *Financial Statistics of Major U.S. Investor-Owned Electric Utilities* (DOE/EIA-0437), which reprints each utility's Form 1. Tables 37 (income), 41 (O&M by function), 42 (plant by function) and 43 (energy account) were read by hand from page images; values and page numbers are in `data/source_extracts/eia0437_texas_1992_1993.csv`. Those tables have no depreciation or accumulated depreciation by function, so for 1992–93 each utility's 1994 Form 1 ratios (depreciation ÷ plant and accumulated depreciation ÷ plant, by function) are applied, scaled to the reported totals. Applying the 1994 ratios to Form 1 years and comparing with actuals (`data/validation/depreciation_shortcut_backtest.csv`): in 1995–96, the years nearest 1994, the error is −2.8% to +2.4% for transmission and −2.1% to +3.0% for distribution. It grows in 1998–2000 (up to +36% for HL&P distribution) when rate-freeze accounting changed depreciation; that does not affect 1992–93.

**Functional revenue requirement:**
- *O&M:* transmission O&M excludes account 565 (transmission by others); distribution O&M plus accounts 901–902 (supervision, meter reading); administrative and general spread by O&M excluding fuel and purchased power.
- *Depreciation by function:* p.336, with general and intangible plant spread by plant.
- *Return:* realized return (net utility operating income ÷ net electric plant) × net functional plant (p.204 less p.219).
- *Taxes:* taxes other than income plus income taxes, by gross-plant share.

**Retail transmission cost:**
- *1994–96:* (own transmission revenue requirement + account 565) × retail share of MWh (sales for resale were bundled then).
- *1997–2001:* own transmission revenue requirement × the utility's ERCOT 4CP share + account 565 (under ERCOT wholesale pricing, other distribution utilities paid the rest of its TCOS). The 4CP share is from the 2002 matrix. ERCOT wholesale transmission pricing began in 1997; the 1997–99 mix of postage-stamp and impedance pricing was not verified from orders.

**Class shares:**
- *Transmission:* the unbundled cost of service residential 4CP allocators (Dockets 22349–22355, in Section 5).
- *Distribution:* the 2002 residential share of distribution revenue, (residential delivery − residential transmission) ÷ (all-class delivery − wholesale transmission cost): TU 0.467, HL&P 0.541, CPL 0.512, WTU 0.514, TNMP 0.447. Class allocations were not extracted from the UCOS orders themselves.
- TNMP's Form 1 covers Texas and New Mexico, so its costs are scaled by Texas's share of retail MWh.
- Business shares are one minus the residential shares, applied to non-residential MWh (retail MWh × Texas share − residential MWh).

**Checks** (`data/validation/regulated_split_seam_checks.csv`):
- Transmission + distribution is 15–27% of the bundled price for TU, HL&P, CPL and TNMP, and 31–44% for WTU, a small, rural, distribution-heavy system.
- *2001→2002 seam* (2002 residential delivery minus 2001 transmission + distribution): every jump is under 0.5¢ (TU/Oncor +0.49¢; WTU/North +0.25¢; HL&P/CenterPoint +0.19¢; TNMP +0.08¢; CPL/Central +0.04¢). Part of the TU jump is real: ERCOT TCOS rose from $705M (2001 matrix, Docket 24418) to $901M (2002), when the UCOS cases reset TU's and Reliant's TCOS.
- *2001 matrix check:* the 2002 4CP share × 2001 ERCOT TCOS ($705.4M) gives 0.27–0.43¢ of transmission. The functional estimate is higher for TU, HL&P, CPL and WTU (0.44–0.76¢) and lower for TNMP; realized return and taxes on transmission plant run above the TCOS the matrix allowed, one reason these rows are C.
- *Rate freeze (1999–2001) and SB 7:* excess earnings went to accelerated depreciation of generation, which lands in the generation + retail remainder, not in transmission and distribution. Realized return still moves year to year (TU distribution dips in 1993 when Comanche Peak 2 entered rate base and in 1998; HL&P dips in 1998–2000); the realized return is in `notes`.

**Gaps.** 1990–91 functional split (the 1990 and 1991 editions of EIA's report were not obtained); HL&P 1997 (PUDL has only a partial filing without plant schedules; statewide series use the 1996/1998 average); class allocations for distribution from the UCOS orders (would raise 2000–01 rows to B); ERCOT transmission matrices for 1997–2000 (the earliest found is 2001, Docket 24418).

## 7. Statewide series

`code/data_build/build_statewide_series.py` builds the five statewide series in `data/statewide_series/` from the utility-level files and the EIA group totals.

- **Competitive era, residential:** wires components are kWh-weighted across Oncor, CenterPoint, merged AEP Texas and TNMP using residential MWh. Retail price = competitive providers' residential revenue per kWh (EIA-861). Energy + retail = retail − wires total. Transmission is weighted the same way from the transmission split.
- **Competitive era, business and all classes:** same, using all-class and non-residential MWh. For 2003–04 AEP's merged all-class delivery is blank, so the statewide all-class and business series impute it as residential delivery × the mean all-class/residential delivery ratio of 2002 and 2005 (flagged `aep_delivery_imputed`).
- **Regulated era:** residential cents per kWh are weighted by residential MWh across the five utilities; business uses the functional revenue requirement × (1 − residential share) over non-residential MWh. HL&P 1997 uses the 1996/1998 average cents per kWh (and the mean of those years' non-residential MWh).
- **Public power:** ERCOT-area municipal utilities and co-ops, EIA-861 revenue ÷ MWh; short-form filers are excluded.
- **Wholesale:** ERCOT market monitor all-in cost per MWh of load (`data/reference/ercot_wholesale_2002_2025.csv`).

## 8. Source anomalies found along the way

- **PUCT rate summary misprints AEP North's CTC by a factor of 10.** The July 2007 Summary of Non-Bypassable Charges prints $0.008170 per kWh. AEP North's 2008 earnings report shows CTC revenue divided by residential MWh of $0.000817 in every month of Jan–May 2008, ending in June. The billed rate ($0.000817, about +0.08¢) is used from July 2007 to May 2008.
- **AEP North's 2006 interim credit** (−$0.019056 per kWh as printed, Sept 2006–Feb 2007; no EMR exists for the period) could not be checked against AEP's reports but is confirmed by the San Angelo *Standard-Times* (Oct 2, 2006): about $19 a month for a 1,000 kWh customer, described by AEP as a "retail clawback".
- **AEP Central's 2005 earnings report** is the only year in which the bond Transition Charge Rider is "Included in WP1", so it is removed from base revenue; the SBF is "Not Included".
- **AEP North's "revised" 2011 earnings report** attaches the 2010 workpapers by mistake; the original filing is used.
- **AEP Texas's 2019 earnings report** labels the transmission cost recovery rider "Not Included", but it is already in WP1 (Section 3.2).
- **TNMP's Aug 2008 PUCT summary** prints the CTC as 0.000310 with the whole TNMP column shifted one decimal place; that version was skipped. **Storm ADFIT credit, Sept 2012:** printed as +0.002960 without the surrounding parentheses; kept as printed.
- **AEP Central negative CTC:** authorized in Oct 2006 but first appears in the Feb 2007 summary. The summaries lag (TC2 was billed from Oct 2006 but printed only from Feb 2007), so it may have started earlier. Not imputed, because no source gives its start date.
- **January 2002** in AEP's earnings reports is "pilot data only" (sheet XI.1a, Note 3), so 2002 revenue and MWh cover roughly Feb–Dec; delivery cents per kWh uses the same months.

## 9. Series breaks

| Date | Break |
|---|---|
| 1997 | ERCOT wholesale transmission pricing begins; the regulated-era method changes here. |
| 2002 | Unbundling and the start of retail choice; competitive-era series begin. TCRF riders begin for all five TDUs (Reliant Feb 2002, Docket 25487; CPL and WTU July 2002, Dockets 26278 and 26279; Oncor Sept 2002, Docket 26353; TNMP Aug 2002, Docket 26397). |
| 2006→2007 | TNMP: source changes from Form 1 to the 10-K, and the CTC began. |
| 2011 (TNMP Mar, Oncor July), Sept 2020 (CenterPoint) | Transmission leaves base rates and moves wholly into TCRF. Visible in billed rates, not in the cost-based split. |
| 2012, 2020 | TNMP source changes (10-K → EIA Operational Data → EIA `Delivery_Companies`). |
| 2017–18 | Oncor absorbs Sharyland's territory; AEP's Central and North merge into AEP Texas Inc. (divisions reported separately through 2018). |
| 2018–19 | Tax Cuts and Jobs Act refunds and rate reductions lower delivery cents per kWh (Oncor 3.89→3.70¢). |
