import httpx
from typing import Dict, List, Any, Optional

from .config import (
    OLLAMA_BASE_URL,
    OLLAMA_TIMEOUT_SECONDS,
    OLLAMA_HEALTH_TIMEOUT_SECONDS,
    MODEL_TEMPERATURE,
    MODEL_TOP_P,
    MODEL_CONTEXT_WINDOW,
    MAX_HISTORY_TURNS,
)
from .model_manager import get_active_model, set_active_model


class LocalSovereignInference:
    """Client for local Ollama HTTP API (http://127.0.0.1:11434)."""

    def __init__(self):
        self.ollama_url = OLLAMA_BASE_URL
        self.client = httpx.Client(timeout=OLLAMA_TIMEOUT_SECONDS)
        self.selected_model: Optional[str] = None

    def set_target_model(self, model_tag: str):
        """Explicitly sets user-chosen active model."""
        self.selected_model = model_tag
        set_active_model(model_tag)

    def check_local_ollama_health(self) -> Dict[str, Any]:
        """
        Read-only health check. Checks if Ollama is running and lists installed models
        WITHOUT mutating the active model state.
        """
        active = get_active_model()
        active_id = active.get("id", "gemma3:4b")
        try:
            resp = self.client.get(
                f"{self.ollama_url}/api/tags",
                timeout=OLLAMA_HEALTH_TIMEOUT_SECONDS
            )
            if resp.status_code == 200:
                raw_models = resp.json().get("models", [])
                model_names = [m.get("name") for m in raw_models if m.get("name")]
                return {
                    "available": True,
                    "models": model_names,
                    "active_model": active_id,
                    "endpoint": self.ollama_url,
                }
        except Exception:
            pass

        return {
            "available": False,
            "models": [],
            "active_model": active_id,
            "endpoint": self.ollama_url,
        }

    def _resolve_target_model(self, model_id: Optional[str], installed_models: List[str]) -> str:
        """Determines which model tag to use for inference, prioritizing router auto-selection."""
        # 1. Target model assigned by the Router for this specific task
        if model_id and (not installed_models or model_id in installed_models):
            return model_id
        # 2. User manual override
        if self.selected_model and self.selected_model in installed_models:
            return self.selected_model
        # 3. First available installed model
        if installed_models:
            return installed_models[0]
        return get_active_model().get("id", "gemma3:4b")



    def _build_messages_payload(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        images: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Constructs the messages list for Ollama /api/chat including visual image payloads."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if history:
            recent_turns = history[-MAX_HISTORY_TURNS:]
            for item in recent_turns:
                role = "user" if item.get("role") == "user" else "assistant"
                content = item.get("content", "")
                if content and not content.startswith("> [!WARNING]"):
                    messages.append({"role": role, "content": content})

        user_msg: Dict[str, Any] = {"role": "user", "content": prompt}
        if images and len(images) > 0:
            user_msg["images"] = images
        messages.append(user_msg)
        return messages

    def generate(
        self,
        prompt: str,
        model_id: Optional[str] = None,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        images: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Sends chat generation request to local Ollama with optional visual image attachments."""
        health = self.check_local_ollama_health()

        if not health["available"]:
            return {
                "success": False,
                "model_online": False,
                "response": (
                    "> [!WARNING]\n"
                    "> **Local Inference Engine Offline**: Could not connect to Ollama at `http://127.0.0.1:11434`.\n\n"
                    "**To start Ollama**:\n"
                    "```bash\n"
                    "ollama run llama3  # or: ollama run gemma3:4b\n"
                    "```"
                ),
                "model_used": "None (Ollama Offline)",
            }

        target_model = self._resolve_target_model(model_id, health["models"])
        set_active_model(target_model)
        messages_payload = self._build_messages_payload(prompt, system_prompt, history, images)



        try:
            chat_payload = {
                "model": target_model,
                "messages": messages_payload,
                "stream": False,
                "options": {
                    "temperature": MODEL_TEMPERATURE,
                    "top_p": MODEL_TOP_P,
                    "num_ctx": MODEL_CONTEXT_WINDOW,
                },
            }
            res = self.client.post(
                f"{self.ollama_url}/api/chat",
                json=chat_payload,
                timeout=OLLAMA_TIMEOUT_SECONDS,
            )

            if res.status_code == 200:
                content = res.json().get("message", {}).get("content", "").strip()
                return {
                    "success": bool(content),
                    "model_online": True,
                    "response": content or "> [!WARNING]\n> Empty response received.",
                    "model_used": f"Ollama ({target_model})",
                }

            return {
                "success": False,
                "model_online": False,
                "response": f"> [!WARNING]\n> **Ollama HTTP Error {res.status_code}**: {res.text}",
                "model_used": f"Ollama ({target_model})",
            }
        except Exception as e:
            return {
                "success": False,
                "model_online": False,
                "response": f"> [!WARNING]\n> **Inference Error**: {str(e)}",
                "model_used": f"Ollama ({target_model})",
            }


# Shared inference engine instance
inference_engine = LocalSovereignInference()


