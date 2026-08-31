import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788158517505.png'
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

# Define the range of x values
x = np.linspace(0, 2 * np.pi, 100)

# Calculate the function and its derivative
y = np.sin(x)
dy = np.cos(x) - np.sin(x)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='sin(x)')
plt.plot(x, dy, label='cos(x) - sin(x)')
plt.title('Sum of Derivatives of sin(x) and cos(x)')
plt.xlabel('x (radians)')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
