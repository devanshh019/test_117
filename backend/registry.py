from typing import List, Optional
from pydantic import BaseModel

from .config import (
    DEFAULT_MODEL_ID,
    DEFAULT_MODEL_NAME,
    DEFAULT_MODEL_VRAM_GB,
    MODEL_TEMPERATURE,
)


class ModelProfile(BaseModel):
    model_id: str
    name: str
    description: str
    temperature: float = MODEL_TEMPERATURE
    vram_footprint_gb: float = DEFAULT_MODEL_VRAM_GB
    capabilities: List[str] = [
        "standards_compliance",
        "python_execution",
        "engineering_math",
        "document_synthesis",
        "rag_retrieval",
    ]


class ModelRegistry:
    """Manages the active sovereign local model profile."""

    def __init__(self):
        self.active_profile = ModelProfile(
            model_id=DEFAULT_MODEL_ID,
            name=DEFAULT_MODEL_NAME,
            description="Local on-premises foundation model for reasoning, calculations, and documents.",
            temperature=MODEL_TEMPERATURE,
            vram_footprint_gb=DEFAULT_MODEL_VRAM_GB,
        )

    def get_active_model(self) -> ModelProfile:
        """Returns the currently active model profile."""
        return self.active_profile

    def set_active_model(self, model_tag: str, name: Optional[str] = None):
        """Updates the active model profile when switching or detecting a local model."""
        display_name = name or model_tag
        self.active_profile = ModelProfile(
            model_id=model_tag,
            name=display_name,
            description=f"Active local model running via Ollama ({model_tag}).",
            temperature=MODEL_TEMPERATURE,
            vram_footprint_gb=DEFAULT_MODEL_VRAM_GB,
        )

    def get_total_vram_usage(self) -> float:
        """Returns the estimated VRAM/RAM footprint in GB."""
        return self.active_profile.vram_footprint_gb


# Shared model registry instance
registry = ModelRegistry()


