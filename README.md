# Estadística UADE — App

Resuelve ejercicios de Estadística General (Dopazo, UADE) con paso a paso,
gráficos, tabla de distribución y un modo de Consultas Teóricas con LaTeX.

---

## Arrancar la app (uso diario)

### 🪟 Windows

**Doble click en `start.bat`.**

Se abre una consola negra, prepara todo y el navegador abre solo en
`http://localhost:8501`. Dejá la consola abierta mientras usás la app.
Para apagar, cerrás la consola.

### 🍎 macOS / Linux

Desde Terminal, parada en la carpeta `ESTADISTICA`:

```bash
./start.sh
```

El script prepara Ollama, precarga el modelo, abre el navegador en
`http://localhost:8501` y deja Streamlit corriendo. Para apagar, `Ctrl+C`.

Si es la primera vez, hacelo ejecutable:

```bash
chmod +x start.sh
```

---

## Modos disponibles

| Modo | Para qué |
|------|----------|
| **Modelos de Probabilidad** | Binomial, Poisson, Pascal, Hipergeométrico, Hiper-Pascal, Multinomial, continuos (Normal, Gamma, Weibull…). |
| **Datos Agrupados** | Tabla de frecuencias, media, varianza, CV, mediana, fractil, histograma, ogiva. |
| **Probabilidad** | Eventos, probabilidad condicional, Bayes / probabilidad total. |
| **TCL / Suma de VA** | Suma de variables independientes + aproximación normal. |
| **Consultas Teóricas** | Preguntas abiertas de teoría con respuesta en LaTeX. |

En todos los modos hay un **Interpretar problema** en el sidebar — pegás el
enunciado en lenguaje natural y la app detecta el modo y pre-llena los campos.

---

## Instalación desde cero (una sola vez)

### 🪟 Windows

```bat
:: 1) Python 3.9+ (probado con 3.14). Descargar desde python.org e instalar.
::    IMPORTANTE: tildar "Add Python to PATH" durante la instalacion.

:: 2) Dependencias de la app
cd C:\Users\PC\Desktop\ESTADISTICA\APP
C:\Python314\python -m pip install -r requirements.txt

:: 3) Ollama (opcional pero recomendado — habilita Consultas Teoricas
::    y el fallback inteligente del interprete).
::    Descargar desde https://ollama.com/download/windows
ollama pull qwen2.5:7b-instruct
ollama pull nomic-embed-text
```

### 🍎 macOS

```bash
# 1) Python 3.9+ (con Homebrew, recomendado)
brew install python@3.12

# 2) Dependencias de la app
cd /ruta/a/ESTADISTICA/APP
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate

# 3) Ollama (opcional pero recomendado)
brew install ollama
ollama pull qwen2.5:7b-instruct
ollama pull nomic-embed-text
```

> En macOS, `start.sh` usa `python3` por default. Si querés forzar otra
> versión: `PYTHON=/ruta/a/python ./start.sh`.

A partir de acá, siempre doble click en `start.bat` (Windows) o
`./start.sh` (macOS).

---

## Resolver problemas

| Síntoma | Solución |
|---------|----------|
| El navegador muestra "sitio no disponible" | La consola de `start.bat` / `start.sh` tiene que seguir abierta. Si la cerraste, volvé a lanzar. |
| Consultas Teóricas responde "Respuesta no disponible momentáneamente" | Ollama no está corriendo. Windows: abrí la app de Ollama. macOS: `ollama serve` en otra terminal. Después recargá la página. |
| Consultas Teóricas tarda mucho (>2 min) | Normal la primera pregunta del día mientras carga el modelo. Las siguientes son más rápidas. |
| Puerto 8501 ocupado | Hay otra instancia abierta. Cerrá todas las consolas de Streamlit antes de relanzar. |
| `ModuleNotFoundError` | Faltan dependencias. Reinstalá: `pip install -r APP/requirements.txt` (macOS con venv activado, o sin venv en Windows). |
| macOS: `./start.sh: Permission denied` | Falta el bit de ejecución. `chmod +x start.sh`. |

---

## Modo CLI (opcional)

Si querés usar Claude API en vez de la UI web:

```bash
cd ESTADISTICA/APP
python main.py          # macOS / Linux
C:\Python314\python main.py   # Windows
```

Requiere `ANTHROPIC_API_KEY` en `APP/.env`.

---

## Para devs

- `APP/CLAUDE.md` — arquitectura, cómo extender modelos, tests.
- `estadistica_v2.md` — análisis del último sprint (fallback local + RAG).
- `APP/tests/` — suite de regresión (`python tests/test_regression_v2.py`).
- `APP/tests/MANUAL_REGRESSION_CHECKLIST.md` — 20 flujos manuales de UI.
