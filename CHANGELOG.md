# Changelog

Versions follow [Semantic Versioning](https://semver.org/) adapted for data: a **major** version changes the structure or meaning of a published series (renamed columns, changed definitions, re-based methods); a **minor** version adds series, years or documentation; a **patch** version corrects values or typos. Dates are release dates.

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
