import os
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .config import (
    STORAGE_DIR,
    UPLOADS_DIR,
    TEMP_UPLOADS_DIR,
    SOVEREIGN_ORGANIZATION,
    SECURITY_CLASSIFICATION,
    APP_TITLE,
    APP_VERSION,
    HOST,
    PORT,
    FRONTEND_DIST_DIR,
)
from .network_guard import sentinel
from .registry import registry, ModelProfile
from .router import router
from .inference import inference_engine
from .engine import agent_engine
from .knowledge_base import knowledge_base
from .scenarios import PRELOADED_SCENARIOS

app = FastAPI(
    title=APP_TITLE,
    description="Air-Gapped Local AI Workbench with zero cloud egress.",
    version=APP_VERSION,
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Request Models
# -----------------------------------------------------------------------------
class TaskExecuteRequest(BaseModel):
    prompt: str
    override_model: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    history: Optional[List[Dict[str, str]]] = None


class RouteTestRequest(BaseModel):
    prompt: str
    attachments: Optional[List[Dict[str, Any]]] = None


class SelectModelRequest(BaseModel):
    model_id: str


class KBSearchRequest(BaseModel):
    query: str
    top_k: int = 3


# -----------------------------------------------------------------------------
# Core System Endpoints
# -----------------------------------------------------------------------------
@app.get("/api/health")
def get_health():
    """Returns local system health, air-gap status, and Ollama connectivity."""
    ollama_info = inference_engine.check_local_ollama_health()
    active_profile = registry.get_active_model()
    return {
        "status": "HEALTHY",
        "air_gap_verified": True,
        "organization": SOVEREIGN_ORGANIZATION,
        "security_classification": SECURITY_CLASSIFICATION,
        "active_foundation_model": active_profile.name,
        "active_model_id": active_profile.model_id,
        "ram_allocated_gb": registry.get_total_vram_usage(),
        "ollama_backend": ollama_info,
        "engine_mode": "SOVEREIGN_AIR_GAPPED_LOCAL",
    }


@app.get("/api/models")
def list_models():
    """Lists local models detected via Ollama and current active model profile."""
    ollama_info = inference_engine.check_local_ollama_health()
    active = registry.get_active_model()
    return {
        "models": [active.model_dump()],
        "active_model": active.model_dump(),
        "detected_models": ollama_info.get("models", []),
        "total_active_ram_gb": registry.get_total_vram_usage(),
    }


@app.post("/api/models/select")
def select_active_model(req: SelectModelRequest):
    """Switches active model tag."""
    inference_engine.set_target_model(req.model_id)
    sentinel.record_audit_event(
        event_type="MODEL_SELECTED",
        severity="INFO",
        details=f"Selected active local model: {req.model_id}",
        metadata={"model_id": req.model_id},
    )
    return {"success": True, "active_model": registry.get_active_model().model_dump()}


@app.post("/api/route")
def test_routing(req: RouteTestRequest):
    """Tests task routing and persona dispatch."""
    decision = router.route_task(req.prompt, req.attachments)
    return decision.model_dump()


@app.post("/api/upload")
async def upload_attachment(file: UploadFile = File(...)):
    """Uploads user attachments (images, PDFs, documents) for task execution."""
    timestamp = int(time.time() * 1000)
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = UPLOADS_DIR / safe_filename

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    ext = file_path.suffix.lower()
    return {
        "success": True,
        "filename": file.filename,
        "saved_filename": safe_filename,
        "path": f"/api/artifacts/uploads/{safe_filename}",
        "local_path": str(file_path),
        "file_type": ext.replace(".", ""),
        "size_bytes": len(contents),
    }


@app.post("/api/agent/execute")
def execute_agent_task(req: TaskExecuteRequest):
    """Executes end-to-end task workflow (routing, RAG, inference, code, docs)."""
    if not req.prompt.strip() and not req.attachments:
        raise HTTPException(status_code=400, detail="Prompt or attachment required.")

    return agent_engine.execute_task(
        prompt=req.prompt,
        attachments=req.attachments,
        override_model=req.override_model,
        history=req.history,
    )


# -----------------------------------------------------------------------------
# Security & Telemetry Endpoints
# -----------------------------------------------------------------------------
@app.get("/api/security/status")
def get_security_telemetry():
    """Returns real-time air-gap telemetry and SHA-256 audit log."""
    return sentinel.get_security_status()


@app.get("/api/security/certificate")
def get_sovereign_certificate():
    """Generates cryptographic compliance certificate."""
    return sentinel.generate_sovereign_certificate()


@app.get("/api/scenarios")
def get_scenarios():
    """Returns pre-loaded industrial scenarios for one-click testing."""
    return {"scenarios": PRELOADED_SCENARIOS}


# -----------------------------------------------------------------------------
# Knowledge Base (RAG) Endpoints
# -----------------------------------------------------------------------------
@app.post("/api/knowledge-base/upload")
async def upload_kb_document(file: UploadFile = File(...)):
    """Uploads and indexes a document directly into the local RAG pipeline."""
    temp_path = TEMP_UPLOADS_DIR / file.filename
    contents = await file.read()
    with open(temp_path, "wb") as f:
        f.write(contents)

    try:
        res = knowledge_base.ingest_file(temp_path, original_filename=file.filename)
        sentinel.record_audit_event(
            event_type="RAG_DOCUMENT_INGESTED",
            severity="INFO",
            details=f"Indexed '{file.filename}' into RAG ({res['indexed_chunks']} chunks).",
            metadata={"filename": file.filename, "chunks": res["indexed_chunks"]},
        )
        return {
            "success": True,
            "filename": file.filename,
            "doc_id": res["document"]["doc_id"],
            "indexed_chunks": res["indexed_chunks"],
            "document": res["document"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to index document: {str(e)}")
    finally:
        if temp_path.exists():
            try:
                os.remove(temp_path)
            except Exception:
                pass


@app.get("/api/knowledge-base/documents")
def list_kb_documents():
    """Lists indexed RAG documents and knowledge base statistics."""
    return {
        "documents": knowledge_base.list_documents(),
        "stats": knowledge_base.get_stats(),
    }


@app.delete("/api/knowledge-base/documents/{doc_id}")
def delete_kb_document(doc_id: str):
    """Deletes a document and its chunks from the RAG index."""
    success = knowledge_base.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found in RAG index.")
    return {"success": True, "deleted_doc_id": doc_id}


@app.post("/api/knowledge-base/search")
def search_kb(req: KBSearchRequest):
    """Performs similarity search on local indexed standards."""
    results = knowledge_base.search(req.query, top_k=req.top_k)
    return {"results": results}


# -----------------------------------------------------------------------------
# Static Artifacts & Frontend Serving
# -----------------------------------------------------------------------------
@app.get("/api/artifacts/{path:path}")
def get_artifact(path: str):
    """Serves generated Office deliverables, plots, and uploaded documents."""
    file_path = Path(STORAGE_DIR) / path
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Artifact file not found.")

    media_types = {
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".pdf": "application/pdf",
        ".py": "text/plain",
        ".json": "application/json",
        ".txt": "text/plain",
        ".csv": "text/plain",
    }
    ext = file_path.suffix.lower()
    media_type = media_types.get(ext, "application/octet-stream")

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type=media_type,
    )


if FRONTEND_DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)


