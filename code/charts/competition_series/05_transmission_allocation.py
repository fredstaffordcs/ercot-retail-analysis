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

g=pd.read_csv(CS/'residential_transmission_allocation_vs_kwh_share_2002_2025.csv',index_col=0)
bc=pd.read_csv(ROOT/'data/by_class/statewide_delivery_by_class_2002_2025.csv'); e=bc[bc.layer=='eia']
m=e.pivot_table(index='year',columns='class_code',values='mwh')[['residential','commercial','industrial']]; t=e.pivot_table(index='year',columns='class_code',values='transmission_cents')[['residential','commercial','industrial']]
bus=(m.commercial*t.commercial+m.industrial*t.industrial)/(m.commercial+m.industrial); avg=(m*t).sum(axis=1)/m.sum(axis=1)
kk=K.reindex(t.index); t=t.mul(kk,axis=0); bus=bus*kk; avg=avg*kk
H=15.9; fy=lambda i:1-(i+.2)/H; fyt=lambda i:1-i/H
f=plt.figure(figsize=(14.4,H),dpi=100,facecolor=BG)
f.text(.05,fyt(1.3),'Households carry a transmission bill sized to\ntheir peak demand, not to their shrinking share of use',fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
sub=(f'In the four big wires companies’ rate cases, households are assigned {g.alloc[2002]:.0%} of transmission costs in 2002 and {g.alloc[2025]:.0%} in 2025, while their share of kWh delivered fell from {g.kwhsh[2002]:.0%} to {g.kwhsh[2025]:.0%}. '
     f'Per kWh, households now pay {t.residential[2025]/bus[2025]:.1f} times what businesses pay for transmission, up from {t.residential[2002]/bus[2002]:.1f}. Under a kWh-based split, the household bill would be {t.residential[2025]-avg[2025]:.1f}¢ lower in 2025.')
f.text(.05,fyt(2.9),textwrap.fill(sub,148),fontsize=13.5,color=MU,va='center',linespacing=1.5)
def base(ax,x1=2026):
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_facecolor(BG); ax.tick_params(length=0,labelsize=11,colors=MU); ax.grid(axis='y',color=GR,lw=.8); ax.set_axisbelow(True)
    ax.set_xlim(2001.4,x1); tk=[2002,2008,2014,2020,2025]; ax.set_xticks(tk); ax.set_xticklabels([str(x) for x in tk],fontsize=11,color=FG)
a=f.add_axes([.055,fy(10.2),.40,5.6/H]); base(a,2032)
a.text(0,1.05,'Residential share, percent',transform=a.transAxes,fontsize=13,color=MU)
a.set_ylim(20,55); a.set_yticks([20,30,40,50]); a.set_yticklabels(['20%','30%','40%','50%'])
a.fill_between(g.index,g.kwhsh*100,g.alloc*100,color=ER,alpha=.14,lw=0,zorder=2)
a.plot(g.index,g.alloc*100,color=ER,lw=3.2,zorder=6); a.plot(g.index,g.kwhsh*100,color=TR,lw=3.2,zorder=6)
a.text(2025.5,g.alloc[2025]*100+.2,f'{g.alloc[2025]:.0%}\nof transmission\ncost assigned',color=ER,fontsize=11.5,fontweight='bold',va='center',linespacing=1.15)
a.text(2025.5,g.kwhsh[2025]*100,f'{g.kwhsh[2025]:.0%}\nof kWh delivered',color=TR,fontsize=11.5,fontweight='bold',va='center',linespacing=1.15)
a.text(2005,g.alloc[2005]*100+1.2,f'{g.alloc[2002]:.0%}',color=ER,fontsize=11.5,fontweight='bold',ha='center'); a.text(2004.5,g.kwhsh[2002]*100-3,f'{g.kwhsh[2002]:.0%}',color=TR,fontsize=11.5,fontweight='bold',ha='center')
b=f.add_axes([.535,fy(10.2),.40,5.6/H]); base(b,2029.5)
b.text(0,1.05,'Transmission charge per kWh delivered, 2025 cents',transform=b.transAxes,fontsize=13,color=MU)
b.set_ylim(0,2.3); b.set_yticks([0,.5,1,1.5,2]); b.set_yticklabels(['0','0.5¢','1¢','1.5¢','2¢'])
for s,c,lw,l in [(t.residential,ER,3.2,'Households'),(bus,TR,3.2,'Businesses'),(avg,MU,1.8,'If split by kWh')]:
    b.plot(s.index,s.values,color=c,lw=lw,ls='-' if lw>2 else (0,(4,2)),zorder=6); b.text(2025.5,s[2025]+(.0 if l!='Businesses' else -.07),f'{l}\n{s[2025]:.2f}¢',color=c,fontsize=11.5,fontweight='bold',va='center',linespacing=1.15)
f.text(.05,fy(10.85),'What this does and does not explain',fontsize=17,fontweight='bold',color=FG,va='center')
txt=(f'• It is about {(t.residential[2025]-bus[2025]):.1f}¢ of the 10.2¢ household–business gap in 2025, roughly a tenth. Most of the gap is in energy and retail charges.\n'
     '• Allocating by peak demand is the rule and is defensible, so a kWh split is not the “right” answer either. The issue is that the split is frozen between rate cases while load changes.\n'
     '• In 2026 the PUCT’s staff report found fixed class factors plus fast load growth have caused inequitable cost shifts between classes and recommends annual updates. It also found some industrial customers cut demand during the four peak intervals, with no matching cut in system costs.')
f.text(.05,fy(11.2),'\n'.join(textwrap.fill(l,138,subsequent_indent='   ') for l in txt.split('\n')),fontsize=12.5,color=FG,va='top',linespacing=1.55)
foot=('Residential allocation factor: the residential share of the 4CP transmission allocator in each wires company’s base-rate case, as read from its transmission cost recovery factor filings; weighted by each company’s ERCOT transmission bill (Oncor, CenterPoint, AEP Texas, TNMP). Residential kWh share: residential kWh over all kWh delivered by the same four companies (EIA-861 classes). '
      'Prices adjusted to 2025 dollars with CPI-U (BLS). Transmission per kWh = each company’s ERCOT transmission bill (4CP load × billed rate, plus in-year updates) × the class’s allocation factor ÷ class kWh; business = commercial and industrial, kWh-weighted. “Average” is total transmission cost ÷ total kWh. '
      'PUCT Project 58484, draft report on transmission cost recovery, March 2026. Data and code: github.com/fredstaffordcs/ercot-retail-analysis.')
f.text(.05,fy(14.0),textwrap.fill(foot,198),fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(Line2D([.05,.95],[fy(15.1)]*2,color=GR,lw=1,transform=f.transFigure))
f.text(.05,fy(15.4),'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center'); f.text(.155,fy(15.4),'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,fy(15.4),'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
f.text(.95,fyt(.42),'5 of 7',fontsize=13,fontweight='bold',color=MU,ha='right',va='center'); f.text(.05,fyt(.42),'TEXAS ELECTRICITY PRICES: HOUSEHOLDS VS BUSINESSES',fontsize=11,color=MU,va='center',fontweight='bold')
OUT=ROOT/'charts/competition_series'; OUT.mkdir(parents=True,exist_ok=True); f.savefig(OUT/'05_transmission_allocation.png',facecolor=BG)
