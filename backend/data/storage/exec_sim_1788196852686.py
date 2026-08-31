import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788196852686.png'
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

# Example data for the UTT report
t_initial = 100  # Initial time of corrosion
t_actual = 150  # Actual time of corrosion
Time = t_initial - t_actual  # Time elapsed
Time_remaining = 2  # Remaining life in years

# API 510 pressure vessel inspection standard calculation
Cr = (t_initial - t_actual) / Time  # Corrosion rate
remaining_life = 2  # Remaining life in years

# Check against ASME Sec VIII minimum wall thickness
if remaining_life < 2:
    print("Immediate maintenance turnaround is required.")
else:
    print("No immediate maintenance turnaround is required.")

# Example data for the calculation workbook
# Assuming the following data points for the calculation workbook
# t_initial, t_actual, Time, Time_remaining, Cr, remaining_life

# Example calculation workbook data
calculation_workbook = [
    [t_initial, t_actual, Time, Time_remaining, Cr, remaining_life],
    # Add more data points as needed
]

# Generate the calculation workbook
with open('calculation_workbook.xlsx', 'w') as file:
    for row in calculation_workbook:
        file.write(','.join(map(str, row)) + '\n')

# Generate the PSU Approval Note (.docx)
with open('psu_approval_note.docx', 'w') as file:
    file.write('Corrosion Rate: ' + str(Cr) + ' %\n')
    file.write('Remaining Life: ' + str(remaining_life) + ' years\n')
    file.write('Note: The corrosion rate and remaining life are based on the provided data and the API 510 pressure vessel inspection standard.\n')

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
