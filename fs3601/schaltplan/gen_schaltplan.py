S=[]
def a(s): S.append(s)
def line(x1,y1,x2,y2,dash=False):
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="2"{" stroke-dasharray=\"6 4\"" if dash else ""}/>')
def poly(pts): a('<polyline points="'+" ".join(f"{x},{y}" for x,y in pts)+'" fill="none" stroke="#111" stroke-width="2"/>')
def dot(x,y): a(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#111"/>')
def cont(x,y): a(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#111" stroke-width="2"/>')
def txt(x,y,t,size=13,anchor="start",w="normal",col="#111"):
    a(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{col}">{t}</text>')
def rh(x1,x2,y,label,dash=False,col="#111"):  # horizontal resistor between x1..x2
    m=(x1+x2)/2; line(x1,y,m-28,y); line(m+28,y,x2,y)
    a(f'<rect x="{m-28}" y="{y-9}" width="56" height="18" fill="#fff" stroke="{col}" stroke-width="2"{" stroke-dasharray=\"5 3\"" if dash else ""}/>')
    txt(m,y-13,label,11.5,"middle",col=col)
def rv(x,y1,y2,label,dash=False,col="#111",lx=14):
    m=(y1+y2)/2; line(x,y1,x,m-28); line(x,m+28,x,y2)
    a(f'<rect x="{x-9}" y="{m-28}" width="18" height="56" fill="#fff" stroke="{col}" stroke-width="2"{" stroke-dasharray=\"5 3\"" if dash else ""}/>')
    for i,l in enumerate(label.split("|")): txt(x+lx,m-4+i*15,l,11.5,col=col)
def arrow(x1,y1,x2,y2):
    import math
    line(x1,y1,x2,y2); ang=math.atan2(y2-y1,x2-x1); L=10
    p=[(x2,y2),(x2-L*math.cos(ang-0.4),y2-L*math.sin(ang-0.4)),(x2-L*math.cos(ang+0.4),y2-L*math.sin(ang+0.4))]
    a('<polygon points="'+" ".join(f"{x:.1f},{y:.1f}" for x,y in p)+'" fill="#111"/>')
W,H=1640,1140
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
txt(20,28,"Fernversteller FS 3601 (Platine C 5148e) – Schaltplan, Stand 17.11.2026",18,w="bold")
txt(20,48,"Bauteilwerte: Farbcode gelesen, 5,11 k und NTC gemessen · Lötaugen-Nummern in grau · blaue Ziffern/Buchstaben = Schalterstellung",12,col="#555")
# rails
K1y,K2y,K3y=90,850,900
line(60,K1y,1030,K1y); line(60,K2y,1385,K2y); line(60,K3y,1430,K3y)
for y,l in [(K1y,"Klemme 1"),(K2y,"Klemme 2"),(K3y,"Klemme 3")]:
    a(f'<rect x="20" y="{y-11}" width="40" height="22" fill="#e8f0e8" stroke="#111" stroke-width="2"/>'); txt(40,y+4,l[-1],13,"middle","bold"); txt(64,y-6,l,12,w="bold")
txt(64,K1y+16,"(90)",11,col="#777"); txt(64,K2y+16,"(91)",11,col="#777"); txt(64,K3y+16,"(92)",11,col="#777")
# --- N bus & NTC
Nx=150; line(Nx,180,Nx,560); dot(Nx,180) if False else None
rv(Nx,560,K2y,"NTC|7,4 k @ 21 °C|(96–98)"); dot(Nx,K2y)
a(f'<line x1="{Nx-16}" y1="{(560+K2y)/2+22}" x2="{Nx+16}" y2="{(560+K2y)/2-22}" stroke="#111" stroke-width="1.5"/>')
txt(Nx-8,175,"N",12,"end","bold")
# K2 bus
Kb=560; line(Kb,170,Kb,K2y); dot(Kb,K2y)
# S1a  (Segment 6 = N)
ys=[170,205,240,275]; cx=240
txt(cx-40,148,"S1a (Segment 6)",12,w="bold")
for y in ys: cont(cx,y)
arrow(Nx,222,cx-8,222); dot(Nx,222)
for y,l,st in zip(ys,["5","3","4","7"],["0","3","6","9"]): txt(cx+8,y-6,l,10,col="#888"); txt(cx-12,y+4,st,12,"end","bold",col="#06c")
line(cx+5,ys[0],Kb,ys[0]); dot(Kb,ys[0])
rh(cx+5,Kb,ys[1],"R1 13,0 k"); dot(Kb,ys[1])
rh(cx+5,Kb,ys[2],"R2 39,2 k"); dot(Kb,ys[2])
rh(cx+5,Kb,ys[3],"Rx n.b. (2–17)",dash=True,col="#888"); dot(Kb,ys[3])
# S1b  (Segment 14 = N)
Xx=620
ys2=[380,415,450,485]
txt(cx-40,358,"S1b (Segment 14)",12,w="bold")
for y in ys2: cont(cx,y)
arrow(Nx,432,cx-8,432); dot(Nx,432)
for y,l,st in zip(ys2,["9","21","25","29"],["0","3","6","9"]): txt(cx+8,y-6,l,10,col="#888"); txt(cx-12,y+4,st,12,"end","bold",col="#06c")
for y,l in zip(ys2[:3],["R6 13,0 k","R7 6,65 k","R8 2,87 k"]):
    rh(cx+5,Xx,y,l); dot(Xx,y)
line(cx+5,ys2[3],Xx,ys2[3]); txt((cx+Xx)/2,ys2[3]-6,"0 Ω",11.5,"middle"); dot(Xx,ys2[3])
line(Xx,170,Xx,560)
txt(Xx-6,164,"X",12,"end","bold")
# S1c  (Segment 24 = Kl. 1)
ys3=[170,205,240,275]; cx3=800
txt(cx3-30,148,"S1c (Segment 24)",12,w="bold")
for y,l,st in zip(ys3,[("28","R5 4,99 k"),("27","R4 10,0 k"),("20","R3 33,2 k"),("8",None)],["0","3","6","9"]):
    if l[1]: rh(Xx,cx3-5,y,l[1]); dot(Xx,y)
    else: txt(cx3-12,y+4,"frei",11,"end",col="#777")
    cont(cx3,y); txt(cx3+8,y-6,l[0],10,col="#888"); txt(cx3+30,y+5,st,12,w="bold",col="#06c")
C3=880; line(C3,K1y,C3,222); dot(C3,K1y); arrow(C3,222,cx3+8,222)
txt(C3+6,215,"(19/24 an Kl. 1)",10,col="#888")

# P1 Sollwert (rheostat) X -> Wn
rv(Xx,560,690,"P1 5 k|„Sollwert ±“|(53/58/64 – 52/57)")
arrow(Xx-34,650,Xx+20,600)
dot(Xx,690)
txt(Xx-8,708,"W",12,"end","bold")
# W -> P2 wiper
Px=960
poly([(Xx,690),(Xx,720),(900,720),(900,305),(Px-14,305)])
arrow(900,305,Px-11,305)
# P2 pot: top to K1, bottom to M
rv(Px,K1y,520,"",lx=16)
for i,l in enumerate(["P2 5 k „Nacht“","(19 – 23, Schleifer 18/22)"]): txt(1040,300+i*15,l,11.5)
dot(Px,K1y)
Mx,My=Px,520; dot(Mx,My); txt(Mx-10,My+4,"M",12,"end","bold")
# S2 – zwei Ebenen, Spalten = Stellungen a..e
def bar(x1,x2,y): a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#111" stroke-width="6"/>')
X3=[1060,1120,1180,1240,1300]; X1=[x+25 for x in X3]
y3,yb3,y1,yb1=610,580,720,750
txt(1040,535,"S2 Betriebsart – 2 Schleifer (180°), Spalte = Raststellung",12,w="bold")
for x,p in zip(X3,"abcde"): txt(x+12,560,p,14,"middle","bold",col="#06c")
bar(1045,1320,yb3); txt(1328,yb3-6,"Seg. 50",10,col="#555")
bar(1070,1345,yb1); txt(1220,yb1+20,"Seg. 56",10,col="#555")
for x,n in zip(X3,["55","44","39","38","40"]):
    line(x,yb3,x,y3-5,dash=True); cont(x,y3); txt(x+7,y3+18,n,9.5,col="#888")
for x,n in zip(X1,["51","63","66","70","65"]):
    line(x,yb1,x,y1+5,dash=True); cont(x,y1); txt(x+7,y1-9,n,9.5,col="#888")
# a: 55 -> R9 -> K2
line(X3[0],y3+5,X3[0],770); rv(X3[0],770,K2y,"R9 5,11 k|(47–72)",lx=-112); dot(X3[0],K2y)
# b: 44 -> M ; d: 70 -> M
line(X3[1],y3+5,X3[1],680); dot(X3[1],680)
poly([(Mx,My),(Mx,680),(X1[3],680),(X1[3],y1-5)]); dot(Mx,680) if False else None
# e: 65 -> R10 -> K2
poly([(X1[4],y1-5),(X1[4],690),(1385,690),(1385,770)]); rv(1385,770,K2y,"R10|5,11 k*",col="#b00",lx=14); dot(1385,K2y)
# Segment 56 -> Kl. 1
poly([(1070,yb1),(1030,yb1),(1030,K1y)]); dot(1030,K1y)
# Segment 50 -> Kl. 3
poly([(1320,yb3),(1430,yb3),(1430,K3y)]); dot(1430,K3y)
# Legende Stellungen
lx=1460; ly=560
txt(lx,ly,"Stellungen S2",12,w="bold")
for i,(p,t) in enumerate([("a","Uhr 0 / ☼"),("b","Uhr ☾ / ☼"),("c","☼ Dauer Tag"),("d","☾ Dauer Nacht"),("e","0 Aus")]):
    txt(lx,ly+22+i*20,p,13,w="bold",col="#06c"); txt(lx+18,ly+22+i*20,t,12.5)
txt(lx,ly+135,"S1 Raumeinfluss",12,w="bold")
txt(lx,ly+155,"Ziffer am Kontakt = Stellung",11.5)
txt(lx,ly+190,"S2 frei: 39, 38, 40, 51, 63, 66",10.5,col="#777")
txt(lx,ly+205,"Pos. f (45 = Kl. 1 / 62) gesperrt",10.5,col="#777")
# Ry
rv(330,K2y,K3y,"Ry n.b. (46–71)",dash=True,col="#888"); dot(330,K2y); dot(330,K3y)
# notes + table
ny=950
txt(20,ny,"S1 „Raumeinfluss 0/3/6/9“: 3 Schleifer (120°). Pos. 0 schließt den NTC kurz → Raumtemperatur ohne Wirkung.",11.5,col="#333")
txt(20,ny+18,"* R10 nachträglich: Kontakt 65 war ab Werk direkt an Kl. 2 (Leiterbahn über 78 / unter 63 aufgebohrt) → Pos. e ab Werk = Brücke K1–K2 = „wie ohne Fernbedienung“.",11.5,col="#b00")
txt(20,ny+36,"Kl. 3 = Schaltuhr-Ausgang der Therme: In Absenkzeiten legt die Uhr Kl. 3 auf Kl. 1 → Pos. a wirkt dann wie e, Pos. b wie d.",11.5,col="#333")
txt(20,ny+54,"K1–K2 bei Raumeinfluss 0 (Nachttrimmer Mitte): Tag 14,7–16,0 k · Nacht 14,0–15,8 k · Aus ≈ 3,8 k (5,11 k ∥ Tag) · ohne FB: 0 Ω",11.5,w="bold")
txt(20,ny+72,"Allgemein: R(K1–K2) = R_S1b + (NTC ∥ R_S1a) + R_S1c ∥ (Ra + P1)  mit Ra = P2-Anteil 19–W (Nacht: Ra ∥ Rb)",11.5,col="#333")
txt(20,ny+90,"n.b. = Bestückungsplatz ohne Bauteil",11.5,col="#555")
a('</svg>')
open('FS3601_Schaltplan.svg','w').write("\n".join(S))
