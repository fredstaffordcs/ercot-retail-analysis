import textwrap, numpy as np, pandas as pd, matplotlib, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
"""Render one PNG per year (1990-2025) of every Texas utility's residential price.
Reads data/utility_level/residential_prices_by_utility_1990_2025.csv; writes frames to charts/animation/frames/.
To make the video:  ffmpeg -framerate 1 -i charts/animation/frames/f%d.png -pix_fmt yuv420p charts/animation/animated.mp4
(frame file names are f1990.png ... f2025.png; use -pattern_type glob -i 'charts/animation/frames/f*.png' to assemble them)
"""
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
for f in fm.findSystemFonts():
    if 'Inter' in f and 'Display' not in f: fm.fontManager.addfont(f)
plt.rcParams['font.family']='Inter'
D=pd.read_csv(ROOT/'data/utility_level/residential_prices_by_utility_1990_2025.csv').rename(columns={'group':'g','res_cents_kwh_real2025':'c','res_cents_kwh_nominal':'c_nom'}); (ROOT/'charts/animation/frames').mkdir(parents=True,exist_ok=True); YEARS=list(range(1990,2026))
BG='#fcfcfb'; FG='#1c2421'; MU='#5d6b66'; GR='#e3e7e5'
COL={'rep':'#c2570c','pub':'#1f77a8','iou':'#7d6e64','npub':'#2a9d70'}
LAB={'rep':'ERCOT: regulated utilities,\nthen retailers (from 2002)','pub':'ERCOT public power\n(municipals and co-ops)','iou':'Non-ERCOT investor-owned\nutilities (bundled)','npub':'Non-ERCOT public power\n(municipals and co-ops)'}
order=['rep','pub','iou','npub']
W,H=1440,1080; AX=[.265,.17,.685,.57]; aw=AX[2]*W; ah=AX[3]*H
x0,x1=4,30; ppc=aw/(x1-x0); KS=.022
def rad(c): return max(2.6,KS*np.sqrt(c))
def swarm(d):
    out=[]; placed=[]
    for _,r in d.sort_values('res_cust',ascending=False).iterrows():
        rd=rad(r.res_cust); px=(min(max(r.c,x0+.15),x1-.15)-x0)*ppc
        for k in range(400):
            off=((k+1)//2)*1.5*(1 if k%2 else -1)
            if all((px-qx)**2+(off-qy)**2>=(rd+qr+.8)**2 for qx,qy,qr in placed): break
        placed.append((px,off,rd)); out.append((r.c,off,rd))
    return out
L={}; need={g:0 for g in order}
for y in YEARS:
    for g in order:
        d=D[(D.Year==y)&(D.g==g)]; s=swarm(d); L[(y,g)]=s
        if s: need[g]=max(need[g],max(abs(o)+r for _,o,r in s))
hts={g:2*need[g]+44 for g in order}
tot=sum(hts.values()); print({g:round(v) for g,v in hts.items()},round(tot),round(ah))
if True: sc=ah/tot; hts={g:v*sc for g,v in hts.items()}; print('scaled',sc)
def frame(y):
    f=plt.figure(figsize=(14.4,10.8),dpi=100,facecolor=BG)
    f.text(.05,.945,'Texas residential electricity prices,\nutility by utility, 1990–2025',fontsize=31,fontweight='bold',color=FG,va='center',linespacing=1.12)
    f.text(.95,.945,str(y),fontsize=62,fontweight='bold',color='#c9d0cd',va='center',ha='right')
    sub=('Each bubble is one utility or retailer: position is its average residential revenue per kWh, bundled (power + delivery), in 2025 cents (CPI-U); area is its number of residential customers.',
         'Black lines are customer-weighted group averages. ERCOT’s top group is its regulated utilities through 2001 and competitive retailers from 2002.')
    f.text(.05,.875,'\n'.join(textwrap.fill(p,135,initial_indent='•  ',subsequent_indent='    ') for p in sub),fontsize=13,color=MU,va='top',linespacing=1.45)
    ax=f.add_axes(AX); ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xlim(x0,x1); ax.set_ylim(0,ah); ax.set_yticks([])
    ax.set_xticks(range(4,31,2)); ax.set_xticklabels([f'{i}¢' for i in range(4,31,2)],fontsize=12,color=MU); ax.tick_params(length=0)
    ax.grid(axis='x',color=GR,lw=.8); ax.set_axisbelow(True)
    top=ah
    for g in order:
        h=hts[g]; cy=top-h/2; top-=h; ax.axhline(top,color=GR,lw=1)
        d=D[(D.Year==y)&(D.g==g)]
        for (c,off,rd) in L[(y,g)]:
            cc=min(max(c,x0+.15),x1-.15)
            ax.scatter(cc,cy-2+off,s=(2*rd*72/100)**2,facecolor=COL[g],edgecolor=BG,linewidth=.7,alpha=.9,zorder=4)
        v=d.res_rev.sum()/d.res_mwh.sum()*100*(D[D.Year==y].c.iloc[0]/D[D.Year==y].c_nom.iloc[0])
        ax.plot([v,v],[cy-h/2+6,cy+h/2-26],color=FG,lw=2,zorder=6)
        ax.text(v,cy+h/2-24,f'{v:.1f}¢',ha='center',va='bottom',fontsize=12,fontweight='bold',color=FG,zorder=7,bbox=dict(boxstyle='round,pad=.15',fc=BG,ec='none'))
        f.text(.05,AX[1]+(cy/ah)*AX[3]+.012,LAB[g],fontsize=12.5,fontweight='bold',color=COL[g],va='center',linespacing=1.25)
        f.text(.05,AX[1]+(cy/ah)*AX[3]-.032,f'{len(d)} companies, {d.res_cust.sum()/1e6:.1f}M customers',fontsize=10.5,color=MU,va='center')
    ax.set_xlabel('Average residential revenue per kWh, in 2025 cents (bundled)',fontsize=12,color=MU,labelpad=8)
    foot=('Source: EIA-861 annual survey, 1990–2025, residential sales of bundled service in Texas; revenue ÷ kWh by company, adjusted to 2025 dollars with CPI-U (BLS). Black lines: customer-weighted group averages. '
          'ERCOT competitive retailers are as reported to EIA, net of any bill credits. Excluded: companies with fewer than 500 residential customers, adjustment rows, behind-the-meter and facility entries. '
          'From 2012 EIA’s full-form data omit small co-ops and municipals that filed earlier, so public-power counts drop that year (2019 filtered to match). Bubbles outside the axis are drawn at its edge (e.g., Griddy Energy, 97¢ in 2021). '
          'Non-ERCOT investor-owned: Entergy, El Paso Electric, SPS, SWEPCO (and in some years Sharyland/other small IOUs).')
    f.text(.05,.118,textwrap.fill(foot,200),fontsize=9.6,color=MU,va='top',linespacing=1.4)
    f.add_artist(Line2D([.05,.95],[.036,.036],color=GR,lw=1,transform=f.transFigure))
    f.text(.05,.018,'Fred Stafford',fontsize=14,fontweight='bold',color=FG,va='center')
    f.text(.155,.018,'@fredstaffordcs',fontsize=14,color=FG,va='center')
    f.text(.95,.018,'PublicPowerReview.org',fontsize=14,fontweight='bold',color=FG,va='center',ha='right')
    f.savefig(str(ROOT/f'charts/animation/frames/f{y}.png'),facecolor=BG); plt.close(f)
for y in (YEARS if len(sys.argv)<2 else [int(v) for v in sys.argv[1:]]): frame(y)
