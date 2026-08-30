# KAVACH-AI: Sovereign Air-Gapped Industrial AI Workbench

An on-premises, sovereign AI engineering workbench powered by local foundation models (Gemma 3 4B / Qwen) with zero cloud egress.

---

## Production Architecture

```text
PS117-v2.0.0/
├── backend/
│   ├── config.py              # Centralized environment, paths, model settings & theme
│   ├── main.py                # FastAPI app entry point & API route handlers
│   ├── engine.py              # Orchestration workflow & pipeline coordination
│   ├── router.py              # Task classification & persona routing
│   ├── inference.py           # Local Ollama LLM integration
│   ├── registry.py            # Local model registration & tracking
│   ├── knowledge_base.py      # Dynamic RAG pipeline with JSON index & search
│   ├── sandbox_executor.py    # Sandboxed Python runner & matplotlib plot capture
│   ├── document_generator.py  # Word (.docx), Excel (.xlsx), & PPT (.pptx) generator
│   ├── multimodal_vision.py   # PIL image analysis & inspection
│   ├── network_guard.py       # Air-gap sentinel, audit logger & compliance certs
│   ├── scenarios.py           # Preloaded industrial & PSU benchmark scenarios
│   ├── tests/
│   │   └── test_workbench.py  # Automated unit & integration test suite
│   └── data/
│       └── storage/           # Persistent storage (uploads, kb_docs, generated deliverables)
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React application & interactive inspectors
│   │   ├── App.css            # Custom UI stylesheet
│   │   ├── index.css          # Tailwind / global base styles
│   │   ├── main.jsx           # React DOM root entry
│   │   ├── assets/            # Static image assets
│   │   └── components/
│   │       └── VoiceOrb.jsx   # Dedicated audio/voice visualizer component
│   ├── public/                # Favicon and public web assets
│   ├── index.html             # HTML entry template
│   ├── vite.config.js         # Vite configuration & proxy settings
│   ├── package.json           # Frontend dependencies & scripts
│   └── dist/                  # Compiled production static bundle
├── start.sh                   # Production launcher script
└── README.md                  # Comprehensive project documentation
```

---

## Key Capabilities

1. **Sovereign Local Inference**: Direct communication with local Ollama (`gemma3:4b`, `qwen3:8b`, `qwen2.5:0.5b`) with zero cloud egress.
2. **Local RAG Pipeline**: Ingests PDFs, Word docs, and plant standards (API 510, ASME Sec VIII, GFR 2017) with keyword & term-frequency similarity matching.
3. **Sandboxed Python Sandbox**: Subprocess execution for simulations & formulas, capturing stdout/stderr and generating high-DPI matplotlib plots.
4. **Office Deliverables Synthesis**: Generates styled Word reports (`.docx`), PowerPoint decks (`.pptx`), and Excel workbooks (`.xlsx`) with on-screen interactive previews.
5. **Air-Gap Security Sentinel**: Cryptographic SHA-256 tamper-evident audit logging and zero external egress verification.

---

## Quick Start

1. **Start Ollama** (if not already running):
   ```bash
   ollama run gemma3:4b
   ```

2. **Launch Application**:
   ```bash
   ./start.sh
   ```

3. Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## Running Tests

```bash
.venv/bin/python -m unittest backend/tests/test_workbench.py
```
