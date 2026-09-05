@echo off
REM TurabIQ Quick Start Script (Windows)
REM Starts mock backend + prints frontend start instructions

setlocal enabledelayedexpansion

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         🧪 TurabIQ Mock Backend Launcher 🧪                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if mock_backend.py exists
if not exist "backend\mock_backend.py" (
    echo ❌ Error: mock_backend.py not found!
    echo    Make sure you run this from the TurabIQ project root:
    echo    cd \path\to\TurabIQ
    echo    start_mock.bat
    pause
    exit /b 1
)

echo 📦 Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo    Installing fastapi and uvicorn...
    pip install fastapi uvicorn --quiet
)

echo ✓ Dependencies ready
echo.

echo 🚀 Starting Mock Backend...
echo    WebSocket: ws://localhost:8000/ws
echo    REST API:  http://localhost:8000
echo    Docs:      http://localhost:8000/docs
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

cd backend
python mock_backend.py

echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
echo ✓ Mock backend stopped
echo.
pause
