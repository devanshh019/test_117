import os
from pathlib import Path

# -----------------------------------------------------------------------------
# Base Directories & Paths
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
STORAGE_DIR = BASE_DIR / "data" / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
TEMP_UPLOADS_DIR = STORAGE_DIR / "temp_uploads"
KB_DOCS_DIR = STORAGE_DIR / "kb_docs"
FRONTEND_DIST_DIR = PROJECT_ROOT / "frontend" / "dist"

# Ensure runtime directories exist
for directory in [STORAGE_DIR, UPLOADS_DIR, TEMP_UPLOADS_DIR, KB_DOCS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Application & Sovereign Security Settings
# -----------------------------------------------------------------------------
APP_NAME = "KAVACH-AI"
APP_TITLE = "KAVACH-AI Sovereign Industrial & PSU Workbench"
APP_VERSION = "1.0.0"
SOVEREIGN_ORGANIZATION = "KAVACH-AI Sovereign Industrial Operations"
SECURITY_CLASSIFICATION = "CONFIDENTIAL // DEFENSE & PSU RESTRICTED"
AIR_GAP_ENFORCED = True
ALLOW_EXTERNAL_CALLS = False
HOST = "127.0.0.1"
PORT = 8000

# -----------------------------------------------------------------------------
# Local Ollama Inference Settings
# -----------------------------------------------------------------------------
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_TIMEOUT_SECONDS = 180.0
OLLAMA_HEALTH_TIMEOUT_SECONDS = 1.0
DEFAULT_MODEL_ID = "gemma3:4b"
DEFAULT_MODEL_NAME = "Gemma 3 4B Sovereign Foundation"
DEFAULT_MODEL_VRAM_GB = 3.4

MODEL_TEMPERATURE = 0.2
MODEL_TOP_P = 0.95
MODEL_CONTEXT_WINDOW = 4096
MAX_HISTORY_TURNS = 10

# -----------------------------------------------------------------------------
# Python Code Sandbox Execution Settings
# -----------------------------------------------------------------------------
SANDBOX_TIMEOUT_SECONDS = 15
SANDBOX_PLOT_DPI = 300
SANDBOX_MPL_CONFIG_DIR = "/tmp/mpl_kavach_cache"

# -----------------------------------------------------------------------------
# Local RAG & Document Ingestion Settings
# -----------------------------------------------------------------------------
RAG_CHUNK_SIZE = 600
RAG_CHUNK_OVERLAP = 80
RAG_DEFAULT_TOP_K = 3
RAG_MIN_SCORE = 0.1
RAG_MAX_SCORE = 1.0

# -----------------------------------------------------------------------------
# Document Generator Theme & Styles
# -----------------------------------------------------------------------------
THEME = {
    # Brand Strings
    "org_title": "KAVACH-AI SOVEREIGN INDUSTRIAL WORKBENCH",
    "subtitle": "Prepared by KAVACH-AI Sovereign Intelligence",
    "confidential_tag": "CONFIDENTIAL // SOVEREIGN AIR-GAPPED WORKBENCH",
    "footer_text": "Zero Cloud Egress • 100% On-Premises",
    
    # Hex Colors
    "primary_orange": "EA580C",
    "dark_navy": "1C1917",
    "soft_bg": "FAF8F5",
    "border_light": "E5DED1",
    "text_dark": "1C1917",
    "text_muted": "44403C",
    "text_subtle": "78716C",
    "text_white": "FFFFFF",
    
    # RGB Tuples for python-docx & python-pptx
    "rgb_orange": (234, 88, 12),
    "rgb_dark": (28, 25, 23),
    "rgb_soft_bg": (250, 248, 245),
    "rgb_muted": (68, 64, 60),
    "rgb_subtle": (168, 162, 158),
    
    # Typography
    "font_family": "Arial",
    "title_size": 36,
    "header_size": 26,
    "body_size": 17,
    "doc_title_size": 13,
    "doc_heading_size": 11,
    "doc_body_size": 10.5
}

# -----------------------------------------------------------------------------
# Task Routing & Intent Trigger Keywords
# -----------------------------------------------------------------------------
PPTX_TRIGGERS = [
    "powerpoint", "power point", "power-point", "ppt", "pptx",
    "presentation", "slides", "slide deck", "deck", "slideshow"
]

DOCX_TRIGGERS = [
    "word", "docx", "approval note", "report", "document",
    "draft note", "memo", "technical note", "brief"
]

XLSX_TRIGGERS = [
    "excel", "xlsx", "spreadsheet", "workbook",
    "calculation sheet", "data sheet", "sheet"
]

VISUAL_TRIGGERS = [
    "visual", "drawing", "draw", "diagram", "plot",
    "schematic", "chart", "graph", "p&id", "audit"
]

MATH_CODE_TRIGGERS = [
    "simulate", "python", "code", "plot", "math",
    "calculus", "formula", "lmtd", "differentiate",
    "integral", "sympy", "solve", "heat exchanger"
]

STANDARDS_TRIGGERS = [
    "api", "asme", "gfr", "standard", "code",
    "sop", "refinery", "column", "vessel", "turnaround", "tender"
]

