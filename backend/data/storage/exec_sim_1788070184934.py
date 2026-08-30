import os
os.environ['MPLCONFIGDIR'] = '/tmp/mpl_kavach_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788070184934.png'
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

import pandas as pd

# Load P&ID data (replace 'pid_data.csv' with your actual file)
try:
    pid_data = pd.read_csv('pid_data.csv')
except FileNotFoundError:
    print("Error: pid_data.csv not found.  Please create this file.")
    exit()

# Example Data (replace with your actual data)
# pid_data = pd.DataFrame({
#     'ValveID': ['V101', 'V102', 'FV104'],
#     'ValveType': ['Globe', 'Butterfly', 'Vessel'],
#     'TransmitterID': ['T101', 'T102', 'T103']
# })

# Function to check for DBB (simplified - needs more logic)
def check_dbb(pid_data):
    # Placeholder - Replace with actual DBB logic based on P&ID
    dbb_present = False
    if 'V101' in pid_data['ValveID'].values and 'V102' in pid_data['ValveID'].values:
        dbb_present = True
    return dbb_present

# Generate Report (simplified)
print("Safety Audit Report:")
print("DBB Isolation:", check_dbb(pid_data))
print("\nControl Valve Inventory:")
print(pid_data[['ValveID', 'ValveType']].to_string())

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
