from air_writer import AirWriter

writer = AirWriter()

writer.start(100, 100)

writer.update(120, 110)
writer.update(140, 130)
writer.update(160, 150)

writer.stop()

print("AIR WRITING POINTS:")
print(writer.points)

print("AIR WRITER TEST COMPLETED")