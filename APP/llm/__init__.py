"""
Cliente LLM local (Ollama). Invisible para el usuario final.
Se usa como fallback del parser y como motor de Consultas Teóricas.
"""

from llm.ollama_client import OllamaClient, OllamaUnavailable, get_default_client

__all__ = ["OllamaClient", "OllamaUnavailable", "get_default_client"]
