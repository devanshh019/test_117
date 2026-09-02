# Local Multimodal Vision and Image Inspection Engine
import os
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image

from .config import STORAGE_DIR


class MultimodalVisionEngine:
    """Local Multimodal Vision & Image Inspection Engine."""

    def __init__(self):
        self.storage_dir = Path(STORAGE_DIR)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def inspect_image_file(self, image_path: str) -> Dict[str, Any]:
        """Inspects image dimensions, format, color space, and metadata."""
        path = Path(image_path)
        if not path.exists():
            return {
                "success": False,
                "error": f"Image file not found at '{image_path}'",
            }

        try:
            with Image.open(path) as img:
                width, height = img.size
                img_format = img.format or path.suffix.replace(".", "").upper()
                info = {
                    "filename": path.name,
                    "width": width,
                    "height": height,
                    "format": img_format,
                    "mode": img.mode,
                    "size_bytes": os.path.getsize(path),
                    "aspect_ratio": round(width / max(1, height), 2),
                }
                return {"success": True, "image_info": info}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def analyze_scanned_inspection_sheet(self, image_path: Optional[str] = None) -> Dict[str, Any]:
        """Analyzes a scanned inspection sheet image dynamically."""
        if not image_path:
            return {
                "document_type": "INSPECTION_SHEET",
                "status": "NO_FILE_SPECIFIED",
                "message": "Please attach an inspection sheet image or PDF to analyze.",
            }

        inspection = self.inspect_image_file(image_path)
        if not inspection.get("success"):
            return inspection

        info = inspection["image_info"]
        return {
            "document_type": "SCANNED_INSPECTION_RECORD",
            "file": info["filename"],
            "resolution": f"{info['width']}x{info['height']}",
            "status": "IMAGE_LOADED_FOR_INFERENCE",
            "analysis_ready": True,
        }

    def analyze_pid_diagram(self, diagram_path: Optional[str] = None) -> Dict[str, Any]:
        """Analyzes a Piping & Instrumentation Diagram (P&ID) image dynamically."""
        if not diagram_path:
            return {
                "drawing_status": "NO_DIAGRAM_SPECIFIED",
                "message": "Please upload a P&ID diagram file for engineering schematic analysis.",
            }

        inspection = self.inspect_image_file(diagram_path)
        if not inspection.get("success"):
            return inspection

        info = inspection["image_info"]
        return {
            "drawing_file": info["filename"],
            "resolution": f"{info['width']}x{info['height']}",
            "format": info["format"],
            "status": "DIAGRAM_LOADED_FOR_INFERENCE",
            "analysis_ready": True,
        }


# Shared vision engine instance
vision_engine = MultimodalVisionEngine()


