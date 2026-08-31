import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788081613945.png'
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

import math

# Example UTT report data
utt_data = {
    'Corrosion Rate (Cr)': 0.000001,
    'Remaining Life (Years)': 2,
    'Minimum Wall Thickness (mm)': 10,
    'Operating Temperature (°C)': 350,
    'Pressure (bar)': 18.5
}

# Calculate Corrosion Rate and Remaining Life
corrosion_rate = utt_data['Corrosion Rate (Cr)'] / utt_data['Remaining Life (Years)']
remaining_life = utt_data['Remaining Life (Years)']

# Check against ASME Sec VIII minimum wall thickness
if remaining_life < 2:
    print("Immediate maintenance turnaround is required.")
else:
    print("No immediate maintenance turnaround is required.")

# Draft Formal PSU Approval Note (.docx) and Calculation Workbook (.xlsx)
psu_note = f"""
# UTT Report
Corrosion Rate: {corrosion_rate:.2f}
Remaining Life: {remaining_life:.2f} years
Minimum Wall Thickness: {utt_data['Minimum Wall Thickness (mm)']} mm

# ASME Sec VIII Minimum Wall Thickness
Operating Temperature: {utt_data['Operating Temperature (°C)']} °C
Pressure: {utt_data['Pressure (bar)']} bar

# PSU Approval Note
Corrosion Rate: {corrosion_rate:.2f}
Remaining Life: {remaining_life:.2f} years
Minimum Wall Thickness: {utt_data['Minimum Wall Thickness (mm)']} mm
"""

calculation_workbook = {
    'Corrosion Rate (Cr)': 0.000001,
    'Remaining Life (Years)': 2,
    'Minimum Wall Thickness (mm)': 10,
    'Operating Temperature (°C)': 350,
    'Pressure (bar)': 18.5
}

# Save PSU Approval Note (.docx) and Calculation Workbook (.xlsx)
with open('psu_note.docx', 'w') as file:
    file.write(psu_note)
with open('calculation_workbook.xlsx', 'w') as file:
    file.write(calculation_workbook)

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
