#!/usr/bin/env python3
import time
import numpy as np
import matplotlib.pyplot as plt
from hx711 import HX711

# -------------------- Calibration --------------------

GAIN = 128
VOLTAGE = 5.0
FS = 1.371  # mV/V
BITS = 24

Scale = (GAIN * VOLTAGE) / (FS * (2**BITS))  # N·m per count

DT_PIN = 5
SCK_PIN = 6

hx = HX711(DT_PIN, SCK_PIN)

print("Taring... hold still.")
hx.tare()
offset = hx.read_average(40)

print("Tare complete.")

# -------------------- High-speed measurement --------------------

def measure_1s(high_speed_filter=True):
    """
    Collect torque at max HX711 rate (~80Hz) during 1 second.
    """
    torque_data = []
    timestamps = []
    t0 = time.time()

    last_value = 0

    while True:
        raw = hx.read() - offset

        if high_speed_filter:
            # light exponential moving average for stability
            alpha = 0.25
            filtered = alpha * raw + (1 - alpha) * last_value
            last_value = filtered
            torque = filtered * Scale
        else:
            torque = raw * Scale

        now = time.time() - t0

        torque_data.append(torque)
        timestamps.append(now)

        if now >= 1.0:
            break

    return timestamps, torque_data


# -------------------- Run & Plot --------------------

input("\nPress ENTER to start 1-second torque capture...")
print("Recording...")

times, torques = measure_1s()

print(f"Captured {len(torques)} samples (expected ~70–80).")

# Plot after acquisition (fast!)
plt.style.use("ggplot")
plt.plot(times, torques, linewidth=2)
plt.title("Torque During 1-Second Movement")
plt.xlabel("Time (s)")
plt.ylabel("Torque (N·m)")
plt.grid(True)
plt.show()

hx.power_down()
