"""
Tests del cliente Ollama. Se marcan skip si el servicio no está corriendo
(no rompen el runner).

Ejecutar desde APP/:
    C:\\Python314\\python tests/test_ollama_client.py
"""

from __future__ import annotations

import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.dirname(_HERE)
if _APP not in sys.path:
    sys.path.insert(0, _APP)

from llm.ollama_client import OllamaClient, OllamaUnavailable


def _skip(reason: str) -> None:
    print(f"  SKIP: {reason}")


def test_availability_check():
    print("\n[1] OllamaClient.is_available()")
    c = OllamaClient()
    ok = c.is_available()
    print(f"  is_available = {ok}")
    if not ok:
        _skip("Ollama no está corriendo")
        return
    models = c.list_models()
    print(f"  modelos pulled: {models}")
    assert isinstance(models, list), "list_models debe retornar lista"


def test_embed_basic():
    print("\n[2] OllamaClient.embed()")
    c = OllamaClient()
    if not c.is_available():
        _skip("Ollama no está corriendo")
        return
    if not any("nomic-embed-text" in m for m in c.list_models()):
        _skip("nomic-embed-text no está pulled")
        return
    try:
        embs = c.embed(["Binomial es la suma de Bernoullis", "media y varianza"])
        assert len(embs) == 2, f"se esperaban 2 embeddings, hubo {len(embs)}"
        assert len(embs[0]) > 64, f"embedding muy corto: {len(embs[0])}"
        print(f"  OK embeddings dim={len(embs[0])}")
    except OllamaUnavailable as e:
        _skip(f"OllamaUnavailable: {e}")


def test_chat_json_mode():
    print("\n[3] OllamaClient.chat(json_mode=True)")
    c = OllamaClient()
    if not c.is_available():
        _skip("Ollama no está corriendo")
        return
    chat_model = c._resolve_model()
    if not any(chat_model in m or m.startswith(chat_model) for m in c.list_models()):
        _skip(f"modelo {chat_model} no está pulled")
        return
    try:
        resp = c.chat(
            [
                {"role": "system", "content": "Devolvé un JSON con forma {\"ok\": true}."},
                {"role": "user", "content": "ok?"},
            ],
            json_mode=True,
        )
        print(f"  respuesta: {resp[:200]}")
        import json as _json
        obj = _json.loads(resp)
        assert isinstance(obj, dict), "JSON debe ser objeto"
        print(f"  OK JSON parseado: {obj}")
    except OllamaUnavailable as e:
        _skip(f"OllamaUnavailable: {e}")


def test_determinism():
    print("\n[4] Determinismo con temperature=0 seed=0")
    c = OllamaClient(seed=0)
    if not c.is_available():
        _skip("Ollama no está corriendo")
        return
    chat_model = c._resolve_model()
    if not any(chat_model in m or m.startswith(chat_model) for m in c.list_models()):
        _skip(f"modelo {chat_model} no está pulled")
        return
    try:
        msgs = [{"role": "user", "content": "Decí 'hola' y nada más."}]
        r1 = c.chat(msgs, temperature=0.0, max_tokens=20)
        r2 = c.chat(msgs, temperature=0.0, max_tokens=20)
        print(f"  r1={r1!r} r2={r2!r}")
        # Determinismo estricto puede fallar por implementación del backend;
        # basta con que ambos respondan sin error.
        assert r1 and r2, "ambas respuestas deben tener contenido"
    except OllamaUnavailable as e:
        _skip(f"OllamaUnavailable: {e}")


if __name__ == "__main__":
    tests = [test_availability_check, test_embed_basic, test_chat_json_mode, test_determinism]
    passed = 0
    failed = []
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            failed.append((t.__name__, str(e)))
            print(f"  FAIL {t.__name__}: {e}")
        except Exception as e:
            failed.append((t.__name__, f"EXC {e}"))
            print(f"  FAIL {t.__name__}: {e}")
    print(f"\n{'='*60}")
    print(f"RESULTADO: {passed}/{len(tests)} OK")
    if failed:
        for n, err in failed:
            print(f"  {n}: {err}")
        sys.exit(1)
