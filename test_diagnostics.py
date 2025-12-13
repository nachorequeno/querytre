from querytre import zonesetq
from querytre import dgzonesetq

zq = zonesetq.from_periods([("2/3","3/4")])
print(zq)
print("-----------------------------------------------")
dsgq = dgzonesetq(zq, "test")
print(dsgq)

zsq1 = zonesetq.from_periods([("15/100", "2/10")])
zsq2 = zonesetq.from_periods([("16/100", "3/10")])
zsq3 = zonesetq.from_periods([("16/100", "3/10"), ("21/100", "4/10"), ("34/100", "5/10")])

print(zsq1)
print(zsq2)
print(zsq3)

dgs1 = dgzonesetq(zsq1, "p")
dgs2 = dgzonesetq(zsq2, "q")
dgs3 = dgzonesetq(zsq3, "r")

zst1 = dgs1 + dgs2
print(zst1)

zst2 = dgs1 & dgs2
print(zst2)

zst3 = dgs1 | dgs2
print(zst3)

zst4 = dgs3.kleene_plus()
print(zst4)

zst5 = dgs3.duration_restriction("11/100", "13/100")
print(zst5)

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
