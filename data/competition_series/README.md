# Inputs for the competition series charts

Used by `code/charts/competition_series/`. Other inputs come from `data/statewide_series/`, `data/reference/` and `data/by_class/`.

| File | What it is | Source |
|---|---|---|
| `nonercot_texas_iou_eia861_1990_2025.csv` | Texas sales (revenue in $ thousand, MWh) by class for the four Texas investor-owned utilities outside ERCOT: El Paso Electric, Southwestern Public Service, SWEPCO, Gulf States/Entergy Texas | EIA-861, Part A, Texas rows only |
| `nonercot_texas_iou_series_1990_2025.csv` | The same, summed across the four utilities, with household and business prices (nominal ¢/kWh) and the household-to-business ratio | Derived from the file above. `ratio_fix` holds the commercial/industrial mix fixed |
| `eia_mer_t09_08_prices_by_sector.csv`, `eia_mer_t07_06_sales_by_sector.csv` | US retail prices and sales by sector | EIA Monthly Energy Review, tables 9.8 and 7.6 |
| `us_series_1990_2025.csv` | US household and business prices (nominal ¢/kWh) and ratio | Derived from the two files above |
| `residential_transmission_allocation_vs_kwh_share_2002_2025.csv` | Residential share of the 4CP transmission allocator (weighted by each utility’s transmission cost) against the residential share of kWh delivered | Transmission cost recovery factor filings; EIA-861 |
| `wholesale_benchmarks_2002_2025.csv` | Wholesale benchmarks in ¢/kWh: `spot` (market monitor all-in), `lag1`, `avg2`, `avg3` (trailing averages), `gas` (Henry Hub annual average × an assumed 7.5 MMBtu/MWh heat rate) | `data/reference/ercot_wholesale_2002_2025.csv`; EIA Henry Hub |
