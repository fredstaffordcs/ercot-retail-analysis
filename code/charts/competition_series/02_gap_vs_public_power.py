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

dr,Pr,pr=load('res'); dc,Pc,pc=load('ci')
def ser(d,P): return pd.concat([P.hist_series_iou.loc[1990:2001],d.retail.loc[2002:2025]])
hs=ser(dr,Pr); bs=ser(dc,Pc); phs=pr.loc[1990:2025]; pbs=pc.loc[1990:2025]
ratio=hs/bs; pratio=phs/pbs; gap=hs-bs; pgap=phs-pbs
H=16.7; fy=lambda i:1-(i+.2)/H; fyt=lambda i:1-i/H
f=plt.figure(figsize=(14.4,H),dpi=100,facecolor=BG)
f.text(.05,fyt(.42),'TEXAS ELECTRICITY PRICES: HOUSEHOLDS VS BUSINESSES',fontsize=11,color=MU,va='center',fontweight='bold'); f.text(.95,fyt(.42),'2 of 8',fontsize=13,fontweight='bold',color=MU,ha='right',va='center')
f.text(.05,fyt(1.75),f'Under competition, ERCOT households’ price\npremium over businesses has grown from {ratio[2001]:.2f}× to {ratio[2025]:.2f}×;\nin public power it barely moved',fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
sub=(f'Household price divided by business price, in the ERCOT region. In 2001, the last year of regulated rates, households paid {ratio[2001]:.2f} times the business price; in 2025, {ratio[2025]:.2f} times. At ERCOT’s municipal utilities and co-ops, which are outside competition, the ratio went from {pratio[2001]:.2f} to {pratio[2025]:.2f}. '
     f'In cents, the household premium grew from {gap[2001]:.1f}¢ to {gap[2025]:.1f}¢ per kWh in competitive ERCOT and from {pgap[2001]:.1f}¢ to {pgap[2025]:.1f}¢ in public power.')
f.text(.05,fyt(3.45),textwrap.fill(sub,152),fontsize=13,color=MU,va='center',linespacing=1.5)
def base(ax,x1=2031):
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_facecolor(BG); ax.tick_params(length=0,labelsize=11,colors=MU); ax.grid(axis='y',color=GR,lw=.8); ax.set_axisbelow(True)
    ax.axvspan(1989.5,2001.5,color='#eef0ef',zorder=0,lw=0); ax.set_xlim(1989.4,x1)
    tk=[1990,2001,2010,2020,2025]; ax.set_xticks(tk); ax.set_xticklabels([str(t) for t in tk],fontsize=11,color=FG)
a=f.add_axes([.055,fy(10.0),.76,5.3/H]); base(a,2025.8)
a.text(0,1.05,'Household price ÷ business price',transform=a.transAxes,fontsize=13,color=MU)
a.set_ylim(.9,2.6); a.set_yticks([1,1.5,2,2.5]); a.set_yticklabels(['1×','1.5×','2×','2.5×']); a.axhline(1,color=MU,lw=.9,ls=(0,(4,3)),zorder=2)
a.text(1995.5,2.55,'Regulated monopolies\n(all utilities)',ha='center',va='top',fontsize=10.5,color=MU,linespacing=1.2)
a.plot(ratio.index,ratio.values,color=ER,lw=3.4,zorder=6,solid_capstyle='round'); a.plot(pratio.index,pratio.values,color=BU,lw=2.6,zorder=6,solid_capstyle='round')
a.scatter([2001],[ratio[2001]],s=60,color=ER,edgecolor=BG,lw=1.5,zorder=8); a.scatter([2001],[pratio[2001]],s=60,color=BU,edgecolor=BG,lw=1.5,zorder=8)
a.text(2001.4,ratio[2001]+.13,f'{ratio[2001]:.2f}×',color=ER,fontsize=11,fontweight='bold',ha='center'); a.text(2001.4,pratio[2001]-.15,f'{pratio[2001]:.2f}×',color=BU,fontsize=11,fontweight='bold',ha='center')
a.text(2026.2,ratio[2025],f'ERCOT competitive\nmarket {ratio[2025]:.2f}×',color=ER,fontsize=11.5,fontweight='bold',va='center',linespacing=1.15)
a.text(2026.2,pratio[2025],f'ERCOT public power\n{pratio[2025]:.2f}×',color=BU,fontsize=11.5,fontweight='bold',va='center',linespacing=1.15)
f.text(.05,fy(10.75),'The same gap in cents',fontsize=17,fontweight='bold',color=FG,va='center')
b=f.add_axes([.055,fy(14.0),.76,2.7/H]); base(b,2025.8)
b.text(0,1.08,'Household price minus business price, 2025 cents per kWh',transform=b.transAxes,fontsize=13,color=MU)
b.set_ylim(0,12); b.set_yticks([0,4,8,12]); b.set_yticklabels(['0','4¢','8¢','12¢'])
b.plot(gap.index,gap.values,color=ER,lw=3.4,zorder=6,solid_capstyle='round'); b.plot(pgap.index,pgap.values,color=BU,lw=2.6,zorder=6,solid_capstyle='round')
b.text(2026.2,gap[2025],f'{gap[2025]:.1f}¢',color=ER,fontsize=11.5,fontweight='bold',va='center'); b.text(2026.2,pgap[2025],f'{pgap[2025]:.1f}¢',color=BU,fontsize=11.5,fontweight='bold',va='center')
foot=('Revenue per kWh from EIA-861. Through 2001: investor-owned utilities in the ERCOT region (TU Electric, HL&P, CPL, WTU, TNMP), bundled; from 2002: competitive retail providers. Business = commercial and industrial customers (ratios here use the same business series as chart 1). Public power = ERCOT-region municipal utilities and co-ops, bundled, with business = all non-residential. '
      'Prices in the lower panel are adjusted to 2025 dollars with CPI-U (BLS); the ratio is unaffected by inflation. The 2002 reclassification of public-authority and lighting customers lowers business prices from 2002 on by about 0.2¢, which overstates the 2025 ratio by about 0.07 relative to 2001. Chart 4 adds Texas utilities outside ERCOT and the US. Data and code: github.com/fredstaffordcs/ercot-retail-analysis.')
f.text(.05,fy(14.35),textwrap.fill(foot,198),fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(Line2D([.05,.95],[fy(15.95)]*2,color=GR,lw=1,transform=f.transFigure))
f.text(.05,fy(16.25),'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center'); f.text(.155,fy(16.25),'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,fy(16.25),'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
OUT=ROOT/'charts/competition_series'; OUT.mkdir(parents=True,exist_ok=True); f.savefig(OUT/'02_gap_vs_public_power.png',facecolor=BG)
print(ratio[[2001,2025]].round(2).to_dict(),pratio[[2001,2025]].round(2).to_dict(),gap[[2001,2025]].round(2).to_dict(),pgap[[2001,2025]].round(2).to_dict())
