"""Parse EIA-861 historical and annual files (raw/hist_tx.pkl, raw/a_tx.pkl) into the per-utility residential price table.
Output is equivalent to data/utility_level/residential_prices_by_utility_1990_2025.csv (columns renamed). Needs the raw EIA files; see docs/sources.md.
"""
import pandas as pd, numpy as np
d='raw/'  # raw EIA-861 pickles (hist_tx.pkl, a_tx.pkl); see docs/SOURCES.md. CPI: data/reference/cpi_annual.csv

cpi=pd.read_csv('data/reference/cpi_annual.csv',index_col=0).value; K=cpi[2025]/cpi
h=pd.read_pickle(d+'hist_tx.pkl'); a=pd.read_pickle(d+'a_tx.pkl'); h=h[h.Year<=2018].copy()
def g_h(r):
    if r.grp=='comp': return 'rep'
    if r.grp=='iou': return ('rep' if r.Year<=2001 else None) if r.ercot else 'iou'
    if r.grp=='pub': return 'pub' if r.ercot else 'npub'
h['g']=h.apply(g_h,axis=1)
h=h[h.g.notna()&(h.Part=='A')|(h.g=='rep')&h.g.notna()]
a=a[a.Own.isin(['Retail Power Marketer','Cooperative','Municipal','Investor Owned'])].copy()
def g_a(r):
    if r.Own=='Retail Power Marketer': return 'rep'
    if r.BA=='ERCO': return 'pub'
    return 'iou' if r.Own=='Investor Owned' else 'npub'
a['g']=a.apply(g_a,axis=1)
# 2019 includes short-form filers; keep public power only if it files the full form in 2018 or 2020
full=set(h[(h.Year==2018)&h.g.isin(['pub','npub'])].Name)|set(a[(a.Year==2020)&a.g.isin(['pub','npub'])].Name)
a=a[~((a.Year==2019)&a.g.isin(['pub','npub'])&~a.Name.isin(full))]
c=['Year','Name','g','res_cust','res_rev','res_mwh']
D=pd.concat([h[c],a[c]]); D=D[(D.res_cust>=500)&(D.res_mwh>0)&(D.res_rev>0)]
D['c']=D.res_rev/D.res_mwh*100*D.Year.map(K)
D['c_nom']=D.res_rev/D.res_mwh*100
D.to_pickle('anim_data.pkl')
print(D.groupby(['Year','g']).size().unstack().loc[[1990,2001,2002,2011,2012,2018,2019,2020,2025]])
print(D.groupby(['Year','g']).res_cust.sum().unstack().loc[[1990,2001,2002,2025]]/1e6)
print(D[(D.Year==2002)&(D.g=='rep')][['Name','res_cust','c']].sort_values('res_cust',ascending=False).head(8))
