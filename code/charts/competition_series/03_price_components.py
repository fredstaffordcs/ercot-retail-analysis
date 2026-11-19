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
def comp(d): 
    x=pd.DataFrame({'tx':d.transmission,'di':d.dist_other+d.other+d.dereg_transition,'en':d.energy_retail}); return x.loc[2002:2025]
R=comp(dr); C=comp(dc)
chg=lambda x:(x.loc[2025]-x.loc[2002])
H=16.2; fy=lambda i:1-(i+.2)/H; fyt=lambda i:1-i/H
f=plt.figure(figsize=(14.4,H),dpi=100,facecolor=BG)
f.text(.05,fyt(1.3),'Under competition, the energy charge hasn’t fallen for\nhouseholds, and transmission charges rose for both',fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
dh,db=chg(R),chg(C)
sub=(f'Change in each part of the price from 2002 to 2025, in 2025 cents per kWh. Households: energy + retail {dh.en:+.1f}¢, transmission {dh.tx:+.1f}¢, distribution and other {dh.di:+.1f}¢, total {dh.sum():+.1f}¢. '
     f'Businesses: energy + retail {db.en:+.1f}¢, transmission {db.tx:+.1f}¢, distribution and other {db.di:+.1f}¢, total {db.sum():+.1f}¢. Households’ energy + retail charge in 2025 is {R.en[2025]:.1f}¢, businesses’ is {C.en[2025]:.1f}¢. Transmission rose for both classes, but energy + retail is the largest part of both bills and the part that diverged.')
f.text(.05,fyt(3.05),textwrap.fill(sub,140),fontsize=13.5,color=MU,va='center',linespacing=1.5)
def base(ax,ymax):
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_facecolor(BG); ax.tick_params(length=0,labelsize=11,colors=MU); ax.grid(axis='y',color=GR,lw=.8); ax.set_axisbelow(True)
    ax.set_xlim(2001.6,2030.5); tk=[2002,2008,2014,2020,2025]; ax.set_xticks(tk); ax.set_xticklabels([str(x) for x in tk],fontsize=11,color=FG)
    ax.set_ylim(0,ymax)
specs=[('en','Energy + retail (competitive)',ER,20,[0,5,10,15,20]),('tx','Transmission',TR,2.4,[0,.5,1,1.5,2]),('di','Distribution + other',DI,4.5,[0,1,2,3,4])]
xs=[.055,.385,.715]; w=.245
for (k,t_,c,ym,tks),x in zip(specs,xs):
    a=f.add_axes([x,fy(9.3),w,4.0/H]); base(a,ym); a.set_yticks(tks)
    a.set_yticklabels([f'{v:g}¢' for v in tks])
    a.text(0,1.05,t_,transform=a.transAxes,fontsize=14,fontweight='bold',color=FG)
    for s,cc,l in [(R[k],ER if k!='en' else ER,'Households'),(C[k],TR if k!='tx' else '#2e7d6f','Businesses')]:
        pass
    a.plot(R.index,R[k].values,color=ER,lw=3.0,zorder=6); a.plot(C.index,C[k].values,color=TR,lw=3.0,zorder=6)
    dy=ym*.035
    a.text(2025.5,R[k][2025]+(dy if R[k][2025]>C[k][2025] else -dy),f'{R[k][2025]:.1f}¢',color=ER,fontsize=11.5,fontweight='bold',va='center')
    a.text(2025.5,C[k][2025]+(dy if C[k][2025]>R[k][2025] else -dy),f'{C[k][2025]:.1f}¢',color=TR,fontsize=11.5,fontweight='bold',va='center')
for xx,t_,c_ in [(.055,'Households',ER),(.15,'Businesses',TR)]:
    f.add_artist(Line2D([xx,xx+.017],[fy(4.4)]*2,color=c_,lw=3,transform=f.transFigure)); f.text(xx+.022,fy(4.4),t_,color=c_,fontsize=12.5,fontweight='bold',va='center')
f.text(.05,fy(10.2),'How the parts changed, 2002 to 2025',fontsize=17,fontweight='bold',color=FG,va='center')
f.text(.05,fy(10.75),'2025 cents per kWh',fontsize=12,color=MU,va='center')
cols=[(.25,'Energy + retail'),(.40,'Transmission'),(.55,'Distribution + other'),(.73,'Total')]
for xx,t_ in cols: f.text(xx,fy(10.75),t_,fontsize=12,color=MU,va='center')
for i,(l,d,c_) in enumerate([('Households',dh,ER),('Businesses',db,TR)]):
    yy=fy(11.3+i*.5); f.text(.05,yy,l,fontsize=13,color=c_,fontweight='bold',va='center')
    for xx,v in zip([.25,.40,.55,.73],[d.en,d.tx,d.di,d.sum()]): f.text(xx,yy,f'{v:+.1f}¢',fontsize=13,color=FG,fontweight='bold',va='center')
txt=('• Transmission grew fastest in percentage terms for both classes (households +148%, businesses +62%), but it is a small part of the bill: 1.9¢ of 17.3¢ for households.\n'
     '• Energy + retail is where the classes part ways: it fell for businesses and rose slightly for households.\n'
     '• 2002 includes net transition credits, which are negative and lower that year’s distribution + other figure.')
f.text(.05,fy(12.4),'\n'.join(textwrap.fill(l,138,subsequent_indent='   ') for l in txt.split('\n')),fontsize=12.5,color=FG,va='top',linespacing=1.55)
foot=('Wires charges are the kWh-weighted charges of Oncor, CenterPoint, AEP Texas and TNMP (FERC Form 1, SEC filings, AEP earnings reports, bond servicer reports, PUCT). Transmission = each wires company’s ERCOT transmission bill (4CP load × postage-stamp rate, plus in-year updates) × the class’s allocation factor (TCRF filings; business = one minus residential) ÷ class kWh. '
      'Distribution + other includes net transition charges, storm bonds and the System Benefit Fund fee. Energy + retail = competitive retail providers’ revenue per kWh (EIA-861) minus the class’s wires charges. Business = commercial and industrial customers. Prices adjusted to 2025 dollars with CPI-U (BLS). Data and code: github.com/fredstaffordcs/ercot-retail-analysis.')
f.text(.05,fy(14.5),textwrap.fill(foot,198),fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(Line2D([.05,.95],[fy(15.5)]*2,color=GR,lw=1,transform=f.transFigure))
f.text(.05,fy(15.82),'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center'); f.text(.155,fy(15.82),'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,fy(15.82),'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
f.text(.95,fyt(.42),'3 of 8',fontsize=13,fontweight='bold',color=MU,ha='right',va='center'); f.text(.05,fyt(.42),'TEXAS ELECTRICITY PRICES: HOUSEHOLDS VS BUSINESSES',fontsize=11,color=MU,va='center',fontweight='bold')
OUT=ROOT/'charts/competition_series'; OUT.mkdir(parents=True,exist_ok=True); f.savefig(OUT/'03_price_components.png',facecolor=BG)
print(dh.round(2).to_dict(),db.round(2).to_dict())
