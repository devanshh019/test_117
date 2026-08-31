import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788197265829.png'
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

# Given values
P = 1000  # psi
R = 10    # inches
S = 20000  # psi
E = 1000000 # psi
t_initial = 0.5 # inches
Time = 10 # years
Cr = 0.01 # inches/year

# Calculate t_min
t_min = (P*R)/(S*E - 0.6*P)

print(f"Minimum required thickness (t_min): {t_min:.2f} inches")

# Plotting the result
plt.figure(figsize=(8, 6))
plt.plot(t_min, [0, 1], label='Minimum Thickness', color='red')
plt.title('ASME VIII Div 1 Minimum Thickness Calculation')
plt.xlabel('Thickness (inches)')
plt.ylabel('Time (years)')
plt.grid(True)
plt.xlim(0, t_min + 0.1)
plt.ylim(0, 1)
plt.legend()
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
