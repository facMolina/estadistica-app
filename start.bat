@echo off
REM =====================================================================
REM  Lanzador unico: prepara Ollama (silencioso) y arranca Streamlit.
REM  Doble click sobre este archivo — listo.
REM =====================================================================

cd /d "%~dp0APP"

echo.
echo === Preparando servicio local (invisible) ===
call scripts\bootstrap.bat

echo.
echo === Precargando modelo (asi la primera respuesta sale rapida) ===
curl -s -X POST http://127.0.0.1:11434/api/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"model\":\"qwen2.5:7b-instruct\",\"prompt\":\"\",\"stream\":false,\"keep_alive\":\"2h\"}" ^
  -o nul -w "  warmup HTTP %%{http_code} en %%{time_total}s\n" 2>nul

echo.
echo === Abriendo la app en el navegador ===
start "" http://localhost:8501

echo.
echo === Iniciando Streamlit (dejar esta ventana abierta) ===
C:\Python314\python -m streamlit run app_streamlit.py --server.headless true --server.port 8501

pause
