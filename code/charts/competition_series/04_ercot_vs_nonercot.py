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

NI='#7d6a5b'; US='#5d6b66'
n=pd.read_csv(CS/'nonercot_texas_iou_series_1990_2025.csv',index_col=0); u=pd.read_csv(CS/'us_series_1990_2025.csv',index_col=0)
def rb(g):
    x=S.xs(g,level='G'); return x.res_rev/x.res_mwh*100,(x.tot_rev-x.res_rev)/(x.tot_mwh-x.res_mwh)*100
er,eb=rb('comp'); ir,ib=rb('iou'); pr,pb=rb('pub')
ER_r=pd.concat([ir.loc[:2001],er.loc[2002:]]); ER_b=pd.concat([ib.loc[:2001],eb.loc[2002:]])
yrs=range(1990,2026)
R={'ERCOT competitive market':(ER_r/ER_b,ER),'Non-ERCOT Texas utilities':(n.ratio,NI),'ERCOT public power':(pr/pb,BU),'United States':(u.ratio,US)}
H=18.7; fy=lambda i:1-(i+.6)/H; fyt=lambda i:1-i/H
f=plt.figure(figsize=(14.4,H),dpi=100,facecolor=BG)
f.text(.05,fyt(1.75),'In 2025, business prices were the same inside and\noutside ERCOT’s competitive market; households\npaid 26% more inside it',fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
yrs_hi=int((ER_r.loc[2002:2025]>n.res_p.loc[2002:2025]).sum())
sub=(f'Business prices: {ER_b[2025]:.1f}¢ per kWh in ERCOT and {n.bus_p[2025]:.1f}¢ outside it. Household prices: {ER_r[2025]:.1f}¢ vs {n.res_p[2025]:.1f}¢. The household-to-business price ratio went from {ER_r[2001]/ER_b[2001]:.2f} to {ER_r[2025]/ER_b[2025]:.2f} in ERCOT between 2001, the last year of regulation, and 2025, from {n.ratio[2001]:.2f} to {n.ratio[2025]:.2f} for other Texas utilities and from {u.ratio[2001]:.2f} to {u.ratio[2025]:.2f} for the US. ERCOT public power went from {(pr/pb)[2001]:.2f} to {(pr/pb)[2025]:.2f}. '
     f'The widening is not unique to ERCOT. But ERCOT households have paid more than households outside it in every year since competition began, by 2% to 57% (26% in 2025).')
f.text(.05,fyt(3.45),textwrap.fill(sub,152),fontsize=13,color=MU,va='center',linespacing=1.5)
def base(ax):
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_facecolor(BG); ax.tick_params(length=0,labelsize=11,colors=MU); ax.grid(axis='y',color=GR,lw=.8); ax.set_axisbelow(True)
    ax.axvspan(1989.5,2001.5,color='#eef0ef',zorder=0,lw=0); ax.set_xlim(1989.4,2030.5)
    tk=[1990,2001,2010,2020,2025]; ax.set_xticks(tk); ax.set_xticklabels([str(t) for t in tk],fontsize=11,color=FG)
a=f.add_axes([.055,fy(10.3),.76,6.0/H]); base(a); a.set_xlim(1989.4,2025.8)
a.text(0,1.05,'Household price ÷ business price',transform=a.transAxes,fontsize=13,color=MU)
a.set_ylim(.9,2.6); a.set_yticks([1,1.5,2,2.5]); a.set_yticklabels(['1×','1.5×','2×','2.5×']); a.axhline(1,color=MU,lw=.9,ls=(0,(4,3)),zorder=2)
a.text(1995.5,2.55,'Regulated monopolies\n(all utilities)',ha='center',va='top',fontsize=10.5,color=MU,linespacing=1.2)
for k,(s,c) in R.items():
    s=s.loc[1990:2025]; ls=(0,(4,2)) if k=='United States' else '-'
    a.plot(s.index,s.values,color=c,lw=3.2 if 'ERCOT comp' in k else 2.4,ls=ls,zorder=6,solid_capstyle='round')
lab={'ERCOT competitive market':(ER_r/ER_b)[2025],'Non-ERCOT Texas utilities':n.ratio[2025],'ERCOT public power':(pr/pb)[2025],'United States':u.ratio[2025]}
ys={'ERCOT competitive market':lab['ERCOT competitive market'],'Non-ERCOT Texas utilities':1.93,'United States':1.5,'ERCOT public power':1.25}
for k,(s,c) in R.items():
    a.text(2026.2,ys[k],f"{k}\n{lab[k]:.2f}×",color=c,fontsize=11.5,fontweight='bold',va='center',linespacing=1.15)
f.text(.05,fy(10.9),'Prices, in 2025 cents per kWh',fontsize=17,fontweight='bold',color=FG,va='center')
nudge={ER:0,NI:0,BU:0}
def lvl(ax,which,t):
    nudge.update({ER:(-.9 if which=='b' else 0),NI:(.9 if which=='b' else -.5),BU:(0 if which=='b' else -.7)})
    base(ax); ax.set_xlim(1989.4,2025.6)
    ax.text(0,1.05,t,transform=ax.transAxes,fontsize=13,color=MU)
    if which=='h': E=ER_r; N=n.res_p; P=pr
    else: E=ER_b; N=n.bus_p; P=pb
    for s,c,lw in [(E,ER,3.2),(N,NI,2.4),(P,BU,2.4)]:
        s=(s*K.reindex(s.index)).loc[1990:2025]; ax.plot(s.index,s.values,color=c,lw=lw,zorder=6,solid_capstyle='round'); ax.text(2025.5,s[2025]+nudge[c],f'{s[2025]:.1f}¢',color=c,fontsize=11.5,fontweight='bold',va='center')
    ax.set_ylim(0,24); ax.set_yticks(range(0,25,6)); ax.set_xlim(1989.4,2028.5)
b1=f.add_axes([.055,fy(15.35),.43,3.8/H]); lvl(b1,'h','Households')
b2=f.add_axes([.515,fy(15.35),.43,3.8/H]); lvl(b2,'b','Businesses (all non-residential)'); b2.sharey=None
for x,t,c in [(.40,'ERCOT',ER),(.47,'Non-ERCOT Texas utilities',NI),(.655,'ERCOT public power',BU)]:
    f.add_artist(Line2D([x,x+.017],[fy(10.9)]*2,color=c,lw=3,transform=f.transFigure)); f.text(x+.022,fy(10.9),t,color=c,fontsize=12,fontweight='bold',va='center')
foot=('Revenue per kWh from EIA-861 bundled sales; business = commercial, industrial and other non-residential customers; prices adjusted to 2025 dollars with CPI-U (BLS), ratios are unaffected by inflation. ERCOT: investor-owned utilities in the ERCOT region (TU Electric, HL&P, CPL, WTU, TNMP) through 2001, competitive retail providers from 2002. '
      'Non-ERCOT Texas utilities: Texas sales of El Paso Electric, Southwestern Public Service, SWEPCO and Gulf States/Entergy Texas, all vertically integrated. ERCOT public power: municipal utilities and co-ops. United States: EIA Monthly Energy Review, all sectors. '
      'Holding the commercial/industrial mix fixed changes the Texas non-ERCOT ratio by at most 0.06. In 2002, public-authority and lighting customers drop out of ERCOT’s reported data as competition begins, which lowers the ERCOT business price from 2002 on by about 0.2¢ and overstates the rise in its 2025 ratio by about 0.07. '
      'Part of the widening everywhere may be mechanical: when energy costs fall, fixed wires costs are a larger share of a household bill. Data and code: github.com/fredstaffordcs/ercot-retail-analysis.')
f.text(.05,fy(15.8),textwrap.fill(foot,198),fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(Line2D([.05,.95],[fy(17.5)]*2,color=GR,lw=1,transform=f.transFigure))
f.text(.05,fy(17.85),'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center'); f.text(.155,fy(17.85),'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,fy(17.85),'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
f.text(.95,fyt(.42),'4 of 8',fontsize=13,fontweight='bold',color=MU,ha='right',va='center'); f.text(.05,fyt(.42),'TEXAS ELECTRICITY PRICES: HOUSEHOLDS VS BUSINESSES',fontsize=11,color=MU,va='center',fontweight='bold')
OUT=ROOT/'charts/competition_series'; OUT.mkdir(parents=True,exist_ok=True); f.savefig(OUT/'04_ercot_vs_nonercot.png',facecolor=BG)
