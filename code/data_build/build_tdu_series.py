"""Build wires_residential_delivery_revenue_2002_2019.csv (+ EIA overlap check and securitization side table).

Run from a directory that contains the raw inputs under data/ (not included in this repository; see docs/sources.md).
Writes its three CSVs to the current directory. Equivalent outputs are in data/utility_level/, data/validation/ and data/source_extracts/.

Sources:
  * FERC Form 1 via PUDL nightly parquet (data/out_ferc1__*.parquet)
  * SEC 10-K figures transcribed from filings in data/sec/
"""
import duckdb
import pandas as pd

SCHED300 = "data/out_ferc1__yearly_operating_revenues_sched300.parquet"
SCHED304 = "data/out_ferc1__yearly_sales_by_rate_schedules_sched304.parquet"
COLS = ["utility", "year", "res_revenue_thousand_usd", "res_mwh", "res_customers", "cents_per_kwh",
        "source", "source_detail", "includes_securitization", "notes"]

rows = []

def add(**kw):
    r = {c: kw.get(c) for c in COLS}
    rows.append(r)

# ---------------------------------------------------------------- Oncor / CenterPoint: Form 1 p.300 acct 440
f1 = duckdb.sql(f"""
  select utility_id_ferc1 id, report_year y, dollar_value/1e3 k, sales_mwh mwh, avg_customers_per_month cust
  from '{SCHED300}' where revenue_type='residential_sales' and utility_id_ferc1 in (293,318)
  and report_year between 2002 and 2025 order by 1,2""").df()

# Oncor transition-charge revenue (all classes, $M) billed for TXU Electric Delivery Transition Bond Co (Bondco),
# from Oncor 10-K MD&A footnotes; not in Form 1 (2010: 10-K op. rev $2,914M vs Form 1 $2,762M; gap = $152M).
ONCOR_TC = {2004: 106, 2005: 152, 2006: 151, 2008: 140, 2009: 147, 2010: 153, 2011: 151, 2012: 144}
# CenterPoint Houston "Transition (and system restoration) bond companies" revenue, all classes, $M (CEHE 10-K segment table).
CNP_BOND = {2004: 75, 2005: 106, 2006: 265, 2007: 277, 2008: 323, 2009: 340, 2010: 437, 2011: 444, 2012: 591,
            2013: 507, 2014: 566, 2015: 481, 2016: 553, 2017: 409, 2018: 594, 2019: 312}

for _, r in f1.iterrows():
    y = int(r.y)
    if r.id == 293:
        util = "Oncor Electric Delivery"
        name = "TXU Electric Delivery" if y < 2007 else "Oncor Electric Delivery"
        if 2003 <= y <= 2016:
            sec = "N"
            tc = ONCOR_TC.get(y)
            note = (f"Excludes transition-bond charges billed for Oncor/TXU Electric Delivery Transition Bond Co "
                    f"(company-wide, all classes: {'$%dM' % tc if tc else 'amount not extracted'}).")
            if y == 2003:
                note = "Excludes transition-bond charges (first series issued Aug 2003; small partial-year amount)."
        else:
            sec = "N"
            note = "No transition bonds outstanding (2004 series matured May 2016), so figure is complete."
            if y == 2002:
                note = "First year of retail choice; no transition bonds yet, so figure is complete."
        if y < 2007:
            note += " Filed as TXU Electric Delivery Co."
        if y == 2003:
            note += " Avg customers drop vs 2002 (2.57M->2.43M) looks definitional; revenue/MWh are continuous."
        if y == 2017:
            note += " Sharyland distribution assets absorbed late 2017 (~29k res. customers)."
        if y == 2018:
            note += " Includes former Sharyland retail territory full year; 2018 MWh also weather-driven."
        if y in (2018, 2019):
            note += " Rates reduced for TCJA tax-rate change."
        add(utility=util, year=y, res_revenue_thousand_usd=round(r.k, 1), res_mwh=r.mwh, res_customers=r.cust,
            source="FERC Form 1", source_detail=f"{name} Form 1 p.300 line 'Residential Sales' acct 440 (= p.304 'TOTAL RESIDENTIAL SALES'); via PUDL out_ferc1__yearly_operating_revenues_sched300, utility_id_ferc1=293",
            includes_securitization=sec, notes=note)
    else:
        util = "CenterPoint Energy Houston Electric"
        b = CNP_BOND.get(y)
        note = ("Excludes charges billed for CenterPoint's bankruptcy-remote Transition/Restoration Bond Companies "
                f"(company-wide, all classes: {'$%dM' % b if b else 'amount not extracted (Bond Co I issued Oct 2001)'}). "
                "Form 1 total = 10-K 'TDU' revenue line, excluding the 'Bond Companies' line.")
        if y == 2002:
            note += " First year of retail choice (Jan 2002)."
        add(utility=util, year=y, res_revenue_thousand_usd=round(r.k, 1), res_mwh=r.mwh, res_customers=r.cust,
            source="FERC Form 1", source_detail="CenterPoint Energy Houston Electric Form 1 p.300 acct 440 Residential Sales (= p.304 'Total Residential', billed + unbilled); PUDL utility_id_ferc1=318",
            includes_securitization="N", notes=note)

# ---------------------------------------------------------------- TNMP 2002-2006: Form 1 p.304 Texas unbundled section
tn = duckdb.sql(f"""
  select report_year y, dollar_value/1e3 k, sales_mwh mwh, avg_customers_per_month cust
  from '{SCHED304}' where utility_id_ferc1=41 and report_year between 2002 and 2006
  and rate_schedule_description like '6.1.1.1 Residential%' order by 1""").df()
for _, r in tn.iterrows():
    y = int(r.y)
    note = ("Texas delivery only. p.300 acct 440 is NOT used: it combines this with New Mexico bundled residential sales "
            "(NM ops moved to PNM 1 Jan 2007). TNMP had no securitization bonds; recovered stranded costs via CTC rider.")
    if y == 2002:
        note += (" 2002 also shows a bundled schedule '3A-1 Residential' (182,548 MWh; $19,078k; ~166k cust) excluded here; "
                 "it appears to be Texas bundled billing during the choice transition, so 2002 Texas delivery MWh may be ~8% understated.")
    add(utility="Texas-New Mexico Power", year=y, res_revenue_thousand_usd=round(r.k, 1), res_mwh=r.mwh, res_customers=r.cust,
        source="FERC Form 1", source_detail="TNMP Form 1 p.304 'Texas Unbundled Service - Delivery' / '6.1.1.1 Residential Service'; PUDL utility_id_ferc1=41",
        includes_securitization="N", notes=note)

# ---------------------------------------------------------------- TNMP 2007-2019: PNM Resources 10-K Comparative Operating Statistics
# year: (revenue $000, MWh, residential consumers, filing)
TNMP_10K = {
    2007: (69488, 2520605, 183260, "PNMR 10-K FY2011"),
    2008: (71673, 2533025, 187888, "PNMR 10-K FY2011"),
    2009: (74739, 2582555, 188812, "PNMR 10-K FY2011"),
    2010: (83645, 2699601, 190809, "PNMR 10-K FY2011"),
    2011: (100290, 2862337, 192356, "PNMR 10-K FY2011"),
    2012: (103255, 2714511, 193550, "PNMR 10-K FY2016"),
    2013: (111373, 2796661, 196799, "PNMR 10-K FY2016"),
    2014: (114826, 2802768, 199963, "PNMR 10-K FY2016"),
    2015: (120771, 2912019, 202359, "PNMR 10-K FY2019"),
    2016: (124462, 2933938, 204744, "PNMR 10-K FY2019"),
    2017: (126587, 2936291, 207788, "PNMR 10-K FY2019"),
    2018: (130288, 3094965, 210696, "PNMR 10-K FY2019"),
    2019: (150742, 3044760, 213435, "PNMR 10-K FY2019"),
}
for y, (k, mwh, cust, fil) in TNMP_10K.items():
    note = "Texas only (NM ops transferred to PNM 1 Jan 2007). No securitization bonds outstanding."
    note += " Customers are TNMP 'consumers' as reported (basis may be year-end, not monthly average)."
    if y == 2007:
        note += " Source switches from Form 1 (2006: 2.31 c/kWh) to 10-K; the 2007 jump is partly the CTC rider and partly the change of source."
    if y == 2018:
        note += " Excludes 'alternative revenue programs' line (-$2.5M to +$4.2M, incl. TCJA refunds) reported separately."
    if y == 2019:
        note += " New base rates from Docket 48401 effective 2019."
    add(utility="Texas-New Mexico Power", year=y, res_revenue_thousand_usd=k, res_mwh=mwh, res_customers=cust,
        source="SEC 10-K", source_detail=f"{fil}, Comparative Operating Statistics: TNMP Revenues/MWh Sales/Consumers - Residential",
        includes_securitization="N", notes=note)

# ---------------------------------------------------------------- AEP Texas
AEP_10K = {  # year: (res revenue $000, res MWh, filing detail)
    2015: (None, 11562000, "AEP 10-K FY2017 Exh.13, AEP Texas MD&A 'Summary of KWh Energy Sales' (revenue by class not disclosed)"),
    2016: (None, 11844000, "AEP 10-K FY2017 Exh.13, AEP Texas MD&A 'Summary of KWh Energy Sales' (revenue by class not disclosed)"),
    2017: (573900, 11569000, "AEP 10-K FY2019: revenue disaggregation 'AEP Texas Retail Revenues Residential Sales'; KWh from FY2019 Exh.13 AEP Texas MD&A"),
    2018: (594600, 12101000, "AEP 10-K FY2019: revenue disaggregation 'AEP Texas Retail Revenues Residential Sales'; KWh from FY2019 Exh.13 AEP Texas MD&A"),
    2019: (588900, 11996000, "AEP 10-K FY2019: revenue disaggregation 'AEP Texas Retail Revenues Residential Sales'; KWh from FY2019 Exh.13 AEP Texas MD&A"),
}
AEP_SEC_NOTE = ("AEP Texas consolidates its Transition Funding LLCs, so the 10-K residential figure probably includes "
                "securitization charges; not confirmed.")
for y in range(2002, 2020):
    for util in ("AEP Texas Central", "AEP Texas North"):
        if y == 2002:
            note = ("Form 1 p.300 shows residential revenue for 2002 only (Central $74.4M/0.97 TWh; North $8.7M/0.16 TWh), "
                    "a partial-year bundled/transition remnant, not delivery. Left blank.")
        elif y >= 2017:
            note = "Central and North merged into AEP Texas Inc. in 2017. The 10-K reports only the combined company; see 'AEP Texas (Central+North)'."
        else:
            note = ("No source found. Form 1 books all delivery in acct 456 with no class split (p.304 empty 2003-2016). "
                    "TCC/TNC 10-Ks (to FY2006) have no class data, and no SEC filings 2007-2016. "
                    "Possible fallbacks: PUCT rate cases (TCC Docket 33309, TNC 33310, test year 2005; AEP Texas 49494, test year 2018) or archived tariff bills.")
        add(utility=util, year=y, source="none", includes_securitization="unknown", notes=note)
    a = AEP_10K.get(y)
    if a:
        k, mwh, det = a
        add(utility="AEP Texas (Central+North)", year=y, res_revenue_thousand_usd=k, res_mwh=mwh,
            source="SEC 10-K", source_detail=det, includes_securitization="unknown",
            notes=(AEP_SEC_NOTE + " MWh rounded to GWh. Residential customers not disclosed."
                   + (" Revenue by class not disclosed for this year, so revenue is blank." if k is None else "")
                   + " In 2020-22 this source ran +0.03 to +0.09 c/kWh above EIA (2022: 10-K kWh 1.7% below EIA, revenue 1.0% below)."))
    else:
        add(utility="AEP Texas (Central+North)", year=y, source="none", includes_securitization="unknown",
            notes="No class-level residential source found; see the Central/North rows.")

df = pd.DataFrame(rows, columns=COLS)
df["cents_per_kwh"] = (df.res_revenue_thousand_usd / df.res_mwh * 100).round(3)  # $000/MWh*100 = c/kWh
df = df[df.year.between(2002, 2019)].sort_values(["utility", "year"])
df.to_csv("wires_residential_delivery_revenue_2002_2019.csv", index=False)

# ---------------------------------------------------------------- overlap check 2020-2022 vs EIA
eia = {("Oncor", 2020): 3.96, ("Oncor", 2021): 4.05, ("Oncor", 2022): 4.32,
       ("CenterPoint", 2020): 4.08, ("CenterPoint", 2021): 4.01, ("CenterPoint", 2022): 4.41,
       ("AEP Texas", 2020): 4.54, ("AEP Texas", 2021): 4.41, ("AEP Texas", 2022): 5.08,
       ("TNMP", 2020): 5.16, ("TNMP", 2021): 5.24, ("TNMP", 2022): 5.68}
ov = []
for _, r in f1[f1.y.between(2020, 2022)].iterrows():
    u = "Oncor" if r.id == 293 else "CenterPoint"
    ov.append((u, int(r.y), round(r.k, 1), r.mwh, "FERC Form 1 p.300 acct 440"))
ov += [("AEP Texas", 2020, 563600, 12163000, "AEP 10-K FY2022"), ("AEP Texas", 2021, 550300, 12284000, "AEP 10-K FY2022"),
       ("AEP Texas", 2022, 667200, 13049000, "AEP 10-K FY2022"),
       ("TNMP", 2020, 158066, 3069600, "PNMR 10-K FY2021/FY2022"), ("TNMP", 2021, 158796, 3018300, "PNMR 10-K FY2021/FY2022"),
       ("TNMP", 2022, 187951, 3309300, "PNMR 10-K FY2022")]
o = pd.DataFrame(ov, columns=["utility", "year", "revenue_thousand_usd", "mwh", "source"])
o["cents_per_kwh"] = (o.revenue_thousand_usd / o.mwh * 100).round(3)
o["eia_cents_per_kwh"] = [eia[(u, y)] for u, y in zip(o.utility, o.year)]
o["diff_cents"] = (o.cents_per_kwh - o.eia_cents_per_kwh).round(3)
o.to_csv("eia_overlap_check_2020_2022.csv", index=False)

# ---------------------------------------------------------------- securitization side table
s = [("Oncor Electric Delivery", y, v * 1000, "Oncor 10-K MD&A footnote: transition charge revenue") for y, v in ONCOR_TC.items()]
s += [("CenterPoint Energy Houston Electric", y, v * 1000, "CEHE 10-K segment table: Transition/System Restoration Bond Companies revenue") for y, v in CNP_BOND.items()]
pd.DataFrame(s, columns=["utility", "year", "securitization_revenue_all_classes_thousand_usd", "source"]).sort_values(["utility", "year"]).to_csv(
    "securitization_revenue_all_classes.csv", index=False)

print(df.pivot(index="year", columns="utility", values="cents_per_kwh").to_string())
print(o.to_string())
