# Changelog

Versions follow [Semantic Versioning](https://semver.org/) adapted for data: a **major** version changes the structure or meaning of a published series (renamed columns, changed definitions, re-based methods); a **minor** version adds series, years or documentation; a **patch** version corrects values or typos. Dates are release dates.

## [1.1.1] - 2026-11-16

### Corrected
- **`data/by_class/statewide_delivery_by_class_2002_2025.csv`: component columns were mostly blank.** A blank component (no such charge in that class and year) made the whole weighted average blank, so in 219 of 222 rows the components did not add up to `total_cents` (the total was right). A blank component in a present row now counts as zero; a utility with no row or no MWh is still left out and named in `missing`. Non-blank cells per component, before → after (of 222 rows): `transition_securitized` 15 → 222, `transition_other` 0 → 222, `storm` 0 → 222, `sbf` 108 → 222. No totals change in the tariff layer.
- **`data/by_class/wires_components_by_eia_class_2002_2025.csv`, CenterPoint 2002–2019 commercial and industrial rows (36 rows).** Delivery was spread by revenue share but `dist_other` and `total` by MWh share, so within a row the components did not add to the total. `dist_other` is now delivery minus transmission and `total` is the sum of the components. Delivery is unchanged. CenterPoint commercial `dist_other` and `total` rise by 0.16–0.25¢/kWh and industrial fall by 0.12–0.19¢/kWh (equal and opposite in dollars, so the class sums still match the all-class totals). In the statewide EIA layer 36 of 48 commercial and industrial year-rows move, by at most +0.07¢ and −0.09¢. One TNMP 2006 row differs by $1 (thousand-dollar column, rounding only).
- **`data/validation/class_checks.csv`:** the bond-allocation check rows were duplicated (525 repeated rows); removed.
- The README citation line now names the current version (it still said v1.0.0 in v1.1.0).
- `docs/by_class.md` said all 438 class-sum checks pass. 437 do: merged AEP Texas 2002 delivery is $174 thousand (0.04%) short of the published all-class total, because the published merged 2002 ¢/kWh is weighted by February–December MWh while the class files use full-year MWh. The data are unchanged; the text now states the exception and its cause.

### Added
- Validation checks on the statewide by-class file (1,124 rows in `class_checks.csv`, `statewide_*`), which stop the build if any fails:
  - components add to `total_cents`, and transmission + distribution equals delivery, in every row of both layers (within 0.001¢);
  - the residential rows equal the published residential statewide series in every component and year (within 0.00055¢, the 3-decimal rounding of the published series plus the 4-decimal rounding of its inputs);
  - the non-residential classes combined, weighted by MWh, equal the published business series in every component, in years where all four utilities have class rows (within 0.001¢).

### Notes
- Charts are unchanged. The tariff-class file, line items and all other data files are unchanged.

## [1.1.0] - 2026-11-15

### Added
- **Wires-company charges by customer class, 2002–2025** ([`data/by_class/`](data/by_class), documented in [`docs/by_class.md`](docs/by_class.md)):
  - Layer A: tariff classes (residential, secondary ≤10 kW and >10 kW, primary, transmission voltage, lighting) for Oncor, CenterPoint, AEP Texas Central, North and merged, and TNMP, from FERC Form 1 rate-schedule sales, PUCT earnings monitoring reports, Rider TCRF class allocation tables and the bond true-up filings.
  - Layer B: EIA customer types (residential, commercial, industrial, transportation), measured from EIA-861 (2020–25), Form 1 (CenterPoint 2002–19, Oncor 2009–19) and the PNM Resources and AEP 10-K filings (TNMP 2007–19; AEP 2004 and 2006, revenue only), otherwise mapped from Layer A.
  - Statewide kWh-weighted averages by class, the tariff-class crosswalk, and a large-load indicator for 2020–25 (commercial MWh served above secondary voltage).
  - Within each utility, year and component the classes add to the published all-class totals and the residential class equals the residential file; imputed cells are labelled with a certainty score and an error band.
- Source extracts: `tcrf_class_allocation_factors.csv`, `bond_charges_by_class_trueup_filings.csv`, `aep_central_transition_trueup_collections.csv`.
- Validation: `class_checks.csv`.

### Changed
- **Charts regenerated** from the revised data (statewide values move by at most 0.02¢/kWh, so the charts look the same). Every chart and the animation now carries an "Updated" date in the footer (`code/charts/stamp.py`). The two 2025 snapshot charts (`residential_price_distribution_2025.png`, `tx_residential_prices_2025_all_utilities.png`) draw only on 2025 EIA-861 data, which did not change; they have no script in the repository and were date-stamped only.
- `anim_render.py`: the encoding instructions now reproduce the published video and GIF timing.

### Corrected
- **Bond charges, residential share (Oncor 2003–16; CenterPoint 2002–24).** The residential share of each bond series now comes from the true-up record filed at the PUCT instead of the fixed financing-order factor:
  - Oncor: transition charges billed by class (Monthly Servicer's Certificates).
  - CenterPoint: forecast revenue by charge class (billing determinants × charge, including class-specific reconciliation adders).

  Residential ¢/kWh changes by −0.007 to +0.015 for Oncor and by up to +0.05 for CenterPoint (TC1 2009–13).
- **AEP Texas 2005 and 2011 residential kWh and customers.** These now come from the same scanned earnings reports as the revenue, accepted where the class totals add to the Total column, instead of PUCT market-share data. The market-share workbook is missing data for 2011.
  - Residential wires charges in 2011: AEP Central 4.45¢ → 4.21¢, North 4.01¢ → 3.82¢.
  - Residential wires charges in 2005: Central 2.80¢ → 2.78¢, North 3.45¢ → 3.31¢.
  - AEP Central 2003–04 delivery, estimated from a Central/North ratio that uses 2005, rises by 0.04¢.
- **TNMP storm rider, all classes.** Uses billed totals for 2019–21; other years use residential × 1.84, the billed all-class/residential ratio. Previously the method scaled by all kWh ÷ residential kWh, which overstated it about twofold. All-class storm falls by about a third and all-class delivery rises by the same amount.
- **TNMP CTC, all classes.** Uses billed totals for 2019–20.
- **Oncor bond refund (2016–17) and CenterPoint TC1 2013, all-class amounts.** Derived with the true-up residential shares.
- **AEP Texas Central 2004 all-class delivery (previously blank).** Now estimated from AEP's FY2004 10-K total retail revenue for TCC, less the other components, × 1.052 (the same relation in 2005). The statewide all-class and business series therefore no longer impute AEP delivery for 2004; their previous imputation was within 0.001¢/kWh of the new value. `build_statewide_series.py` now imputes only where the published value is blank.
- `wires_residential_components_line_items.csv` restores the CenterPoint 2005 CTC line, which the totals already included.
- `residential_components_checks.csv`: the TNMP 2025 rows now match the published 2025 value (7.09¢).

### Effect on statewide series
- Competitive-area residential components move by at most 0.02¢/kWh in any year (2010, 2011).
- Business and all-class components move by at most 0.01¢/kWh.

## [1.0.0] - 2026-11-10

First public release.

### Data
- Statewide ERCOT price components for households, businesses and all classes: transmission, distribution + other, transition, storm and state-fee charges, and energy + retail, 2002–2025.
- Regulated-era (1990–2001) bundled prices with a cost-of-service transmission and distribution split for 1992–2001.
- Utility-level wires-company components, residential and all-class, 2002–2025; transmission/distribution split by utility.
- Residential prices for every Texas-area utility, 1990–2025; EIA-861 ownership-group totals; bundled prices by ownership.
- Source extracts, reference series (CPI, ERCOT wholesale) and validation checks.

### Code and documentation
- `build_statewide_series.py` rebuilds the statewide series from the utility-level files.
- Chart scripts and a year-by-year animation of utility prices.
- Methodology, sources, limitations and a data guide.

### Known limitations
See [`docs/limitations.md`](docs/limitations.md).

[1.1.1]: https://github.com/fredstaffordcs/ercot-retail-analysis/releases/tag/v1.1.1
[1.1.0]: https://github.com/fredstaffordcs/ercot-retail-analysis/releases/tag/v1.1.0
[1.0.0]: https://github.com/fredstaffordcs/ercot-retail-analysis/releases/tag/v1.0.0
