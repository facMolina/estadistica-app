#!/usr/bin/env python3
"""
Calculadora de Estadística General — Fase 1: CLI con Claude API.

Uso:
    python main.py              # Modo interactivo: describe el problema
    python main.py --streamlit  # Abre Streamlit directamente sin CLI
"""

import os
import sys
import subprocess


def _load_env():
    """Carga .env si existe. Retorna True si la API key está disponible."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def _launch_streamlit():
    """Lanza app_streamlit.py en segundo plano."""
    app_path = os.path.join(os.path.dirname(__file__), "app_streamlit.py")
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", app_path,
         "--server.headless", "false"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("\n  Streamlit abierto → http://localhost:8501")
    print("  (Si no se abre automáticamente, abrí esa URL en el navegador)\n")


def main():
    # Modo --streamlit: saltear CLI y abrir Streamlit directo
    if "--streamlit" in sys.argv:
        _launch_streamlit()
        return

    # Verificar API key
    if not _load_env():
        print("\n  ERROR: ANTHROPIC_API_KEY no configurada.")
        print("  Crear archivo .env en APP/ con:")
        print("    ANTHROPIC_API_KEY=sk-ant-api03-...")
        print("\n  O ejecutar con --streamlit para abrir la app sin la CLI.")
        sys.exit(1)

    # Imports aquí para que _load_env() ya haya corrido antes
    from interpreter.problem_parser import ProblemParser

    print("\n" + "=" * 60)
    print("  CALCULADORA DE ESTADÍSTICA GENERAL — UADE")
    print("  Ing. Sergio Anibal Dopazo")
    print("=" * 60)
    print()
    print("  Describí tu problema en texto libre y la app identifica")
    print("  el modelo, extrae los parámetros y abre Streamlit.")
    print()
    print("  Ejemplos:")
    print('    "Se lanza una moneda 15 veces. P(exactamente 4 caras)."')
    print('    "Llegan 3 autos por minuto en promedio. P(>= 5 en 2 min)."')
    print('    "Binomial n=12, p=0.45, calcular F(4)."')
    print()
    print("  Escribí 'salir' para terminar.")
    print()

    parser = ProblemParser()

    while True:
        try:
            user_input = input("  Tu problema: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Hasta luego.")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in ("salir", "exit", "q", "quit"):
            print("\n  Hasta luego.")
            sys.exit(0)

        print("\n  Interpretando con Claude...")

        result = parser.parse(user_input)

        if result is None:
            print("\n  Operación cancelada.")
            # Permitir reintentar
            retry = input("\n  ¿Querés intentar con otro problema? (S/n): ").strip().lower()
            if retry in ("n", "no"):
                sys.exit(0)
            # Reiniciar parser para nueva conversación
            parser = ProblemParser()
            print()
            continue

        confirmed = parser.confirm_and_write_config(result)

        if confirmed:
            _launch_streamlit()
            sys.exit(0)
        else:
            # Permitir corregir
            retry = input("\n  ¿Querés intentar con otro problema? (S/n): ").strip().lower()
            if retry in ("n", "no"):
                sys.exit(0)
            parser = ProblemParser()
            print()


if __name__ == "__main__":
    main()
