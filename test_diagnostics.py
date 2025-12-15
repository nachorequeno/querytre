from querytre import zonesetq
from querytre import dgzonesetq

zq = zonesetq.from_periods([("2/3","3/4")])
print(zq)
print("-----------------------------------------------")
dsgq = dgzonesetq(zq, "test")
print("-----------------------------------------------")
print(dsgq)
print("-----------------------------------------------")
zsq1 = zonesetq.from_periods([("15/100", "2/10")])
zsq2 = zonesetq.from_periods([("16/100", "3/10")])
zsq3 = zonesetq.from_periods([("16/100", "3/10"), ("21/100", "4/10"), ("34/100", "5/10")])

print(zsq1)
print(zsq2)
print(zsq3)
print("-----------------------------------------------")

dgs1 = dgzonesetq(zsq1, "p")
dgs2 = dgzonesetq(zsq2, "q")
dgs3 = dgzonesetq(zsq3, "r")

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
dt = dgs1.create_tree(0,("16/100", "17/100"))
dt.print()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

zst1 = dgs1 + dgs2
print(zst1)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
dt = zst1.create_tree(0,("16/100", "17/100"))
dt.print()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

zst2 = dgs1 & dgs2
print(zst2)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
dt = zst2.create_tree(0,("16/100", "17/100"))
dt.print()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

zst3 = dgs1 | dgs2
print(zst3)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
dt = zst3.create_tree(0,("16/100", "17/100"))
dt.print()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

zst4 = dgs3.kleene_plus()
print(zst4)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
dt = zst4.create_tree(0,("16/100", "17/100"))
dt.print()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

zst5 = dgs3.duration_restriction("11/100", "13/100")
print(zst5)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
dt = zst5.create_tree(0,("16/100", "27/100"))
dt.print()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# [TODO]? add an additional check if the zone at index actually contains the interval
print("Test all trivial infer operations:")
print(zst2.infer(0, ("16/100", "17/100")))
print(zst3.infer(0, ("16/100", "17/100")))
print(zst5.infer(0, ("16/100", "17/100")))
print(dgs3.infer(0, ("16/100", "17/100")))

diag_vec = zst1.infer_concatenation(0, dgs1, dgs2, ("16/100", "17/100"))
print(diag_vec)
print("chids:", zst1.child_zone_indices(0))
concat_infer_test = zst1.infer(0, ("16/100", "17/100"))
print(concat_infer_test)

kindex = 1
kplus_vec = zst4.infer_kleene_plus(kindex, zst3, ("16/100", "17/100"));
print(kplus_vec)

kindex = 4
kplus_vec = zst4.infer_kleene_plus(kindex, dgs3, ("18/100", "4/10"));
print(kplus_vec)
print("chids:", zst4.child_zone_indices(kindex))
kplus_infer_test = zst4.infer(kindex, ("18/100", "4/10"))
print(kplus_infer_test)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
dt = zst4.create_tree(kindex, ("18/100", "4/10"))
dt.print()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

zsq10 = zonesetq.from_periods([("16/100", "3/10")])
zsq11 = zonesetq.from_periods([("21/100", "4/10")])
zsq12 = zonesetq.from_periods([("34/100", "5/10")])

dgs10 = dgzonesetq(zsq10, "l")
dgs11 = dgzonesetq(zsq11, "m")
dgs12 = dgzonesetq(zsq12, "n")

dgstemp1 = dgs10 | dgs11

dgstemp2 = dgstemp1 | dgs12

zst6 = dgstemp2.kleene_plus()
print(zst6)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
dt = zst6.create_tree(kindex, ("18/100", "4/10"))
dt.print()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
