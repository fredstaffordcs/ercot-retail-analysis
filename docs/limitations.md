# Limitations

Read these before reusing a series.

**Estimates versus measurements**
- **1992–2001 transmission and distribution are estimates**, built from each utility's cost of service (FERC Form 1; EIA's *Financial Statistics* for 1992–93) and class shares from the 2000 unbundling dockets. Every row is graded C. There is no split for 1990–91. HL&P 1997 has no source filing; the statewide series use the 1996/1998 average.
- **From 2002 the wires charges are measured but still partly modelled.** Transmission is cost-based (load × billed ERCOT rate plus interim updates, times the filed allocation factor), not read from bills. Riders use PUCT rate × kWh. Bond charges use collections times the residential allocation in each financing order. Grades and error bands are in the data.
- **AEP Texas has gap years** (Central 2003–04 and 2006–07; North 2006–07) where no earnings report exists; delivery and some credits are imputed and labelled with a certainty score. Residential and business statewide series include the imputed values; the merged AEP all-class delivery for 2003–04 is imputed at the statewide level only.

**Definitions**
- **Business = all classes minus residential**, so it includes lighting and other small classes.
- **Business transmission** is one minus the residential allocation factor. It does not separate secondary, primary and transmission-voltage customers.
- **Energy + retail is a residual** (retail price minus wires charges). It includes retail margin, bad debt and the provider mix of the year, not just wholesale energy.
- **Retail prices are class averages** from EIA-861 revenue per kWh; customer mix differs between areas and shifts over time. The competitive-era price covers competitive retail providers in ERCOT's competitive area; the regulated-era price covers the investor-owned utilities in the ERCOT region. The two are different populations.
- **EIA's own delivery series is not like-for-like across utilities**: it excludes bond charges for Oncor and CenterPoint but includes them for AEP Texas. This repository rebuilds delivery from filings to avoid that.

**Coverage**
- EIA reports delivery-only revenue only from 2020; earlier delivery figures come from FERC Form 1 and SEC filings.
- From 2012 EIA's full-form data drops small co-ops and municipals, so public-power series are filtered for consistency (see methodology).
- Small items omitted: TDU-billed storm credits after Aug 2021 (≤0.015¢), nuclear decommissioning (left in delivery), CenterPoint SRC3 bonds (issued late 2025).
- The wholesale series is the market monitor's all-in cost per MWh of load; its definition changes (energy only 2002–06; energy plus ancillary services from 2010) and some years are unavailable.

**Reuse**
- Chart scripts need the repository's data files and the Inter font for the exact look. Scripts that start from raw downloads expect them in `raw/` (not included; see `sources.md`).
- The scripts that parsed the raw filings into the wires-company files (PUCT rate summaries, AEP earnings reports, bond servicer reports, transmission matrices, TCRF petitions) are not included. The resulting data, line items, sources and methods are.
