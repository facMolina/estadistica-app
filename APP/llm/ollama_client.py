"""
Cliente HTTP minimal para Ollama local (http://127.0.0.1:11434).

Diseño:
- Sin dependencias nuevas: usa `requests` (ya en requirements).
- Cachea `is_available()` 30 s para no spamear el endpoint.
- `json_mode=True` pide al modelo que devuelva JSON estricto.
- Determinismo por default: temperature=0, seed=0.
- Si el servicio no responde, lanza OllamaUnavailable (los callers
  deben atrapar y degradar silenciosamente: el usuario no debe
  ver ningún rastro de esta infra).
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

import requests

from config.settings import (
    LOG_DIR,
    OLLAMA_EMBED_MODEL,
    OLLAMA_ENABLED,
    OLLAMA_HOST,
    OLLAMA_KEEP_ALIVE,
    OLLAMA_MODEL,
    OLLAMA_MODEL_FALLBACK,
    OLLAMA_TIMEOUT,
)


_AVAILABILITY_TTL = 30.0


os.makedirs(LOG_DIR, exist_ok=True)
_logger = logging.getLogger("llm.ollama")
if not _logger.handlers:
    _fh = logging.FileHandler(os.path.join(LOG_DIR, "ollama.log"), encoding="utf-8")
    _fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    _logger.addHandler(_fh)
    _logger.setLevel(logging.INFO)


class OllamaUnavailable(RuntimeError):
    """Lanzada cuando el servicio no responde o el modelo no está pulled."""


class OllamaClient:
    def __init__(
        self,
        model: str | None = None,
        host: str | None = None,
        timeout: float | None = None,
        seed: int = 0,
    ) -> None:
        self.model = model or OLLAMA_MODEL
        self.fallback_model = OLLAMA_MODEL_FALLBACK
        self.host = (host or OLLAMA_HOST).rstrip("/")
        self.timeout = float(timeout if timeout is not None else OLLAMA_TIMEOUT)
        self.seed = seed
        self._avail_cache: tuple[float, bool] | None = None
        self._resolved_model: str | None = None

    # ------------------------------------------------------------------
    # Availability
    # ------------------------------------------------------------------
    def is_available(self) -> bool:
        if not OLLAMA_ENABLED:
            return False
        now = time.monotonic()
        if self._avail_cache and (now - self._avail_cache[0]) < _AVAILABILITY_TTL:
            return self._avail_cache[1]
        ok = False
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=3)
            ok = r.status_code == 200
        except Exception as e:
            _logger.info("is_available: ping failed: %r", e)
            ok = False
        self._avail_cache = (now, ok)
        return ok

    def list_models(self) -> list[str]:
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=3)
            r.raise_for_status()
            data = r.json()
            return [m.get("name", "") for m in data.get("models", [])]
        except Exception as e:
            _logger.info("list_models failed: %r", e)
            return []

    def _resolve_model(self) -> str:
        if self._resolved_model:
            return self._resolved_model
        pulled = self.list_models()
        for candidate in (self.model, self.fallback_model):
            if any(m == candidate or m.startswith(candidate + ":") for m in pulled):
                self._resolved_model = candidate
                return candidate
        # Último recurso: usamos `self.model` tal cual y dejamos que Ollama
        # devuelva error si no está pulled — los callers saben atraparlo.
        self._resolved_model = self.model
        return self.model

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------
    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        json_mode: bool = False,
        temperature: float = 0.0,
        max_tokens: int = 2048,
        model: str | None = None,
    ) -> str:
        if not self.is_available():
            raise OllamaUnavailable("servicio Ollama no responde")

        chosen = model or self._resolve_model()
        payload: dict[str, Any] = {
            "model": chosen,
            "messages": messages,
            "stream": False,
            "keep_alive": OLLAMA_KEEP_ALIVE,
            "options": {
                "temperature": float(temperature),
                "seed": int(self.seed),
                "num_predict": int(max_tokens),
            },
        }
        if json_mode:
            payload["format"] = "json"

        start = time.monotonic()
        try:
            r = requests.post(
                f"{self.host}/api/chat",
                json=payload,
                timeout=self.timeout,
            )
            r.raise_for_status()
            data = r.json()
        except requests.exceptions.RequestException as e:
            _logger.warning("chat HTTP error: %r", e)
            raise OllamaUnavailable(f"http error: {e}")
        except ValueError as e:
            _logger.warning("chat JSON parse error: %r", e)
            raise OllamaUnavailable(f"bad json response: {e}")
        finally:
            elapsed = time.monotonic() - start
            _logger.info("chat elapsed=%.2fs model=%s", elapsed, chosen)

        msg = data.get("message", {})
        content = msg.get("content", "")
        if not content:
            raise OllamaUnavailable("respuesta vacía del modelo")
        return content

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------
    def embed(
        self,
        texts: list[str],
        *,
        model: str | None = None,
    ) -> list[list[float]]:
        if not self.is_available():
            raise OllamaUnavailable("servicio Ollama no responde")

        chosen = model or OLLAMA_EMBED_MODEL
        try:
            r = requests.post(
                f"{self.host}/api/embed",
                json={"model": chosen, "input": texts, "keep_alive": OLLAMA_KEEP_ALIVE},
                timeout=self.timeout,
            )
            r.raise_for_status()
            data = r.json()
        except requests.exceptions.RequestException as e:
            _logger.warning("embed HTTP error: %r", e)
            raise OllamaUnavailable(f"embed http error: {e}")
        except ValueError as e:
            _logger.warning("embed JSON parse error: %r", e)
            raise OllamaUnavailable(f"embed bad json: {e}")

        embs = data.get("embeddings")
        if not embs or not isinstance(embs, list):
            raise OllamaUnavailable("embeddings vacío")
        return embs


    # ------------------------------------------------------------------
    # Warm-up: dispara una request mínima para forzar carga en RAM/VRAM.
    # Pensado para llamarse en background cuando el usuario entra al modo.
    # ------------------------------------------------------------------
    def warmup(self, *, also_embed: bool = True) -> bool:
        if not self.is_available():
            return False
        chosen = self._resolve_model()
        ok = True
        try:
            requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": chosen,
                    "prompt": "",
                    "stream": False,
                    "keep_alive": OLLAMA_KEEP_ALIVE,
                },
                timeout=self.timeout,
            )
        except Exception as e:
            _logger.info("warmup chat failed: %r", e)
            ok = False
        if also_embed:
            try:
                requests.post(
                    f"{self.host}/api/embed",
                    json={
                        "model": OLLAMA_EMBED_MODEL,
                        "input": [""],
                        "keep_alive": OLLAMA_KEEP_ALIVE,
                    },
                    timeout=self.timeout,
                )
            except Exception as e:
                _logger.info("warmup embed failed: %r", e)
        return ok


_default_client: OllamaClient | None = None


def get_default_client() -> OllamaClient:
    global _default_client
    if _default_client is None:
        _default_client = OllamaClient()
    return _default_client
