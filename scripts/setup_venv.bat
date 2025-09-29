@echo off
setlocal
cd /d %~dp0..
python -m venv .venv
if errorlevel 1 ( echo [ERR] venv failed & exit /b 1 )
call .venv\Scripts\pip install --upgrade pip
call .venv\Scripts\pip install -r requirements.txt
echo [OK] ENV READY.
