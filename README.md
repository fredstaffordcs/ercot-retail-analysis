# Texas retail electricity prices, 1990–2025

Data, code and documentation for splitting Texas retail electricity prices into **transmission, distribution, transition and storm charges, and energy + retail**, for households and businesses, from the regulated era (1990–2001) through retail choice (2002–2025). It was built to test whether falling ERCOT wholesale prices reached Texas retail bills.

Maintained by Fred Stafford · [@fredstaffordcs](https://twitter.com/fredstaffordcs) · [PublicPowerReview.org](https://publicpowerreview.org)

## What is here

| | |
|---|---|
| **[`data/`](data)** | Statewide series, utility-level detail, source extracts, reference series and validation checks. Start with the [data guide](data/README.md) |
| **[`docs/`](docs)** | [Methodology](docs/methodology.md), [sources](docs/sources.md) and [limitations](docs/limitations.md) |
| **[`charts/`](charts)** | Finished charts and a year-by-year animation of every Texas utility's residential price |
| **[`code/`](code)** | Scripts that build the statewide series and draw the charts |

## A first look

Nominal cents per kWh, ERCOT competitive area:

| | Households 2019 | Households 2025 | Business 2019 | Business 2025 |
|---|---|---|---|---|
| Retail price | 12.6 | 17.3 | 6.7 | 7.1 |
| Wires companies' charges | 3.8 | 5.6 | 2.0 | 2.1 |
| of which transmission | 1.4 | 1.9 | 0.8 | 0.8 |
| Energy + retail | 8.5 | 11.6 | 4.5 | 5.0 |
| ERCOT all-in wholesale (per kWh) | 5.1 | 3.8 | | |

Wires charges include transition and storm items; see the data guide for the exact split. Series are in [`data/statewide_series/`](data/statewide_series).

## Quick start

```python
import pandas as pd
res = pd.read_csv("data/statewide_series/competitive_residential_components_2002_2025.csv", index_col="year")
print(res[["retail", "transmission", "dist_other", "dereg_transition", "energy_retail"]].loc[[2002, 2010, 2019, 2025]])
```

Regenerate the statewide series from the utility-level files, and the charts from the statewide series:

```
python code/data_build/build_statewide_series.py
python code/charts/make15.py        # households vs. businesses
```

Python 3 with pandas, numpy and matplotlib (`requirements.txt`). Charts use the Inter font.

## Conventions

- Prices are **nominal cents per kWh** unless noted. Charts convert to 2025 dollars with CPI-U annual averages ([`data/reference/cpi_annual.csv`](data/reference/cpi_annual.csv)).
- "Business" means all customer classes minus residential.
- Through 2001 the price is the bundled price of the regulated investor-owned utilities in the ERCOT region; from 2002 it is the competitive retail providers' price minus the kWh-weighted wires charges of Oncor, CenterPoint, AEP Texas and TNMP.
- Rows and cells carry certainty grades (A reported, B checked method, C weak). Cells are blank, not interpolated, when no source exists.

## Limits

The 1992–2001 split is a cost-of-service estimate, not a billed amount; AEP Texas has gap years that are imputed and scored; business transmission is the complement of the residential allocation. Read [`docs/limitations.md`](docs/limitations.md) before reusing any series.

## Not included

About 800 MB of raw public downloads (EIA-861, PUCT and SEC filings, ERCOT market monitor reports, PUDL tables). [`docs/sources.md`](docs/sources.md) says where each comes from. The scripts that parsed those raw filings into the wires-company files are also not included; the resulting files and their methods are.

## License

- Data, charts and documentation: [CC BY 4.0](LICENSE-DATA.txt). Reuse freely with attribution to Fred Stafford, Public Power Review.
- Code in `code/`: [MIT](LICENSE-CODE.txt).
- Source data from EIA, FERC, PUCT, SEC, BLS and ERCOT are public records.

## Citation

Stafford, F. (2026). *Texas retail electricity prices, 1990–2025* (v1.0.0) [Data set]. Public Power Review. https://github.com/fredstaffordcs/ercot-retail-analysis

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff); version history is in [`CHANGELOG.md`](CHANGELOG.md).
