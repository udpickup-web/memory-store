@echo off
REM scripts\loop_sync_push_purge.bat — бесконечный цикл каждые SYNC_INTERVAL_MIN минут
setlocal
cd /d %~dp0..
call scripts\load_env.bat
if not defined SYNC_INTERVAL_MIN set SYNC_INTERVAL_MIN=120
:loop
echo [%date% %time%] RUN once_sync_push_purge
call scripts\once_sync_push_purge.bat
echo [%date% %time%] SLEEP %SYNC_INTERVAL_MIN% min...
timeout /t %SYNC_INTERVAL_MIN% /nobreak >nul
goto loop
