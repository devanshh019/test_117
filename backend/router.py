from typing import Dict, List, Any, Optional
from pydantic import BaseModel

from .config import (
    PPTX_TRIGGERS,
    DOCX_TRIGGERS,
    XLSX_TRIGGERS,
    MATH_CODE_TRIGGERS,
    STANDARDS_TRIGGERS,
)
from .model_manager import get_model_for_task


class RoutingDecision(BaseModel):
    task_category: str
    selected_model_id: str
    model_name: str
    confidence: float
    routing_reasons: List[str]


class DynamicTaskRouter:
    """Classifies user intent and routes tasks to the specialized model in model.yaml."""

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

    def _determine_category(self, prompt_lower: str, has_image: bool, has_doc: bool) -> tuple[str, str]:
        if has_image:
            return "MULTIMODAL_IMAGE_INSPECTION", "Attached visual image/diagram"
        if has_doc:
            return "DOCUMENT_RAG_ANALYSIS", "Attached reference document"
        if any(k in prompt_lower for k in MATH_CODE_TRIGGERS):
            return "ENGINEERING_MATH_AND_CODE", "Engineering calculation or Python code simulation"
        if any(k in prompt_lower for k in (PPTX_TRIGGERS + DOCX_TRIGGERS + XLSX_TRIGGERS)):
            return "ENTERPRISE_DELIVERABLE_SYNTHESIS", "Office deliverable generation (Word / Excel / PPTX)"
        if any(k in prompt_lower for k in STANDARDS_TRIGGERS):
            return "STANDARDS_AND_GOVERNANCE_REASONING", "Plant standards lookup and compliance review"
        return "GENERAL_ENGINEERING_REASONING", "General technical reasoning"

    def route_task(
        self,
        prompt: str,
        attachments: List[Dict[str, Any]] = None,
        requested_mode: Optional[str] = None,
    ) -> RoutingDecision:
        prompt_lower = prompt.lower()
        attachments = attachments or []

        has_image = self._has_image_attachment(attachments)
        has_doc = self._has_doc_attachment(attachments)
        category, reason = self._determine_category(prompt_lower, has_image, has_doc)

        # Auto-select the specialized model for this specific task category from model.yaml
        target_model = get_model_for_task(category)
        model_id = target_model.get("id", "gemma3:4b")
        model_name = target_model.get("name", model_id)
        reasons = [reason, f"Auto-selected specialized model: {model_name}"]

        return RoutingDecision(
            task_category=category,
            selected_model_id=model_id,
            model_name=model_name,
            confidence=0.98,
            routing_reasons=reasons,
        )


# Default shared router instance
router = DynamicTaskRouter()
