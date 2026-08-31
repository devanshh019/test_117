import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

from .config import (
    STORAGE_DIR,
    SANDBOX_TIMEOUT_SECONDS,
    SANDBOX_PLOT_DPI,
    SANDBOX_MPL_CONFIG_DIR,
    SANDBOX_MAX_OUTPUT_CHARS,
)



class SandboxedPythonExecutor:
    """Executes Python code in an isolated subprocess and captures terminal output and plots."""

    def __init__(self):
        self.storage_dir = Path(STORAGE_DIR)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _prepare_paths(self, prefix: str) -> tuple[Path, str, Path, str]:
        """Creates unique script and plot file paths."""
        timestamp = int(time.time() * 1000)
        script_name = f"{prefix}_{timestamp}.py"
        script_path = self.storage_dir / script_name
        plot_name = f"plot_{prefix}_{timestamp}.png"
        plot_path = self.storage_dir / plot_name
        return script_path, script_name, plot_path, plot_name

    def _build_code_harness(self, user_code: str, plot_path: Path) -> str:
        """Wraps user code with headless matplotlib plot capture."""
        header = (
            f"import os\n"
            f"os.environ['MPLCONFIGDIR'] = '{SANDBOX_MPL_CONFIG_DIR}'\n"
            f"import matplotlib\n"
            f"matplotlib.use('Agg')\n"
            f"import matplotlib.pyplot as plt\n"
            f"import numpy as np\n\n"
            f"_target_plot_path = r'{str(plot_path)}'\n"
            f"_orig_savefig = plt.savefig\n"
            f"def _patched_savefig(*args, **kwargs):\n"
            f"    kwargs['dpi'] = kwargs.get('dpi', {SANDBOX_PLOT_DPI})\n"
            f"    kwargs['bbox_inches'] = kwargs.get('bbox_inches', 'tight')\n"
            f"    _orig_savefig(_target_plot_path, **kwargs)\n"
            f"plt.savefig = _patched_savefig\n\n"
            f"_orig_close = plt.close\n"
            f"def _patched_close(*args, **kwargs):\n"
            f"    if plt.get_fignums() and not os.path.exists(_target_plot_path):\n"
            f"        try:\n"
            f"            _orig_savefig(_target_plot_path, dpi={SANDBOX_PLOT_DPI}, bbox_inches='tight')\n"
            f"        except Exception:\n"
            f"            pass\n"
            f"    return _orig_close(*args, **kwargs)\n"
            f"plt.close = _patched_close\n\n"
        )
        footer = (
            f"\n\nif plt.get_fignums() and not os.path.exists(_target_plot_path):\n"
            f"    try:\n"
            f"        _orig_savefig(_target_plot_path, dpi={SANDBOX_PLOT_DPI}, bbox_inches='tight')\n"
            f"    except Exception:\n"
            f"        pass\n"
        )
        return header + user_code + footer

    def _collect_plots(self, plot_path: Path, plot_name: str, start_time: float) -> List[Dict[str, str]]:
        """Collects the primary plot deliverable or recently modified plots."""
        if plot_path.exists():
            return [{
                "filename": plot_name,
                "path": f"/api/artifacts/{plot_name}",
                "title": "Generated Engineering Schematic / Plot",
            }]

        plots = []
        for png_file in self.storage_dir.glob("*.png"):
            if png_file.stat().st_mtime >= start_time - 1:
                plots.append({
                    "filename": png_file.name,
                    "path": f"/api/artifacts/{png_file.name}",
                    "title": png_file.stem.replace("_", " ").title(),
                })
                break
        return plots

    def execute(self, code_str: str, script_name_prefix: str = "sandbox_sim") -> Dict[str, Any]:
        """Runs the code string in a subprocess and returns outputs and plots."""
        script_path, script_name, plot_path, plot_name = self._prepare_paths(script_name_prefix)
        full_code = self._build_code_harness(code_str, plot_path)

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(full_code)

        start_time = time.time()
        env = dict(os.environ)
        env["MPLCONFIGDIR"] = SANDBOX_MPL_CONFIG_DIR

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=SANDBOX_TIMEOUT_SECONDS,
                cwd=str(self.storage_dir),
                env=env,
            )
            elapsed = round(time.time() - start_time, 3)
            plots = self._collect_plots(plot_path, plot_name, start_time)

            stdout_clean = (result.stdout or "")[:SANDBOX_MAX_OUTPUT_CHARS]
            stderr_clean = (result.stderr or "")[:SANDBOX_MAX_OUTPUT_CHARS]

            return {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": stdout_clean,
                "stderr": stderr_clean,
                "elapsed_seconds": elapsed,
                "script_path": f"/api/artifacts/{script_name}",
                "script_filename": script_name,
                "plots": plots,
                "code": code_str,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Execution timed out after {SANDBOX_TIMEOUT_SECONDS}s.",
                "elapsed_seconds": float(SANDBOX_TIMEOUT_SECONDS),
                "script_path": f"/api/artifacts/{script_name}",
                "script_filename": script_name,
                "plots": [],
                "code": code_str,
            }
        except Exception as e:
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Execution error: {str(e)}",
                "elapsed_seconds": 0.0,
                "script_path": f"/api/artifacts/{script_name}",
                "script_filename": script_name,
                "plots": [],
                "code": code_str,
            }


# Shared sandbox executor instance
sandbox = SandboxedPythonExecutor()

