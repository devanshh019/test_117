import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788182231884.png'
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

# Parameters
P = 1000  # Design pressure (Pa)
R = 1  # Radius (m)
E = 200e9 # Modulus of elasticity (Pa)
S = 200e9 # Yield strength (Pa)
Cr = 0.001 # Corrosion rate (mm/year)
Time = 10 # Inspection time (years)
t_initial = 10 # Initial thickness (mm)

# Calculate minimum thickness before corrosion
t_min_initial = (P * R) / (S * E - 0.6 * P)

# Calculate actual thickness after corrosion
t_actual = t_initial - (Cr * Time)

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(t_initial, t_min_initial, marker='o', label='Initial Thickness')
plt.plot(t_actual, t_min_initial, marker='x', label='Actual Thickness after Corrosion')
plt.xlabel('Thickness (mm)')
plt.ylabel('Minimum Allowable Thickness (mm) - ASME VIII Div 1')
plt.title('Impact of Corrosion on Minimum Thickness')
plt.grid(True)
plt.legend()
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
