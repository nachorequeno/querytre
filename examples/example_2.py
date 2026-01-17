from anytree.exporter import UniqueDotExporter

from querytre import zonesetf
from querytre import dgzonesetq

from querytre.timedrel_ext_int import zone, lower_bound, upper_bound

# Zone[(0.0, 2.0, 4.0, 5.0, 3.0, 4.0), (0, 1, 0, 1, 1, 1)],
# Zone[(12.0, 15.0, 15.0, 19.0, 3.0, 4.0), (1, 0, 0, 0, 1, 1)]
# zone1 = (0/1, 2/1, 4/1, 5/1, 3/1, 4/1)
# zone2 = (12/1, 15/1, 15/1, 19/1, 3/1, 4/1)

values2 = [12.0, 15.0, 15.0, 19.0, 3.0, 4.0]
signs2 = [True, False, False, False, True, True]
# signs2 = (1, 0, 0, 0, 1, 1)

args = [lower_bound(*item) if i % 2 == 0 else upper_bound(*item) for i, item in enumerate(zip(values2, signs2))]
zone2 = zone.make(*args)

zq = zonesetf()
zq.add2(values2, signs2)

print("-----------------------------------------------")
print(zq)
print("-----------------------------------------------")
dgs1 = dgzonesetq(zq, "p;q")
print("-----------------------------------------------")
print(dgs1)
print("-----------------------------------------------")

print("-----------------------------------------------")
zsq1 = zonesetf.from_periods([("15/100", "2/10")])
zsq2 = zonesetf.from_periods([("16/100", "3/10")])
zsq3 = zonesetf.from_periods([("16/100", "3/10"), ("21/100", "4/10"), ("34/100", "5/10")])

print(zsq1)
print(zsq2)
print(zsq3)
print("-----------------------------------------------")

dgs1 = dgzonesetq(zsq1, "p")
dgs2 = dgzonesetq(zsq2, "q")

zst2 = dgs1 & dgs2
print(zst2)

dgs3 = dgzonesetq(zst2, "r")

zst5 = dgs3.duration_restriction("11/100", "13/100")
print(zst5)