@echo off
setlocal
cd /d %~dp0..
call .venv\Scripts\python tools\gen_purge_request.py
type out\PURGE_REQUEST.txt
