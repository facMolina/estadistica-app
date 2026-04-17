"""Intérprete de problemas estadísticos para Streamlit — usa parser regex, sin API."""

import pandas as pd
from interpreter.nl_parser import NLParser
from config.model_catalog import normalize_model_name, is_implemented, IMPLEMENTED_MODELS


def interpret_turn(messages: list[dict], user_text: str) -> dict:
    """
    Parsea user_text (combinando contexto parcial si existe).
    Retorna dict con:
      - action: "complete" | "follow_up" | "error"
      - sc:       dict con toda la info (siempre incluye "mode")
      - question: str (si follow_up)
      - partial:  dict con datos parciales (si follow_up)
      - message:  str con descripción del error (si error)
      - messages: historial actualizado (siempre)
    """
    parser = NLParser()
    combined = _build_combined_text(messages, user_text)
    updated_messages = messages + [{"role": "user", "content": user_text}]

    try:
        result = parser.parse(combined)
    except Exception as e:
        return {
            "action": "error",
            "message": f"Error al interpretar el problema: {e}",
            "messages": updated_messages,
        }

    if result["status"] == "compound":
        from calculation.compound_solver import solve_compound
        try:
            solution = solve_compound(result)
        except Exception as e:
            return {
                "action": "error",
                "message": f"Error al resolver problema compuesto: {e}",
                "messages": updated_messages,
            }
        sc = {
            "mode": "Problema Compuesto",
            "compound_solution": solution,
            "interpretation": result.get("interpretation", "Problema compuesto detectado."),
        }
        return {"action": "complete", "sc": sc, "messages": updated_messages}

    if result["status"] == "complete":
        mode = result.get("mode", "Modelos de Probabilidad")

        # ---- Datos Agrupados ------------------------------------------------
        if mode == "Datos Agrupados":
            sc = {
                "mode": "Datos Agrupados",
                "dp_intervals":    result.get("dp_intervals"),
                "dp_frequencies":  result.get("dp_frequencies"),
                "interpretation":  result.get("interpretation", "Datos agrupados detectados."),
            }
            return {"action": "complete", "sc": sc, "messages": updated_messages}

        # ---- Probabilidad (Bayes / básica) ----------------------------------
        if mode == "Probabilidad":
            sc = {
                "mode":            "Probabilidad",
                "prob_submode":    result.get("prob_submode", "Bayes / Probabilidad Total"),
                "bayes_labels":    result.get("bayes_labels"),
                "bayes_priors":    result.get("bayes_priors"),
                "bayes_likelihoods": result.get("bayes_likelihoods"),
                "bayes_evidence":  result.get("bayes_evidence", "E"),
                "prob_pA":         result.get("prob_pA"),
                "prob_pB":         result.get("prob_pB"),
                "prob_pAB":        result.get("prob_pAB"),
                "prob_rel":        result.get("prob_rel"),
                "prob_name_A":     result.get("prob_name_A", "A"),
                "prob_name_B":     result.get("prob_name_B", "B"),
                "interpretation":  result.get("interpretation", "Probabilidad detectada."),
            }
            return {"action": "complete", "sc": sc, "messages": updated_messages}

        # ---- Modelos de Probabilidad (distribucion discreta) ----------------
        model = normalize_model_name(result.get("model", ""))
        if not is_implemented(model):
            disponibles = ", ".join(sorted(IMPLEMENTED_MODELS))
            return {
                "action": "error",
                "message": (f"El modelo '{model}' fue identificado pero aún no está "
                            f"implementado. Disponibles: {disponibles}."),
                "messages": updated_messages,
            }
        sc = {
            "mode":        "Modelos de Probabilidad",
            "model":       model,
            "params":      result.get("params", {}),
            "query_type":  result.get("query_type", "full_analysis"),
            "query_params": result.get("query_params", {}),
            "interpretation": result.get("interpretation", ""),
        }
        return {"action": "complete", "sc": sc, "messages": updated_messages}

    if result["status"] == "need_more_info":
        partial_msg = {"role": "assistant", "content": _encode_partial(result)}
        return {
            "action": "follow_up",
            "question": result.get("question", "¿Podés dar más detalles?"),
            "partial": result,
            "messages": updated_messages + [partial_msg],
        }

    return {
        "action": "error",
        "message": "No se pudo interpretar el problema. Intentá con más detalle.",
        "messages": updated_messages,
    }


def apply_sc_to_session(sc: dict, st_session) -> None:
    """
    Pre-carga datos del session config en session_state para cada modo.
    Llamar después de recibir action='complete'.
    """
    mode = sc.get("mode", "Modelos de Probabilidad")

    # Limpiar solución compuesta si el nuevo modo no es compuesto
    if mode != "Problema Compuesto":
        st_session.pop("compound_solution", None)

    # Problema Compuesto — guardar solución sin cambiar modo
    if mode == "Problema Compuesto":
        st_session["compound_solution"] = sc.get("compound_solution")
        return

    # Cambiar modo (pendiente — se aplica antes del widget en el próximo rerun)
    if mode in ("Datos Agrupados", "Probabilidad"):
        st_session["_pending_mode"] = mode

    # Datos Agrupados — pre-llenar tabla
    if mode == "Datos Agrupados" and sc.get("dp_intervals") and sc.get("dp_frequencies"):
        st_session["dp_df"] = pd.DataFrame({
            "Li": [a for a, b in sc["dp_intervals"]],
            "Ls": [b for a, b in sc["dp_intervals"]],
            "fai": sc["dp_frequencies"],
        })

    # Probabilidad — pre-llenar parámetros
    if mode == "Probabilidad":
        submode = sc.get("prob_submode", "Bayes / Probabilidad Total")
        st_session["prob_submode"] = submode

        if sc.get("bayes_labels") and sc.get("bayes_priors") and sc.get("bayes_likelihoods"):
            st_session["bayes_df"] = pd.DataFrame({
                "Hipotesis": sc["bayes_labels"],
                "P(Hi)":     sc["bayes_priors"],
                "P(E|Hi)":   sc["bayes_likelihoods"],
            })
        if sc.get("bayes_evidence"):
            st_session["prob_ev"] = sc["bayes_evidence"]
        if sc.get("prob_name_A"):
            st_session["prob_nameA"] = sc["prob_name_A"]
        if sc.get("prob_name_B"):
            st_session["prob_nameB"] = sc["prob_name_B"]

        # Construir multiselect y valores para el solver genérico
        known_sel = []
        _KEY_MAP = {
            "prob_pA": ("P(A)", "prob_pA"),
            "prob_pB": ("P(B)", "prob_pB"),
            "prob_pAB": ("P(A∩B)", "prob_pAB"),
            "prob_pAB_comp": ("P(A'∩B') — ninguno", "prob_pNone"),
        }
        for sc_key, (label, st_key) in _KEY_MAP.items():
            if sc.get(sc_key) is not None:
                known_sel.append(label)
                st_session[st_key] = float(sc[sc_key])
        if known_sel:
            st_session["prob_known_sel"] = known_sel


# ---------------------------------------------------------------------------
# Helpers para contexto multi-turno
# ---------------------------------------------------------------------------

def _encode_partial(partial: dict) -> str:
    model = partial.get("model") or ""
    params = partial.get("params") or {}
    parts = []
    if model:
        parts.append(f"modelo={model}")
    for k, v in params.items():
        parts.append(f"{k}={v}")
    return "__partial__:" + " ".join(parts)


def _build_combined_text(messages: list[dict], new_text: str) -> str:
    for msg in reversed(messages):
        if msg.get("role") == "assistant" and msg.get("content", "").startswith("__partial__:"):
            context = msg["content"].replace("__partial__:", "").strip()
            return f"{context} {new_text}"
    return new_text
