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
