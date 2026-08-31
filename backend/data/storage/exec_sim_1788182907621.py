import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788182907621.png'
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

def calculate_remaining_life(api_data, initial_life, remaining_life_threshold=2):
    """
    Calculate the remaining life of a pressure vessel based on API 510 records.
    
    Parameters:
    - api_data: A dictionary containing API 510 records with keys 'api_id', 'api_name', 'api_value', 'api_unit'.
    - initial_life: The initial life of the pressure vessel in years.
    - remaining_life_threshold: The remaining life threshold in years. If the remaining life is under this threshold, immediate maintenance is required.
    
    Returns:
    - remaining_life: The remaining life of the pressure vessel.
    """
    remaining_life = initial_life
    for api_id, api_data in api_data.items():
        if api_data['api_value'] < remaining_life_threshold:
            remaining_life = api_data['api_value']
            break
    return remaining_life

# Example data (API 510 records)
api_data = {
    '1234567890': {'api_id': 1234567890, 'api_name': 'Pressure Vessel 1', 'api_value': 10, 'api_unit': 'years'},
    '9876543210': {'api_id': 9876543210, 'api_name': 'Pressure Vessel 2', 'api_value': 5, 'api_unit': 'years'}
}

# Calculate remaining life
remaining_life = calculate_remaining_life(api_data, 10)

# Plot the remaining life
plt.plot(api_data.keys(), api_data.values())
plt.title('Remaining Life of Pressure Vessels')
plt.xlabel('API ID')
plt.ylabel('Remaining Life (years)')
plt.grid(True)
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
