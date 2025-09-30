@echo off
setlocal
cd /d %~dp0
IF NOT EXIST .venv (
  py -3.11 -m venv .venv
)
call .venv\Scripts\pip install -r requirements.txt
echo NOTE: Make sure Tesseract OCR is installed and in PATH (tesseract.exe).
call .venv\Scripts\python app\main.py
