"""UI para el modo 'Consultas Teóricas'.

Contrato de invisibilidad:
- No se muestra el stack técnico (Ollama, LLM, RAG, embeddings, fuentes).
- Si el servicio no responde, se muestra literal 'Respuesta no disponible
  momentáneamente.' sin explicación.
"""

from __future__ import annotations

import threading

import streamlit as st

from theory.answerer import answer


def _init_state():
    if "theory_history" not in st.session_state:
        st.session_state["theory_history"] = []
    if not st.session_state.get("_theory_warmed"):
        st.session_state["_theory_warmed"] = True
        threading.Thread(target=_warmup_silent, daemon=True).start()


def _warmup_silent():
    try:
        from llm.ollama_client import get_default_client
        get_default_client().warmup(also_embed=True)
    except Exception:
        pass


def render_theory_sidebar():
    _init_state()
    st.header("Consultas Teóricas")
    st.caption("Preguntá cualquier tema de estadística y recibí una respuesta con desarrollo en fórmulas.")
    if st.button("Nueva conversación", use_container_width=True):
        st.session_state["theory_history"] = []
        st.rerun()


def render_theory_main():
    _init_state()
    st.subheader("Consultas Teóricas")

    history = st.session_state["theory_history"]
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Escribí tu pregunta sobre teoría...")
    if question:
        history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("..."):
                ans = answer(question, history=history[:-1])
            st.markdown(ans.text)
        history.append({"role": "assistant", "content": ans.text})
        # Cortar historial a 12 turnos (6 idas y vueltas)
        if len(history) > 24:
            st.session_state["theory_history"] = history[-24:]
