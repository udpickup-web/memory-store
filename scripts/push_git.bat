@echo off
REM scripts\push_git.bat — коммит и пуш encrypted/ + manifest.json
setlocal
cd /d %~dp0..
call scripts\load_env.bat
if not exist .git (
  echo [ERR] Git repo not initialized. Run once:
  echo    git init ^&^& git add . ^&^& git commit -m "init" ^&^& git branch -M main ^&^& git remote add origin https://github.com/<user>/<repo>.git
  exit /b 1
)
if not defined REPO_PATH set "REPO_PATH=%cd%"
call .venv\Scripts\python tools\push_git.py
endlocal
