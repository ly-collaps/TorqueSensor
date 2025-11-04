# ------------ Calibration------------------------
# Calibration determines the scale factor (how many raw units = 1 gram)

#!/usr/bin/env python3
import time
import sys
from hx711 import HX711

# Set your GPIO pins here
DT_PIN = 5      # DOUT
SCK_PIN = 6     # SCK
g = 9.80665       #Gravity in kg.m/s²
l=10/1000       #Lever length in [m] here for e.g. 10cm

# Create an HX711 object to handle communication with your sensor
hx = HX711(DT_PIN, SCK_PIN)

# Safe shutdown function: called when the script ends normally or is interrupted
def cleanAndExit():
    print("Cleaning up...")
    hx.power_down()
    hx.power_up()
    sys.exit()

try:
    print("Initializing... remove all weight from the torque sensor.")
    time.sleep(2)
    hx.reset()
    hx.tare()
    print("Tare done. Place a known weight on the sensor.")

    known_weight = float(input("Enter the known weight in grams (e.g. 500): "))

    print("Reading values...")
    time.sleep(2)
    Torque_reading = hx.read_average(10)  #takes 10 samples from the HX711 and averages them.

    if Torque_reading:
        print(f"Raw average reading: {Torque_reading}")
        Known_torque = known_weight*g*l
        ratio = Torque_reading / Known_torque
        print(f"Calculated scalling ratio: {ratio}")
        print("Use this ratio in your measurement code as set_scale_ratio().")
    else:
        print("No valid reading received.")
    cleanAndExit()

except (KeyboardInterrupt, SystemExit):
    cleanAndExit()
