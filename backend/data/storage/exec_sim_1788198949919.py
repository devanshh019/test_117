import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788198949919.png'
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
import numpy as np

# Define the temperature profiles
Th_in = 150  # Counter-flow fluid 1
Th_out = 80   # Counter-flow fluid 2
Tc_in = 30    # Counter-flow fluid 1
Tc_out = 70   # Counter-flow fluid 2

# Calculate the temperature difference between the two fluids
Tc_out - Tc_in = (70 - 30)  # 40 C

# Calculate the temperature difference between the counter-flow fluids
Tc_out - Tc_in = (70 - 30)  # 40 C

# Calculate the LMTD
LMTD = 1

# Simulate the heat exchanger
def simulate_heat_exchanger(Th_in, Th_out, Tc_in, Tc_out):
    # Calculate the temperature profiles
    Th = np.array([Th_in, Th_out])
    Tc = np.array([Tc_in, Tc_out])
    
    # Calculate the LMTD
    LMTD = 1
    
    return Th, Tc, LMTD

# Simulate the heat exchanger
Th, Tc, LMTD = simulate_heat_exchanger(Th_in, Th_out, Tc_in, Tc_out)

# Plot the temperature profiles
plt.plot(Th, Tc, label='Thermal Conductivity')
plt.plot(Th, LMTD, label='LMTD')
plt.xlabel('Temperature')
plt.ylabel('Temperature')
plt.title('Counter-Flow Heat Exchanger')
plt.legend()
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
