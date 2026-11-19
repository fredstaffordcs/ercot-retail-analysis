# Wires-company charges by customer class, ERCOT competitive area, 2002–2025

This dataset splits the wires-company (transmission and distribution utility, TDU) charges for Oncor, CenterPoint, AEP Texas (Central, North and merged) and TNMP into individual customer classes. The components are the same as in the residential and all-class files:

- delivery, split into transmission and distribution + other;
- transition charges, securitized and other;
- storm charges;
- the System Benefit Fund (SBF).

Classes are given in two layers:

- **Layer A, tariff classes.** These are the classes the wires companies bill by. They are defined by voltage and demand, and they are consistent from 2002 to 2025.
- **Layer B, EIA customer types.** These are residential, commercial, industrial and transportation, as used in EIA-861. Retail prices are reported in these types.

**Reconciliation rule.** For every utility, year and component, the classes add back to the published all-class total, and the residential class equals the published residential file exactly. The non-residential amount (all-class minus residential) is spread over the non-residential classes with weights read from filed sources. Where a source's own non-residential total differs from the published one, the difference is reported in `class_checks.csv` and not absorbed silently.

Units: nominal dollars (thousands, `_kusd`), MWh, and cents per kWh (`_cents`), by calendar year.

The published totals are those in [`data/utility_level/`](../data/utility_level): `wires_residential_components_2002_2025.csv` and `wires_all_class_components_2002_2025.csv`.

## Files

In [`data/by_class/`](../data/by_class):

| File | Content |
|---|---|
| `wires_components_by_tariff_class_2002_2025.csv` | Layer A. One row per utility, year and tariff class. Includes MWh, customers, every component in $ thousand and ¢/kWh, the transmission allocation factor, a grade per component, imputation fields and flags. |
| `wires_components_by_eia_class_2002_2025.csv` | Layer B, same structure. `measured_or_mapped` and `basis` say how each row was obtained. Commercial rows for 2020–25 carry a large-load diagnostic (`diag_*`; see Layer B). |
| `wires_components_by_class_line_items.csv` | Every amount behind the two files, with its grade, method and source. |
| `tariff_class_crosswalk.csv` | How every source class maps to a class code: Form 1 p.304 rate schedules, earnings-report columns, Rider TCRF sub-classes, financing-order classes and TNMP's legacy CTC classes. |
| `statewide_delivery_by_class_2002_2025.csv` | kWh-weighted averages across Oncor, CenterPoint, merged AEP Texas and TNMP, per layer, class and year. `n_util` and `missing` list the utilities included. A blank component in a utility's class row means no such charge existed in that class and year, and counts as zero in the average. A utility with no class row for that year (or no MWh) is missing: it is left out and named in `missing`. |

In [`data/source_extracts/`](../data/source_extracts):

| File | Content |
|---|---|
| `tcrf_class_allocation_factors.csv` | Rider TCRF class allocation factors for every allocation regime, with sub-classes and sources. |
| `bond_charges_by_class_trueup_filings.csv` | The class detail behind the bond allocations: CenterPoint forecast billing determinants, charges and revenue by charge class from every true-up filing read; Oncor transition charges billed by class each month, and the small/large split of secondary and primary. |
| `aep_central_transition_trueup_collections.csv` | AEP Texas Central TF1 and TC-2 collections by legacy TC class, from the true-up workpapers (see Bond charges). |

In [`data/validation/`](../data/validation): `class_checks.csv`, every check (see Checks).

## Classes

**Layer A.** All classes outside residential and lighting are non-residential (business).

| Code | Tariff classes |
|---|---|
| `res` | Residential Service |
| `sec_small` | Secondary Service ≤10 kW (CenterPoint: ≤10 kVA; **TNMP: <5 kW**) |
| `sec_large` | Secondary Service >10 kW (TNMP: ≥5 kW), with NCP- and 4CP-billed, or IDR and non-IDR, combined |
| `pri` | Primary Service ≤10 kW and >10 kW, distribution line and substation |
| `trans` | Transmission Service (transmission-voltage customers) |
| `light` | Street, area and miscellaneous lighting |

Every source class mapped to one of these codes, so the `other` class is not used. Sub-classes (NCP/4CP, IDR/non-IDR, substation) are kept in `tcrf_class_allocation_factors.csv` and in the crosswalk. Form 1 p.304 does not split Secondary >10 kW by billing basis. TNMP's tariff boundary between small and large secondary is 5 kW rather than 10 kW.

**Layer B:**
- `residential`;
- `commercial`, which includes street and highway lighting, as EIA-861 has since 2003;
- `industrial`;
- `transportation` (rail transit; EIA-861 only, 2020–25; Oncor and CenterPoint each report one customer).

The commercial/industrial line is drawn by each reporter. It is not a tariff concept: see Definitional breaks.

## Sources and methods, Layer A

### Volumes and class revenue

| Utility | Years | Source |
|---|---|---|
| Oncor, CenterPoint | 2002–2025 | FERC Form 1 p.304, sales of electricity by rate schedule (PUDL). Revenue, MWh and customers by rate schedule. Unbilled revenue and MWh are spread over each section's schedules pro rata. The p.304 total equals p.300 sales to ultimate consumers in every year except CenterPoint 2002, where p.300 excludes unbilled revenue, so p.304 is used for shares only. |
| TNMP | 2002–2006 | Form 1 p.304, Texas Unbundled Delivery schedules 6.1.1.1–6.1.1.6. New Mexico and bundled schedules are excluded. |
| TNMP | 2007, 2011–18, 2020–25 | PUCT earnings monitoring reports (16 TAC §25.73), schedules X.1a/XI.1a (revenue), X.2a/XI.2a (sales) and X.4/XI.4 (delivery points). From 2020 the reports carry rider workpapers by class: TCRF, EECRF, rate-case surcharge, CTC and hurricane cost recovery. Spreadsheet filings: Projects 35466 item 21, 40327 item 9, 41327 item 7, 45636 item 10, 46910 item 7, 48158 item 10, 49355 item 7, 52952 item 2, 57406 item 2, 59188 item 9. PDF-only filings, read from the text layer: 42290 item 7 (2013), 44550 item 15 (2014), 51718 item 6 (2020), 54451 item 2 (2022), 55977 item 3 (2023). |
| TNMP | 2019 | Earnings report filed in Project 50655, item 3, under the title "Electric Investor-Owned Utilities" (spreadsheet), with rider workpapers by class. |
| AEP Texas Central, North; merged AEP Texas | Central 2002, 2005, 2008–18; North 2002–05, 2008–18; merged 2019–25 | AEP earnings monitoring reports, the same schedules, plus rider workpapers by class: transition charges, CTC, excess mitigation credits, SBF, storm and ADFIT, nuclear decommissioning, and so on. Class delivery = base revenue (WP1) − non-delivery riders included in it + nuclear decommissioning where billed separately, the same definition as the residential and all-class files. Merged AEP 2002–18 is the sum of the two divisions. |
| AEP, scanned reports | 2005 (Project 32534, items 18 and 19), 2011 (Project 40327, items 17 and 18) | Read by OCR. A page is accepted only if its six class totals add to the Total column (within $3 or 3 MWh), or if every column's twelve monthly lines add to its total; where two OCR passes both verify, they must agree. Accepted: base revenue, billed MWh and delivery points in all four division-years, and most rider workpapers. AEP Central 2011's WP1 page did not verify, so its class delivery weights use schedule XI.1a base revenue, which leaves out some included riders (chiefly the metering fee); grade B. |
| AEP Texas Central | 2007 (imputed) | No earnings report. AEP's TCRF petition workbooks give each tariff class's annual billing determinants (kWh for residential and Secondary ≤10 kW; average 4CP kW or summed monthly maximum kW for the rest; 2007 determinants in PUCT Control No. 35226). Class revenue = class revenue per billing determinant in the 2008 report × 2007 billing determinants; class MWh = 2008 MWh × billing-determinant growth; lighting scales with the other classes. Base rates were unchanged from March 2006 to July 2008, which covers all of 2007 and seven months of 2008. Back-tested on pairs of measured years under the same base rates (Central 2008↔2009, North 2008↔2009 and 2002→2003/04): class shares of non-residential delivery within 0.3–2 points and of MWh within 2 points. Across a rate change (Central 2002→2008) the error is 6 points. Labelled imputation, certainty 55; the error band is the difference from using the 2002 report's unit revenues (a different base-rate regime, so a generous band). Not applied to Central 2003–04: interval-metered and other demand customers are billed on different kW measures (average 4CP vs summed monthly maximum), customers moved between them after 2002, and the published all-class delivery for 2003 is blank. |

**Scaling.** Non-residential class MWh are scaled so they sum to published all-class MWh minus residential MWh. Before scaling, the sources are within ±1% of the published figures in most years, with these exceptions:
- AEP 2002: −1% to −4%, because January 2002 is pilot data in AEP's reports.
- Merged AEP 2025: −2%.
- TNMP 2017 (+2%), 2023 (+4%) and 2025 (+3%).

### Delivery

Non-residential delivery is the published all-class delivery minus published residential delivery. It is spread by class revenue from the source:
- **Form 1 (Oncor, CenterPoint, TNMP 2002–06):** retail delivery revenue.
- **AEP reports:** delivery as defined above.
- **TNMP 2020–25:** base revenue plus delivery riders.
- **TNMP 2007 and 2011–18:** these reports have base revenue only. Transmission has been recovered entirely through Rider TCRF since March 2011, so each class's transmission cost (below) is added to its base revenue before spreading.

### Transmission

```
class transmission = TDU wholesale transmission cost × Rider TCRF class allocation factor
dist_other         = delivery − transmission
```

The TDU wholesale transmission cost is the time-weighted cost in the published residential transmission split. Class factors are the full class allocation tables of Rider TCRF, read from the semi-annual TCRF petitions (16 TAC §25.193), day-weighted within change years. Regime start dates are those of the published residential split. The residential factor reproduces the published one in every year, within 0.00013.

| Utility | Regimes (start) and source of the class table |
|---|---|
| Oncor | 2002: Docket 22350, petition 27365 Att. B. Sept 17, 2009: Docket 35717, petition 38460. July 1, 2011: Docket 38929, petitions 39456/40451/41002. Nov 27, 2017: Docket 46957, petition 49593 Att. A. Sept 1, 2023: Docket 53601, petition 55075. |
| CenterPoint | 2002: Docket 22355, petition 29226. Oct 2006: Docket 32093, petition 33750. Sept 2011: Docket 38339, petition 39953. Sept 2020: Docket 49421, petition 50890. Sept 2025: Docket 56211, petition 58178. |
| AEP Texas Central | 2002: Docket 22352, petition 26278 ("AEP TCRF Proof"). Oct 2005: Docket 28840, petition 31368 Att. D (printed to 0.01%, grade B). July 2008: Docket 33309, petition 45402. |
| AEP Texas North | 2002: Docket 22354, petition 26278. June 2007: Docket 33310, petition 45403. |
| AEP Texas (merged) | 2020 to Feb 2021: the division tables, weighted so residential = 0.4708 as in the published split. Mar 2021: Docket 49494, petition 51554. Sept 2022: Docket 53236 allocator, petition 53653. Mar 2025: petition 57356. |
| TNMP | 2002: Docket 22349, petition 29295. Sept 2009: Docket 36025, petition 37233. Mar 2011: Docket 38480, petition 39457. Jan 1, 2019: Docket 48401, petitions 48932/49585. Sept 2020: petition 51559 (first update using the Docket 48401 allocators). |

Lighting receives no transmission allocation. The tables sum to 1 within 0.0001 as printed and are normalized.

### Bond charges (transition_securitized) and storm bonds

| Case | Method | Grade |
|---|---|---|
| AEP report years | Transition-charge and system-restoration rider workpapers, billed by class. | A |
| CenterPoint (TC1, TC2, TC3, TC5, SRC1, SRC2) | True-up filings: forecast revenue by charge class (billing determinants × final charge), day-weighted over the year by the period each filing's charges were in effect, mapped to tariff classes (below). | B (C before a series' first filing found) |
| Oncor (Series 2003-1 and 2004-1) | True-up filings: transition charges billed by class in the Monthly Servicer's Certificates, using only months whose class amounts add to the certificate total. Secondary and primary are split into non-demand (small) and demand (large) by the estimated-month table of the nearest filing. | B (C for 2016, which uses 2015 shares) |
| AEP Texas Central 2002 (TF1) and 2007 (TF1 and TC-2), no workpaper | Non-residential class shares of the transition charges billed in AEP Texas Central's 2008 report (labelled imputation, certainty 60). The error band is the difference from using the 2005 billed shares instead. | C |

**CenterPoint.** Each annual or interim true-up compliance filing carries a workbook (or, from 2017 for TC2 and TC5, a PDF with a text layer) with the forecast billing determinants by charge class, grouped by voltage, and the final charge per unit. Sixty filings were read, 2003–2026. Charge classes map to tariff classes as follows:
- Residential → `res`; non-metered lighting → `light`;
- MGS-D ≤10 kVA (TC1) → `sec_small`; MGS-D >10 kVA (TC1, billed per kVA) → `sec_large`;
- MGS-D (TC2, TC3, TC5, billed per kWh, all sizes) → `sec_small` for the kWh of the Secondary ≤10 kVA tariff class, the rest `sec_large`;
- LGS-D → `pri` for the kWh of the Primary tariff class not served under ISS-D or SES-D, the rest `sec_large`;
- ISS-D, SES-D → `pri`;
- every transmission-voltage charge class (MGS-T, LGS-T, LOS-A, LOS-B, SCP, the interruptible and standby classes) → `trans`;
- SRC: Secondary ≤10, Secondary >10, Primary and Lighting → the same tariff classes. SRC is not billed at transmission voltage.

The filings place LOS-A (large overhead service) at transmission voltage. The earlier financing-order mapping had assumed primary.

**Oncor.** The certificates give each class's billed transition charges each month: residential, general service secondary, general service primary, high voltage, lighting, instantaneous and noticed interruptible. Of 198 bond-months found (Sept 2003–May 2015), 124 add exactly to the certificate total; the rest have digit errors in the text layer and are not used. Interruptible classes are counted as transmission voltage. The non-demand share of secondary charges is 0.5%–3% through 2009 and 9%–17% from 2010; the non-demand share of primary is under 5%.

**Comparison with the financing-order mapping** (previous method; `bond_alloc_trueup_vs_legacy_mapping` in the checks). On average across years, the true-up record moves about 8 points of CenterPoint's non-residential bond charges from `sec_large` (−6) and `pri` (−2 to −4) to `trans` (+8). For Oncor it moves about 3 points from `sec_large` to `sec_small`.

**AEP.** The financing-order allocations of the AEP series use pre-2002 classes. Tested against billed amounts (AEP Central 2008–18), the legacy mapping puts far too much on Secondary ≤10 kW and too little on lighting and Secondary >10 kW (see Checks). Billed workpapers are used wherever they exist.

AEP Central's own true-up workpapers (TF1 under the Docket 21528 financing order, Control Nos. 26870, 30360, 31960, 34961, 36326 and 37604 for 2002, 2004, 2005, 2007, 2008 and 2009; TC-2, Control No. 34617 for November 2006–June 2007) give the amounts collected by legacy TC class each month (`aep_central_transition_trueup_collections.csv`). They cannot split the charges by tariff class directly: legacy Commercial Energy is about 40% of non-residential collections, while Secondary ≤10 kW receives about 6% in every billed year. They are used instead to test whether one year's tariff-class shares can stand in for another's. Non-residential collections by legacy group:

| Series, year | Commercial Energy + Muni | Commercial Demand | Large Industrial + Standby |
|---|---|---|---|
| TF1 2002 | 42% | 44% | 15% |
| TF1 2004 | 37% | 51% | 12% |
| TF1 2005 | 40% | 46% | 14% |
| TF1 2007 | 45% | 41% | 14% |
| TF1 2008 | 45% | 44% | 11% |
| TF1 2009 | 43% | 46% | 11% |
| TC-2 Nov 2006–Jun 2007 | 36% | 53% | 11% |

The mix moves by up to 7 points from year to year, and TC-2 in its first year differs from TF1 in 2008 by up to 9 points. In tariff classes, AEP's billed transition charges (2005, 2008–10) put 9–12% of non-residential at transmission voltage and 5–6% on Secondary ≤10 kW. These ranges are what the error bands on the 2002 and 2007 imputations are meant to cover. TC-2 uses the same eight legacy classes as TF1, with allocation factors within 3 points of TF1's, so the 2008 billed shares (which cover both series) are applied to TC-2 in 2007 as well. The financing-order mapping used before put 26% of 2007 non-residential bond charges on Secondary ≤10 kW (10.9¢/kWh); with the 2008 shares the figure is 2.4¢/kWh, against 2.1–2.5¢ in the billed years 2008–10.

### Other transition charges, storm riders and SBF

| Item | Method | Grade |
|---|---|---|
| AEP excess mitigation credits, CTC and true-up, SBF, ADFIT | Rider workpapers by class (report years). AEP Central CTC in 2007: non-residential class shares billed in 2008 (labelled imputation, certainty 55; error band = difference from the 2009 billed shares). Otherwise the related financing-order allocation. | A / C |
| Oncor and CenterPoint excess mitigation credits, CenterPoint CTC, Oncor bond refund, CenterPoint storm ADFIT credits | Allocated like the bond charges they offset or accompany, from the true-up record (Oncor billed shares; CenterPoint TC1, TC2 and SRC forecast shares). | C |
| TNMP CTC (2007–20) | Billed by class in 2019 and 2020 (CTC workpapers, Project 50655 item 3; Project 51718 item 6). Other years: 2020 class rates per MWh × class MWh. The CTC was billed in pre-2002 classes, per kW for larger customers, and no class billing units are published for other years. Labelled imputation (certainty 55); the error band is the difference from spreading by class revenue. | A (2019–20) / C |
| TNMP storm (hurricane) rider | Billed by class 2019–21. Otherwise distribution-class MWh. | A / C |
| SBF (to Aug 2013) | Class MWh × the class's SBF rate relative to residential: 1.0 secondary, 0.978 primary, 0.966 transmission (Oncor column, PUCT Summary of Non-Bypassable Charges, Mar 1, 2010). AEP report years: workpapers. | B / A |
| Retail clawback credits | Non-residential remainder spread by MWh. | C |

### Grades and imputations

- **A:** class split read from a filed source as used.
- **B:** computed by a method checked against filed values, or a source scaled more than 5% to the published total.
- **C:** an allocation by legacy class mapping or by MWh.

Residential rows are `published`. `min_certainty` is the worst grade among a row's components. Imputed cells have `*_status = imputed`, a certainty score (0–100), an error band in ¢/kWh and a method.

`billed_kw` is blank throughout. Neither Form 1 p.304 nor the earnings reports give annual billed kW by class. The TCRF petitions give six-month billing determinants that do not cover calendar years.

## Sources and methods, Layer B

| Basis | Utility-years | Method |
|---|---|---|
| `measured_eia` | All utilities, 2020–25 | EIA-861 `Delivery_Companies`: MWh, customers and revenue by class. Non-residential MWh are scaled to the published total; EIA is within 0.3% of it. Delivery is spread by EIA class revenue. AEP's EIA revenue includes bond charges, so the bond and storm charges carried from Layer A are subtracted first. Other components are carried from Layer A through a class-to-type matrix. Transportation gets the non-residential average per MWh for non-delivery components. |
| `measured_form1_p304` | CenterPoint 2002–19 | Form 1 p.304 sections 442-1 Commercial, 442-2 Industrial and 444 Municipal (lighting, counted as commercial). The same rate schedules (SVL, PVS) appear in both sections, so the commercial/industrial split crosses tariff classes. Components are carried from Layer A by each class's MWh share (revenue share for delivery) in each section; `dist_other` is delivery minus transmission and `total` is the sum of the components, so each row adds up. |
| `measured_form1_p300` | Oncor 2009–19 | Form 1 p.300: small or commercial = all secondary; large or industrial = primary, substation and transmission. Lighting is counted as commercial. |
| `measured_10k` | TNMP 2007–19 | PNM Resources 10-K "Comparative Operating Statistics": TNMP MWh and revenue by Residential, Commercial, Industrial and Other. Commercial includes Other MWh (about 0.1 TWh: lighting and other retail). Other revenue is transmission and miscellaneous revenue, not a class, and is left out of the delivery weights, which are therefore 4–6% below published non-residential delivery. TNMP's revenue includes its CTC and storm riders; the Layer A amounts of those are subtracted from the weights. MWh equal the published totals. Figures before 2007 include TNMP's New Mexico operations (sold in 2007) and are not used. |
| `measured_10k_revenue` | AEP Texas Central 2004 and 2006, AEP Texas North 2006, merged 2004 and 2006 (years with no tariff-class source) | AEP 10-K "Classes of Service": TCC and TNC retail revenue by Residential, Commercial, Industrial and Other (FY2004, accession 0001015402-05-001007; FY2006, 0000004904-07-000041). The 10-K states that TCC and TNC delivery revenue from retail electric providers is reported in these classes, so the shares include bond charges. Other retail (public lighting, municipal) is counted as commercial. Every non-residential component is split by the commercial/industrial revenue shares. No class MWh are published, so cents per kWh are blank. Later 10-Ks drop the two companies from the table. |
| `mapped` | Oncor 2002–08; AEP 2002–19; TNMP 2002–06 | Approximation from Layer A, not a measurement: commercial = Secondary + lighting; industrial = Primary + Transmission voltage. |

**Test of the mapping against EIA, 2020–25** (`layerA_mapped_to_eia_vs_eia` in the checks):

| Utility | Largest error in MWh share | Largest error in ¢/kWh | Reading |
|---|---|---|---|
| Oncor | 0.2 points | 0.02¢ | Oncor reports EIA classes by voltage, so the mapping reproduces EIA. |
| CenterPoint | 9 points | 0.17¢ commercial, 0.27¢ industrial | CenterPoint reports by business type across voltages. |
| AEP Texas | 7 points (2020–21) rising to 28 points (2025) | up to 2¢ commercial | Large new loads served at primary or transmission voltage are reported as commercial by EIA. |
| TNMP | 14 points (2021) rising to 47 points (2025) | up to 3.8¢ commercial | Same pattern as AEP. |

So for AEP, mapped commercial and industrial before 2020 are approximations. Two earlier tests are possible:
- **AEP 2005:** the AEP 10-K gives commercial (including other retail) as 83% of non-residential revenue, against 79% (Central) to 87% (North) from the mapping.
- **TNMP 2007–19:** the mapping's commercial share of non-residential MWh is below the 10-K's by 4 points in 2007, 5 in 2011, 9 in 2016 and 14 in 2019. TNMP's secondary-voltage load was flat over the period (about 2.1–2.4 TWh) while primary and transmission-voltage load more than doubled, and the 10-K counts a growing part of that higher-voltage load as commercial: about 0.16 TWh in 2007, 0.5 TWh in 2016 and 1.1 TWh in 2019. What those customers are is not shown; the timing fits oil-and-gas growth in TNMP's West Texas territory as well as other large loads, and reclassification by the reporter cannot be ruled out.

**Large-load diagnostic (commercial rows, 2020–25).** `diag_commercial_mwh_above_secondary` = EIA commercial MWh − Layer A Secondary and lighting MWh; `diag_share_of_commercial_mwh` is that as a share of EIA commercial MWh. A positive value is load that EIA counts as commercial but the utility serves at primary or transmission voltage. EIA-861's instructions (2024 form) list "crypto mining and data centers" in the commercial sector. The indicator is not a count of data centers: large institutions and offices on primary service are included. A negative value means the reporter counts some secondary load as industrial.

| Utility | 2020 | 2025 |
|---|---|---|
| AEP Texas (merged) | 13% | 47% |
| TNMP | 33% | 75% |
| Oncor | 0% | 0% |
| CenterPoint | −23% | −17% |

The indicator accounts for the AEP and TNMP mapping errors above: load served above secondary voltage that the reporter counts as commercial. At TNMP it was already growing before 2020 (see the 10-K test); its composition is not identified by these sources.

## Checks (`data/validation/class_checks.csv`)

**Class sums equal the published totals (bookkeeping check).** In all 118 utility-years with class data, the classes add to the published all-class total for delivery, every other component present that year, and MWh: 438 checks, of which 437 are within $500 or 1 MWh (largest gap $1.10). The exception is merged AEP Texas 2002 delivery, $174 thousand (0.04%) short of the published total (see the AEP 2002 note below). The sums hold by construction, because the non-residential classes divide the published non-residential amount (all-class minus residential) by source weights. The check confirms that no class is dropped or double-counted, that the merged AEP rows equal Central plus North, and that imputed cells keep the totals. It does not test the split between classes. The independent tests are the source-vs-published comparisons below, made before scaling, and the 10-K and true-up comparisons above. The residential class equals the published residential file, including ¢/kWh, in every year. For AEP 2002 the residential dollars are put on a full-year basis (published ¢/kWh × full-year MWh) before the subtraction. The published residential dollars cover February–December only (January is pilot data in AEP's earnings report), while the all-class file scales the same report to the full year (`residential_kusd_full_year_basis` in the checks). The published merged ¢/kWh for 2002 is weighted by February–December MWh, so merged residential dollars (¢/kWh × full-year MWh) are $174 thousand below the sum of the two divisions', and the merged class rows, which are the sum of the division rows plus the merged residential row, fall short by that amount. Layer B non-residential delivery for AEP 2002 equals all-class minus full-year residential rather than minus the published residential dollars; in every other utility-year it equals all-class minus the published residential dollars to within $1 thousand.

**The statewide file adds up and reproduces the published statewide series.** These checks stop the build if any fails (`statewide_*` in the checks file, 1,124 rows):
- In every row of both layers, delivery + transition_securitized + transition_other + storm + sbf equals `total_cents` within 0.001¢, and `transmission_cents` + `dist_other_cents` equals `delivery_cents` within 0.001¢.
- The tariff `res` row and the EIA `residential` row equal `competitive_residential_components_2002_2025.csv` in every component and year within 0.00055¢. The published series is rounded to 3 decimals (0.0005¢) and averages utility ¢/kWh that are rounded to 4 decimals (0.00005¢).
- The non-residential classes combined (tariff layer: `sec_small`, `sec_large`, `pri`, `trans`, `light`; EIA layer: `commercial`, `industrial`, `transportation`), weighted by MWh, equal `competitive_business_components_2002_2025.csv` in every component within 0.001¢. This is compared in years where every utility has class rows (2002, 2005 and 2011–2025 in the tariff layer; transportation exists only for Oncor and CenterPoint, 2020–25).
- Layer B rows add up in the same way (components to total, transmission + distribution to delivery) wherever transmission is given. AEP division rows for 2020–25 have delivery but no transmission or distribution split; those blanks are missing data, not zero, and the statewide file does not use the division rows.

**Residential transmission matches the published split.** The residential transmission factor and dollars match within 0.00013 and 0.02%.

**TCRF factors sum to 1** for every regime: within 0.0001 as printed, exactly after normalization.

**Source vs published non-residential delivery, before scaling:**

| Utility | Gap |
|---|---|
| Oncor | 0.0% |
| CenterPoint | −1.3% to +4.5%. The +4.5% is 2006–07, when published delivery removes the CTC from Form 1. |
| AEP | 0.0% in spreadsheet years, except 2002 (−6% to −11%, January pilot data); scanned years 2005 and 2011: −11% to +4% (2011 Central uses schedule XI.1a, see above) |
| TNMP | −8.7% to +0.1% |

**Billed by class (AEP and TNMP workpapers) vs published non-residential amounts:**
- Transition bonds and most SBF and CTC: 0.0%.
- TNMP storm rider 2019–21 and CTC 2019–20: the published all-class amounts are now the billed totals. The non-residential gaps that remain (storm −16% in 2019, +29% in 2021; CTC −8% in 2020) come from the published residential amounts, which are PUCT rate × residential kWh rather than billed.
- AEP North SBF 2016: −27% of a very small amount.

**Bond residential shares.** The published residential share of each Oncor and CenterPoint bond series now comes from the same true-up record used here; the check shows agreement to rounding.

**AEP bond financing-order allocation (legacy classes mapped) vs billed by class, 2008–25:**

| Class | Mapping error |
|---|---|
| Secondary ≤10 kW | +206% to +550% |
| Secondary >10 kW | −21% to −52% |
| Lighting | −95% |

This is why billed workpapers are used wherever they exist.

**Flags.**
- 91 class-years have transmission above 60% of delivery, all in the transmission-voltage class. These customers take almost no distribution service, so their delivery charge is mostly the transmission allocation.
- 7 of those years also have a negative `dist_other`: CenterPoint 2006 and 2023, AEP North 2016, merged AEP 2024, and TNMP 2019, 2021 and 2024. In those years the allocated transmission cost exceeds what the class was billed: TCRF recovers costs with a lag, and before 2011 part of transmission was in base rates set in the last rate case.

**Bond charges, true-up record vs financing-order mapping** (`bond_alloc_trueup_vs_legacy_mapping`): see Bond charges above.

## Definitional breaks

- **EIA commercial vs industrial is the reporter's choice.** Oncor reports by voltage; CenterPoint, AEP and TNMP by business type. AEP and TNMP report thousands of small accounts as industrial (oil-field and agricultural load), and from 2022–23 report very large new loads as commercial. TNMP's commercial MWh nearly doubled from 2024 to 2025 while industrial fell.
- **Oncor's Form 1 small/large split.** In 2002–08, "Small (or Commercial)" was Secondary ≤10 kW only. From 2009 it is all secondary. Layer B for Oncor 2002–08 is therefore mapped with the 2009+ rule.
- **Lighting** is in commercial in Layer B in all years. Form 1 reports it separately (account 444).
- **AEP Central and North** are reported as separate divisions through 2018 and as one company from 2019. Division Layer A rows for 2019–25 are blank; Layer B division rows for 2020–25 come from EIA.
- **EIA-861 delivery-only data before 2020.** EIA's delivery-only rows for the Texas wires companies exist for 2008–09 but are all zero, and there are none for 2003–07 or 2010–19. Layer B cannot be measured from EIA before 2020.
- **TNMP's small/large secondary boundary** is 5 kW (10 kW elsewhere).
- **New allocation tables** at each base-rate case change the transmission split by class; regimes are listed above.
- **Transmission leaves base rates** (TNMP Mar 2011, Oncor July 2011, CenterPoint Sept 2020). This affects billed amounts, not the cost-based transmission split.

## Gaps

| Utility | Years with no tariff-class source (non-residential classes blank) | Reason |
|---|---|---|
| AEP Texas Central | 2003–04, 2006 | No earnings report. 2003–04: exemption notices; see the AEP 2007 note above. 2006: none filed, because of an active rate case (Docket 33309), per the PUCT staff memo of Oct. 10, 2007 (Project 34025, item 60); a Public Information Act request (No. 2026-512) found no responsive records. No class billing determinants either (the 2006–07 petitions carry only the price sheets). Layer B for 2004 and 2006 comes from the AEP 10-K (revenue only). |
| AEP Texas North | 2006–07 | No earnings report. 2006: none filed, because a rate case had just been completed (Docket 33310, final order May 29, 2007), per the same memo and records response. 2007: exemption notice. Layer B for 2006 from the 10-K. |
| Merged AEP | 2003–04, 2006–07 | At least one division blank. |
| AEP divisions | 2019–25 | AEP reports only the merged company; EIA gives Layer B for 2020–25. |
| TNMP | 2008–10 | TNMP filed exemption notices instead of reports (rate cases pending; e.g. Project 36823 item 11 cites Docket 36025). Layer B is measured from the PNM Resources 10-K. |

In those years, transmission by class is still given in dollars (factor × cost). The statewide averages then cover three utilities; the `missing` column names the absent one.

Other limitations:
- Bond class splits for CenterPoint use forecast, not billed, revenue by class; the forecasts include each period's reconciliation adder by class.
- Mapped Layer B rows for AEP and TNMP are approximations.
- Nuclear decommissioning charges stay in delivery, as in the published files.
- `billed_kw` is blank. The true-up and TCRF filings give billing determinants for forecast periods, not calendar years.

## Regulated era, 1992–2001

Not covered. A transmission split by class would use the unbundled cost-of-service (UCOS) class allocators of Dockets 22349–22355, whose 2002 tables are in `tcrf_class_allocation_factors.csv`. A distribution split would also need the UCOS distribution allocators and class MWh in the pre-2002 bundled rate classes (Form 1 p.304), with their own crosswalk.

## Revisions to the published totals

Building the class split surfaced several corrections to the utility-level files. They are listed under "Unreleased" in the [changelog](../CHANGELOG.md); the class files are built on the corrected totals.
