from querytre import zonesetq

zq1 = zonesetq()
print(zq1)
zq2 = zonesetq.from_periods([("2/3","3/4")])
print(zq2)
zq3 = zonesetq.from_periods([("7/10","1")])
print(zq3)

print(zq2 & zq3)
