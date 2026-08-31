import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788182001799.png'
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
import matplotlib.patches as patches

# Create a figure and axes
fig, ax = plt.subplots(figsize=(12, 8))

# Set background color
ax.set_facecolor('lightgray')

# Add title
ax.set_title('Pressure Vessel Inspection & Corrosion Assessment P&ID', fontsize=16)

# Grid
ax.grid(True, linestyle='--', alpha=0.7)

# Vessel Representation (Simplified)
vessel_width = 8
vessel_height = 6
vessel_x = 2
vessel_y = 2
vessel = patches.Rectangle((vessel_x, vessel_y), vessel_width, vessel_height, linewidth=2, edgecolor='black', facecolor='skyblue')
ax.add_patch(vessel)

# Corrosion Area
corrosion_x = vessel_x + vessel_width/2
corrosion_y = vessel_y + vessel_height/3
corrosion_rect = patches.Rectangle((corrosion_x, corrosion_y), vessel_width/2, vessel_height/5, linewidth=2, edgecolor='red', facecolor='lightcoral')
ax.add_patch(corrosion_rect)

# Manway (Simplified)
manway_x = vessel_x + vessel_width/4
manway_y = vessel_y + vessel_height/2
manway = patches.Circle((manway_x, manway_y), 0.3, linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(manway)

# Flow Lines (Simplified)
ax.plot([vessel_x, vessel_x + 1], [vessel_y, vessel_y + 1], 'k-', linewidth=1)
ax.plot([vessel_x + vessel_width, vessel_x + vessel_width + 1], [vessel_y, vessel_y + 1], 'k-', linewidth=1)

# Labels (Simplified)
ax.text(vessel_x + 1, vessel_y + 0.5, 'Pressure Vessel', fontsize=12)
ax.text(corrosion_x + 0.5, corrosion_y + 0.5, 'Corrosion Area', fontsize=12)
ax.text(manway_x + 0.5, manway_y - 0.3, 'Manway', fontsize=12)

# Axis limits
ax.set_xlim(0, vessel_x + vessel_width + 2)
ax.set_ylim(0, vessel_y + vessel_height + 2)

# Remove axis ticks and labels
ax.set_xticks([])
ax.set_yticks([])

# Show the plot
plt.show()

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
