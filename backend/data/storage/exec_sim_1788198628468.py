import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788198628468.png'
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

# Data (from hypothetical UTT report)
initial_thickness = 128.0
actual_thickness = 125.5
time_since_inspection = 8
corrosion_rate = 0.625

# Calculate remaining life
remaining_life = time_since_inspection / corrosion_rate

# Create data for plotting
x = np.linspace(0, remaining_life, 100)
y = corrosion_rate * x

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(x, y, label=f'Corrosion Rate: {corrosion_rate} mm/year')
plt.axvline(x=2, color='red', linestyle='--', label='API 510 Limit (2 years)')
plt.axvline(x=12.8, color='green', linestyle='--', label='Remaining Life (12.8 years)')
plt.axhline(y=109.5, color='gray', linestyle='--', label='ASME Minimum Thickness')
plt.xlabel('Time (Years)')
plt.ylabel('Thickness (mm)')
plt.title('UTT Analysis - Distillation Column C-101')
plt.grid(True)
plt.legend()
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
