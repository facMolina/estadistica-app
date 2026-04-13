"""Loop de conversación CLI: interpreta el problema y prepara la config para Streamlit."""

import json
import os
import re

from interpreter.claude_client import ClaudeClient
from interpreter.system_prompt import SYSTEM_PROMPT
from config.model_catalog import is_implemented, normalize_model_name
from config.settings import SESSION_CONFIG_PATH

# Mapeo de query_type a la etiqueta que muestra Streamlit
QUERY_TYPE_LABELS = {
    "probability": "P(r = valor)",
    "cdf_left": "F(r) = P(VA <= valor)",
    "cdf_right": "G(r) = P(VA >= valor)",
    "range": "P(A <= r <= B)",
    "full_analysis": "Análisis completo",
}


def _clean_json(text: str) -> str:
    """Elimina bloques markdown si Claude los incluyó por error."""
    text = text.strip()
    # Remover ```json ... ``` o ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        return match.group(1).strip()
    return text


class ProblemParser:
    """
    Maneja el loop de conversación con Claude para interpretar un problema estadístico.

    Flujo:
      1. Usuario describe el problema en texto libre.
      2. Claude retorna JSON con status "complete" o "need_more_info".
      3. Si falta info, CLI muestra la pregunta y espera la respuesta del usuario.
      4. Al completar, muestra el resumen y pide confirmación.
      5. Si confirma, escribe session_config.json para que Streamlit lo lea.
    """

    def __init__(self):
        self.client = ClaudeClient()
        self.history: list[dict] = []

    def parse(self, initial_input: str) -> dict | None:
        """
        Ejecuta el loop hasta obtener un resultado completo.
        Retorna el dict del resultado o None si el usuario cancela.
        """
        self.history.append({"role": "user", "content": initial_input})

        max_turns = 8  # Evitar loops infinitos
        for _ in range(max_turns):
            raw = self.client.interpret(self.history, SYSTEM_PROMPT)
            self.history.append({"role": "assistant", "content": raw})

            # Parsear JSON (tolerante a markdown code blocks)
            try:
                result = json.loads(_clean_json(raw))
            except json.JSONDecodeError:
                # Claude respondió algo que no es JSON — pedir que lo corrija
                print("\n  [Reintentando — respuesta no era JSON válido]")
                self.history.append({
                    "role": "user",
                    "content": "Tu respuesta anterior no era JSON válido. Respondé únicamente con JSON según el formato indicado en el system prompt.",
                })
                continue

            status = result.get("status")

            if status == "complete":
                # Normalizar nombre del modelo
                if result.get("model"):
                    result["model"] = normalize_model_name(result["model"])
                return result

            elif status == "need_more_info":
                question = result.get("question", "¿Podés dar más detalles?")
                model_so_far = result.get("model")
                params_so_far = result.get("params", {})

                # Mostrar progreso
                if model_so_far:
                    print(f"\n  Modelo identificado: {normalize_model_name(model_so_far)}", end="")
                    if params_so_far:
                        params_str = ", ".join(f"{k}={v}" for k, v in params_so_far.items())
                        print(f"  |  Parámetros hasta ahora: {params_str}", end="")
                    print()

                print(f"\n  {question}")
                user_answer = input("  > ").strip()

                if not user_answer or user_answer.lower() in ("salir", "exit", "cancelar", "q"):
                    return None

                self.history.append({"role": "user", "content": user_answer})
                continue

            else:
                print(f"\n  [Error] Estado desconocido en la respuesta: {status!r}")
                return None

        print("\n  [Se alcanzó el máximo de turnos sin completar el análisis]")
        return None

    def show_result(self, result: dict) -> None:
        """Muestra el resumen del resultado en consola."""
        model = result.get("model", "Desconocido")
        params = result.get("params", {})
        query_type = result.get("query_type", "full_analysis")
        query_params = result.get("query_params", {})
        interpretation = result.get("interpretation", "")

        query_label = QUERY_TYPE_LABELS.get(query_type, query_type)
        params_str = "  ".join(f"{k} = {v}" for k, v in params.items())
        query_str = f"{query_label}" + (f"  →  {query_params}" if query_params else "")

        print("\n" + "─" * 60)
        print("  INTERPRETACIÓN DEL PROBLEMA")
        print("─" * 60)
        print(f"  Modelo:      {model}")
        print(f"  Parámetros:  {params_str}")
        print(f"  Consulta:    {query_str}")
        print(f"\n  {interpretation}")
        print("─" * 60)

    def confirm_and_write_config(self, result: dict) -> bool:
        """
        Muestra el resultado, verifica si está implementado, pide confirmación
        y escribe session_config.json si el usuario confirma.
        Retorna True si se confirmó y escribió el config.
        """
        self.show_result(result)
        model = result.get("model", "")

        # Verificar implementación
        if not is_implemented(model):
            from config.model_catalog import IMPLEMENTED_MODELS
            print(f"\n  El modelo '{model}' aún no está implementado en la app.")
            print(f"  Modelos disponibles: {', '.join(sorted(IMPLEMENTED_MODELS))}")
            return False

        # Pedir confirmación
        answer = input("\n  ¿Es correcto? (S/n): ").strip().lower()
        if answer in ("n", "no"):
            print("  Podés describir el problema nuevamente para corregirlo.")
            return False

        # Escribir session_config.json
        config = {
            "model": model,
            "params": result.get("params", {}),
            "query_type": result.get("query_type", "full_analysis"),
            "query_params": result.get("query_params", {}),
            "interpretation": result.get("interpretation", ""),
        }
        os.makedirs(os.path.dirname(SESSION_CONFIG_PATH), exist_ok=True)
        with open(SESSION_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        return True
