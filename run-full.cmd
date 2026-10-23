@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Missing .venv. Copy this project beside your existing .venv.
  pause
  exit /b 1
)
.venv\Scripts\python.exe run.py full
pause
