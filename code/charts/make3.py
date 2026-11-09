import glob, json, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for f in fm.findSystemFonts():
    if 'Inter' in f and 'Display' not in f: fm.fontManager.addfont(f)
plt.rcParams['font.family']='Inter'
df=pd.read_csv(ROOT/'code/charts/inputs/wires_components_2019_2025_preliminary.csv')
D=None; dec=pd.read_csv(ROOT/'data/reference/wholesale_and_retail_2019_2025.csv').set_index('y')
# calibrate 2019 totals so kWh-weighted average equals the page's statewide 2019 delivery estimate
m=df.year==2019
SRC19={'Oncor':3.697,'CenterPoint':3.845,'AEP Texas':4.909,'TNMP':4.951}  # FERC Form 1 / 10-K (replaces tariff estimate)
KWH19={'Oncor':45544.4,'CenterPoint':30334.2,'AEP Texas':11996.0,'TNMP':3044.8}  # GWh, same sources
for u,v in SRC19.items():
    i=m&(df.utility==u); df.loc[i,'total']=v; df.loc[i,'res_kwh_m']=KWH19[u]
    df.loc[i,'transmission']=df.loc[i,'tx_cost_musd']*df.loc[i,'alloc']*1e6/(KWH19[u]*1e6)*100
df.loc[m,'est']=False
df['distribution_other']=df.total-df.transmission
# corrected 2019-25 transmission (billed postage-stamp rate, filed allocation factors, in-year TCOS updates) (wires_residential_transmission_split_2002_2025.csv)
_t=pd.read_csv(ROOT/'data/utility_level/wires_residential_transmission_split_2002_2025.csv'); _t['utility']=_t.utility.replace({'AEP Texas (Central+North)':'AEP Texas'})
_t=_t.set_index(['utility','year'])
for i,r in df.iterrows():
    k=(r.utility,r.year); df.loc[i,'total']=_t.loc[k,'delivery_cents']; df.loc[i,'transmission']=_t.loc[k,'res_tx_cents']; df.loc[i,'res_kwh_m']=_t.loc[k,'res_mwh']/1e3; df.loc[i,'alloc']=_t.loc[k,'res_tx_alloc_factor']; df.loc[i,'tx_cost_musd']=_t.loc[k,'tdu_wholesale_tx_cost_kusd']/1e3
df['distribution_other']=df.total-df.transmission
df.round(3).to_csv(str(ROOT/'data/utility_level/wires_residential_components_2019_2025_summary.csv'),index=False)
Y=list(range(2019,2026))
C3=pd.read_csv(ROOT/'data/utility_level/wires_residential_components_2002_2025.csv')
C3['utility']=C3.utility.replace({'AEP Texas (Central+North)':'AEP Texas'})
C3=C3.set_index(['utility','year'])
SW=pd.read_csv(ROOT/'data/statewide_series/competitive_residential_components_2002_2025.csv',index_col=0)
BG='#fcfcfb'; FG='#1c2421'; MU='#5d6b66'; GR='#e3e7e5'
WH='#7a3fb0'; SECC='#e3f4f0'; OT='#6b7a75'; TX='#009280'; DO='#93d3c9'; ER='#c2570c'
YMAX=14; W=.62
def base(ax,title,note):
    ax.set_facecolor(BG); ax.set_ylim(0,YMAX); ax.set_xlim(-.6,6.6)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_yticks(range(0,YMAX+1,2)); ax.tick_params(length=0,labelsize=10.5,colors=MU)
    ax.set_xticks(range(7)); ax.set_xticklabels([str(y) for y in Y],fontsize=11.5,color=FG)
    ax.grid(axis='y',color=GR,lw=.8); ax.set_axisbelow(True)
    ax.set_title(title,loc='left',fontsize=18,fontweight='bold',color=FG,pad=34)
    ax.text(0,1.03,note,transform=ax.transAxes,ha='left',va='bottom',fontsize=12.5,color=FG)
def tot(ax,i,v):
    ax.text(i,v+.2,f'{v:.1f}',ha='center',va='bottom',fontsize=10.5,color=FG,fontweight='bold')
def util(ax,u,title):
    g=df[df.utility==u].set_index('year')
    for i,y in enumerate(Y):
        c=C3.loc[(u,y)]
        dl=c.delivery_cents_per_kwh; tr=c.deregulation_transition_cents_per_kwh if pd.notna(c.deregulation_transition_cents_per_kwh) else 0
        ot=(0 if pd.isna(c.storm_cents_per_kwh) else c.storm_cents_per_kwh)+(0 if pd.isna(c.sbf_cents_per_kwh) else c.sbf_cents_per_kwh)
        t=g.transmission[y]; o=dl-t
        ax.bar(i,t,W,color=TX,zorder=3); ax.bar(i,o,W,bottom=t,color=DO,zorder=3)
        top=dl
        if tr>0.005: ax.bar(i,tr,W,bottom=top,color=SECC,edgecolor=TX,hatch='///',lw=0,zorder=3); top+=tr
        if ot>0.005: ax.bar(i,ot,W,bottom=top,color=OT,zorder=3); top+=ot
        ax.plot([i-W/2,i+W/2],[t,t],color=BG,lw=2,zorder=4); tot(ax,i,top)
        if y in(2019,2025):
            ax.text(i,t+o/2,f'{o:.1f}',ha='center',va='center',fontsize=9.5,color=FG,fontweight='bold',zorder=5)
            ax.text(i,t/2,f'{t:.1f}',ha='center',va='center',fontsize=9.5,color='white',fontweight='bold',zorder=5)
    a,b=C3.loc[(u,2019)],C3.loc[(u,2025)]
    d=b.delivery_cents_per_kwh-a.delivery_cents_per_kwh; p=d/a.delivery_cents_per_kwh*100
    tb=b.tdu_bill_total_cents_per_kwh-a.tdu_bill_total_cents_per_kwh
    base(ax,title,f'2019→25:  delivery {d:+.1f}¢ ({p:+.0f}%)  ·  whole wires bill {tb:+.1f}¢')
def er(ax):
    for i,y in enumerate(Y):
        ax.bar(i,SW.energy_retail[y],W,color=ER,zorder=3); tot(ax,i,SW.energy_retail[y])
    d=SW.energy_retail[2025]-SW.energy_retail[2019]; p=d/SW.energy_retail[2019]*100
    base(ax,'Energy + retail vs. all-in wholesale',f'2019→25:  energy + retail {d:+.1f}¢  ({p:+.0f}%)   ·   wholesale {dec.wh[2025]-dec.wh[2019]:+.1f}¢')
    a2=ax.twinx(); a2.set_ylim(0,20); a2.set_yticks([0,5,10,15,20])
    for sp in a2.spines.values(): sp.set_visible(False)
    a2.tick_params(length=0,labelsize=10.5,colors=WH); a2.set_ylabel('All-in wholesale, ¢/kWh',color=WH,fontsize=11,labelpad=8)
    x=list(range(7)); v=list(dec.wh.values)
    a2.plot(x,v,color=WH,lw=2.8,zorder=6,solid_capstyle='round'); a2.scatter(x,v,s=52,color=WH,edgecolor=BG,lw=1.6,zorder=7)
    for i,y in enumerate(Y):
        if y in(2019,2023,2025): a2.annotate(f'{v[i]:.1f}',(i,v[i]),xytext=(0,-19),textcoords='offset points',ha='center',fontsize=10.5,color=WH,fontweight='bold',zorder=9,bbox=dict(boxstyle='round,pad=.2',fc='white',ec=WH,lw=.8))
    a2.annotate('19.2 (Winter Storm Uri)',(2,v[2]),xytext=(9,-1),textcoords='offset points',ha='left',va='center',fontsize=10,color=WH,fontweight='bold',zorder=9)
f=plt.figure(figsize=(14.4,16.6),dpi=100,facecolor=BG)
f.text(.05,.958,'Wires charges are up since 2019.\nEnergy and retail charges are up more.',fontsize=33,fontweight='bold',color=FG,va='center',linespacing=1.12)
f.text(.05,.903,'Average residential price in ERCOT’s competitive area, ¢ per kWh. Wires-company delivery charges at Oncor, CenterPoint and AEP Texas\nrose 1.5–1.9¢ since 2019 while expiring transition bonds offset part of it. Energy and retail rose 3.1¢. The first three panes share one scale.',fontsize=13.5,color=MU,va='center',linespacing=1.5)
items=[('Transmission',TX),('Distribution and other',DO),('Transition bonds',SECC),('Storm bonds',OT),('Energy + retail',ER),('All-in wholesale (right axis)',WH)]
xs=[.05,.175,.335,.48,.6,.735]; ly=.868
for (lab,c),x in zip(items,xs):
    if c==WH:
        f.add_artist(plt.Line2D([x-.002,x+.014],[ly,ly],color=c,lw=2.6,transform=f.transFigure)); f.add_artist(plt.Line2D([x+.006],[ly],marker='o',color=c,ms=7,transform=f.transFigure))
    else: f.patches.append(plt.Rectangle((x,ly-.005),.012,.01,transform=f.transFigure,fc=c,ec=TX if c==SECC else 'none',hatch='///' if c==SECC else None,lw=0))
    f.text(x+.017,ly,lab,fontsize=12.5,color=FG,va='center')
pos=[(.07,.52),(.55,.52),(.07,.175),(.55,.175)]
for (l,b),fn in zip(pos,[lambda ax:util(ax,'Oncor','Oncor'),lambda ax:util(ax,'CenterPoint','CenterPoint Houston'),lambda ax:util(ax,'AEP Texas','AEP Texas'),er]):
    ax=f.add_axes([l,b,.40,.265]); fn(ax)
foot=('Delivery = wires-company residential charges per kWh excluding transition and storm bonds (FERC Form 1, AEP earnings monitoring reports at the PUCT, SEC 10-Ks, bond servicer reports, EIA-861). '
      'Transmission = each utility’s wholesale transmission cost (prior-year 4CP load × ERCOT billed postage-stamp rate from PUCT final matrices, plus in-year TCOS updates) × its residential allocation factor (TCRF petitions) ÷ residential kWh; distribution and other = the rest of delivery. '
      'Transition bonds = stranded-cost securitization charges; storm bonds = hurricane restoration charges (plus AEP’s 2021 COVID relief fee). Energy + retail = competitive-area residential retail price minus the kWh-weighted wires bill of '
      'Oncor, CenterPoint, AEP Texas and TNMP; statewide, not by utility. Wholesale = market monitor’s all-in cost per MWh of load (Potomac Economics), right-hand axis. Nominal dollars.')
import textwrap; foot=textwrap.fill(foot.replace('\n',' '),200)
f.text(.05,.118,foot,fontsize=9.6,color=MU,va='top',linespacing=1.5)
f.add_artist(plt.Line2D([.05,.95],[.03,.03],color=GR,lw=1,transform=f.transFigure))
f.text(.05,.015,'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center')
f.text(.155,.015,'@fredstaffordcs',fontsize=14,color=FG,va='center')
f.text(.95,.015,'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
f.savefig(str(ROOT/'charts'/'delivery_vs_energy.png'),facecolor=BG)
g=df.pivot(index='year',columns='utility',values='total'); print(g.round(2)); print((g.loc[2025]-g.loc[2019]).round(2), (g.loc[2025]/g.loc[2019]-1).mul(100).round(0)); print((g.loc[2025]-g.loc[2023]).round(2))
print(dec.energy.round(2).to_dict())
