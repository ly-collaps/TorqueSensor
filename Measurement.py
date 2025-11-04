#!/usr/bin/env python3
import time
from hx711 import HX711

DT_PIN = 5
SCK_PIN = 6
CALIBRATION_RATIO = 220.5   # replace this with the value from the Scaling code

hx = HX711(DT_PIN, SCK_PIN)
#hx.set_scale_ratio(CALIBRATION_RATIO)
hx.tare()

print("Code is ready... measuring torques\n")


#The main loop that runs continuously until you stop it.
try:
    while True:
        raw_average=hx.read_average(1)
        # Get average of 10 readings
        Torque = hx.get_weight_mean(10)

        # Display results
        print(f" Torque: {Torque:.3f} N·m")

        time.sleep(0.001)

except KeyboardInterrupt:
    print("Exiting...")
    hx.power_down()
