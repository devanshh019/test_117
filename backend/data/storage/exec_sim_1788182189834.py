import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788182189834.png'
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

import matplotlib.pyplot as plt
import numpy as np

# Placeholder Values - Replace with actual image-derived data
t_initial = 10.0  # Initial thickness (mm) - Example
t_actual = 9.5    # Actual corrosion thickness (mm) - Example
Time = 5          # Time in years (Example)
P = 1000          # Pressure (MPa) - Example
R = 1.0           # Radius (m) - Example
S = np.pi * R**2  # Area (m^2) - Example
E = 0.8          # Joint Efficiency - Example

# Calculate Corrosion Rate
Cr = (t_initial - t_actual) / Time

print(f"Corrosion Rate (Cr): {Cr:.4f} mm/year")

# Calculate Remaining Life
RL = (t_actual - t_min) / Cr
t_min = (P*R)/(S*E - 0.6*P)
print(f"Remaining Life (RL): {RL:.2f} years")

# Plotting - Illustrative
plt.figure(figsize=(8, 6))
plt.plot([0, Time], [t_initial, t_actual], marker='o', linestyle='-', color='red')
plt.title('Corrosion Thickness vs. Time')
plt.xlabel('Time (Years)')
plt.ylabel('Thickness (mm)')
plt.grid(True)
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
