from typing import Dict, List, Any, Optional
import numpy as np
from pydantic import BaseModel
from chromadb.utils import embedding_functions

from .model_manager import get_model_for_task

emb_fn = embedding_functions.DefaultEmbeddingFunction()


class RoutingDecision(BaseModel):
    task_category: str
    selected_model_id: str
    model_name: str
    confidence: float
    routing_reasons: List[str]


# Semantic Domain Descriptions for Vector Matching (Zero Hardcoding)
CATEGORY_DESCRIPTIONS = {
    "MULTIMODAL_IMAGE_INSPECTION": "Visual image, scanned PDF drawing, P&ID diagram, engineering blueprint, schematic, photograph inspection, OCR, control valve bypass.",
    "ENTERPRISE_DELIVERABLE_SYNTHESIS": "Generating Office deliverables, formal Word approval notes (.docx), PowerPoint slide presentation decks (.pptx), and Excel calculation spreadsheets (.xlsx).",
    "STANDARDS_AND_GOVERNANCE_REASONING": "Auditing compliance against ASME Boiler and Pressure Vessel Code, API 510/570 inspection standards, GFR-2017 procurement rules, tender evaluations, turnaround reports, and regulatory plant governance.",
    "ENGINEERING_MATH_AND_CODE": "Mathematical calculations, numerical formulas, algebra, calculus, differential equations, physics equations, LMTD, Reynolds number, and writing or executing Python code scripts, algorithms, and internal tools.",
    "GENERAL_ENGINEERING_REASONING": "General engineering reasoning, physics principles, materials science, thermodynamics, chemistry, and technical questions.",
}


class DynamicTaskRouter:
    """Routes tasks using on-premises semantic vector embeddings and cosine similarity."""

    def __init__(self):
        self._centroids = {}
        for cat, desc in CATEGORY_DESCRIPTIONS.items():
            vec = np.array(emb_fn([desc])[0])
            norm = np.linalg.norm(vec)
            self._centroids[cat] = vec / norm if norm > 0 else vec

    def _has_image_attachment(self, attachments: List[Dict[str, Any]]) -> bool:
        return any(
            a.get("type", "").startswith("image/") or
            a.get("name", "").lower().endswith((".png", ".jpg", ".jpeg", ".webp")) or
            a.get("filename", "").lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            for a in attachments
        )

    def _has_doc_attachment(self, attachments: List[Dict[str, Any]]) -> bool:
        return any(
            a.get("name", "").lower().endswith((".pdf", ".docx", ".txt", ".csv")) or
            a.get("filename", "").lower().endswith((".pdf", ".docx", ".txt", ".csv"))
            for a in attachments
        )

    def _determine_category(self, prompt: str, has_image: bool, has_doc: bool) -> tuple[str, str, float]:
        if has_image:
            return "MULTIMODAL_IMAGE_INSPECTION", "Attached visual image/drawing", 1.0
        if has_doc:
            return "DOCUMENT_RAG_ANALYSIS", "Attached reference document", 1.0

        # Semantic Vector Cosine Similarity
        try:
            q_vec = np.array(emb_fn([prompt])[0])
            q_norm = np.linalg.norm(q_vec)
            q_unit = q_vec / q_norm if q_norm > 0 else q_vec

            scores = {cat: float(np.dot(q_unit, c_vec)) for cat, c_vec in self._centroids.items()}
            best_cat = max(scores, key=scores.get)
            confidence = round(max(0.75, min(0.99, scores[best_cat] + 0.5)), 2)
            return best_cat, f"Matched semantic intent vector with score {scores[best_cat]:.3f}", confidence
        except Exception:
            return "GENERAL_ENGINEERING_REASONING", "Default technical reasoning fallback", 0.80

    def route_task(
        self,
        prompt: str,
        attachments: List[Dict[str, Any]] = None,
        requested_mode: Optional[str] = None,
    ) -> RoutingDecision:
        attachments = attachments or []
        has_image = self._has_image_attachment(attachments)
        has_doc = self._has_doc_attachment(attachments)
        category, reason, confidence = self._determine_category(prompt, has_image, has_doc)

        # Auto-select the specialized model for this specific task category from model.yaml
        target_model = get_model_for_task(category)
        model_id = target_model.get("id", "gemma3:4b")
        model_name = target_model.get("name", model_id)
        reasons = [reason, f"Auto-selected specialized model: {model_name}"]

        return RoutingDecision(
            task_category=category,
            selected_model_id=model_id,
            model_name=model_name,
            confidence=confidence,
            routing_reasons=reasons,
        )


router = DynamicTaskRouter()
