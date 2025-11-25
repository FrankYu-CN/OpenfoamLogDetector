# ofLogDetector.py
import re
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# —— path —— #
if len(sys.argv) < 2:
    print("Please drag a log.waveFoam file onto this program.")
    input("Press Enter to exit...")
    sys.exit()
else:
    log_file = sys.argv[1]
    if not os.path.isfile(log_file):
        print("File not found:", log_file)
        input("Press Enter to exit...")
        sys.exit()

# —— data —— #
data = {
    "courantMax": [],
    "deltaT": [],
    "time": [],
    "UxResidual": [],
    "UzResidual": [],
    "clockTime": []
}

with open(log_file, "r") as f:
    for line in f:

        m = re.search(r"^Courant Number mean:\s*[\d.eE+-]+\s*max:\s*([\d.eE+-]+)", line)
        if m:
            data["courantMax"].append(float(m.group(1)))

        m = re.search(r"^deltaT\s*=\s*([\d.eE+-]+)$", line)
        if m:
            data["deltaT"].append(float(m.group(1)))

        m = re.search(r"^Time\s*=\s*([\d.eE+-]+)$", line)
        if m:
            data["time"].append(float(m.group(1)))

        m = re.search(r"Solving for Ux.*Final residual =\s*([\d.eE+-]+)", line)
        if m:
            data["UxResidual"].append(float(m.group(1)))

        m = re.search(r"Solving for Uz.*Final residual =\s*([\d.eE+-]+)", line)
        if m:
            data["UzResidual"].append(float(m.group(1)))

        m = re.search(r"ClockTime =\s*([\d.eE+-]+)", line)
        if m:
            data["clockTime"].append(float(m.group(1)))

if data["courantMax"]:
    data["courantMax"].pop(0)

# —— into numpy —— #
time = np.array(data["time"])
courant = np.array(data["courantMax"])
deltaT = np.array(data["deltaT"])
ux = np.array(data["UxResidual"])
uz = np.array(data["UzResidual"])
clock = np.array(data["clockTime"])

# Alignment length
min_len = min(len(time), len(courant), len(deltaT), len(ux), len(uz), len(clock))
time = time[:min_len]
courant = courant[:min_len]
deltaT = deltaT[:min_len]
ux = ux[:min_len]
uz = uz[:min_len]
clock = clock[:min_len]

# —— plot —— #
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.plot(time, ux, color="tab:green", linestyle="--", label="Ux Residual", alpha=0.2)
ax1.plot(time, uz, color="tab:red", linestyle="--", label="Uz Residual", alpha=0.2)
ax1.set_yscale("log")
ax1.set_ylabel("Residual (log scale)", color="tab:red")
ax1.set_xlabel("Time(s)")
ax1.tick_params(axis='y', labelcolor="tab:red")

ax2 = ax1.twinx()
ax2.plot(time, deltaT, color="tab:orange", label="deltaT")
ax2.set_ylabel("deltaT(s)", color="tab:orange")
ax2.tick_params(axis='y', labelcolor="tab:orange")

ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.15))
ax3.plot(time, courant, color="tab:blue", label="Courant Max")
ax3.set_ylabel("Courant Max", color="tab:blue")
ax3.tick_params(axis='y', labelcolor="tab:blue")
ax3.set_xlabel("Time(s)")
ax3.grid(True)

# —— ClockTime notation (skip the first one, unit: hour) —— #
n = 5
indices = np.linspace(0, len(clock)-1, n, dtype=int)[1:]
for idx in indices:
    ax1.axvline(x=time[idx], color='black', linestyle=':', linewidth=1)
    ax1.text(time[idx], ax1.get_ylim()[1]*1.2, f"{clock[idx]/3600:.2f}h",
             rotation=90, verticalalignment='bottom', horizontalalignment='center', fontsize=8)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
lines_3, labels_3 = ax3.get_legend_handles_labels()
ax3.legend(lines_1 + lines_2 + lines_3, labels_1 + labels_2 + labels_3, loc="upper right")

plt.tight_layout()
plt.show()
