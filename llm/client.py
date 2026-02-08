import time
from typing import Optional, Dict, Any
import json
import urllib.request
from config import Config


class LLMClient:
    def __init__(self, config: Config):
        self.config = config

    def generate(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.config.LLM_URL}/api/generate"

        full_prompt = prompt if not system else f"{system}\n\n{prompt}"
        payload: Dict[str, Any] = {
            "model": self.config.LLM_MODEL,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": self.config.LLM_TEMPERATURE,
                "num_predict": self.config.LLM_MAX_TOKENS,
                "num_ctx": self.config.LLM_MAX_CTX,
            },
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                raw = resp.read().decode("utf-8")
                obj = json.loads(raw)

                return {
                    "text": obj.get("response", "").strip(),

                    "prompt_time_ms": obj.get("prompt_eval_duration", 0) / 1_000_000,
                    "eval_time_ms": obj.get("eval_duration", 0) / 1_000_000,

                    "prompt_tokens": obj.get("prompt_eval_count", 0),
                    "eval_tokens": obj.get("eval_count", 0),
                }

        except Exception as e:
            raise RuntimeError(
                "Failed to call Ollama. "
                "Ensure Ollama is running: `ollama serve` and model is pulled."
            ) from e