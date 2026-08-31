import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788197680019.png'
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

import numpy as np
import matplotlib.pyplot as plt

# Parameters (Example - these would be actual values for a vessel)
diameter = 1.0  # meters
length = 2.0  # meters
yield_strength = 250e6  # Pa (250 MPa) - Example steel yield strength
safety_factor = 2.0  # ASME VIII typically uses safety factors of 2 or 3

# Calculate Allowable Stress
allowable_stress = yield_strength / safety_factor

# Create x values for the plot
x = np.linspace(0, length, 100)

# Calculate stresses (simplified - hoop stress for a cylinder)
hoop_stress = (yield_strength / (2 * diameter)) * (x / length)**2

# Plot the Allowable Stress
plt.figure(figsize=(8, 6))
plt.plot(x, allowable_stress, color='green', linestyle='--', label='Allowable Stress')
plt.plot(x, hoop_stress, color='red', linewidth=2, label='Hoop Stress')
plt.xlabel('Length (m)')
plt.ylabel('Stress (Pa)')
plt.title('Simulated Allowable Stress vs. Length')
plt.grid(True)
plt.legend()
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
