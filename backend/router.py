from typing import Dict, List, Any, Optional
from pydantic import BaseModel

from .config import (
    PPTX_TRIGGERS,
    DOCX_TRIGGERS,
    XLSX_TRIGGERS,
    VISUAL_AND_DRAWING_TRIGGERS,
    STANDARDS_AND_GOVERNANCE_TRIGGERS,
    MATH_AND_CODE_TRIGGERS,
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
        # 1. Image Attachments or Explicit P&ID / Drawing / Schematic Queries
        if has_image or any(k in prompt_lower for k in VISUAL_AND_DRAWING_TRIGGERS):
            return "MULTIMODAL_IMAGE_INSPECTION", "P&ID schematic, drawing, or visual inspection"

        # 2. Document Attachments
        if has_doc:
            return "DOCUMENT_RAG_ANALYSIS", "Attached reference document"

        # 3. Office Deliverables (.docx, .pptx, .xlsx)
        if any(k in prompt_lower for k in (PPTX_TRIGGERS + DOCX_TRIGGERS + XLSX_TRIGGERS)):
            return "ENTERPRISE_DELIVERABLE_SYNTHESIS", "Office deliverable generation (Word / Excel / PPTX)"

        # 4. Standards & Governance (pure compliance/audit lookup without explicit math calculation)
        if any(k in prompt_lower for k in STANDARDS_AND_GOVERNANCE_TRIGGERS) and not any(k in prompt_lower for k in ["calculate", "compute", "derive", "solve", "integral", "derivative", "python", "script", "code", "plot", "simulate"]):
            return "STANDARDS_AND_GOVERNANCE_REASONING", "Plant standards lookup and compliance review"

        # 5. Engineering Math, Numerical Calculations & Python Scripting
        if any(k in prompt_lower for k in MATH_AND_CODE_TRIGGERS):
            return "ENGINEERING_MATH_AND_CODE", "Engineering mathematics, calculation, or Python simulation"

        # 6. Standards fallback
        if any(k in prompt_lower for k in STANDARDS_AND_GOVERNANCE_TRIGGERS):
            return "STANDARDS_AND_GOVERNANCE_REASONING", "Plant standards lookup and compliance review"

        # 7. Default: General Technical & Engineering Reasoning
        return "GENERAL_ENGINEERING_REASONING", "General engineering and technical reasoning"

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
