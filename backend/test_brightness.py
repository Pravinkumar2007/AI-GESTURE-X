from brightness import BrightnessControl
import time

brightness = BrightnessControl()

print("BRIGHTNESS TEST START")

brightness.increase()

time.sleep(2)

brightness.decrease()

print("BRIGHTNESS TEST COMPLETED")