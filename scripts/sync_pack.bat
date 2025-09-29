@echo off
setlocal
cd /d %~dp0..
REM Загружаем только строки формата KEY=VALUE, игнорируем комментарии/пустые строки
for /f "usebackq tokens=1* delims==" %%A in (`findstr /r "^[A-Za-z0-9_][A-Za-z0-9_]*=" ".env"`) do set "%%A=%%B"
call .venv\Scripts\python tools\sync_pack.py
if errorlevel 1 ( echo [ERR] sync_pack failed & exit /b 1 )
echo [OK] sync_pack done.
