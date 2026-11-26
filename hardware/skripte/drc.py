import pcbnew,sys
b=pcbnew.LoadBoard(sys.argv[1])
b.BuildConnectivity()
ok=pcbnew.WriteDRCReport(b,'drc.rpt',pcbnew.EDA_UNITS_MILLIMETRES,True)
print('drc',ok)
