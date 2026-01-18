from anytree.exporter import UniqueDotExporter

from querytre import zonesetq
from querytre import dgzonesetq

# zone_set_p = zonesetq.from_periods([("0/1", "5/1"), ("12/1", "15/1")])
# zone_set_q = zonesetq.from_periods([("0/1", "2/1"), ("4/1", "5/1"), ("8/1", "12/1"), ("15/1", "18/1")])

zone_set_p = zonesetq.from_periods([("0", "5"), ("12", "15")])
zone_set_q = zonesetq.from_periods([("0", "2"), ("4", "5"), ("8/1", "12"), ("15", "18")])

diag_set_p = dgzonesetq(zone_set_p, "p")
diag_set_q = dgzonesetq(zone_set_q, "q")

zone_set_p_dot_q = diag_set_p + diag_set_q
print(zone_set_p_dot_q)

# diag_set_duration = dgzonesetq(zone_set_p_dot_q, "r")

# zst5 = diag_set_duration.duration_restriction("3/10", "4/10")
# zst5 = zone_set_p_dot_q.duration_restriction("3/1", "4/1")
zst5 = zone_set_p_dot_q.duration_restriction("3", "4")
print(zst5)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
# dt = zst5.create_tree(0, ("1/1", "3/1"))
# dt = zst5.create_tree(0, ("13/1", "17/1"))
dt = zst5.create_tree(0, ("1/2", "9/2"))
dt.print()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# Visualize and store as image
diag_root_node = dt.anytree_node()
UniqueDotExporter(diag_root_node).to_picture("tre_diagnosis.png")