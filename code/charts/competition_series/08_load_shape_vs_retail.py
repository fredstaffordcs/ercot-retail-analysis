import textwrap, pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CS=ROOT/'data/competition_series'
for f in fm.findSystemFonts():
    if 'Inter' in f and 'Display' not in f: fm.fontManager.addfont(f)
plt.rcParams['font.family']='Inter'
BG='#fcfcfb'; FG='#1c2421'; MU='#5d6b66'; GR='#e3e7e5'; TR='#00574d'; ER='#c2570c'; WH='#7a3fb0'

# ---- data (all converted to 2025 cents per kWh with CPI-U) ----
cpi=pd.read_csv(ROOT/'data/reference/cpi_annual.csv',index_col=0).value; K=cpi[2025]/cpi
Y=list(range(2011,2026)); k=K.reindex(Y)
sh=pd.read_csv(CS/'load_shape_cost_by_profile_2011_2026.csv',index_col=0)   # nominal ¢/kWh; 2021 excludes Feb 10-20 (Uri)
r=pd.read_csv(ROOT/'data/statewide_series/competitive_residential_components_2002_2025.csv',index_col=0)
c=pd.read_csv(ROOT/'data/statewide_series/competitive_business_components_2002_2025.csv',index_col=0)
hw=sh.res.loc[Y]*k          # household shape cost: mean of RESLOWR and RESHIWR
bw=sh.BUSIDRRQ.loc[Y]*k     # business shape cost: interval-metered large business
bws=sh.bus_small.loc[Y]*k   # sensitivity: small business profiles
hr=r.energy_retail.loc[Y]*k; br=c.energy_retail.loc[Y]*k
ht=r.retail.loc[Y]*k; bt=c.retail.loc[Y]*k
G=pd.DataFrame({'shape':hw-bw,'shape_small':hw-bws,'er':hr-br,'tot':ht-bt})
def win(a,b): return G.loc[b[0]:b[1]].mean()-G.loc[a[0]:a[1]].mean()
x=np.array(Y); tr={kk:np.polyfit(x,G[kk],1)[0]*10 for kk in G}
w1=win((2011,2013),(2023,2025))
print(G.round(2)); print('w1',w1.round(2).to_dict()); print('trend/decade',{a:round(b,2) for a,b in tr.items()})
print('hh shape',hw[[2011,2025]].round(2).to_dict(),'bus shape',bw[[2011,2025]].round(2).to_dict(),'hh er',hr[[2011,2025]].round(2).to_dict(),'bus er',br[[2011,2025]].round(2).to_dict())

# ---- figure ----
H=18.9; fy=lambda i:1-(i+.2)/H; fyt=lambda i:1-i/H
f=plt.figure(figsize=(14.4,H),dpi=100,facecolor=BG)
f.text(.05,fyt(1.75),'Under competition, the household–business gap in retail\nenergy charges has grown four times as fast as the gap\nin what their power costs wholesale',fontsize=29,fontweight='bold',color=FG,va='center',linespacing=1.15)
sub=(f'We priced the hourly load shape of a typical household and a typical large business at ERCOT real-time prices. '
     f'Since 2011, the household’s wholesale cost has risen relative to the business’s by a trend {tr["shape"]:.1f}¢ per kWh per decade, driven by the 2022–23 scarcity years. '
     f'The household energy + retail charge has risen relative to the business charge by {tr["er"]:.1f}¢ per decade (2025 dollars). '
     f'Comparing the first and last three years gives {w1["shape"]:.1f}¢ against {w1["er"]:.1f}¢. Load shape is not why households’ retail energy charges have pulled away.')
f.text(.05,fyt(3.6),textwrap.fill(sub,142),fontsize=13.5,color=MU,va='center',linespacing=1.5)
def base(ax):
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_facecolor(BG); ax.tick_params(length=0,labelsize=11,colors=MU); ax.grid(color=GR,lw=.8,axis='y'); ax.set_axisbelow(True)
    ax.set_xlim(2010.4,2028.6); ax.set_xticks([2011,2014,2017,2020,2023,2025])
a=f.add_axes([.065,fy(10.9),.41,5.6/H]); base(a)
a.text(0,1.05,'Retail energy charge (solid) and wholesale cost of each\nclass’s load shape (dashed), 2025 cents per kWh',transform=a.transAxes,fontsize=13,color=MU,linespacing=1.3)
a.plot(Y,hr,color=ER,lw=3.2); a.plot(Y,br,color=TR,lw=3.2)
a.plot(Y,hw,color=ER,lw=2,ls=(0,(4,2.5))); a.plot(Y,bw,color=TR,lw=2,ls=(0,(4,2.5)))
a.set_ylim(0,13.5); a.set_yticks([0,3,6,9,12]); a.set_yticklabels([f'{v}¢' for v in [0,3,6,9,12]])
lab=lambda y,t,col,w='bold': a.text(2025.5,y,t,color=col,fontsize=11.5,fontweight=w,va='center',linespacing=1.2)
lab(hr[2025],f'Household\nretail charge\n{hr[2025]:.1f}¢',ER); lab(6.1,f'Business retail\ncharge {br[2025]:.1f}¢',TR)
lab(4.55,f'Household\nwholesale {hw[2025]:.1f}¢',ER,'normal'); lab(2.75,f'Business\nwholesale {bw[2025]:.1f}¢',TR,'normal')
b=f.add_axes([.56,fy(10.9),.39,5.6/H]); base(b)
b.text(0,1.05,'Household minus business: retail (solid) and wholesale\n(dashed), 2025 cents per kWh',transform=b.transAxes,fontsize=13,color=MU)
b.plot(Y,G['shape'],color=FG,lw=2,ls=(0,(4,2.5)),zorder=4)
b.plot(Y,G['er'],color=FG,lw=3.2,zorder=4)
for kk in ['er','shape']:
    p=np.polyfit(x,G[kk],1); b.plot([2011,2025],np.polyval(p,[2011,2025]),color=MU,lw=1.2,ls=(0,(1,2)),zorder=3)
b.set_ylim(0,8.2); b.set_yticks([0,2,4,6,8]); b.set_yticklabels([f'{v}¢' for v in [0,2,4,6,8]]); b.set_xlim(2010.4,2029.5)
b.text(2025.6,G.er[2025],f'Retail energy\ncharge gap\n{G.er[2025]:.1f}¢',color=FG,fontsize=11.5,fontweight='bold',va='center',linespacing=1.2)
b.text(2025.6,G['shape'][2025]+.45,f'Wholesale\nload-shape\ngap {G["shape"][2025]:.1f}¢',color=FG,fontsize=11.5,fontweight='normal',va='center',linespacing=1.2)
b.text(2011,7.6,f'Gray dotted lines: linear trend. Retail gap +{tr["er"]:.1f}¢ per decade;\nload-shape gap +{tr["shape"]:.1f}¢ per decade',fontsize=10.5,color=MU,va='center',linespacing=1.3)

# ---- table ----
f.text(.05,fy(12.15),'The retail gap grew more than the load-shape gap whichever years are compared',fontsize=17,fontweight='bold',color=FG,va='center')
cols=[(.47,'Wholesale\nload-shape gap'),(.62,'Retail energy\ncharge gap'),(.77,'Total retail\nprice gap')]
f.text(.05,fy(12.8),'Change in household minus business, 2025 cents per kWh',fontsize=12,color=MU,va='center')
for xx,t in cols: f.text(xx,fy(12.8),t,fontsize=11,color=MU,va='center',linespacing=1.2)
rows=[('First 3 years vs last 3 (2011–13 vs 2023–25)',w1),('First 5 years vs last 5 (2011–15 vs 2021–25)',win((2011,2015),(2021,2025))),
      ('Calm years only (2012–17 vs 2024–25)',win((2012,2017),(2024,2025))),('Linear trend 2011–25, per decade',pd.Series(tr))]
for i,(l,v) in enumerate(rows):
    yy=fy(13.5+i*.45); f.text(.05,yy,l,fontsize=12.5,color=FG,va='center')
    for (xx,_),kk,col in zip(cols,['shape','er','tot'],[FG,FG,FG]): f.text(xx,yy,f'{v[kk]:+.1f}¢',fontsize=12.5,color=col,fontweight='bold',va='center')
note=('The wholesale shape gap jumps in scarcity years (2011, 2019, 2022, 2023), when evening and summer-peak prices spike, and falls back afterward. '
      'Retail charges lag wholesale because most customers are on fixed-price contracts, so the five-year comparison, which puts the 2022–23 spike in its later period, '
      'gives load shape its largest share, about half. In calm years, load shape explains almost none of the change.')
f.text(.05,fy(15.4),textwrap.fill(note,146),fontsize=12.5,color=FG,va='top',linespacing=1.5)
foot=('Wholesale cost = ERCOT backcasted 15-minute load profiles (modeled, run on actual weather) priced at real-time load-zone settlement prices, '
      'weather zones weighted by native load; energy only, no ancillary services or hedging costs. Household = average of the gas-heat and electric-heat '
      'residential profiles (equal weights; rooftop-solar homes excluded). Business = interval-metered large-business profile; using the small-business '
      f'profiles instead makes the wholesale gap smaller in level, with the same trend (+{tr["shape_small"]:.1f}¢ per decade). 2021 excludes Winter Storm Uri (Feb 10–20). '
      'Retail energy charge = competitive retail providers’ revenue per kWh from EIA-861 minus the kWh-weighted wires charges of Oncor, CenterPoint, '
      'AEP Texas and TNMP; business = commercial and industrial. Total retail price includes wires charges. Prices adjusted to 2025 dollars with CPI-U (BLS). '
      'Data and code: github.com/fredstaffordcs/ercot-retail-analysis.')
f.text(.05,fy(16.75),textwrap.fill(foot,200),fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(plt.Line2D([.05,.95],[fy(17.85),fy(17.85)],color=GR,lw=1))
f.text(.05,fy(18.15),'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center'); f.text(.155,fy(18.15),'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,fy(18.15),'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
f.text(.95,fyt(.42),'8 of 8',fontsize=13,fontweight='bold',color=MU,ha='right',va='center'); f.text(.05,fyt(.42),'TEXAS ELECTRICITY PRICES: HOUSEHOLDS VS BUSINESSES',fontsize=11,color=MU,va='center',fontweight='bold')
OUT=ROOT/'charts/competition_series'; OUT.mkdir(parents=True,exist_ok=True); f.savefig(OUT/'08_load_shape_vs_retail.png',facecolor=BG)
