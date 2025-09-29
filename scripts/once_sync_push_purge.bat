@echo off
REM scripts\once_sync_push_purge.bat — единичный цикл SYNC -> PUSH -> PURGE
setlocal
cd /d %~dp0..
call scripts\load_env.bat
echo [1/3] SYNC_PACK...
call scripts\sync_pack.bat || exit /b 1
echo [2/3] PUSH_GIT...
call scripts\push_git.bat
echo [3/3] GEN_PURGE_REQUEST...
call scripts\gen_purge_request.bat
echo.
echo --- COPY THIS TO CHAT ---
type out\PURGE_REQUEST.txt
echo --- END ---
endlocal
