import textwrap, pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for f in fm.findSystemFonts():
    if 'Inter' in f and 'Display' not in f: fm.fontManager.addfont(f)
plt.rcParams['font.family']='Inter'; plt.rcParams['hatch.linewidth']=1.2
d=pd.read_csv(ROOT/'data/statewide_series/competitive_residential_components_2002_2025.csv',index_col=0); d['other']=d.storm+d.sbf
P=pd.read_csv(ROOT/'data/statewide_series/regulated_residential_functional_split_1990_2001.csv',index_col=0)
cpi=pd.read_csv(ROOT/'data/reference/cpi_annual.csv',index_col=0).value; K=cpi[2025]/cpi
S=pd.read_csv(ROOT/'data/statewide_series/eia861_ownership_group_totals_1990_2025.csv').set_index(['Year','G'])
pub=S.xs('pub',level='G'); pubR=(pub.res_rev/pub.res_mwh*100).loc[1990:2025]; pubR=pubR*K.reindex(pubR.index)
for c in ['retail','transmission','dist_other','dereg_transition','other','energy_retail']: d[c]=d[c]*K.reindex(d.index)
for c in ['hist_series_iou','transmission','distribution','gen_retail']: P[c]=P[c]*K.reindex(P.index)
wh=pd.read_csv(ROOT/'data/reference/ercot_wholesale_2002_2025.csv',index_col=0).usd_per_mwh/10; whR=wh*K.reindex(wh.index)
BG='#fcfcfb'; FG='#1c2421'; MU='#5d6b66'; GR='#e3e7e5'; TR='#00574d'; DI='#2fae9c'; SEC='#93d3c9'; OT='#6b7a75'; ER='#c2570c'; BU='#1f77a8'; IOU='#b5a49a'; BUN='#d9d2cc'; WH='#7a3fb0'
W=.72
f=plt.figure(figsize=(14.4,12.8),dpi=100,facecolor=BG)
f.text(.05,.945,'Texas household power prices in today’s dollars:\ntransmission, distribution and the rest',fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
r25=d.loc[2025]
f.text(.05,.862,textwrap.fill(f'Average residential price in the ERCOT region, in 2025 cents per kWh (CPI-U). Through 2001: investor-owned utilities’ bundled price, with transmission and distribution estimated from their costs (1992–2001). '
       f'From 2002: competitive retail providers’ price, split into the wires companies’ charges and energy + retail. In 2025, transmission was {r25.transmission:.1f}¢, distribution and other {r25.dist_other:.1f}¢, energy + retail {r25.energy_retail:.1f}¢.',150),fontsize=13,color=MU,va='center',linespacing=1.5)
items=[('Transmission',TR,'box'),('Distribution + other',DI,'box'),('Transition charges (net)',SEC,'hatch'),
       ('Energy + retail (competitive)',ER,'box'),('Generation + retail (regulated)',IOU,'box'),('Regulated, bundled (no split)',BUN,'box'),('Public power',BU,'line'),('Wholesale (all-in)',WH,'line')]
pos=[(.05,.8),(.17,.8),(.335,.8),(.53,.8),(.05,.775),(.29,.775),(.53,.775),(.72,.775)]
for (lab,c,k),(x,ly) in zip(items,pos):
    if k=='line':
        f.add_artist(Line2D([x-.002,x+.022],[ly,ly],color=c,lw=2.8,transform=f.transFigure)); f.add_artist(Line2D([x+.01],[ly],marker='o',color=c,ms=6,transform=f.transFigure))
    else: f.patches.append(plt.Rectangle((x,ly-.006),.014,.012,transform=f.transFigure,fc=c,ec=TR if k=='hatch' else 'none',hatch='///' if k=='hatch' else None,lw=0))
    f.text(x+(.03 if k=='line' else .02),ly,lab,fontsize=11.2,color=FG,va='center')
ax=f.add_axes([.065,.215,.885,.53]); ax.set_facecolor(BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_ylim(-1.2,27); ax.set_xlim(1989.4,2026.6); ax.set_yticks(range(0,28,3)); ax.axhline(0,color=MU,lw=.8,zorder=2); ax.tick_params(length=0,labelsize=11,colors=MU)
ax.set_xticks([1990,1995,2001,2005,2010,2015,2020,2025]); ax.set_xticklabels(['1990','1995','2001','2005','2010','2015','2020','2025'],fontsize=12,color=FG)
ax.grid(axis='y',color=GR,lw=.8); ax.set_axisbelow(True)
ax.axvspan(1989.5,2001.5,color='#eef0ef',zorder=0,lw=0); ax.text(1995.5,26.3,'Regulated monopolies: bundled price;\ntransmission and distribution are\ncost-of-service estimates (1992–2001)',ha='center',va='top',fontsize=11,color=MU,linespacing=1.25)
for y,r in P.iterrows():
    if np.isnan(r.transmission): ax.bar(y,r.hist_series_iou,W,color=BUN,zorder=3,lw=0)
    else:
        ax.bar(y,r.transmission,W,color=TR,zorder=3,lw=0); ax.bar(y,r.distribution,W,bottom=r.transmission,color=DI,zorder=3,lw=0)
        ax.bar(y,r.gen_retail,W,bottom=r.transmission+r.distribution,color=IOU,zorder=3,lw=0)
        ax.plot([y-W/2,y+W/2],[r.transmission+r.distribution]*2,color=BG,lw=1.6,zorder=4)
    if y in (1990,2001): ax.text(y,r.hist_series_iou+.25,f'{r.hist_series_iou:.1f}',ha='center',va='bottom',fontsize=11.5,fontweight='bold',color=FG,zorder=8)
for y,r in d.iterrows():
    ax.bar(y,r.transmission,W,color=TR,zorder=3,lw=0); top=r.transmission
    ax.bar(y,r.dist_other,W,bottom=top,color=DI,zorder=3,lw=0); top+=r.dist_other
    tr=r.dereg_transition
    if tr>0.005: ax.bar(y,tr,W,bottom=top,color=SEC,edgecolor=TR,hatch='///',zorder=3,lw=0); top+=tr
    elif tr<-0.005: ax.bar(y,tr,W,bottom=0,color=SEC,edgecolor=TR,hatch='///',zorder=3,lw=0)
    if r.other>0.005: ax.bar(y,r.other,W,bottom=top,color=DI,zorder=3,lw=0); top+=r.other
    ax.bar(y,r.energy_retail,W,bottom=top,color=ER,zorder=3,lw=0); ax.plot([y-W/2,y+W/2],[top]*2,color=BG,lw=1.6,zorder=4)
    if y in (2006,2017,2025): ax.text(y,top+r.energy_retail+.25,f'{r.retail:.1f}',ha='center',va='bottom',fontsize=11.5,fontweight='bold',color=FG,zorder=8)
    if y==2025:
        ax.text(y,r.transmission/2,f'{r.transmission:.1f}',ha='center',va='center',fontsize=9.5,fontweight='bold',color='white',zorder=8)
        ax.text(y,top+r.energy_retail/2,f'{r.energy_retail:.1f}',ha='center',va='center',fontsize=10,fontweight='bold',color='white',zorder=8)
ax.annotate('Transition credits\n(net, 2002–04)',(2003,-0.3),xytext=(2006.8,-0.9),fontsize=9.5,color=MU,va='center',arrowprops=dict(arrowstyle='-',color=MU,lw=.8))
ax.plot(list(pubR.index),pubR.values,color=BU,lw=2.8,zorder=6,solid_capstyle='round'); ax.scatter(list(pubR.index),pubR.values,s=30,color=BU,edgecolor=BG,lw=1.2,zorder=7)
ax.plot(list(whR.index),whR.values,color=WH,lw=2.4,zorder=6,solid_capstyle='round'); ax.scatter(list(whR.index),whR.values,s=24,color=WH,edgecolor=BG,lw=1.1,zorder=7)
bb=lambda c:dict(boxstyle='round,pad=.18',fc='white',ec=c,lw=.8)
for y,dx,dy in [(2008,0,14),(2021,34,0),(2025,24,-2)]:
    ax.annotate(f'{whR[y]:.1f}',(y,whR[y]),xytext=(dx,dy),textcoords='offset points',ha='center',va='center',fontsize=11,fontweight='bold',color=WH,zorder=9,bbox=bb(WH))
ax.annotate('Winter Storm Uri',(2021,whR[2021]),xytext=(34,18),textcoords='offset points',ha='center',va='center',fontsize=10,color=WH)
for y in (1990,2025):
    ax.annotate(f'{pubR[y]:.1f}',(y,pubR[y]),xytext=(24,0) if y==2025 else (0,-20),textcoords='offset points',ha='center',va='center',fontsize=11,fontweight='bold',color=BU,zorder=9,bbox=bb(BU))
foot=('Adjusted to 2025 dollars with CPI-U (BLS). 1990–2001: residential revenue per kWh of investor-owned utilities in the ERCOT region (TU Electric, HL&P, CPL, WTU, TNMP), bundled, EIA-861. Their transmission and distribution for 1992–2001 are cost-of-service estimates: '
      'O&M, depreciation, return on net plant and taxes by function (FERC Form 1; EIA Financial Statistics for 1992–93), times residential shares from the 2000 unbundling dockets and 2002 wires data; no split for 1990–91; HL&P 1997 averaged from 1996 and 1998. '
      '2002–2025: competitive retail providers’ residential revenue per kWh (EIA-861) minus the kWh-weighted wires charges of Oncor, CenterPoint, AEP Texas and TNMP (FERC Form 1, SEC filings, AEP earnings reports, bond servicer reports, PUCT). '
      'Distribution + other includes storm bonds and the state System Benefit Fund fee. Transmission = each wires company’s ERCOT transmission bill (4CP load × postage-stamp rate, PUCT matrices, plus in-year updates) × residential allocation factor (TCRF filings) ÷ residential kWh. Public power = ERCOT municipal utilities and co-ops, bundled. '
      'Wholesale: ERCOT market monitor all-in price (energy-only 2002–06; energy plus ancillary services 2010–18).')
f.text(.05,.168,textwrap.fill(foot,198),fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(Line2D([.05,.95],[.036,.036],color=GR,lw=1,transform=f.transFigure))
f.text(.05,.018,'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center'); f.text(.155,.018,'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,.018,'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
f.savefig(str(ROOT/'charts'/'price_history_real_tx_dist_1990_2025.png'),facecolor=BG)
print(d.loc[[2002,2010,2019,2025],['retail','transmission','dist_other','energy_retail']].round(2)); print(P.loc[[1992,2001]].round(2))
