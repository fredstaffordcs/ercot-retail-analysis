# Data guide

All prices are **nominal cents per kWh** unless a column name says otherwise. Money columns ending `_kusd` or `_thousand_usd` are thousands of dollars; `_mwh` is MWh. Blank means "not available", never zero (except where a column documents otherwise). Method details are in [`../docs/methodology.md`](../docs/methodology.md).

| Folder | What it holds |
|---|---|
| [`statewide_series/`](statewide_series) | Headline series for the ERCOT region, ready to chart |
| [`utility_level/`](utility_level) | Wires-company and utility detail behind the statewide series |
| [`by_class/`](by_class) | Wires-company charges split by customer class, 2002–2025 |
| [`source_extracts/`](source_extracts) | Figures transcribed or parsed from source documents, used as inputs |
| [`reference/`](reference) | CPI, wholesale prices and other small reference series |
| [`validation/`](validation) | Cross-checks of the series against independent sources |

Most rows have a certainty grade or flag; see "Grades" in the methodology. To keep only well-supported values, drop rows or cells graded C or with low `*_certainty`.

## statewide_series/

### Competitive-era components (2002–2025)

`competitive_residential_components_2002_2025.csv`, `competitive_business_components_2002_2025.csv`, `competitive_all_classes_components_2002_2025.csv` — one row per year. The all-classes file has no transmission split.

| Column | Meaning |
|---|---|
| `year` | Calendar year |
| `retail` | Competitive retail providers' revenue per kWh for the class (EIA-861) |
| `delivery` | The wires companies' own retail charges, kWh-weighted over Oncor, CenterPoint, AEP Texas and TNMP. Excludes the items below |
| `transmission` | Part of `delivery`: the transmission bill allocated to the class (not in the all-classes file) |
| `dist_other` | `delivery − transmission`: distribution, metering and non-transmission riders |
| `transition_securitized` | Transition-bond charges (including post-retirement refunds). Can be negative |
| `transition_other` | CTC, excess mitigation credits, retail clawback credits, true-up expenses. Can be negative |
| `dereg_transition` | `transition_securitized + transition_other` |
| `storm` | Storm-restoration bond charges and riders |
| `sbf` | State System Benefit Fund fee (to Aug 2013; AEP's 2021 COVID relief program charge is included in 2021) |
| `other` | `storm + sbf` (business and all-classes files) |
| `tdu_total` | `delivery + transition_securitized + transition_other + storm + sbf` |
| `energy_retail` | `retail − tdu_total`: what remains for energy and retail service |
| `public_power` | ERCOT-area municipal and co-op revenue per kWh for the same class |
| `n_util`, `check_total`, `min_certainty` | (residential) utilities in the average; total recomputed utility by utility; lowest certainty among imputed cells that year (blank if none) |
| `tdu_mwh`, `rep_mwh`, `aep_delivery_imputed` | (business, all classes) MWh behind the wires average; competitive providers' MWh; `True` where AEP's delivery was imputed (2003–04) |
| `deliv_check` | (residential) delivery recomputed from the transmission-split file, for reconciliation with `delivery` |

### Regulated era (1990–2001)

`regulated_residential_functional_split_1990_2001.csv`: `year, bundled` (weighted bundled price of the five utilities with data), `transmission, distribution` (cost-of-service estimates, blank for 1990–91), `hist_series_iou` (EIA-861 residential revenue ÷ MWh for the regulated ERCOT investor-owned utilities), `gen_retail = hist_series_iou − transmission − distribution`.

`regulated_business_functional_split_1992_2001.csv`: `year, transmission, distribution, ci_mwh` for non-residential customers.

### Other series

| File | Content |
|---|---|
| `bundled_prices_by_ownership_1990_2025.csv` | Bundled revenue per kWh. `iou_*` = regulated investor-owned utilities in the ERCOT region (through 2001); `pub_*` = ERCOT-area public power; `*_all` all classes, `*_ci` non-residential |
| `eia861_ownership_group_totals_1990_2025.csv` | EIA-861 revenue (thousand $), MWh and customers by year, ownership group `G` (`iou`, `pub`, `comp`) and class (`res`, `com`, `ind`, `oth`, `tot`) |
| `ercot_private_vs_public_residential_1990_2025_{nominal,real2025}.csv` | Residential, commercial and industrial prices: `private` (regulated IOU through 2001, competitive providers after; see `private_type`) versus `public_power`. The real file is in 2025 dollars |

## utility_level/

| File | Content |
|---|---|
| `wires_residential_components_2002_2025.csv` | One row per wires company and year: residential MWh and customers, reported revenue and source, and delivery, transition_securitized, transition_other, storm and sbf in both $ thousand and ¢/kWh; `tdu_bill_total_cents_per_kwh`; imputation status, certainty, error band and method columns for AEP gap years; `data_flags` |
| `wires_residential_components_line_items.csv` | Every line item behind that file with method, source and coverage |
| `wires_residential_delivery_revenue_2002_2019.csv` | Reported residential delivery revenue, MWh, customers and ¢/kWh before the component split (`includes_securitization` flags whether bond charges are inside) |
| `wires_all_class_components_2002_2025.csv` | All-class counterpart: `all_*_kusd` by component, `all_mwh`, `res_mwh`, per-kWh versions and `ci_*` (non-residential) columns, `source_detail` and `min_certainty` |
| `wires_all_class_components_line_items.csv` | Line items with grade, method and source |
| `wires_residential_transmission_split_2002_2025.csv` | Transmission versus distribution: `tdu_4cp_kw`, `ercot_postage_stamp_rate`, `ercot_total_tcos_kusd`, `tdu_wholesale_tx_cost_kusd` (time-weighted), `in_year_tcos_updates_kusd`, `res_tx_alloc_factor` and `alloc_source`, `res_tx_cents`, `dist_other_cents`, `tx_share_of_delivery`, `min_certainty`, `notes` |
| `regulated_residential_functional_split_1990_2001.csv` | Regulated utilities: `bundled_cents`, `tx_cents`, `dist_cents`, `gen_retail_cents`, revenue requirements, residential shares and their sources, `min_certainty`, `notes` |
| `residential_prices_by_utility_1990_2025.csv` | Every Texas-area utility's residential customers, revenue, MWh and price (nominal and 2025 dollars) by year and group (`rep` competitive/regulated ERCOT retailers, `pub` ERCOT public power, `iou`/`npub` outside ERCOT). Entities with fewer than 500 residential customers are excluded |
| `competitive_providers_residential_2025.csv`, `bundled_prices_by_utility_2025.csv` | 2025 snapshots by provider and by utility |
| `wires_residential_components_2019_2025_summary.csv` | Residential delivery split into transmission and distribution + other for 2019–2025 (chart input; produced by `code/charts/make3.py`) |

## by_class/

Wires-company charges for Oncor, CenterPoint, AEP Texas (Central, North and merged) and TNMP, split into customer classes in two layers. Within each utility, year and component the classes add to the all-class file and the residential class equals the residential file. Methods, grades and gaps are in [`../docs/by_class.md`](../docs/by_class.md).

| File | Content |
|---|---|
| `wires_components_by_tariff_class_2002_2025.csv` | Layer A, tariff classes: one row per utility, year and `class_code` (`res`, `sec_small`, `sec_large`, `pri`, `trans`, `light`). `mwh`, `customers`, each component (`delivery`, `transmission`, `dist_other`, `transition_securitized`, `transition_other`, `storm`, `sbf`, `total`) as `_kusd` and `_cents`; `tx_alloc_factor`, `tx_share_of_delivery`; a grade per component and `min_certainty`; `*_status`, `*_certainty`, `*_error_band_cents`, `*_imputation_method` for imputed cells; `flag`, `source`, `method`, `tx_alloc_source`, `notes`. `billed_kw` is blank |
| `wires_components_by_eia_class_2002_2025.csv` | Layer B, EIA customer types (`residential`, `commercial`, `industrial`, `transportation`), same components. `measured_or_mapped` and `basis` say whether a row is measured (EIA-861, Form 1, 10-K) or mapped from Layer A. Commercial rows for 2020–25 carry a large-load indicator (`diag_commercial_mwh_above_secondary`, `diag_share_of_commercial_mwh`, `diag_note`) |
| `wires_components_by_class_line_items.csv` | Every amount behind the two files: `utility, year, class_code, component, item, kusd, grade, method, source` |
| `statewide_delivery_by_class_2002_2025.csv` | kWh-weighted averages over Oncor, CenterPoint, merged AEP Texas and TNMP by `layer`, `year` and `class_code`, in ¢/kWh; `n_util`, `utilities` and `missing` say which utilities are included; `share_mwh_mapped` (Layer B) is the MWh share from mapped rows |
| `tariff_class_crosswalk.csv` | How every source class (Form 1 rate schedules, earnings-report columns, Rider TCRF sub-classes, financing-order and legacy classes) maps to a class code and EIA type, with dates and sources |

Non-residential classes are blank where no class-level source exists (AEP Central 2003–04 and 2006, AEP North 2006–07, the AEP divisions 2019–25). TNMP 2008–10 has Layer B only.

## source_extracts/

Inputs transcribed or parsed from source documents; each file's columns are self-describing.

| File | Content |
|---|---|
| `ferc1_functional_revenue_requirement_1992_2001.csv` | Every Form 1 component of each utility's functional revenue requirement |
| `eia0437_texas_1992_1993.csv` | 1992–93 inputs hand-read from EIA's *Financial Statistics*, with page numbers |
| `securitization_collections_by_series.csv`, `securitization_revenue_all_classes.csv` | Bond-company collections by series and year, with residential factors |
| `aep_earnings_reports_residential_annual.csv`, `aep_residential_rates.csv`, `aep_delivery_model_test.csv` | AEP earnings-report extracts, archived PUCT rider rates, and the rate-model test used for gap years |
| `puct_market_share_residential_annual.csv` | Residential MWh and customers by TDU area from the PUCT retail market share workbook |
| `tcrf_class_allocation_factors.csv` | Rider TCRF transmission allocation factors by class and sub-class for every allocation regime, 2002–2025 |
| `bond_charges_by_class_trueup_filings.csv` | Bond true-up filings: CenterPoint forecast billing determinants, charges and revenue by charge class; Oncor transition charges billed by class each month |
| `aep_central_transition_trueup_collections.csv` | AEP Texas Central TF1 and TC-2 collections by legacy TC class from the true-up workpapers, 2002–09 |

## reference/

| File | Content |
|---|---|
| `cpi_annual.csv` | CPI-U annual averages (`year, value`) |
| `ercot_wholesale_2002_2025.csv` | ERCOT market monitor wholesale cost, $/MWh, with the definition for each year (energy only, or energy plus ancillary services) |
| `wholesale_and_retail_2019_2025.csv` | 2019–2025 residential and business retail, delivery, energy and wholesale cents per kWh (`ret`, `deliv`, `energy`, `wh`, and `com_*`, `ind_*` for commercial and industrial) used by one chart |
| `ercot_switches_2018_2025.csv` | Retail switching and move-in counts and customer totals |

## validation/

| File | What it checks |
|---|---|
| `residential_components_checks.csv`, `all_class_checks.csv` | Components against EIA, FERC Form 1, AEP and bond-issuer reports |
| `class_checks.csv` | Class files: class sums against the published totals, sources before scaling against the published amounts, billed class amounts, the transmission factors, and mapped Layer B against EIA-861 and the 10-K filings (`check_group`, `value`, `target`, `diff`, `within_tolerance`) |
| `eia_overlap_check_2020_2022.csv` | Delivery series against EIA's own 2020–2022 delivery data |
| `transmission_split_checks.csv`, `billed_vs_cost_transmission_2005_2010.csv` | Transmission estimates against 10-K disclosures and billed tariffs; comparison with the superseded TOTAL-row rate method |
| `regulated_split_seam_checks.csv`, `depreciation_shortcut_backtest.csv` | The 2001/2002 seam and the 1992–93 depreciation shortcut |
