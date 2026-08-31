import os
os.environ['MPLCONFIGDIR'] = '/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/on_premises_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

_target_plot_path = r'/Users/devanshkumarverma/Desktop/PS117-v2.0.0/backend/data/storage/plot_exec_sim_1788199159953.png'
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

**[Refinery Name] – Turnaround Boiler Inspection & Maintenance Authorization**

**Document ID:** RB-TM-2024-001
**Date:** October 26, 2023
**Prepared By:** KAVACH-AI, Local Sovereign Industrial Engineering Assistant
**Approved By:** [Name & Title of Approving Authority - e.g., John Smith, Plant Manager]

**1. Executive Summary:**

This document authorizes the inspection and maintenance activities for the [Boiler Name/ID] boiler system as part of the upcoming [Refinery Name] Turnaround scheduled for [Start Date] – [End Date].  This authorization is based on established API 510 standards and internal risk assessment protocols.  The primary objective is to ensure the boiler system’s continued safe and reliable operation, adhering to all relevant regulatory requirements.

**2. Scope of Work:**

The approved scope of work includes, but is not limited to:

*   **Non-Destructive Examination (NDE):**  Visual inspection, Ultrasonic Thickness Testing (UT), Magnetic Particle Inspection (MPI) as per API 510 requirements.
*   **Component Inspection:**  Detailed examination of burner assemblies, feedwater systems, refractory linings, and control systems.
*   **Maintenance Activities:**  Tube cleaning, refractory repair/replacement, valve servicing, instrumentation calibration, and lubrication.
*   **Corrosion Rate Assessment:** Calculation of corrosion rates based on API 510 Section 7.1, considering initial operating life and current operating conditions.  A remaining life assessment will be conducted, with immediate turnaround authorization triggered if the calculated remaining life falls below 2 years.

**3. Regulatory Compliance:**

This work is conducted in accordance with:

*   API 510 Pressure Vessel Inspection Standard, latest edition.
*   [Insert Relevant Local/Regional Regulatory Body Standards - e.g., OSHA, EPA, etc.]
*   [Refinery Name] Internal Procedures for Boiler Maintenance and Inspection.

**4. Risk Assessment:**

A comprehensive risk assessment has been conducted, identifying potential hazards associated with the work. Mitigation measures, including lockout/tagout procedures, confined space entry protocols, and appropriate personal protective equipment (PPE), are in place and will be strictly enforced.

**5. Authorization:**

Based on the above assessment, I, [Name & Title of Approving Authority], hereby authorize the execution of the scope of work outlined in this document.  All work must be performed by qualified and certified personnel.

**6. Contingency:**

Should the inspection or assessment reveal conditions requiring immediate shutdown and repair beyond the scope of this authorization, the Plant Manager retains the authority to implement an immediate turnaround.  Corrosion rate calculations will be continuously monitored, and the 2-year remaining life threshold will trigger an immediate turnaround if breached.

---

**Attachments:**

*   Detailed Inspection Plan (RB-TM-2024-002)
*   Risk Assessment Report (RB-TM-2024-003)
*   Vendor Quotes (as applicable)

if plt.get_fignums() and not os.path.exists(_target_plot_path):
    try:
        _orig_savefig(_target_plot_path, dpi=300, bbox_inches='tight')
    except Exception:
        pass
