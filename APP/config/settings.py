"""Constantes globales y configuracion."""

import math

# Constante de Euler-Mascheroni
EULER_MASCHERONI = 0.5772156649015329

# Pi
PI = math.pi

# Niveles de detalle
DETAIL_MAX = 3        # Maximo detalle: cada sub-calculo
DETAIL_INTERMEDIATE = 2  # Intermedio: formulas con valores reemplazados
DETAIL_BASIC = 1      # Basico: solo formula y resultado

DETAIL_LABELS = {
    DETAIL_MAX: "Maximo detalle",
    DETAIL_INTERMEDIATE: "Detalle intermedio",
    DETAIL_BASIC: "Formula y resultado",
}

# Tolerancia para comparaciones numericas
EPSILON = 1e-10

# Maximo de terminos para sumatorias infinitas (Poisson, Pascal)
MAX_SUMMATION_TERMS = 1000

# Ruta base del proyecto
import os
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEORIA_DIR = os.path.join(os.path.dirname(APP_DIR), "TEORIA")
GUIA_PATH = os.path.join(os.path.dirname(APP_DIR),
    "Guia Problemas Estadística General - Probabilidad y Estadística - UADE (1).pdf")
SESSION_CONFIG_PATH = os.path.join(APP_DIR, ".session_config.json")
GUIA_INDEX_CACHE = os.path.join(APP_DIR, "guide_index", "index.json")

# Ollama (local LLM) — invisible al usuario final
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b-instruct")
OLLAMA_MODEL_FALLBACK = os.environ.get("OLLAMA_MODEL_FALLBACK", "qwen2.5:14b-instruct")
OLLAMA_EMBED_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_ENABLED = os.environ.get("OLLAMA_ENABLED", "1") not in ("0", "false", "False", "")
OLLAMA_TIMEOUT = float(os.environ.get("OLLAMA_TIMEOUT", "180"))
OLLAMA_KEEP_ALIVE = os.environ.get("OLLAMA_KEEP_ALIVE", "2h")

THEORY_CACHE_DIR = os.path.join(APP_DIR, "theory", "_cache")
MACHETE_PATH = os.path.join(TEORIA_DIR, "MACHETE.md")
LOG_DIR = os.path.join(APP_DIR, "logs")


def resolve_guia_path():
    """Return a usable path to the guide PDF, searching for NFD/NFC filename variants."""
    if os.path.exists(GUIA_PATH):
        return GUIA_PATH
    import glob
    matches = glob.glob(os.path.join(os.path.dirname(APP_DIR), "Guia*.pdf"))
    return matches[0] if matches else GUIA_PATH
