from querytre import zonesetq

zq1 = zonesetq()
print(zq1)
zq2 = zonesetq.from_periods([("2/3","3/4")])
print(zq2)
zq3 = zonesetq.from_periods([("7/10","1")])
print(zq3)

print(zq2 & zq3)

print('------------------------------')
# Print result for restrict operation
print(zq3.restrict("15/100", "2/10"))

print('------------------------------')
# Print results for all the diamond functions
print(zonesetq.modal_diamond(zq3, "A", "15/100", "2/10"))
print(zonesetq.modal_diamond(zq3, "Ai", "15/100", "2/10"))
print(zonesetq.modal_diamond(zq3, "B", "15/100", "2/10"))
print(zonesetq.modal_diamond(zq3, "Bi", "15/100", "2/10"))
print(zonesetq.modal_diamond(zq3, "E", "15/100", "2/10"))
print(zonesetq.modal_diamond(zq3, "Ei", "15/100", "2/10"))

print('------------------------------')
# Print results for all the box functions
print(zonesetq.modal_box(zq3, "A", "15/100", "2/10"))
print(zonesetq.modal_box(zq3, "Ai", "15/100", "2/10"))
print(zonesetq.modal_box(zq3, "B", "15/100", "2/10"))
print(zonesetq.modal_box(zq3, "Bi", "15/100", "2/10"))
print(zonesetq.modal_box(zq3, "E", "15/100", "2/10"))
print(zonesetq.modal_box(zq3, "Ei", "15/100", "2/10"))
