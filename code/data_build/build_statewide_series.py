"""Build the statewide ERCOT price-component series from the utility-level files.

Inputs (all in this repo):
  data/utility_level/wires_residential_components_2002_2025.csv
  data/utility_level/wires_all_class_components_2002_2025.csv
  data/utility_level/wires_residential_transmission_split_2002_2025.csv
  data/utility_level/regulated_residential_functional_split_1990_2001.csv
  data/source_extracts/ferc1_functional_revenue_requirement_1992_2001.csv
  data/statewide_series/eia861_ownership_group_totals_1990_2025.csv

Outputs (written to --out, default data/statewide_series/):
  competitive_residential_components_2002_2025.csv
  competitive_business_components_2002_2025.csv
  competitive_all_classes_components_2002_2025.csv
  regulated_residential_functional_split_1990_2001.csv
  regulated_business_functional_split_1992_2001.csv

All prices are nominal cents per kWh. "Business" is all classes minus residential.
Run from anywhere:  python code/data_build/build_statewide_series.py [--out DIR]
"""
import argparse
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser(); ap.add_argument('--out', default=str(ROOT / 'data/statewide_series')); out = Path(ap.parse_args().out); out.mkdir(parents=True, exist_ok=True)
UL, SS = ROOT / 'data/utility_level', ROOT / 'data/statewide_series'
U = ['Oncor', 'CenterPoint', 'AEP Texas (Central+North)', 'TNMP']          # wires companies in the competitive area
COMP = ['delivery', 'transition_securitized', 'transition_other', 'storm', 'sbf']

res = pd.read_csv(UL / 'wires_residential_components_2002_2025.csv'); res = res[res.utility.isin(U)].copy()
allc = pd.read_csv(UL / 'wires_all_class_components_2002_2025.csv'); allc = allc[allc.utility.isin(U)].set_index(['utility', 'year'])
tx = pd.read_csv(UL / 'wires_residential_transmission_split_2002_2025.csv'); tx = tx[tx.utility.isin(U)].set_index(['utility', 'year'])
S = pd.read_csv(SS / 'eia861_ownership_group_totals_1990_2025.csv').set_index(['Year', 'G'])
rep, pub = S.xs('comp', level='G'), S.xs('pub', level='G')   # competitive retail providers; ERCOT-area public power

# ---------------- 2002-2025, residential ----------------
for c in COMP: res[c + '_k'] = res[c + '_cents_per_kwh'].fillna(0) * res.res_mwh / 100        # $ thousands
g = res.groupby('year')[[c + '_k' for c in COMP] + ['res_mwh']].sum()
W = pd.DataFrame({c: g[c + '_k'] / g.res_mwh * 100 for c in COMP})
W['tdu_total'] = W.sum(axis=1); W['n_util'] = res.groupby('year').utility.nunique()
W['check_total'] = res.groupby('year').apply(lambda x: (x.tdu_bill_total_cents_per_kwh * x.res_mwh).sum() / x.res_mwh.sum())
W['retail'] = rep.res_rev / rep.res_mwh * 100; W['public_power'] = pub.res_rev / pub.res_mwh * 100
W['energy_retail'] = W.retail - W.tdu_total; W['dereg_transition'] = W.transition_securitized + W.transition_other
W['min_certainty'] = res.groupby('year').min_certainty_of_imputed.min()
t = tx.reset_index(); gt = t.groupby('year')
W['transmission'] = gt.apply(lambda x: (x.res_tx_cents * x.res_mwh).sum() / x.res_mwh.sum())
W['deliv_check'] = gt.apply(lambda x: (x.delivery_cents * x.res_mwh).sum() / x.res_mwh.sum())
W['dist_other'] = W.delivery - W.transmission
W.index.name = 'year'; W.round(3).to_csv(out / 'competitive_residential_components_2002_2025.csv')

# ---------------- 2002-2025, all classes and business ----------------
A = pd.DataFrame({c: allc['all_' + c + '_kusd'] for c in COMP}); A['mwh'] = allc.all_mwh
r = res.set_index(['utility', 'year'])
k = 'AEP Texas (Central+North)'
# AEP merged all-class delivery is blank for 2003-04 (no earnings reports); impute from residential delivery
# times the mean all-class / residential delivery ratio of 2002 and 2005.
ratio = lambda y: (A.loc[(k, y), 'delivery'] / A.loc[(k, y), 'mwh']) / (r.loc[(k, y), 'delivery_cents_per_kwh'] / 100)
R = (ratio(2002) + ratio(2005)) / 2
for y in (2003, 2004): A.loc[(k, y), 'delivery'] = r.loc[(k, y), 'delivery_cents_per_kwh'] / 100 * R * A.loc[(k, y), 'mwh']
A = A.fillna({c: 0 for c in COMP if c != 'delivery'})
Rs = pd.DataFrame({c: r[c + '_cents_per_kwh'].fillna(0) * r.res_mwh / 100 for c in COMP}); Rs['mwh'] = r.res_mwh
Cc = A - Rs
# transmission for business: each wires company's wholesale transmission cost x (1 - residential allocation factor)
txc = (tx.tdu_wholesale_tx_cost_kusd * (1 - tx.res_tx_alloc_factor)).groupby('year').sum()
for name, D in [('all_classes', A), ('business', Cc)]:
    g = D.groupby(level='year').sum()
    X = pd.DataFrame({c: g[c] / g.mwh * 100 for c in COMP}); X['tdu_total'] = X.sum(axis=1); X['tdu_mwh'] = g.mwh
    if name == 'all_classes': rv, mw, pv, pm = rep.tot_rev, rep.tot_mwh, pub.tot_rev, pub.tot_mwh
    else: rv, mw, pv, pm = rep.tot_rev - rep.res_rev, rep.tot_mwh - rep.res_mwh, pub.tot_rev - pub.res_rev, pub.tot_mwh - pub.res_mwh
    X['retail'] = rv / mw * 100; X['rep_mwh'] = mw; X['energy_retail'] = X.retail - X.tdu_total
    X['dereg_transition'] = X.transition_securitized + X.transition_other; X['other'] = X.storm + X.sbf
    X['public_power'] = (pv / pm * 100).reindex(X.index); X['aep_delivery_imputed'] = X.index.isin([2003, 2004])
    if name == 'business':
        X['transmission'] = txc / g.mwh * 100; X['dist_other'] = X.delivery - X.transmission
    X.index.name = 'year'; X.round(4).to_csv(out / f'competitive_{name}_components_2002_2025.csv')

# ---------------- 1990-2001, regulated utilities ----------------
reg = pd.read_csv(UL / 'regulated_residential_functional_split_1990_2001.csv')
fr = pd.read_csv(ROOT / 'data/source_extracts/ferc1_functional_revenue_requirement_1992_2001.csv')
# HL&P 1997 has no functional data (partial Form 1 filing); fill with the 1996 / 1998 average for the statewide series only.
def fill_hlp(df, cols, key=('Houston Lighting & Power',)):
    df = df.copy(); m = df.utility.isin(key)
    for y in (1997,):
        if not ((df.utility.isin(key)) & (df.year == y)).any(): continue
        row = (df.utility.isin(key)) & (df.year == y)
        for c in cols: df.loc[row, c] = df.loc[m & df.year.isin([1996, 1998]), c].mean()
    return df
reg = fill_hlp(reg, ['tx_cents', 'dist_cents'])
byr = reg.groupby('year')
def wavg(x, c):
    ok = x[c].notna() & x.res_mwh.notna(); return (x.loc[ok, c] * x.loc[ok, 'res_mwh']).sum() / x.loc[ok, 'res_mwh'].sum() if ok.any() else np.nan
H = pd.DataFrame({'bundled': byr.apply(lambda x: wavg(x, 'bundled_cents')), 'transmission': byr.apply(lambda x: wavg(x, 'tx_cents')), 'distribution': byr.apply(lambda x: wavg(x, 'dist_cents'))})
H['hist_series_iou'] = (S.xs('iou', level='G').res_rev / S.xs('iou', level='G').res_mwh * 100).reindex(H.index)
H['gen_retail'] = H.hist_series_iou - H.transmission - H.distribution
H.index.name = 'year'; H.to_csv(out / 'regulated_residential_functional_split_1990_2001.csv')

# business: functional revenue requirement x (1 - residential share), over non-residential MWh
f = fr.merge(reg[['utility', 'year', 'res_mwh', 'res_tx_share', 'res_dist_share', 'tx_rev_req_kusd', 'dist_rev_req_kusd']], on=['utility', 'year'])
f['ci_mwh'] = f.retail_mwh * f.texas_share - f.res_mwh
f['tx_ci'] = f.tx_rev_req_kusd * (1 - f.res_tx_share); f['dist_ci'] = f.dist_rev_req_kusd * (1 - f.res_dist_share)
f = f[f.year.between(1992, 2001)]
gb = f.groupby('year')[['tx_ci', 'dist_ci', 'ci_mwh']].sum()
# HL&P 1997: use the average of its 1996 and 1998 cents per kWh and the mean of those years' non-residential MWh.
h = f[(f.utility == 'Houston Lighting & Power') & f.year.isin([1996, 1998])].set_index('year')
hm = h.ci_mwh.mean(); htx = (h.tx_ci / h.ci_mwh).mean(); hd = (h.dist_ci / h.ci_mwh).mean()
oth = f[(f.year == 1997) & (f.utility != 'Houston Lighting & Power')][['tx_ci', 'dist_ci', 'ci_mwh']].sum()
gb.loc[1997] = [oth.tx_ci + htx * hm, oth.dist_ci + hd * hm, oth.ci_mwh + hm]
B = pd.DataFrame({'transmission': gb.tx_ci / gb.ci_mwh * 100, 'distribution': gb.dist_ci / gb.ci_mwh * 100, 'ci_mwh': gb.ci_mwh})
B.index.name = 'year'; B.round(4).to_csv(out / 'regulated_business_functional_split_1992_2001.csv')
print('wrote', out)
