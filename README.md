# KAVACH-AI: Sovereign Air-Gapped Industrial AI Workbench
### Complete Codebase Reference, File-by-File Documentation & Technical Architecture Guide

---

## 1. Executive Summary & System Overview

**KAVACH-AI** is a 100% on-premises, air-gapped sovereign AI workbench designed for critical industrial engineering operations (refineries, petrochemical complexes, and power plants). It enforces zero cloud egress, ensures compliance with international standards (API 510/570, ASME BPVC, GFR-2017), and automates complex engineering tasks through a multi-turn **ReAct (Reasoning + Acting)** agent loop.

```
                                  +---------------------------------------+
                                  |         React Frontend (UI)           |
                                  |  (Chat, Traces, Deliverables, Voice)  |
                                  +-------------------+-------------------+
                                                      | HTTP / SSE
                                                      v
                                  +---------------------------------------+
                                  |      FastAPI Server (backend/main.py) |
                                  +-------------------+-------------------+
                                                      |
                         +----------------------------+----------------------------+
                         |                                                         |
                         v                                                         v
        +---------------------------------+                       +---------------------------------+
        |  Dynamic Task Router (ONNX)     |                       |    Air-Gap Security Sentinel    |
        |  (Cosine Similarity Centroids)  |                       |  (SHA-256 Cryptographic Chain)  |
        +----------------+----------------+                       +---------------------------------+
                         |
                         v
        +-------------------------------------------------------------------------------------------+
        |                       Sovereign Agent Engine (backend/engine.py)                          |
        |                                                                                           |
        |  Turn 1: Thought -> Action (Tool) -> Action Input                                         |
        |             |                                                                             |
        |             v                                                                             |
        |     [Tool Registry: RAG / Python Sandbox / Word / PPT / Excel Renderers]                 |
        |             |                                                                             |
        |             v                                                                             |
        |  Turn 2: Observation -> Next Action or Final Answer Synthesis                              |
        +---------------------------------------------+---------------------------------------------+
                                                      | Local HTTP (127.0.0.1:11434)
                                                      v
                                  +---------------------------------------+
                                  |      Local Ollama Inference Engine    |
                                  |  (Qwen 2.5 / Gemma 3 / Mistral / etc) |
                                  +---------------------------------------+
```

---

## 2. File-by-File Technical Deep Dive

---

### `backend/main.py`
* **Purpose**: The primary API Gateway and application server built with **FastAPI**. It handles HTTP requests from the React frontend, manages CORS policies, exposes REST endpoints, and serves static files.
* **Key Functions & Endpoints**:
  - `health_check()` (`GET /api/health`): Returns system status, active models, Ollama connectivity, and air-gap verification.
  - `execute_agent_task(req: AgentTaskRequest)` (`POST /api/agent/execute`): The main endpoint that triggers the `SovereignAgentEngine` ReAct loop with user prompts, attachments, and conversation history.
  - `download_generated_document(filename: str)` (`GET /api/documents/download/{filename}`): Securely streams generated `.docx`, `.pptx`, and `.xlsx` files to the user's browser.
  - `get_security_status()` (`GET /api/security/status`): Fetches live network interface bindings and cryptographic SHA-256 audit logs.
  - `get_sovereign_certificate()` (`GET /api/security/certificate`): Generates a verifiable compliance certificate.
  - `upload_knowledge_document()` (`POST /api/knowledge/upload`): Ingests user-uploaded plant standards into the ChromaDB vector database.
* **Complex / Non-Obvious Logic**:
  - **Dynamic SPA Fallback**: Mounts the compiled frontend `dist/` folder and intercepts all client-side routes, falling back to `index.html` so single-page navigation works seamlessly without 404 errors.

---

### `backend/engine.py`
* **Purpose**: The central brain of KAVACH-AI. Implements the **ReAct (Reasoning + Acting) execution loop**, parses model outputs, dispatches tools, maintains working memory across turns, and ensures deliverables are compiled.
* **Key Classes & Functions**:
  - `AgentExecutionState`: Dataclass tracking execution history, deliverables, citations, execution steps/phases, and scratchpad memory for a specific task.
  - `SovereignAgentEngine`: The main orchestration class.
  - `execute_task(prompt, attachments, override_model, history)`: Coordinates intent routing, system prompt assembly, multi-turn LLM inference, tool execution, and deliverable creation.
  - `_extract_all_actions(text: str)`: Regex engine extracting `Action:` and `Action Input:` blocks.
  - `_parse_react_response(text: str)`: Identifies `Thought`, `Action`, `Action Input`, or `Final Answer`.
  - `_ensure_requested_deliverables(prompt, state)`: Cross-turn deliverable safety net. If the user asks for a document or slide deck, it extracts content from current or previous assistant messages and guarantees file creation.
* **Difficult / Complex Lines Explained**:
  ```python
  # 1. Segmenting Multiple Tool Calls in One Turn:
  pattern = r"(?:\*\*)?Action:?(?:\*\*)?\s*`?([a-zA-Z0-9_\-]+)`?\s*(?:\*\*)?Action Input:?(?:\*\*)?\s*(.*?)(?=(?:\*\*)?Action:|$)"
  matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
  ```
  *Explanation*: Uses non-greedy regex lookaheads `(?=(?:\*\*)?Action:|$)` to parse multiple tool actions in a single response without JSON text overlapping.
  ```python
  # 2. Multi-Turn History Bridging:
  source_text = state.final_answer if len(state.final_answer.strip()) > 150 else (last_assistant_content or state.final_answer)
  ```
  *Explanation*: If a user says *"take that into a PPT"*, `state.final_answer` might be brief. The engine inspects `last_assistant_content` from conversation history to extract the full prior technical context into the slides.

---

### `backend/router.py`
* **Purpose**: Semantic Intent Classifier and Model Persona Dispatcher. Classifies user prompts into specialized domains without any hardcoded keyword if-checks.
* **Key Classes & Functions**:
  - `DynamicTaskRouter`: Encodes domain centroids into high-dimensional space and evaluates query similarity.
  - `route_task(prompt, attachments)`: Returns a `RoutingDecision` containing the task category, selected model ID, and confidence score.
* **Mathematical Algorithm (Vector Cosine Similarity)**:
  ```python
  # Projects prompt into embedding space:
  q_vec = np.array(emb_fn([prompt])[0])
  q_unit = q_vec / np.linalg.norm(q_vec)

  # Computes normalized dot product with each category centroid:
  scores = {cat: float(np.dot(q_unit, c_vec)) for cat, c_vec in self._centroids.items()}
  best_cat = max(scores, key=scores.get)
  ```
  *Explanation*: Evaluates the cosine similarity between the user's prompt vector and pre-computed domain centroids. The domain with the highest cosine score is selected dynamically.

---

### `backend/network_guard.py`
* **Purpose**: The Air-Gap Sentinel and Cryptographic Audit Chain. Monitors local network interfaces to verify zero outbound cloud leaks and logs every event to an immutable SHA-256 ledger.
* **Key Classes & Functions**:
  - `AirGapSentinel`: System auditor tracking uptime, network egress, and SHA-256 hashes.
  - `check_socket_interfaces()`: Dynamically queries OS network adapters (`ifconfig` / `ip addr`) to identify active bindings.
  - `record_audit_event(event_type, severity, details, metadata)`: Appends an event to the cryptographic blockchain-style ledger.
* **Difficult Logic (Cryptographic Hash Chaining)**:
  ```python
  # Merkle-like Hash Linkage:
  event["prev_hash"] = self.audit_chain_hash
  serialized = json.dumps(event, sort_keys=True)
  event["event_hash"] = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
  self.audit_chain_hash = event["event_hash"]
  ```
  *Explanation*: Each audit record incorporates the SHA-256 hash of the previous record (`prev_hash`). Any tampering or modification of historical records invalidates the entire chain head hash.

---

### `backend/knowledge_base.py`
* **Purpose**: Local Retrieval-Augmented Generation (RAG) knowledge engine powered by **ChromaDB**. Stores, indexes, and retrieves refinery standard operating procedures (SOPs), API 510/570 codes, and ASME guidelines.
* **Key Classes & Functions**:
  - `LocalRAGKnowledgeBase`: Manages vector collections and file parsers.
  - `extract_text_from_file(file_path: str)`: Universal multi-format extractor supporting `.docx` (via `python-docx`), `.pdf` (via `pypdf`), and plaintext files.
  - `query_standards(query_text: str, n_results: int)`: Performs cosine similarity search over vector chunks and formats citations with document metadata.

---

### `backend/sandbox_executor.py`
* **Purpose**: Isolated Python Code Sandbox. Safely runs scientific computations, thermodynamics simulations, and data visualizations on local hardware with execution timeouts and automatic plot capture.
* **Key Classes & Functions**:
  - `IsolatedSandboxExecutor`: Manages temporary execution directories and isolated subprocesses.
  - `execute(code: str, timeout: int)`: Writes code to a temporary script, invokes a sandboxed Python runner, captures standard output (`stdout`), standard error (`stderr`), and encodes any generated Matplotlib charts into base64 PNGs.

---

### `backend/document_generator/` (Industrial Document Strategy Engine)
Implements the **Industry-Standard Strategy Pattern** for generating deliverables:
1. **`schemas.py`**: Pydantic models defining the strict contract: `DocxSpec`, `PptxSpec`, `XlsxSpec`, `SectionSpec`, `SlideSpec`, and `CellRule`.
2. **`renderers/base.py`**: Defines the abstract base class `BaseRenderer` with the contract method `render(spec) -> DocumentResult`.
3. **`renderers/docx_renderer.py`**: Generates formal Word documents (`.docx`) using `python-docx`.
4. **`renderers/pptx_renderer.py`**: Generates 16:9 widescreen PowerPoint decks (`.pptx`) using `python-pptx`.
5. **`renderers/xlsx_renderer.py`**: Generates Excel workbooks (`.xlsx`) using `openpyxl` with dynamic conditional formatting.
6. **`service.py`**: The unified `DocumentService` facade.

---

### `backend/tools.py`
* **Purpose**: Tool Registry and execution wrappers. Bridges ReAct agent actions to real backend functions.
* **Registered Tools**:
  1. `search_knowledge_base`: Queries ChromaDB for refinery standards.
  2. `execute_python_code`: Runs calculations in the Python sandbox.
  3. `generate_word_document`: Calls `DocumentService` to produce `.docx`.
  4. `generate_powerpoint_presentation`: Calls `DocumentService` to produce `.pptx`.
  5. `generate_excel_spreadsheet`: Calls `DocumentService` to produce `.xlsx`.
  6. `inspect_image_and_drawings`: Inspects images and extracts visual metadata.

---

### `backend/inference.py`
* **Purpose**: Local Ollama HTTP Client. Communicates with the local Ollama instance (`http://127.0.0.1:11434`) via non-blocking HTTP requests.

---

### `backend/model_manager.py` & `backend/model.yaml`
* **Purpose**: Manages model registry, task-capability mappings, and active model selection stored persistently in `model.yaml`.

---

### `frontend/src/App.jsx`
* **Purpose**: The complete React single-page application (SPA).
* **Key Components & Features**:
  - **Execution Trace Accordion**: Displays phase-by-phase execution timing, step statuses, and full unclipped trace details (`whitespace-pre-wrap font-mono`).
  - **Deliverables Hub & Right Panel Inspector**: Allows instant in-browser inspection and one-click downloading of generated Word, PPT, and Excel files.
  - **Voice Dictation (Web Speech API)**: Transcribes spoken engineering voice prompts directly into the chat input.
  - **Air-Gap Sentinel Drawer**: Live display of local network bindings, zero outbound bytes telemetry, and cryptographic audit ledger.

---

## 3. How the ReAct Loop Works Step-by-Step

```
Turn 1:
├── Agent Prompt: User Request + Tool Definitions
├── Model Output:
│   Thought: I need to generate the PowerPoint presentation first.
│   Action: generate_powerpoint_presentation
│   Action Input: { "title": "FCCU Shutdown", "slides": [...] }
└── Engine Interception:
    ├── Executes generate_powerpoint_presentation
    ├── Compiles FCCU_Shutdown_570e9c36.pptx
    └── Produces Observation: "Generated PowerPoint deck '...pptx' (33 KB)"

Turn 2:
├── Agent Prompt: Previous Observation in Working Memory
├── Model Output:
│   Thought: The presentation is ready. Now I will generate the Word document.
│   Action: generate_word_document
│   Action Input: { "title": "FCCU Shutdown Procedure", "sections": [...] }
└── Engine Interception:
    ├── Executes generate_word_document
    ├── Compiles FCCU_Shutdown_5bc0e94b.docx
    └── Produces Observation: "Generated Word document '...docx' (24 KB)"

Turn 3:
├── Agent Prompt: Both Observations in Working Memory
├── Model Output:
│   Thought: Both deliverables are created.
│   Final Answer: Both deliverables have been compiled and verified.
└── UI Display: Deliverables (2) active in top bar and right inspector!
```

---

## 4. Setup & Running Instructions

### Single-Laptop Setup (Standalone)
```bash
./.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Open **`http://127.0.0.1:8000`**.

### Dual-Laptop Setup (Hosting Models on RTX 4050 GPU Laptop)
1. **On Friend's Laptop (GPU Host)**:
   - Run: `OLLAMA_HOST=0.0.0.0:11434 ollama serve`
   - Find Local IP: `192.168.1.45`
2. **On Your Laptop**:
   - Run: `export OLLAMA_BASE_URL=http://192.168.1.45:11434`
   - Run: `./.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`

---

## 5. Running Automated Tests

```bash
./.venv/bin/python -m unittest backend/tests/test_workbench.py
```
**Expected Result**: `Ran 10 tests in 4.5s -> OK`.
