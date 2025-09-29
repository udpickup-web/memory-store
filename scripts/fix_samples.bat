@echo off
setlocal
cd /d %~dp0..
REM Пересоздаём демонстрационные JSONL в UTF-8 через PowerShell
powershell -NoProfile -Command "$p='out/plain'; New-Item -ItemType Directory -Force -Path $p | Out-Null; Set-Content -Path (Join-Path $p 'memory_2025-09-29_demo.jsonl') -Value '{\"id\":\"mem.rule.2025-09-29.selcheck\",\"op\":\"upsert\",\"text\":\"Селективная сверка на КАЖДОЕ сообщение\",\"tags\":[\"Core\",\"Workflow\"],\"priority\":\"HIGH\"}' -Encoding UTF8; Set-Content -Path (Join-Path $p 'instr_2025-09-29_demo.jsonl') -Value '{\"id\":\"instr.fix.2025-09-29.no-want\",\"op\":\"confirm\",\"text\":\"Запрет формулировок «хочешь/хотите».\",\"status\":\"active\"}' -Encoding UTF8"
echo [OK] samples recreated in UTF-8.
