@echo off
REM scripts\load_env.bat — безопасно загружает .env (KEY=VALUE)
setlocal EnableDelayedExpansion
cd /d %~dp0..
for /f "usebackq tokens=1* delims==" %%A in (`findstr /r "^[A-Za-z0-9_][A-Za-z0-9_]*=" ".env"`) do set "%%A=%%B"
endlocal & (
  for /f "usebackq tokens=1* delims==" %%A in (`findstr /r "^[A-Za-z0-9_][A-Za-z0-9_]*=" ".env"`) do set "%%A=%%B"
)
