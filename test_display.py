from querytre import zoneset, zonesetf
zs = zoneset.from_periods([(2,3), (5,6)])
print(zs)
zs.display()
zimage = zs.get_image()
zimage.save('zimage.png')
