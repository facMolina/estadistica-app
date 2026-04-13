"""Wrapper del SDK de Anthropic con prompt caching."""

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

# Modelo usado para interpretar el enunciado.
# claude-haiku-4-5 es suficiente para extracción/clasificación y es más económico.
# Cambiar a "claude-opus-4-6" para mayor precisión si se desea.
INTERPRETER_MODEL = "claude-haiku-4-5"


class ClaudeClient:
    """Cliente de la API de Anthropic con caching del system prompt."""

    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY no encontrada.\n"
                "Crear archivo .env en la carpeta APP/ con:\n"
                "  ANTHROPIC_API_KEY=sk-ant-..."
            )
        self.client = anthropic.Anthropic(api_key=api_key)

    def interpret(self, messages: list[dict], system_prompt: str) -> str:
        """
        Envía los mensajes a Claude y retorna la respuesta como string.

        El system_prompt se cachea con ephemeral cache (TTL 5 min) para
        reducir costos en conversaciones multi-turno.
        """
        response = self.client.messages.create(
            model=INTERPRETER_MODEL,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},  # Cache del prompt grande
                }
            ],
            messages=messages,
        )
        return response.content[0].text
