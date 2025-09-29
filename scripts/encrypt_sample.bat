@echo off
setlocal
cd /d %~dp0..
if not exist .venv\Scripts\python.exe (
  echo [ERR] Run scripts\setup_venv.bat first
  exit /b 1
)
if not exist .env (
  echo [ERR] Create .env from .env.example and set ENCRYPTION_KEY
  exit /b 1
)
echo test>sample.txt
call .venv\Scripts\python tools\encrypt.py sample.txt encrypted\memory\sample.txt.enc --aad manifest:1.0
