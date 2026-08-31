import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788197789423.png'
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

import numpy as np
import matplotlib.pyplot as plt

# Define parameters (These are illustrative - real values would be obtained from material data)
P = 100000  # Pressure (Pa) - Example value
R = 3000    # Radius (m) - Example value
S = 50      # Allowable Stress (Pa) - Example value
E = 200     # Young's Modulus (Pa) - Example value

# Define the allowable stress range
x = np.linspace(0, 1000, 400) # Pressure range
y = S * (1 - (P / x)) # Allowable stress based on ASME VIII-1

# Plot the allowable stress vs. pressure
plt.figure(figsize=(8, 6))
plt.plot(x, y, color='blue')
plt.xlabel('Pressure (Pa)')
plt.ylabel('Allowable Stress (Pa)')
plt.title('Allowable Stress vs. Pressure (Conceptual)')
plt.grid(True)
plt.axvline(x=P, color='red', linestyle='--', label='Operating Pressure')
plt.legend()
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
