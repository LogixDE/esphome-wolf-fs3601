import pcbnew, math
from pcbnew import VECTOR2I_MM as V, FromMM as mm
L='/usr/share/kicad/footprints/'
VERSION='FS3601-ESP v1.2'
b=pcbnew.BOARD()
ds=b.GetDesignSettings()
ds.SetCopperLayerCount(2)
ds.m_TrackMinWidth=mm(0.2); ds.m_MinClearance=mm(0.2)
nc=ds.m_NetSettings.m_DefaultNetClass
nc.SetClearance(mm(0.2)); nc.SetTrackWidth(mm(0.3)); nc.SetViaDiameter(mm(0.6)); nc.SetViaDrill(mm(0.3))
W,H=76,52.5
nets={}
F=pcbnew.F_Cu; B=pcbnew.B_Cu
def net(n):
    if n not in nets:
        ni=pcbnew.NETINFO_ITEM(b,n); b.Add(ni); nets[n]=ni
    return nets[n]
def place(lib,name,ref,val,x,y,rot=0,padnets={}):
    f=pcbnew.FootprintLoad(L+lib+'.pretty',name)
    f.SetReference(ref); f.SetValue(val); f.SetFPID(pcbnew.LIB_ID(lib,name))
    b.Add(f); f.SetPosition(V(x,y)); f.SetOrientationDegrees(rot)
    for p in f.Pads():
        if p.GetNumber() in padnets: p.SetNet(net(padnets[p.GetNumber()]))
    f.Value().SetVisible(False)
    t=f.Reference(); t.SetTextSize(V(0.8,0.8)); t.SetTextThickness(mm(0.12))
    return f
def pads(f): return {p.GetNumber():(pcbnew.ToMM(p.GetPosition().x),pcbnew.ToMM(p.GetPosition().y)) for p in f.Pads()}

# ---------- routing helpers (45 deg) ----------
def sgn(v): return (v>0)-(v<0)
def p45(a,b_,first='s'):
    """a->b with one straight (h or v) and one 45deg segment. first='s' straight first, 'd' diagonal first"""
    dx,dy=b_[0]-a[0],b_[1]-a[1]; s=min(abs(dx),abs(dy))
    if s<1e-6 or abs(abs(dx)-abs(dy))<1e-6: return [a,b_]
    if first=='d': m=(a[0]+sgn(dx)*s,a[1]+sgn(dy)*s)
    elif abs(dy)>abs(dx): m=(a[0],b_[1]-sgn(dy)*s)
    else: m=(b_[0]-sgn(dx)*s,a[1])
    return [a,m,b_]
def chamf(pts,c=0.8):
    """replace 90deg axis corners by 45deg chamfers"""
    out=[pts[0]]
    for i in range(1,len(pts)-1):
        p0,p1,p2=out[-1],pts[i],pts[i+1]
        d1=(p1[0]-p0[0],p1[1]-p0[1]); d2=(p2[0]-p1[0],p2[1]-p1[1])
        l1=math.hypot(*d1); l2=math.hypot(*d2)
        ax1=abs(d1[0])<1e-6 or abs(d1[1])<1e-6; ax2=abs(d2[0])<1e-6 or abs(d2[1])<1e-6
        if ax1 and ax2 and l1>1e-6 and l2>1e-6 and abs(d1[0]*d2[0]+d1[1]*d2[1])<1e-6:
            k=min(c,l1*0.5 if i>1 else l1,l2*0.5 if i<len(pts)-2 else l2)
            out.append((p1[0]-d1[0]/l1*k,p1[1]-d1[1]/l1*k)); out.append((p1[0]+d2[0]/l2*k,p1[1]+d2[1]/l2*k))
        else: out.append(p1)
    out.append(pts[-1]); return out
def track(pts,n,layer=F,w=0.3):
    for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
        if abs(x1-x2)<1e-6 and abs(y1-y2)<1e-6: continue
        t=pcbnew.PCB_TRACK(b); t.SetStart(V(x1,y1)); t.SetEnd(V(x2,y2)); t.SetWidth(mm(w)); t.SetLayer(layer); t.SetNet(net(n)); b.Add(t)
def via(x,y,n,d=0.6,dr=0.3):
    v=pcbnew.PCB_VIA(b); v.SetPosition(V(x,y)); v.SetWidth(mm(d)); v.SetDrill(mm(dr)); v.SetNet(net(n)); b.Add(v)
def text(s,x,y,size=1.0,layer=pcbnew.F_SilkS,bold=False,just=None):
    t=pcbnew.PCB_TEXT(b); t.SetText(s); t.SetPosition(V(x,y)); t.SetLayer(layer)
    t.SetTextSize(V(size,size)); t.SetTextThickness(mm(size*0.15*(1.4 if bold else 1)))
    if just=='L': t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
    if just=='R': t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_RIGHT)
    b.Add(t); return t
def line(x1,y1,x2,y2,layer=pcbnew.Edge_Cuts,w=0.1):
    s=pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(V(x1,y1)); s.SetEnd(V(x2,y2)); s.SetLayer(layer); s.SetWidth(mm(w)); b.Add(s)
def arc(cx,cy,r,a0,a1,layer=pcbnew.Edge_Cuts,w=0.1):
    s=pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_ARC); s.SetLayer(layer); s.SetWidth(mm(w))
    s.SetCenter(V(cx,cy)); s.SetStart(V(cx+r*math.cos(math.radians(a0)),cy+r*math.sin(math.radians(a0)))); s.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(a1-a0,pcbnew.DEGREES_T)); b.Add(s)
def flip(f): f.Flip(f.GetPosition(),False)
def combo(f):
    """0805 pads carry 0603 too: draw both outlines on fab + small silk marks"""
    f.SetFPID(pcbnew.LIB_ID('FS3601','R_0603_0805_Combo'))
    o=f.GetOrientationDegrees(); x,y=pcbnew.ToMM(f.GetPosition().x),pcbnew.ToMM(f.GetPosition().y)
    for (lx,ly) in [(0.8,0.4)]:
        s=pcbnew.FP_SHAPE(f); s.SetShape(pcbnew.SHAPE_T_RECT); s.SetLayer(pcbnew.F_Fab); s.SetWidth(mm(0.08))
        if abs(o)%180==90: s.SetStart(V(x-ly,y-lx)); s.SetEnd(V(x+ly,y+lx))
        else: s.SetStart(V(x-lx,y-ly)); s.SetEnd(V(x+lx,y+ly))
        f.Add(s)

# ---------- outline with rounded corners ----------
RC=1.5
line(RC,0,W-RC,0); line(W,RC,W,H-RC); line(W-RC,H,RC,H); line(0,H-RC,0,RC)
arc(RC,RC,RC,180,270); arc(W-RC,RC,RC,270,360); arc(W-RC,H-RC,RC,0,90); arc(RC,H-RC,RC,90,180)

KW=0.5; MW=1.0; SW=0.3; PW=0.6
# ================= K side (Therme) =================
xc=[15.5+5.6*j for j in range(8)]
yo,yl=11.2,18.82          # SMDIP-4 pad rows
y8o,y8l=15.01-2.75,15.01+2.75   # SOP-4 (K8) pad rows
ym=(yo+yl)/2
outn=[('NAUS','K2')]+[(f'N{k}',f'N{k+1}' if k<6 else 'K2') for k in range(1,7)]+[('K2','K1')]
K=[]
for j in range(8):
    p4,p3=outn[j]
    if j<7: f=place('Package_DIP','SMDIP-4_W7.62mm',f'K{j+1}','TLP240A',xc[j],ym,90,{'1':'3V3','2':f'LEDK{j+1}','3':p3,'4':p4})
    else:   f=place('Package_SO','SOP-4_3.8x4.1mm_P2.54mm',f'K{j+1}','CPC1117N',xc[j],ym,90,{'1':'3V3','2':f'LEDK{j+1}','3':p3,'4':p4})
    K.append(f)
K[7].Reference().SetPosition(V(xc[7],ym-0.95)); K[7].Reference().SetTextAngleDegrees(0)
TB='TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal'
J1=place('TerminalBlock_Phoenix',TB,'J1','SPTH 1,5/2-5,08',5.5,3.2,-90,{'1':'K1','2':'K2'})
D1=place('Diode_SMD','D_SMA','D1','SMAJ12CA',9.3,5.74,90,{'1':'K1','2':'K2'}); flip(D1)
R8=place('Resistor_SMD','R_0805_2012Metric','R8','5k11',xc[0]-1.27,4.2,90,{'2':'K1','1':'NAUS'}); combo(R8)
R1=place('Resistor_SMD','R_0805_2012Metric','R1','13k0',xc[1]-1.27,4.2,90,{'2':'K1','1':'N1'}); combo(R1)
chainval=['49R9','100R','200R','390R','820R','1k6']
yr=7.6
for k in range(1,7):
    a1,a2=outn[k]
    combo(place('Resistor_SMD','R_0805_2012Metric',f'R{k+1}',chainval[k-1],xc[k],yr,0,{'1':a1,'2':a2}))
dp=pads(D1); jp=pads(J1)
yb=1.5     # K1 top bus
yk2=9.4    # K2 bottom bus
# K1: J1.1 -> bus -> K8 pad3
xk1=xc[7]+1.27
track(chamf([jp['1'],(jp['1'][0]+1.7,yb),(xk1,yb),(xk1,y8o)],1.2),'K1',w=KW)
for x in (xc[0]-1.27,xc[1]-1.27): track([(x,yb),(x,4.2-0.912)],'K1',w=KW)
track(p45(jp['1'],dp['1'],'d'),'K1',B,w=KW)
# K2: J1.2 -> D1.2 -> bottom bus -> vias
track(p45(jp['2'],dp['2'],'d'),'K2',B,w=KW)
track(p45(dp['2'],(dp['2'][0]+abs(yk2-dp['2'][1]),yk2),'d')+[(xc[7]-1.27,yk2)],'K2',B,w=KW)
for xv,ye in ((xc[0]+1.27,yo),(xc[7]-1.27,y8o)):
    via(xv,yk2,'K2'); track([(xv,yk2),(xv,ye)],'K2',w=KW)
# NAUS / N1
track([(xc[0]-1.27,4.2+0.912),(xc[0]-1.27,yo)],'NAUS',w=KW)
track(p45((xc[1]-1.27,4.2+0.912),(xc[1]-0.912,yr),'s'),'N1',w=KW)
# chain resistors -> relay pads, links along pad row
for k in range(1,7):
    a1,a2=outn[k]
    for sx,n in ((-1,a1),(1,a2)):
        xa=xc[k]+sx*0.912; xb=xc[k]+sx*1.27
        track([(xa,yr)]+p45((xa,yr+0.912),(xb,yo),'d'),n,w=KW)
    xe=xc[k+1]-1.27; ye=yo if k<6 else y8o
    track(p45((xc[k]+1.27,yo),(xe,ye),'s'),a2,w=KW)

# ================= ESP side =================
X0,Ya=2.6,28.0; Yb=Ya+15.24
rowA=['5V','GND','3V3','IO4','IO3','IO2','IO1','IO0']
rowB=['IO5','IO6','IO7','IO8','IO9','IO10','IO20','IO21']
m={'IO4':'S1','IO3':'S2','IO1':'S3','IO0':'S4','IO5':'S5','IO6':'S6','IO7':'S7','IO10':'S8','3V3':'3V3','5V':'5V','GND':'GND'}
UA=place('Connector_PinSocket_2.54mm','PinSocket_1x08_P2.54mm_Vertical','U1A','SuperMini A',X0,Ya,90,{str(i+1):m.get(n,'NC_'+n) for i,n in enumerate(rowA)})
UB=place('Connector_PinSocket_2.54mm','PinSocket_1x08_P2.54mm_Vertical','U1B','SuperMini B',X0,Yb,90,{str(i+1):m.get(n,'NC_'+n) for i,n in enumerate(rowB)})
UA.Reference().SetVisible(False); UB.Reference().SetVisible(False)
px=lambda k: X0+2.54*(k-1)
y3=21.0; yR=21.9
for j in range(8):
    ylj=yl if j<7 else y8l
    track([(xc[j]-1.27,ylj),(xc[j]-1.27,y3)],'3V3'); via(xc[j]-1.27,y3,'3V3')
    r=place('Resistor_SMD','R_0805_2012Metric',f'R{11+j}','390R',xc[j]+1.27,yR,90,{'2':f'LEDK{j+1}','1':f'S{j+1}'})
    track([(xc[j]+1.27,ylj),(xc[j]+1.27,yR-0.912)],f'LEDK{j+1}')
track([(px(3),y3),(xc[7]-1.27,y3)],'3V3',B,w=0.4)
track([(px(3),Ya),(px(3),y3)],'3V3',w=0.4); via(px(3),y3,'3V3')
lev=[24.3,25.1,25.9,26.7]
yRb=yR+0.912
for i,(k,n) in enumerate([(4,'IO4'),(5,'IO3'),(7,'IO1'),(8,'IO0')]):
    x=px(k); xr=xc[i]+1.27
    track(chamf([(x,Ya),(x,lev[i]),(xr,lev[i]),(xr,yRb)],0.6),f'S{i+1}',w=SW)
yv=24.0
for i,(k,n) in enumerate([(1,'IO5'),(2,'IO6'),(3,'IO7'),(6,'IO10')]):
    j=4+i; x=px(k); g=x+1.27; xr=xc[j]+1.27
    track([(x,Yb),(g,Yb-1.27)]+chamf([(g,Yb-1.27),(g,lev[i]),(xr,lev[i]),(xr,yv)],0.6)[1:],f'S{j+1}',B,w=SW)
    via(xr,yv,f'S{j+1}'); track([(xr,yv),(xr,yRb)],f'S{j+1}',w=SW)

# ================= 230 V =================
Xp,Yp=59.3,40.0
PS1=place('Converter_ACDC','Converter_ACDC_Hi-Link_HLK-PMxx','PS1','HLK-PM01',Xp,Yp,180,{'1':'L_F','2':'N','3':'GND','4':'5V_PS'})
F1=place('Fuse','Fuseholder_TR5_Littelfuse_No560_No460','F1','T315mA',70.5,31.5,90,{'1':'L_IN','2':'L_F'})
RV1=place('Varistor','RV_Disc_D7mm_W3.4mm_P5mm','RV1','S07K275',66.0,14.0,-90,{'1':'L_F','2':'N'})
J3=place('TerminalBlock_Phoenix',TB,'J3','SPTH 1,5/2-5,08',70.5,45.3,90,{'1':'N','2':'L_IN'})
for f_ in b.GetFootprints():
    r_=f_.GetReference()
    if r_[0] in 'RFCDJ' or r_.startswith('RV'): f_.Reference().SetVisible(False)
fp=pads(F1); rp=pads(RV1); pp=pads(PS1); j3=pads(J3)
track([j3['2'],fp['1']],'L_IN',w=MW)
# L_F top: F1.2 up to varistor
track(p45(fp['2'],rp['1'],'s'),'L_F',w=MW)
# L_F bottom: F1.2 -> PS1 pin1
xl=63.3
track(chamf([fp['2'],(xl,fp['2'][1]),(xl,pp['1'][1]-(xl-pp['1'][0]))],1.0)+[pp['1']],'L_F',B,w=MW)
# N: J3.1 -> PS1 pin2 and varistor
xn=64.2
track(chamf([j3['1'],(xn,j3['1'][1]),(xn,pp['2'][1]+(xn-pp['2'][0]))],1.2)+[pp['2']],'N',w=MW)
track(chamf([(xn,pp['2'][1]+(xn-pp['2'][0])),(xn,rp['2'][1]+1.0)],1)+[rp['2']],'N',w=MW)
# ================= DC =================
D2=place('Diode_SMD','D_SMA','D2','B180',22.5,31.6,0,{'1':'5V','2':'5V_PS'})
for g_ in list(D2.GraphicalItems()):
    if g_.GetLayer()==pcbnew.F_SilkS: D2.Remove(g_)
C1=place('Capacitor_SMD','C_0805_2012Metric','C1','10uF',12.0,32.4,90,{'2':'5V','1':'GND'})
C1.Reference().SetVisible(False); D2.Reference().SetVisible(False)
d2=pads(D2)
track(p45(pp['4'],(d2['2'][0]+0.0,31.6),'d'),'5V_PS',w=PW)
track(chamf([d2['1'],(X0,31.6),(X0,Ya)],1.0),'5V',w=PW)
# GND via pour (both layers)
# ================= GND pour (SELV area only) =================
for lay in (F,B):
    z=pcbnew.ZONE(b); z.SetLayer(lay); z.SetNet(net('GND')); z.SetLocalClearance(mm(0.3)); z.SetMinThickness(mm(0.25))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL); z.SetThermalReliefGap(mm(0.3)); z.SetThermalReliefSpokeWidth(mm(0.4))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    o=z.Outline(); o.NewOutline()
    for x,y in [(0.4,20.3),(51,20.3),(51,50.6),(49.5,52.1),(1.9,52.1),(0.4,50.6)]: o.Append(mm(x),mm(y))
    b.Add(z)
# antenna keepout: no copper pour under the chip antenna end of the Super Mini (opposite USB-C)
ka=pcbnew.ZONE(b); ka.SetIsRuleArea(True); ka.SetDoNotAllowCopperPour(True); ka.SetDoNotAllowTracks(False); ka.SetDoNotAllowVias(False); ka.SetDoNotAllowPads(False); ka.SetDoNotAllowFootprints(False)
lsa=pcbnew.LSET(); lsa.AddLayer(F); lsa.AddLayer(B); ka.SetLayerSet(lsa)
oa=ka.Outline(); oa.NewOutline()
for x,y in [(14.5,27.0),(27.5,27.0),(27.5,44.5),(14.5,44.5)]: oa.Append(mm(x),mm(y))
b.Add(ka)
# stitching vias
for (x,y) in [(5.0,47.5),(16,47.5),(25,48.5),(36,49.5),(44,49.5),(44,37),(49.5,30),(49.5,45),(8,34.5),(36,46)]:
    via(x,y,'GND')
# holes
for (x,y) in [(70.0,5.0),(12.0,48.8),(4.0,19.5)]:
    h=pcbnew.FootprintLoad(L+'MountingHole.pretty','MountingHole_3.2mm_M3'); h.SetFPID(pcbnew.LIB_ID('MountingHole','MountingHole_3.2mm_M3')); h.SetReference('H'); h.SetPosition(V(x,y)); h.Reference().SetVisible(False); h.Value().SetVisible(False); b.Add(h)
# keepout band between relay pad rows
za=pcbnew.ZONE(b); za.SetIsRuleArea(True); za.SetDoNotAllowTracks(True); za.SetDoNotAllowVias(True); za.SetDoNotAllowCopperPour(True); za.SetDoNotAllowPads(False); za.SetDoNotAllowFootprints(False)
ls=pcbnew.LSET(); ls.AddLayer(F); ls.AddLayer(B); za.SetLayerSet(ls)
o=za.Outline(); o.NewOutline()
for x,y in [(12.5,13.0),(58.0,13.0),(58.0,17.0),(12.5,17.0)]: o.Append(mm(x),mm(y))
b.Add(za)
# silkscreen
SB=pcbnew.B_SilkS
for j,t in enumerate(['AUS','50','100','200','390','820','1k6','FB']): text(t,xc[j],15.0 if j<7 else ym+0.95,0.8)
text('K1',12.0,jp['1'][1],0.9,bold=True); text('K2',12.0,jp['2'][1],0.9,bold=True); text('Therme',5.5,12.2,0.8); text('K1 = N',5.5,13.4,0.8)
text('L',75.0,36.4,0.9,bold=True,just='R'); text('N',75.0,49.6,0.9,bold=True,just='R')
text('230V~',70.5,22.2,0.9,bold=True)
for i,t in enumerate(['5V','G','3V3','4','3','2','1','0']): text(t,X0+2.54*i,30.25,0.8)
for i,t in enumerate(['5','6','7','8','9','10','20','21']): text(t,X0+2.54*i,40.95,0.8)
text('< USB-C',1.0,36.6,0.8,just='L')
text('R1-R8: 0603/0805',30.0,4.6,0.8,just='L')
def tb(s,x,y,size=0.8,bold=False):
    t=pcbnew.PCB_TEXT(b); t.SetText(s); t.SetPosition(V(x,y)); t.SetLayer(SB); t.SetTextSize(V(size,size)); t.SetTextThickness(mm(size*0.15*(1.4 if bold else 1))); t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT); t.SetMirrored(True); b.Add(t)
tb(VERSION,58,30,1.2,True)
tb('Ersatz Wolf FS 3601 (K1-K2)',58,32.0)
rows=[('K1 AUS 5k11','IO4'),('K2 Bit0 49R9','IO3'),('K3 Bit1 100R','IO1'),('K4 Bit2 200R','IO0'),('K5 Bit3 390R','IO5'),('K6 Bit4 820R','IO6'),('K7 Bit5 1k6','IO7'),('K8 Fallback NC','IO10')]
for i,(a_,g) in enumerate(rows): tb(a_+'  '+g,58,34.0+i*1.2)
tb('GPIO aktiv LOW',58,44.0)
pcbnew.SaveBoard('fb3.kicad_pcb',b)
b=pcbnew.LoadBoard('fb3.kicad_pcb'); b.BuildConnectivity()
filler=pcbnew.ZONE_FILLER(b); filler.Fill(b.Zones())
pcbnew.SaveBoard('fb3.kicad_pcb',b)
print('ok', pp, d2)
