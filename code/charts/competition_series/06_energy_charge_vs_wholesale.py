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

r=pd.read_csv(ROOT/'data/statewide_series/competitive_residential_components_2002_2025.csv',index_col=0); c=pd.read_csv(ROOT/'data/statewide_series/competitive_business_components_2002_2025.csv',index_col=0)
Y=range(2002,2026); k=K.reindex(list(Y))
wr=whR.loc[2002:2025]; er=r.energy_retail.loc[2002:2025]*k; ec=c.energy_retail.loc[2002:2025]*k
mr=er-wr; mc=ec-wr
av=lambda s,a,b:s.loc[a:b].mean()
print({n:(round(av(mr,*p),1),round(av(mc,*p),1)) for n,p in [('02-08',(2002,2008)),('10-19',(2010,2019)),('22-25',(2022,2025))]}, round(mr[2025],1),round(mc[2025],1))
H=15.8; fy=lambda i:1-(i+.2)/H; fyt=lambda i:1-i/H
f=plt.figure(figsize=(14.4,H),dpi=100,facecolor=BG)
f.text(.05,fyt(1.75),'In Texas’s competitive market, the business energy\ncharge has fallen '+f'{1-ec[2025]/ec[2002]:.0%} since 2002; the household\ncharge is up {er[2025]/er[2002]-1:.0%}',fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
sub=(f'The energy and retail part of the bill is what competitive retail providers charge above the wires. In 2002, the first year of competition, households paid {er[2002]:.1f}¢ and businesses {ec[2002]:.1f}¢ (2025 dollars). In 2025 households paid {er[2025]:.1f}¢ and businesses {ec[2025]:.1f}¢. '
     f'The gap between the two grew from {er[2002]-ec[2002]:.1f}¢ to {er[2025]-ec[2025]:.1f}¢. Households and businesses buy the same wholesale power, shown in purple for reference.')
f.text(.05,fyt(3.3),textwrap.fill(sub,140),fontsize=13.5,color=MU,va='center',linespacing=1.5)
def base(ax,x1=2031):
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_facecolor(BG); ax.tick_params(length=0,labelsize=11,colors=MU); ax.grid(axis='y',color=GR,lw=.8); ax.set_axisbelow(True)
    ax.set_xlim(2001.4,x1); tk=[2002,2008,2014,2020,2025]; ax.set_xticks(tk); ax.set_xticklabels([str(x) for x in tk],fontsize=11,color=FG)
a=f.add_axes([.055,fy(10.5),.41,5.6/H]); base(a)
a.text(0,1.05,'Energy + retail charge and wholesale price, 2025 cents per kWh',transform=a.transAxes,fontsize=13,color=MU)
a.set_ylim(0,24); a.set_yticks(range(0,25,6))
for s,c_,lw,l,dy in [(er,ER,3.2,'Households',0),(ec,TR,3.2,'Businesses',.9),(wr,WH,2.4,'Wholesale',-.9)]:
    sp=s.clip(upper=22) if l=='Wholesale' else s
    a.plot(sp.index,sp.values,color=c_,lw=lw,zorder=6,solid_capstyle='round')
    a.text(2025.5,s[2025]+dy,f'{l}\n{s[2025]:.1f}¢',color=c_,fontsize=11.5,fontweight='bold',va='center',linespacing=1.15)
a.annotate(f'Winter Storm Uri 2021: wholesale {wr[2021]:.0f}¢',(2021,22),xytext=(2015.3,22.9),fontsize=10.5,color=WH,fontweight='bold',arrowprops=dict(arrowstyle='-',color=WH,lw=.8),va='center')
b=f.add_axes([.535,fy(10.5),.41,5.6/H]); base(b)
b.text(0,1.05,'Energy + retail charge, 2002 = 100',transform=b.transAxes,fontsize=13,color=MU)
ix=lambda s_:s_/s_[2002]*100
b.set_ylim(40,215); b.set_yticks([50,100,150]); b.axhline(100,color=MU,lw=.9,ls=(0,(4,3)),zorder=3)
for s_,c_,l in [(er,ER,'Households'),(ec,TR,'Businesses')]:
    v=ix(s_); b.plot(v.index,v.values,color=c_,lw=3.2,zorder=6,solid_capstyle='round'); b.text(2025.5,v[2025]+(4 if l=='Households' else -4),f'{l}\n{v[2025]:.0f}',color=c_,fontsize=11.5,fontweight='bold',va='center',linespacing=1.15)
f.text(.05,fy(11.15),'What the gap contains, and what we cannot split out',fontsize=17,fontweight='bold',color=FG,va='center')
txt=('• The difference between each class’s charge and the wholesale price covers the retailer’s margin, marketing and bad debt, line losses, and the cost of shaping a flat wholesale price to a customer’s load. Households peak on summer afternoons, so shaping costs more for them. We cannot yet split these.\n'
     '• Fixed-price contracts mean retail charges lag wholesale, so a single year can mislead. Uri is the extreme case: most customers were on fixed-price contracts, so retail charges barely moved in 2021. The household charge has also not tracked the cost of gas since 2013.\n'
     '• Wholesale prices are the market monitor’s all-in figure. The definition changes over time: energy only 2002–06, energy plus ancillary services 2010–14, uplift added 2015–18.')
f.text(.05,fy(11.5),'\n'.join(textwrap.fill(l,138,subsequent_indent='   ') for l in txt.split('\n')),fontsize=12.5,color=FG,va='top',linespacing=1.55)
foot=('Energy + retail = the competitive retail providers’ revenue per kWh from EIA-861 for each class, minus the kWh-weighted wires charges of Oncor, CenterPoint, AEP Texas and TNMP. Business = commercial and industrial customers. Wholesale = ERCOT market monitor all-in price in ¢/kWh, not matched to each class’s load shape or contract timing. '
      'Prices adjusted to 2025 dollars with CPI-U (BLS). Data and code: github.com/fredstaffordcs/ercot-retail-analysis.')
f.text(.05,fy(14.2),textwrap.fill(foot,198),fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(Line2D([.05,.95],[fy(14.95)]*2,color=GR,lw=1,transform=f.transFigure))
f.text(.05,fy(15.25),'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center'); f.text(.155,fy(15.25),'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,fy(15.25),'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
f.text(.95,fyt(.42),'6 of 7',fontsize=13,fontweight='bold',color=MU,ha='right',va='center'); f.text(.05,fyt(.42),'TEXAS ELECTRICITY PRICES: HOUSEHOLDS VS BUSINESSES',fontsize=11,color=MU,va='center',fontweight='bold')
OUT=ROOT/'charts/competition_series'; OUT.mkdir(parents=True,exist_ok=True); f.savefig(OUT/'06_energy_charge_vs_wholesale.png',facecolor=BG)
