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
def ser(d,P):
    s=pd.concat([P.hist_series_iou.loc[1990:2001],d.retail.loc[2002:2025]]); return s
hs=ser(dr,Pr); bs=ser(dc,Pc); phs=pr.loc[1990:2025]; pbs=pc.loc[1990:2025]
H=15.3; fy=lambda i:1-i/H
f=plt.figure(figsize=(14.4,H),dpi=100,facecolor=BG)
f.text(.05,fy(1.3),'Since Texas introduced retail competition, household prices\n'+f'are up just {hs[2025]/hs[2001]-1:.0%}; business prices are down {1-bs[2025]/bs[2001]:.0%}',fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
sub=(f'In 2025 dollars, the average household price was {hs[2001]:.1f}¢ per kWh in 2001, the last year of regulated rates before retail competition began, and {hs[2025]:.1f}¢ in 2025. The average business price went from {bs[2001]:.1f}¢ to {bs[2025]:.1f}¢. '
     f'Public power (municipal utilities and co-ops, which are outside competition) fell for both: households from {phs[2001]:.1f}¢ to {phs[2025]:.1f}¢ ({phs[2025]/phs[2001]-1:.0%}), businesses from {pbs[2001]:.1f}¢ to {pbs[2025]:.1f}¢ ({pbs[2025]/pbs[2001]-1:.0%}).')
f.text(.05,fy(3.05),textwrap.fill(sub,140),fontsize=13.5,color=MU,va='center',linespacing=1.5)
def base(ax,x1):
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_facecolor(BG); ax.tick_params(length=0,labelsize=11,colors=MU); ax.grid(axis='y',color=GR,lw=.8); ax.set_axisbelow(True)
    ax.axvspan(1989.5,2001.5,color='#eef0ef',zorder=0,lw=0); ax.set_xlim(1989.4,x1)
    tk=[1990,2001,2010,2020,2025]; ax.set_xticks(tk); ax.set_xticklabels([str(t) for t in tk],fontsize=11,color=FG)
a=f.add_axes([.055,fy(11.0),.42,5.9/H]); base(a,2031)
a.text(0,1.05,'Average retail price, 2025 cents per kWh',transform=a.transAxes,fontsize=13,color=MU)
a.set_ylim(0,26); a.set_yticks(range(0,25,6)); a.text(1995.5,25.5,'Regulated monopolies',ha='center',va='top',fontsize=10.5,color=MU)
for s,c,lw,ls,l,dy in [(hs,ER,3.2,'-','Households',0),(bs,TR,3.2,'-','Businesses',0),(phs,BU,1.8,'-','Public power\nhouseholds',0.4),(pbs,BU,1.8,(0,(4,2)),'Public power\nbusinesses',-0.6)]:
    a.plot(s.index,s.values,color=c,lw=lw,ls=ls,zorder=6,solid_capstyle='round'); a.text(2025.6,s[2025]+dy,f'{l}\n{s[2025]:.1f}¢' if 'Public' not in l else f'{l} {s[2025]:.1f}¢',color=c,fontsize=10.5 if 'Public' in l else 11.5,fontweight='bold',va='center',linespacing=1.1)
b=f.add_axes([.555,fy(11.0),.39,5.9/H]); base(b,2029.5)
b.text(0,1.05,'Same prices, 2001 (last regulated year) = 100',transform=b.transAxes,fontsize=13,color=MU)
ix=lambda s:s/s[2001]*100
b.set_xlim(2000.4,2029.5); b.axvspan(1989.5,2001.5,color=BG,zorder=0); b.set_xticks([2001,2010,2020,2025]); b.set_xticklabels(['2001','2010','2020','2025'])
b.set_ylim(40,185); b.set_yticks([50,100,150]); b.axhline(100,color=MU,lw=.9,ls=(0,(4,3)),zorder=3)
for s,c,lw,ls,l,dy in [(hs,ER,3.2,'-','Households',3),(bs,TR,3.2,'-','Businesses',0),(phs,BU,1.8,'-','Public power households',3),(pbs,BU,1.8,(0,(4,2)),'Public power businesses',-3)]:
    v=ix(s).loc[2001:2025]; b.plot(v.index,v.values,color=c,lw=lw,ls=ls,zorder=6,solid_capstyle='round'); b.text(2025.5,v[2025]+dy,f'{l if "Public" not in l else l.replace("Public power ","PP ")} {v[2025]:.0f}',color=c,fontsize=10.5,fontweight='bold',va='center')
f.text(.05,fy(11.65),'The household–business difference',fontsize=17,fontweight='bold',color=FG,va='center')
txt=(f'• The household price was {hs[2001]/bs[2001]:.2f} times the business price in 2001 and {hs[2025]/bs[2025]:.2f} times in 2025.\n'
     '• Business prices fell after the 2006–08 gas-price spike and kept falling. Household prices fell with them until about 2016, then recovered.\n'
     '• This chart shows what happened, not why. The next charts split the price into energy, transmission and distribution, and compare ERCOT with utilities outside it.')
f.text(.05,fy(12.0),'\n'.join(textwrap.fill(l,138,subsequent_indent='   ') for l in txt.split('\n')),fontsize=12.5,color=FG,va='top',linespacing=1.55)
foot=('Revenue per kWh from EIA-861. Through 2001: investor-owned utilities in the ERCOT region (TU Electric, HL&P, CPL, WTU, TNMP), bundled. From 2002: competitive retail providers. Business = commercial and industrial customers. Public power = ERCOT-region municipal utilities and co-ops, bundled. Prices adjusted to 2025 dollars with CPI-U (BLS). '
      'In 2002 public-authority and lighting customers drop out of the reported data, which lowers the 2002 and later business prices by about 0.2¢, so the business decline since 2001 is overstated by about 2 percentage points. Data and code: github.com/fredstaffordcs/ercot-retail-analysis.')
f.text(.05,fy(13.75),textwrap.fill(foot,198),fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(Line2D([.05,.95],[fy(14.8)]*2,color=GR,lw=1,transform=f.transFigure))
f.text(.05,fy(15.1),'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center'); f.text(.155,fy(15.1),'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,fy(15.1),'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
f.text(.95,fy(.42),'1 of 8',fontsize=13,fontweight='bold',color=MU,ha='right',va='center'); f.text(.05,fy(.42),'TEXAS ELECTRICITY PRICES: HOUSEHOLDS VS BUSINESSES',fontsize=11,color=MU,va='center',fontweight='bold')
OUT=ROOT/'charts/competition_series'; OUT.mkdir(parents=True,exist_ok=True); f.savefig(OUT/'01_price_levels.png',facecolor=BG)
print(hs[[2001,2025]].round(2).to_dict(),bs[[2001,2025]].round(2).to_dict(),phs[[2001,2025]].round(2).to_dict(),pbs[[2001,2025]].round(2).to_dict())
