S=[]
def a(s): S.append(s)
def line(x1,y1,x2,y2,dash=False,col="#111",w=2):
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{" stroke-dasharray=\"6 4\"" if dash else ""}/>')
def dot(x,y): a(f'<circle cx="{x}" cy="{y}" r="4" fill="#111"/>')
def txt(x,y,t,size=13,anchor="start",w="normal",col="#111"):
    a(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{col}">{t}</text>')
def rh(x1,x2,y,label):
    m=(x1+x2)/2; line(x1,y,m-24,y); line(m+24,y,x2,y)
    a(f'<rect x="{m-24}" y="{y-8}" width="48" height="16" fill="#fff" stroke="#111" stroke-width="2"/>'); txt(m,y-12,label,11.5,"middle")
def rv(x,y1,y2,label,lx=12):
    m=(y1+y2)/2; line(x,y1,x,m-24); line(x,m+24,x,y2)
    a(f'<rect x="{x-8}" y="{m-24}" width="16" height="48" fill="#fff" stroke="#111" stroke-width="2"/>')
    for i,l in enumerate(label.split("|")): txt(x+lx,m-2+i*14,l,11.5)
def contact_h(x1,x2,y,nc=False,label=""):
    # horizontal switch contact between x1..x2 at y
    m=(x1+x2)/2; line(x1,y,m-12,y); line(m+12,y,x2,y)
    a(f'<circle cx="{m-12}" cy="{y}" r="2.5" fill="#111"/><circle cx="{m+12}" cy="{y}" r="2.5" fill="#111"/>')
    if nc: line(m-12,y,m+14,y+3)
    else: line(m-12,y,m+12,y-10)
    txt(m,y+20,label,11,"middle",col="#0a5")
def contact_v(x,y1,y2,nc=False,label=""):
    m=(y1+y2)/2; line(x,y1,x,m-12); line(x,m+12,x,y2)
    a(f'<circle cx="{x}" cy="{m-12}" r="2.5" fill="#111"/><circle cx="{x}" cy="{m+12}" r="2.5" fill="#111"/>')
    if nc: line(x,m-12,x+3,m+14)
    else: line(x,m-12,x-10,m+12)
    txt(x+8,m+4,label,11,col="#0a5")
W,H=1320,985
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#fff"/>')
txt(20,30,"FS3601-ESP v1.2 (Bestückung Firmware 1.4) – Ersatz für den Fernversteller Wolf FS 3601 (nur Klemmen 1 und 2)",18,w="bold")
txt(20,50,"Therme-Seite (oben) und ESP-Seite (unten) sind nur über die PhotoMOS-Optokoppler verbunden (K1–K7 TLP240A 5 kV, K8 CPC1117N 1,5 kV).",12,col="#555")
# rails
yK1,yK2=110,330
line(120,yK1,1270,yK1); line(120,yK2,1270,yK2)
a(f'<rect x="30" y="{yK1-12}" width="50" height="24" fill="#e8f0e8" stroke="#111" stroke-width="2"/>'); txt(55,yK1+5,"K1",13,"middle","bold")
a(f'<rect x="30" y="{yK2-12}" width="50" height="24" fill="#e8f0e8" stroke="#111" stroke-width="2"/>'); txt(55,yK2+5,"K2",13,"middle","bold")
line(80,yK1,120,yK1); line(80,yK2,120,yK2); txt(30,yK1-18,"J1 → Therme Kl. 1 (N)",11.5); txt(30,yK2+30,"J1 → Therme Kl. 2",11.5)
# TVS
x=150; dot(x,yK1); dot(x,yK2); line(x,yK1,x,200); line(x,240,x,yK2)
a(f'<polygon points="{x-10},200 {x+10},200 {x},220" fill="#fff" stroke="#111" stroke-width="2"/><polygon points="{x-10},240 {x+10},240 {x},220" fill="#fff" stroke="#111" stroke-width="2"/>')
line(x-12,220,x+12,220); txt(x+14,224,"D1 SMAJ12CA",11.5)
# FB (K8, NC)
x=290; dot(x,yK1); dot(x,yK2); contact_v(x,yK1,yK2,nc=True,label="K8 CPC1117N (Öffner)")
txt(x-12,yK2+48,"Fallback: ESP aus →",11,"middle",col="#b00"); txt(x-12,yK2+62,"Brücke = Therme intern",11,"middle",col="#b00")
# AUS
x=470; dot(x,yK1); dot(x,yK2); rv(x,yK1,200,"R8|5,11 k",lx=12); contact_v(x,200,yK2,label="K1 „Aus“")
# chain
xs=600; dot(xs,yK1); line(xs,yK1,xs,220); 
x0=xs; rh(xs,690,220,"R1 13,0 k")
xx=690; vals=[("R2","68"),("R3","120"),("R4","220"),("R5","470"),("R6","910"),("R7","1,8 k")]
for i,(r,v) in enumerate(vals):
    x1=xx+i*95; x2=x1+95
    rh(x1,x2,220,f"{r} {v}")
    dot(x1,220); dot(x2,220); line(x1,220,x1,265); line(x2,220,x2,265); contact_h(x1,x2,265,label=f"K{i+2} Bit{i}")
xe=xx+6*95; line(xe,220,xe+12,220); line(xe+12,220,xe+12,yK2); dot(xe+12,yK2)
txt(625,165,"R(K1–K2) = 13,0 k + Σ (Widerstände, deren Relais offen ist)",12,col="#333")
txt(625,182,"→ 13,0 … 16,6 kΩ (gemessen 12,88 … 16,37 kΩ), 64 Kombinationen, Firmware wählt die nächstliegende",12,col="#333")
# separation
line(20,415,W-20,415,dash=True,col="#b00",w=2); txt(W-30,408,"Trennung über PhotoMOS (TLP240A / CPC1117N)",12,"end",col="#b00")
# ESP side
ux,uy=60,470
a(f'<rect x="{ux}" y="{uy}" width="230" height="290" fill="#eef3fb" stroke="#111" stroke-width="2"/>')
txt(ux+115,uy+24,"U1 ESP32-C3 Super Mini",13,"middle","bold"); txt(ux+115,uy+42,"5 V von PS1 über D2 (oder USB-C)",11,"middle",col="#555")
gp=[("IO4","K1 Aus"),("IO3","K2 Bit0"),("IO1","K3 Bit1"),("IO0","K4 Bit2"),("IO5","K5 Bit3"),("IO6","K6 Bit4"),("IO7","K7 Bit5"),("IO10","K8 Fallback")]
y3=500; line(420,y3,1270,y3); txt(1270,y3-8,"3V3",12,"end","bold")
line(ux+230,y3,420,y3); txt(ux+236,y3-6,"3V3",11)
for i,(g,k) in enumerate(gp):
    y=uy+70+i*27
    txt(ux+222,y+4,g,12,"end"); line(ux+230,y,360+i*0,y)
    # resistor to LED cathode, LED anode to 3V3
    xr=360; xl=560+i*90
    rh(xr,xr+110,y,"390 Ω") if False else None
    line(ux+230,y,xl-40,y)
    a(f'<rect x="{xl-90}" y="{y-7}" width="40" height="14" fill="#fff" stroke="#111" stroke-width="1.6"/>')
    txt(xl-70,y-10,"390",10,"middle")
    # LED (vertical, anode up)
    line(xl,y,xl,y) 
    line(xl-40,y,xl,y); line(xl,y,xl,y-14)
    a(f'<polygon points="{xl-7},{y-28} {xl+7},{y-28} {xl},{y-16}" fill="#fff" stroke="#111" stroke-width="1.6"/>'); line(xl-7,y-16,xl+7,y-16,w=1.6)
    line(xl,y-28,xl,y3); dot(xl,y3)
    txt(xl+10,y-18,k,10.5,col="#0a5")
txt(560,uy+300,"Ansteuerung aktiv LOW: GPIO = LOW → LED an (≈ 5 mA). Beim Booten / ohne Firmware sind alle LEDs aus:",12,col="#333")
txt(560,uy+316,"Schließer K1–K7 offen, Öffner K8 geschlossen → K1–K2 überbrückt, Therme regelt wie ohne Fernbedienung.",12,col="#333")

# supply section
line(20,812,W-20,812,dash=True,col="#b00",w=2); txt(W-30,830,"Netzteil: 230 V → 5 V (HLK-PM01, 3 kV isoliert)",12,"end",col="#b00")
yL,yN=870,940
a(f'<rect x="30" y="{yL-12}" width="50" height="24" fill="#fde8e8" stroke="#111" stroke-width="2"/>'); txt(55,yL+5,"L",13,"middle","bold")
a(f'<rect x="30" y="{yN-12}" width="50" height="24" fill="#fde8e8" stroke="#111" stroke-width="2"/>'); txt(55,yN+5,"N",13,"middle","bold")
txt(30,yL-18,"J3 230 V~",11.5)
line(80,yL,150,yL); a(f'<rect x="150" y="{yL-8}" width="60" height="16" fill="#fff" stroke="#111" stroke-width="2"/>'); line(150,yL,210,yL,w=1.2); txt(180,yL-12,"F1 T315mA",11,"middle")
line(210,yL,420,yL); line(80,yN,420,yN)
x=300; dot(x,yL); dot(x,yN); line(x,yL,x,yL+20); line(x,yN,x,yN-20)
a(f'<rect x="{x-8}" y="{yL+20}" width="16" height="30" fill="#fff" stroke="#111" stroke-width="2"/>'); line(x-14,yL+50,x+14,yL+20,w=1.4); txt(x+14,yL+40,"RV1 S07K275",11)
a(f'<rect x="420" y="{yL-20}" width="170" height="{yN-yL+40}" fill="#f5f5f5" stroke="#111" stroke-width="2"/>')
txt(505,(yL+yN)/2-4,"PS1 HLK-PM01",13,"middle","bold"); txt(505,(yL+yN)/2+14,"230 V~ → 5 V / 0,6 A",11,"middle")
txt(428,yL+4,"AC/L",10.5); txt(428,yN+4,"AC/N",10.5); txt(582,yL+4,"+Vo",10.5,"end"); txt(582,yN+4,"−Vo",10.5,"end")
line(590,yL,680,yL); a(f'<polygon points="680,{yL-9} 680,{yL+9} 700,{yL}" fill="#fff" stroke="#111" stroke-width="2"/>'); line(700,yL-9,700,yL+9); txt(690,yL-14,"D2 B180",11,"middle")
line(700,yL,900,yL); txt(905,yL+4,"5V → U1 Pin 5V",12,w="bold")
line(590,yN,900,yN); txt(905,yN+4,"GND → U1 Pin GND",12,w="bold")
x=780; dot(x,yL); dot(x,yN); line(x,yL,x,(yL+yN)/2-5); line(x,(yL+yN)/2+5,x,yN); line(x-12,(yL+yN)/2-5,x+12,(yL+yN)/2-5); line(x-12,(yL+yN)/2+5,x+12,(yL+yN)/2+5); txt(x+16,(yL+yN)/2+4,"C1 10 µF",11)
txt(905,yL+26,"D2 verhindert Rückspeisung ins Netzteil,",11,col="#555"); txt(905,yL+40,"wenn zusätzlich USB-C steckt.",11,col="#555")
a('</svg>')
open('out/FS3601-ESP_Schaltplan.svg','w').write("\n".join(S))
