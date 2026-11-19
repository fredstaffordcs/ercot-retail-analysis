# Competition series: households vs. businesses in Texas

Seven charts on whether retail competition has lowered Texas electricity bills. Prices are in 2025 dollars (CPI-U); ratios are unaffected by inflation.

| # | File | Base year |
|---|---|---|
| 1 | `01_price_levels.png` | 2001 |
| 2 | `02_gap_vs_public_power.png` | 2001 |
| 3 | `03_price_components.png` | 2002 |
| 4 | `04_ercot_vs_nonercot.png` | 2001 |
| 5 | `05_transmission_allocation.png` | 2002 |
| 6 | `06_energy_charge_vs_wholesale.png` | 2002 |
| 7 | `07_load_shape_vs_retail.png` | 2011 (first year of load-profile prices) |

**Base years differ.** 2001 is the last year of regulated, bundled rates, and is used where total prices are compared (charts 1, 2 and 4). The energy-and-retail split, the transmission allocation and the wholesale comparisons exist only from competition in 2002, so charts 3, 5 and 6 start there. Chart 7 starts in 2011, the first full year of ERCOT's nodal real-time prices, and compares trends and multi-year averages rather than a single base year.

**Reclassification caveat.** From 2002, public-authority and lighting customers drop out of the reported ERCOT data, which lowers the business price by about 0.2¢. Measured from 2001, this overstates the business decline by about 2 percentage points and the 2025 household-to-business ratio by about 0.07.

Scripts: `code/charts/competition_series/NN_*.py`, one per chart. Run any of them from any directory (`python code/charts/competition_series/01_price_levels.py`); each rewrites its PNG here. Inputs are listed in `data/competition_series/README.md` and the existing `data/` folders. Charts use the Inter font.

Chart-specific sources and definitions are in each chart's footer. License: CC BY 4.0 (see `LICENSE-DATA.txt`).
