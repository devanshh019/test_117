# Semantic Intent Classifier and Model Persona Router
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


# Pure Semantic Vector Centroids for Cosine Similarity (Zero Hardcoding)
CATEGORY_DESCRIPTIONS = {
    "MULTIMODAL_IMAGE_INSPECTION": "Visual image inspection, examine photos, review blueprints, P&ID drawings, optical character recognition OCR, and visual defect detection in images.",
    "STANDARDS_AND_GOVERNANCE_REASONING": "Regulatory statutory compliance, safety guidelines, operating procedures, audits, statutory governance, and technical standard rules.",
    "ENGINEERING_MATH_AND_CODE": "Write code, programming functions, scripts, algorithms, mathematical equations, physics simulations, plot engineering curves, render charts, generate diagrams, and execute Python code.",
    "ENTERPRISE_DELIVERABLE_SYNTHESIS": "Generate formatted office reports, structured summary documents, presentation slide decks, and tabular data spreadsheets.",
    "GENERAL_ENGINEERING_REASONING": "Conversational greetings, general inquiries, conceptual discussions, plant engineering explanations, and open-ended technical questions.",
}


class DynamicTaskRouter:
    """Routes tasks using 100% on-premises semantic vector embeddings and cosine similarity."""

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

        # Pure Semantic Vector Cosine Similarity
        try:
            q_vec = np.array(emb_fn([prompt])[0])
            q_norm = np.linalg.norm(q_vec)
            q_unit = q_vec / q_norm if q_norm > 0 else q_vec

            scores = {cat: float(np.dot(q_unit, c_vec)) for cat, c_vec in self._centroids.items()}
            best_cat = max(scores, key=scores.get)
            confidence = round(max(0.75, min(0.99, scores[best_cat] + 0.5)), 2)
            return best_cat, f"Matched semantic intent vector ({best_cat}) with score {scores[best_cat]:.3f}", confidence
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

        target_model = get_model_for_task(category)
        model_id = target_model.get("id", "gemma3:4b")
        model_name = target_model.get("name", model_id)
        reasons = [reason, f"Dispatched model: {model_name}"]

        return RoutingDecision(
            task_category=category,
            selected_model_id=model_id,
            model_name=model_name,
            confidence=confidence,
            routing_reasons=reasons,
        )


router = DynamicTaskRouter()
