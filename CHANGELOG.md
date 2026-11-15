# Changelog

Versions follow [Semantic Versioning](https://semver.org/) adapted for data: a **major** version changes the structure or meaning of a published series (renamed columns, changed definitions, re-based methods); a **minor** version adds series, years or documentation; a **patch** version corrects values or typos. Dates are release dates.

## [Unreleased]

### Added
- **Wires-company charges by customer class, 2002–2025** ([`data/by_class/`](data/by_class), documented in [`docs/by_class.md`](docs/by_class.md)):
  - Layer A: tariff classes (residential, secondary ≤10 kW and >10 kW, primary, transmission voltage, lighting) for Oncor, CenterPoint, AEP Texas Central, North and merged, and TNMP, from FERC Form 1 rate-schedule sales, PUCT earnings monitoring reports, Rider TCRF class allocation tables and the bond true-up filings.
  - Layer B: EIA customer types (residential, commercial, industrial, transportation), measured from EIA-861 (2020–25), Form 1 (CenterPoint 2002–19, Oncor 2009–19) and the PNM Resources and AEP 10-K filings (TNMP 2007–19; AEP 2004 and 2006, revenue only), otherwise mapped from Layer A.
  - Statewide kWh-weighted averages by class, the tariff-class crosswalk, and a large-load indicator for 2020–25 (commercial MWh served above secondary voltage).
  - Within each utility, year and component the classes add to the published all-class totals and the residential class equals the residential file; imputed cells are labelled with a certainty score and an error band.
- Source extracts: `tcrf_class_allocation_factors.csv`, `bond_charges_by_class_trueup_filings.csv`, `aep_central_transition_trueup_collections.csv`.
- Validation: `class_checks.csv`.

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

[1.0.0]: https://github.com/fredstaffordcs/ercot-retail-analysis/releases/tag/v1.0.0
