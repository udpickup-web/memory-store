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
call .venv\Scripts\python tools\decrypt.py encrypted\memory\sample.txt.enc out_sample.txt --aad manifest:1.0
type out_sample.txt
