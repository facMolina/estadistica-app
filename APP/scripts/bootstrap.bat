@echo off
REM Bootstrap Sprint v2 — prepara el entorno local para la app.
REM
REM Silencioso: si algo falla, continúa. La app sigue funcionando aun sin
REM servicio local (parser regex + todos los modos existentes).

set LOG_DIR=%~dp0..\logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set LOG=%LOG_DIR%\bootstrap.log

echo [%date% %time%] bootstrap start >> "%LOG%"

REM Detecta si el servicio local está instalado. Si no, salir silencioso.
where ollama >nul 2>&1
if errorlevel 1 (
    echo [%date% %time%] ollama no instalado - skip >> "%LOG%"
    goto :end
)

REM Verificar modelos. Si no están, los descarga en background.
ollama list >> "%LOG%" 2>&1
ollama list | findstr /I "qwen2.5:14b-instruct" >nul
if errorlevel 1 (
    echo [%date% %time%] pulling qwen2.5:14b-instruct >> "%LOG%"
    ollama pull qwen2.5:14b-instruct >> "%LOG%" 2>&1
)

ollama list | findstr /I "nomic-embed-text" >nul
if errorlevel 1 (
    echo [%date% %time%] pulling nomic-embed-text >> "%LOG%"
    ollama pull nomic-embed-text >> "%LOG%" 2>&1
)

REM Smoke test
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [%date% %time%] servicio no responde - starting serve en background >> "%LOG%"
    start /b ollama serve >> "%LOG%" 2>&1
)

:end
echo [%date% %time%] bootstrap done >> "%LOG%"
exit /b 0
