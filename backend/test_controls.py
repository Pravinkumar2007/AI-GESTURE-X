from backend.app import SystemControls
import time


controls = SystemControls()

print("CONTROL TEST STARTED")

print("Volume UP")
controls.volume_up()
time.sleep(1)

print("Volume DOWN")
controls.volume_down()
time.sleep(1)

print("Next Media")
controls.next_media()
time.sleep(1)

print("Previous Media")
controls.previous_media()

print("CONTROL TEST COMPLETED")