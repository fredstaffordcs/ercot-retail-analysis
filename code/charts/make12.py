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
cpi=pd.read_csv(ROOT/'data/reference/cpi_annual.csv',index_col=0).value; K=cpi[2025]/cpi
B=pd.read_csv(ROOT/'data/statewide_series/bundled_prices_by_ownership_1990_2025.csv',index_col=0)
S=pd.read_csv(ROOT/'data/statewide_series/eia861_ownership_group_totals_1990_2025.csv').set_index(['Year','G'])
wh=pd.read_csv(ROOT/'data/reference/ercot_wholesale_2002_2025.csv',index_col=0).usd_per_mwh/10; whR=wh*K.reindex(wh.index)
IOU='#b5a49a'; W=.72; WH='#7a3fb0'
BG='#fcfcfb'; FG='#1c2421'; MU='#5d6b66'; GR='#e3e7e5'; TX='#009280'; SEC='#93d3c9'; OT='#6b7a75'; ER='#c2570c'; BU='#1f77a8'
Y0,Y1,STEP=-1.2,27,3
def load(key):
    if key=='res':
        d=pd.read_csv(ROOT/'data/statewide_series/competitive_residential_components_2002_2025.csv',index_col=0); d['other']=d.storm+d.sbf
        iou=S.xs('iou',level='G'); iouc=(iou.res_rev/iou.res_mwh*100).loc[1990:2001]
        pub=S.xs('pub',level='G'); pubc=(pub.res_rev/pub.res_mwh*100).loc[1990:2025]
    else:
        d=pd.read_csv(ROOT/f"data/statewide_series/competitive_{ {'all':'all_classes','ci':'business'}[key] }_components_2002_2025.csv",index_col=0)
        iouc=B['iou_'+key].loc[1990:2001]; pubc=B['pub_'+key].loc[1990:2025]
    for c in ['retail','delivery','dereg_transition','other','energy_retail']: d[c]=d[c]*K.reindex(d.index)
    return d,iouc*K.reindex(iouc.index),pubc*K.reindex(pubc.index)
def panel(ax,d,iouR,pubR,small=False,ylab=True):
    fs=9.5 if small else 11.5; Wd=W
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_facecolor(BG); ax.set_ylim(Y0,Y1); ax.set_xlim(1989.4,2028.2 if small else 2026.6)
    ax.set_yticks(range(0,28,STEP)); ax.axhline(0,color=MU,lw=.8,zorder=2); ax.tick_params(length=0,labelsize=11,colors=MU)
    tk=[1990,2001,2010,2020,2025] if small else [1990,1995,2001,2005,2010,2015,2020,2025]
    ax.set_xticks(tk); ax.set_xticklabels([str(t) for t in tk],fontsize=11 if small else 12,color=FG)
    ax.grid(axis='y',color=GR,lw=.8); ax.set_axisbelow(True)
    ax.axvspan(1989.5,2001.5,color='#eef0ef',zorder=0,lw=0)
    ax.text(1995.5,Y1*.985,'Regulated\nmonopolies' if small else 'Regulated monopolies:\nbundled price only',ha='center',va='top',fontsize=10 if small else 11,color=MU,linespacing=1.2)
    pk=d.retail.idxmax()
    for y,v in iouR.items():
        ax.bar(y,v,Wd,color=IOU,zorder=3,lw=0)
        if y in (1990,2001): ax.text(y,v+.25,f'{v:.1f}',ha='center',va='bottom',fontsize=fs-(1 if small else 0),fontweight='bold',color=FG,zorder=8)
    for y in d.index:
        dl,tr,ot,e,R=d.delivery[y],d.dereg_transition[y],d.other[y],d.energy_retail[y],d.retail[y]
        ax.bar(y,dl,Wd,color=TX,zorder=3,lw=0); top=dl
        if tr>0.005: ax.bar(y,tr,Wd,bottom=top,color=SEC,edgecolor=TX,hatch='///',zorder=3,lw=0); top+=tr
        elif tr<-0.005: ax.bar(y,tr,Wd,bottom=0,color=SEC,edgecolor=TX,hatch='///',zorder=3,lw=0)
        if ot>0.005: ax.bar(y,ot,Wd,bottom=top,color=OT,zorder=3,lw=0); top+=ot
        ax.bar(y,e,Wd,bottom=top,color=ER,zorder=3,lw=0)
        ax.plot([y-Wd/2,y+Wd/2],[top]*2,color=BG,lw=1.6,zorder=4)
        if y in (pk,2025): ax.text(y,top+e+.25,f'{R:.1f}',ha='center',va='bottom',fontsize=fs-(1 if small else 0),fontweight='bold',color=FG,zorder=8)
        if y==2025 and not small:
            ax.text(y,dl/2,f'{dl:.1f}',ha='center',va='center',fontsize=10,fontweight='bold',color='white',zorder=8)
            ax.text(y,top+e/2,f'{e:.1f}',ha='center',va='center',fontsize=10,fontweight='bold',color='white',zorder=8)
    ax.annotate('Transition credits\n(net, 2002–04)',(2002.6,-0.3),xytext=(2006.8,-0.9),fontsize=9 if small else 9.5,color=MU,va='center',arrowprops=dict(arrowstyle='-',color=MU,lw=.8))
    ax.plot(list(pubR.index),pubR.values,color=BU,lw=2.6,zorder=6,solid_capstyle='round')
    ax.scatter(list(pubR.index),pubR.values,s=20 if small else 30,color=BU,edgecolor=BG,lw=1.1,zorder=7)
    ax.plot(list(whR.index),whR.values,color=WH,lw=2.2,zorder=6,solid_capstyle='round')
    ax.scatter(list(whR.index),whR.values,s=16 if small else 24,color=WH,edgecolor=BG,lw=1,zorder=7)
    bb=lambda c:dict(boxstyle='round,pad=.18',fc='white',ec=c,lw=.8)
    for y,dx,dy in [(2008,0,14),(2025,20 if small else 24,-2)]:
        v=whR[y]; ax.annotate(f'{v:.1f}',(y,v),xytext=(dx,dy),textcoords='offset points',ha='center',va='center',fontsize=fs-1,fontweight='bold',color=WH,zorder=9,bbox=bb(WH))
    ax.annotate(f'{whR[2021]:.1f}',(2021,whR[2021]),xytext=(-22 if small else 34,0),textcoords='offset points',ha='center',va='center',fontsize=fs-.5,fontweight='bold',color=WH,zorder=9,bbox=bb(WH))
    ax.annotate('Winter Storm Uri',(2021,whR[2021]),xytext=(-24 if small else 34,17),textcoords='offset points',ha='center',va='center',fontsize=9 if small else 10,color=WH)
    for y in (1990,2025):
        v=pubR[y]; ax.annotate(f'{v:.1f}',(y,v),xytext=(20 if small else 24,0) if y==2025 else (0,18 if pubR[1990]>iouR[1990]+.5 else -20),textcoords='offset points',ha='center',va='center',fontsize=fs-.5,fontweight='bold',color=BU,zorder=9,bbox=bb(BU))
def header(f,title,sub,ly,top=.945,sy=.857):
    f.text(.05,top,title,fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
    f.text(.05,sy,sub,fontsize=13,color=MU,va='center',linespacing=1.5)
    items=[('Regulated utility, bundled',IOU,'box'),('Wires delivery',TX,'box'),('Transition charges (net)',SEC,'hatch'),('Storm bonds + state fee',OT,'box'),('Energy + retail',ER,'box'),('Public power',BU,'line'),('Wholesale (all-in)',WH,'line')]
    xs=[.05,.205,.31,.47,.63,.735,.845]
    for (lab,c,k),x in zip(items,xs):
        if k=='line':
            f.add_artist(Line2D([x-.002,x+.022],[ly,ly],color=c,lw=2.8,transform=f.transFigure)); f.add_artist(Line2D([x+.01],[ly],marker='o',color=c,ms=6,transform=f.transFigure))
        else: f.patches.append(plt.Rectangle((x,ly-.006),.014,.012,transform=f.transFigure,fc=c,ec=TX if k=='hatch' else 'none',hatch='///' if k=='hatch' else None,lw=0))
        f.text(x+(.03 if k=='line' else .02),ly,lab,fontsize=11.2,color=FG,va='center')
def footer(f,foot,fy):
    f.text(.05,fy,textwrap.fill(foot,195),fontsize=9.6,color=MU,va='top',linespacing=1.5)
    f.add_artist(Line2D([.05,.95],[.036,.036],color=GR,lw=1,transform=f.transFigure))
    f.text(.05,.018,'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center')
    f.text(.155,.018,'@fredstaffordcs',fontsize=14,color=FG,va='center')
    f.text(.95,.018,'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
FOOT=('Adjusted to 2025 dollars with CPI-U annual averages (BLS). Prices are revenue per kWh from EIA-861. 1990–2001: investor-owned utilities in the ERCOT region (TXU, HL&P, CPL, WTU, TNMP), bundled. '
 '2002–2025: competitive retail providers, minus the kWh-weighted wires-company charges of Oncor, CenterPoint, AEP Texas and TNMP for the same customers (FERC Form 1, EIA-861, AEP earnings monitoring reports, SEC filings, bond servicer reports, PUCT rates); '
 'AEP Texas Central’s 2003–04 delivery charges are estimated from its residential charges for the business and all-class versions. Transition charges include stranded-cost bonds and credits. Public power = ERCOT municipal utilities and co-ops (excluding short-form filers), bundled. '
 'Business = commercial, industrial and other non-residential customers (all classes minus residential). Wholesale: ERCOT market monitor all-in price (energy-only 2002–06; energy plus ancillary services 2010–18). Customer mix differs between areas and shifts over time. All panels use the same vertical scale.')
TT={'res':('Texas household power prices in today’s dollars:\nregulated, then competitive, vs. public power','household'),
    'all':('Texas power prices for all customers in today’s dollars:\nregulated, then competitive, vs. public power','all customer classes (residential, commercial, industrial and other)'),
    'ci':('Texas business power prices in today’s dollars:\nregulated, then competitive, vs. public power','commercial, industrial and other non-residential customers')}
OUT={'res':'price_history_real_1990_2025_sameaxis.png','all':'price_history_real_allclass_1990_2025_sameaxis.png','ci':'price_history_real_ci_1990_2025_sameaxis.png'}
for key in ['res','all','ci']:
    d,iouR,pubR=load(key); pk=d.retail.idxmax()
    f=plt.figure(figsize=(14.4,12.6),dpi=100,facecolor=BG)
    who=TT[key][1]
    sub=(f'Average price per kWh for {who if key!="res" else "households"} in the ERCOT region, in 2025 cents (CPI-U), 1990–2025. Through 2001: investor-owned utilities’ bundled price.\n'
         f'From 2002: competitive retail providers, split into wires charges and energy + retail. Private-area price {iouR[1990]:.1f}¢ in 1990, {iouR[2001]:.1f}¢ in 2001, {d.retail[pk]:.1f}¢ at the {pk} peak, {d.retail[2025]:.1f}¢ in 2025;\n'
         f'public power {pubR[1990]:.1f}¢, {pubR[2001]:.1f}¢ and {pubR[2025]:.1f}¢. Same vertical scale on all versions of this chart.')
    sub='\n'.join(textwrap.fill(p,128) for p in sub.split('\n')) if False else textwrap.fill(sub.replace('\n',' '),150)
    header(f,TT[key][0],sub,.795)
    ax=f.add_axes([.065,.2,.885,.55]); panel(ax,d,iouR,pubR)
    footer(f,FOOT,.155); f.savefig(str(ROOT/'charts'/OUT[key]),facecolor=BG); plt.close(f)
# two-panel
dr,ir,pr=load('res'); dc,ic,pc=load('ci')
f=plt.figure(figsize=(14.4,12.2),dpi=100,facecolor=BG)
sub=(f'Average price per kWh in the ERCOT region, in 2025 cents (CPI-U), 1990–2025, on the same vertical scale.\nThrough 2001: investor-owned utilities’ bundled price; from 2002: competitive retail providers.\n'
     f'Households: {ir[1990]:.1f}¢ in 1990, {ir[2001]:.1f}¢ in 2001, {dr.retail[2025]:.1f}¢ in 2025 (public power {pr[1990]:.1f}¢, {pr[2001]:.1f}¢, {pr[2025]:.1f}¢). '
     f'Business: {ic[1990]:.1f}¢, {ic[2001]:.1f}¢, {dc.retail[2025]:.1f}¢ (public power {pc[1990]:.1f}¢, {pc[2001]:.1f}¢, {pc[2025]:.1f}¢).')
sub=textwrap.fill(sub.replace('\n',' '),150)
header(f,'Texas households vs. businesses: power prices\nin today’s dollars, competitive vs. public power',sub,.775,top=.94,sy=.835)
a1=f.add_axes([.055,.2,.44,.52]); a2=f.add_axes([.515,.2,.435,.52],sharey=a1)
panel(a1,dr,ir,pr,small=True); panel(a2,dc,ic,pc,small=True); a2.tick_params(labelleft=False)
for a,t in [(a1,'Households'),(a2,'Businesses (commercial + industrial)')]:
    a.set_title(t,loc='left',fontsize=17,fontweight='bold',color=FG,pad=10)
footer(f,FOOT,.15); f.savefig(str(ROOT/'charts'/'price_history_real_households_vs_business.png'),facecolor=BG)
print('ok')
