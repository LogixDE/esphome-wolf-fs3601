import pcbnew,itertools
import sys; b=pcbnew.LoadBoard(sys.argv[1] if len(sys.argv)>1 else 'fb.kicad_pcb')
groups={'NETZ':{'L_IN','L_F','N'},'THERME':{'K1','K2','NAUS'}|{f'N{i}' for i in range(1,7)},'SELV':None}
def grp(n):
    for g,s in groups.items():
        if s and n in s: return g
    return 'SELV' if n else None
items=[]
for t in b.GetTracks():
    items.append((grp(t.GetNetname()),t.GetEffectiveShape()))
for p in b.GetPads():
    if p.GetNetname(): items.append((grp(p.GetNetname()),p.GetEffectiveShape(pcbnew.F_Cu)))
best={}
for (g1,s1),(g2,s2) in itertools.combinations(items,2):
    if g1==g2: continue
    k=tuple(sorted((g1,g2)))
    # coarse: bbox distance
    d=s1.GetClearance(s2) if hasattr(s1,'GetClearance') else None
    if d is None: continue
    if k not in best or d<best[k]: best[k]=d
for k,v in best.items(): print(k, round(pcbnew.ToMM(v),2),'mm')
