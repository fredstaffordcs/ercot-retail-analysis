import textwrap, pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CS=ROOT/'data/competition_series'
for f in fm.findSystemFonts():
    if 'Inter' in f and 'Display' not in f: fm.fontManager.addfont(f)
plt.rcParams['font.family']='Inter'; plt.rcParams['hatch.linewidth']=1.2
cpi=pd.read_csv(ROOT/'data/reference/cpi_annual.csv',index_col=0).value; K=cpi[2025]/cpi
S=pd.read_csv(ROOT/'data/statewide_series/eia861_ownership_group_totals_1990_2025.csv').set_index(['Year','G'])
B=pd.read_csv(ROOT/'data/statewide_series/bundled_prices_by_ownership_1990_2025.csv',index_col=0)
wh=pd.read_csv(ROOT/'data/reference/ercot_wholesale_2002_2025.csv',index_col=0).usd_per_mwh/10; whR=wh*K.reindex(wh.index)
BG='#fcfcfb'; FG='#1c2421'; MU='#5d6b66'; GR='#e3e7e5'; TR='#00574d'; DI='#2fae9c'; SEC='#93d3c9'; ER='#c2570c'; BU='#1f77a8'; IOU='#b5a49a'; BUN='#d9d2cc'; WH='#7a3fb0'
W=.72
def load(key):
    if key=='res':
        d=pd.read_csv(ROOT/'data/statewide_series/competitive_residential_components_2002_2025.csv',index_col=0)
        P=pd.read_csv(ROOT/'data/statewide_series/regulated_residential_functional_split_1990_2001.csv',index_col=0)
        pub=S.xs('pub',level='G'); pubR=(pub.res_rev/pub.res_mwh*100).loc[1990:2025]
    else:
        d=pd.read_csv(ROOT/'data/statewide_series/competitive_business_components_2002_2025.csv',index_col=0)
        Q=pd.read_csv(ROOT/'data/statewide_series/regulated_business_functional_split_1992_2001.csv',index_col=0)
        P=pd.DataFrame({'hist_series_iou':B.iou_ci.loc[1990:2001]}); P['transmission']=Q.transmission; P['distribution']=Q.distribution; P['gen_retail']=P.hist_series_iou-P.transmission-P.distribution
        pubR=B.pub_ci.loc[1990:2025]
    d['other']=d.storm+d.sbf
    for c in ['retail','transmission','dist_other','dereg_transition','other','energy_retail']: d[c]=d[c]*K.reindex(d.index)
    for c in ['hist_series_iou','transmission','distribution','gen_retail']: P[c]=P[c]*K.reindex(P.index)
    return d,P,pubR*K.reindex(pubR.index)

B=pd.read_csv(CS/'wholesale_benchmarks_2002_2025.csv',index_col=0)
r=pd.read_csv(ROOT/'data/statewide_series/competitive_residential_components_2002_2025.csv',index_col=0); c=pd.read_csv(ROOT/'data/statewide_series/competitive_business_components_2002_2025.csv',index_col=0)
Y=list(range(2002,2026)); k=K.reindex(Y)
er=r.energy_retail.loc[Y]*k; ec=c.energy_retail.loc[Y]*k; g=B.gas.loc[Y]*k
E1=[y for y in range(2002,2013) if y!=2021]; E2=[y for y in range(2013,2026) if y!=2021]
fit=lambda s,idx:np.polyfit(g.loc[idx],s.loc[idx],1)
H=16.8; fy=lambda i:1-(i+.2)/H; fyt=lambda i:1-i/H
f=plt.figure(figsize=(14.4,H),dpi=100,facecolor=BG)
f.text(.05,fyt(1.3),'After 2012, the household energy charge has\nstopped responding to the cost of gas',fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
pr1,pr2=fit(er,E1),fit(er,E2); pc1,pc2=fit(ec,E1),fit(ec,E2)
sub=(f'Each dot is a year. Across 2002–12, every extra cent of gas-implied generation cost raised the household energy + retail charge by {pr1[0]:.1f}¢ and the business charge by {pc1[0]:.1f}¢. Across 2013–25, the household response is {abs(pr2[0]):.1f}¢ (a flat line at about {pr2[1]:.0f}¢) and the business response is {pc2[0]:.1f}¢. '
     f'At the 2025 gas cost the household charge is {er[2025]:.1f}¢ and the business charge {ec[2025]:.1f}¢. Winter Storm Uri year (2021) is left out.')
f.text(.05,fyt(2.95),textwrap.fill(sub,148),fontsize=13.5,color=MU,va='center',linespacing=1.5)
def base(ax):
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_facecolor(BG); ax.tick_params(length=0,labelsize=11,colors=MU); ax.grid(color=GR,lw=.8); ax.set_axisbelow(True)
    ax.set_xlim(1.4,10.6); ax.set_ylim(3,21); ax.set_xticks([2,4,6,8,10]); ax.set_xticklabels([f'{x}¢' for x in [2,4,6,8,10]]); ax.set_yticks([4,8,12,16,20]); ax.set_yticklabels([f'{x}¢' for x in [4,8,12,16,20]])
def pan(ax,s,title,p1,p2,c1):
    base(ax); ax.text(0,1.045,title,transform=ax.transAxes,fontsize=13.5,color=MU)
    xs=np.array([g.loc[E1].min(),g.loc[E1].max()]); ax.plot(xs,np.polyval(p1,xs),color=c1,lw=2,ls=(0,(4,3)),alpha=.8,zorder=3)
    xs=np.array([g.loc[E2].min(),g.loc[E2].max()]); ax.plot(xs,np.polyval(p2,xs),color=c1,lw=3.2,zorder=3)
    ax.scatter(g.loc[E1],s.loc[E1],s=80,facecolor=BG,edgecolor=c1,lw=2,zorder=6); ax.scatter(g.loc[E2],s.loc[E2],s=80,color=c1,edgecolor=BG,lw=1.2,zorder=7)
    for y in (2002,2006,2008,2012,2016,2022,2025): ax.annotate(str(y),(g[y],s[y]),xytext=(7,7),textcoords='offset points',fontsize=10,color=FG,zorder=9)
a=f.add_axes([.065,fy(9.5),.41,5.7/H]); pan(a,er,'Household energy + retail charge vs gas-implied generation cost',pr1,pr2,ER)
b=f.add_axes([.545,fy(9.5),.41,5.7/H]); pan(b,ec,'Business energy + retail charge vs gas-implied generation cost',pc1,pc2,TR)
a.set_ylabel('2025 cents per kWh',fontsize=11,color=MU); a.set_xlabel('Henry Hub gas × 7.5 MMBtu per MWh, 2025 cents per kWh',fontsize=11,color=MU,labelpad=8); b.set_xlabel('Henry Hub gas × 7.5 MMBtu per MWh, 2025 cents per kWh',fontsize=11,color=MU,labelpad=8)
a.text(.98,.04,'○ 2002–12 (dashed fit)   ● 2013–25 (solid fit)',transform=a.transAxes,ha='right',fontsize=10.5,color=MU)
f.text(.05,fy(10.7),'How much depends on the benchmark',fontsize=17,fontweight='bold',color=FG,va='center')
rows=[]
for n,l in [('spot','Same-year wholesale (market monitor all-in)'),('avg2','Two-year trailing wholesale average'),('avg3','Three-year trailing wholesale average'),('gas','Gas-implied generation cost')]:
    b_=B[n].loc[Y]*k; m1=(er-b_)[2002]; m2=(er-b_)[2025]; n1=(ec-b_)[2002]; n2=(ec-b_)[2025]
    rows.append((l,m1,m2,n1,n2))
x0=.05
f.text(x0,fy(11.3),'Markup over benchmark, 2025 cents per kWh',fontsize=12,color=MU,va='center'); 
for xx,t in [(.46,'Households'),(.62,'Businesses')]: f.text(xx,fy(11.3),t+'\n2002 → 2025',fontsize=11,color=MU,ha='left',va='center',linespacing=1.2)
for i,(l,m1,m2,n1,n2) in enumerate(rows):
    yy=fy(11.95+i*.45); f.text(x0,yy,l,fontsize=12.5,color=FG,va='center')
    f.text(.46,yy,(f'{m1:.1f} → {m2:.1f}' if m1==m1 else f'— → {m2:.1f}'),fontsize=12.5,color=ER,fontweight='bold',va='center'); f.text(.62,yy,(f'{n1:.1f} → {n2:.1f}' if n1==n1 else f'— → {n2:.1f}'),fontsize=12.5,color=TR,fontweight='bold',va='center')
note=(f'Whichever benchmark is used, the difference between the household and business markups, which is the energy + retail gap, is the same: {er[2002]-ec[2002]:.1f}¢ in 2002 and {er[2025]-ec[2025]:.1f}¢ in 2025. The benchmark only changes how it is split between “cost of power” and “markup.” Trailing averages need earlier years, so they have no 2002 value.')
f.text(.05,fy(13.95),textwrap.fill(note,128),fontsize=12.5,color=FG,va='top',linespacing=1.5)
foot=('Energy + retail = competitive retail providers’ revenue per kWh from EIA-861 minus the kWh-weighted wires charges of Oncor, CenterPoint, AEP Texas and TNMP; business = commercial and industrial customers. Gas-implied cost = Henry Hub annual spot price (EIA) × 7.5 MMBtu per MWh, an assumed heat rate, not ERCOT’s actual fuel mix. Wholesale = ERCOT market monitor all-in price; its definition changes (energy only 2002–06, energy plus ancillary services 2010–14, uplift added 2015–18). '
      'Prices in 2025 dollars (CPI-U, BLS). Fits use 11 and 12 annual points and are descriptive, not forecasts. Data and code: github.com/fredstaffordcs/ercot-retail-analysis.')
f.text(.05,fy(14.95),textwrap.fill(foot,198),fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(Line2D([.05,.95],[fy(16.0)]*2,color=GR,lw=1,transform=f.transFigure))
f.text(.05,fy(16.3),'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center'); f.text(.155,fy(16.3),'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,fy(16.3),'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
f.text(.95,fyt(.42),'7 of 8',fontsize=13,fontweight='bold',color=MU,ha='right',va='center'); f.text(.05,fyt(.42),'TEXAS ELECTRICITY PRICES: HOUSEHOLDS VS BUSINESSES',fontsize=11,color=MU,va='center',fontweight='bold')
OUT=ROOT/'charts/competition_series'; OUT.mkdir(parents=True,exist_ok=True); f.savefig(OUT/'07_energy_charge_vs_gas_cost.png',facecolor=BG)
print(pr1,pr2,pc1,pc2,(er-ec)[[2002,2025]])
