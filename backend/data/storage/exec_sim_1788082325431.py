import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788082325431.png'
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

# Example code to identify control valves and transmitters
control_valves = ["V101", "V102", "V103", "V104", "V105", "V106", "V107", "V108", "V109", "V110"]
transmitters = ["FV-101", "FV-102", "FV-103", "FV-104", "FV-105", "FV-106", "FV-107", "FV-108", "FV-109", "FV-110"]

# Example code to check bypass line against SOP-SAF-402
def check_bypass_line(piping_drawing):
    bypass_lines = ["FV-104", "FV-105", "FV-106", "FV-107", "FV-108", "FV-109", "FV-110"]
    for line in bypass_lines:
        if line in piping_drawing:
            return True
    return False

# Example code to flag missing DBB isolation
def flag_missing_isolation(control_valves, transmitters):
    for valve in control_valves:
        if valve not in transmitters:
            print(f"Missing double block and bleed (DBB) isolation for valve {valve}")

# Example code to generate visual safety audit
def generate_visual_safety_audit(control_valves, transmitters, bypass_lines, flag_missing_isolation):
    # This is a placeholder for the actual code
    print("Visual Safety Audit:")
    print("Control Valves:")
    for valve in control_valves:
        print(f"  {valve}")
    print("\nTransmitters:")
    for transmitter in transmitters:
        print(f"  {transmitter}")
    print("\nBypass Lines:")
    for line in bypass_lines:
        print(f"  {line}")
    print("\nFlagging Missing DBB Isolation:")
    flag_missing_isolation(control_valves, transmitters)

# Example usage
piping_drawing = "PID-ADU2-04-102-REV4"
piping_drawing = "PID-ADU2-04-102-REV4"  # Example P&ID drawing
piping_drawing = "PID-ADU2-04-102-REV4"  # Example P&ID drawing
piping_drawing = "PID-ADU2-04-102-REV4"  # Example P&ID drawing

# Check bypass line against SOP-SAF-402
if check_bypass_line(piping_drawing):
    print("Bypass line is correctly connected.")
else:
    print("Bypass line is not correctly connected.")

# Flag missing DBB isolation
flag_missing_isolation(control_valves, transmitters)

# Generate visual safety audit
generate_visual_safety_audit(control_valves, transmitters, bypass_lines, flag_missing_isolation)

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
