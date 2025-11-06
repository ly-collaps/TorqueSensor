#!/usr/bin/env python3
import time
from hx711 import HX711

# ------------- Calculations
Gain = 128
Voltage = 5 #Voltage in V
Volage_half = Voltage/2 #Voltage for 0-10N 
Max_torque= 10 #N.m
number_bits = 24 #Number of bits
FS= 1.371    #Output sensitivity in mV/V
Factor_a = (1000*Voltage/Gain)/(Voltage*FS) #Multiplying by 1000 to have mV/mV at the end giving a scale

#----- The equation is Actual_torque = Scale * Raw_reading_from_HX711
Scale = Factor_a /(2**number_bits) #Scale of the torque in [N.m]

#------------Pin definition 
DT_PIN = 5
SCK_PIN = 6
#CALIBRATION_RATIO = 220.5   # replace this with the value from the Scaling code

hx = HX711(DT_PIN, SCK_PIN)
#hx.set_scale_ratio(CALIBRATION_RATIO)
hx.tare()
print("Code is ready... measuring torques\n")


#The main loop that runs continuously until you stop it.
try:
    while True:
        raw_average=hx.read_average(10)
        # Get average of 10 readings
        Torque = raw_average * Scale

        # Display results
        print(f" Raw Torque Reading: {raw_average:.3f}")
        print(f" Torque: {Torque:.3f} N·m")

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    hx.power_down()