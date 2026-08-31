import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788180835333.png'
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

# Define parameters
Hot_Inlet_Temp = 280  # °C
Hot_Out_Temp = 160    # °C
Cold_Inlet_Temp = 45  # °C
Cold_Out_Temp = 130   # °C
Hot_Flow_Rate = 35  # kg/s
Cold_Flow_Rate = 35  # kg/s  (Assuming equal flow rates for simplicity)
Tube_Length = 10  # meters
Num_Sections = 10  # Number of sections for temperature profile
LMTD_Target = 20  # Target LMTD for verification

# Calculate Heat Duty (Q)
Q = Hot_Flow_Rate * (Hot_Inlet_Temp - Hot_Out_Temp)

# Calculate Log Mean Temperature Difference (LMTD)
LMTD = (Cold_Out_Temp - Cold_Inlet_Temp) / np.log( (Hot_Out_Temp - Cold_Out_Temp) / (Hot_Inlet_Temp - Cold_Inlet_Temp) )

# Calculate Overall Heat Transfer Coefficient (U)
# Simplified U calculation - This is a significant simplification.  A real calculation would require more detailed heat transfer analysis.
# We'll assume a constant U for this simulation.
U = Q / (Hot_Flow_Rate * LMTD)

# Generate temperature profiles
x = np.linspace(0, Tube_Length, Num_Sections)
Hot_Temp = Hot_Inlet_Temp - (Hot_Flow_Rate / (Num_Sections * Hot_Flow_Rate)) * x
Cold_Temp = Cold_Inlet_Temp + (Cold_Flow_Rate / (Num_Sections * Cold_Flow_Rate)) * x

# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(x, Hot_Temp, label='Hot Fluid Temperature', color='red')
plt.plot(x, Cold_Temp, label='Cold Fluid Temperature', color='blue')
plt.xlabel('Tube Length (m)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Profiles Along Tube Length')
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(x, Q, label='Heat Duty (Q)', color='green')
plt.xlabel('Tube Length (m)')
plt.ylabel('Heat Duty (W)')
plt.title('Heat Duty vs. Tube Length')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print(f"Heat Duty (Q): {Q:.2f} W")
print(f"Log Mean Temperature Difference (LMTD): {LMTD:.2f} °C")
print(f"Overall Heat Transfer Coefficient (U): {U:.2f} W/m²·K")

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
