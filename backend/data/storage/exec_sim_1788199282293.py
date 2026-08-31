import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788199282293.png'
_orig_savefig = plt.savefig
def _patched_savefig(*args, **kwargs):
    kwargs['dpi'] = kwargs.get('dpi', 300)
    kwargs['bbox_inches'] = kwargs.get('bbox_inches', 'tight')
    _orig_savefig(_target_plot_path, **kwargs)
plt.savefig = _patched_savefig

_orig_close = plt.close
def _patched_close(*args, **kwargs):
    if plt.get_fignums() and not os.path.exists(_target_plot_path):
        try:
            _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
        except Exception:
            pass
    return _orig_close(*args, **kwargs)
plt.close = _patched_close

_orig_plot = plt.plot
def _safe_plot(*args, **kwargs):
    args_list = list(args)
    if len(args_list) >= 2:
        x, y = args_list[0], args_list[1]
        if isinstance(x, (list, np.ndarray)) and not isinstance(y, (list, np.ndarray)) and isinstance(y, (int, float, np.number)):
            args_list[1] = np.full_like(x, float(y))
        elif isinstance(y, (list, np.ndarray)) and not isinstance(x, (list, np.ndarray)) and isinstance(x, (int, float, np.number)):
            args_list[0] = np.full_like(y, float(x))
    return _orig_plot(*args_list, **kwargs)
plt.plot = _safe_plot

import matplotlib.pyplot as plt

# Placeholder data - Replace with actual P&ID data
valve_data = {
    "Valve1": {"Type": "Globe", "Size": 6", "Position": 60, "SetPoint": 75},
    "Valve2": {"Type": "Gate", "Size": 4", "Position": 80, "SetPoint": 80},
    "Transmitter1": {"Type": "Pressure", "Range": (0, 150), "Reading": 70},
    "BypassValve": {"Type": "Ball", "Size": 3, "Position": 100, "SetPoint": 120}
}

# Plot Valve Positions
valve_positions = [valve_data[v]["Position"] for v in valve_data]
plt.figure(figsize=(8, 6))
plt.plot(valve_positions, color='blue', marker='o')
plt.xlabel("Valve ID")
plt.ylabel("Position (%)")
plt.title("Valve Positions")
plt.grid(True)
plt.show()

# Plot Transmitter Readings
transmitter_readings = [valve_data[t]["Reading"] for t in valve_data if "Transmitter" in t]
plt.figure(figsize=(8, 6))
plt.plot(transmitter_readings, color='green', marker='x')
plt.xlabel("Transmitter ID")
plt.ylabel("Reading")
plt.title("Transmitter Readings")
plt.grid(True)
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
