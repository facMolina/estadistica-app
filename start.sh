#!/usr/bin/env bash
# =====================================================================
#  Lanzador unico macOS/Linux: prepara Ollama y arranca Streamlit.
#  Uso: ./start.sh   (desde la carpeta ESTADISTICA)
# =====================================================================

set -e
cd "$(dirname "$0")/APP"

PY="${PYTHON:-python3}"

echo
echo "=== Preparando servicio local (invisible) ==="
if command -v ollama >/dev/null 2>&1; then
    # Arrancar ollama serve en background si no esta corriendo
    if ! curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
        echo "  iniciando ollama serve..."
        nohup ollama serve >/tmp/ollama.log 2>&1 &
        sleep 3
    fi
    # Pullear modelos si faltan
    if ! ollama list 2>/dev/null | grep -q "qwen2.5:7b-instruct"; then
        echo "  descargando qwen2.5:7b-instruct (una sola vez, ~4.7 GB)..."
        ollama pull qwen2.5:7b-instruct
    fi
    if ! ollama list 2>/dev/null | grep -q "nomic-embed-text"; then
        echo "  descargando nomic-embed-text..."
        ollama pull nomic-embed-text
    fi
else
    echo "  ollama no instalado — la app corre igual, solo Consultas Teoricas no funciona."
fi

echo
echo "=== Precargando modelo (primera respuesta mas rapida) ==="
curl -s -X POST http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:7b-instruct","prompt":"","stream":false,"keep_alive":"2h"}' \
  -o /dev/null -w "  warmup HTTP %{http_code} en %{time_total}s\n" 2>/dev/null || true

echo
echo "=== Abriendo la app en el navegador ==="
( sleep 4 && open http://localhost:8501 ) &

echo
echo "=== Iniciando Streamlit (Ctrl+C para apagar) ==="
"$PY" -m streamlit run app_streamlit.py --server.headless true --server.port 8501
