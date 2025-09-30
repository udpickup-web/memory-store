# ClickerBot (No API, Two Zones) — Skeleton

- Без API: всё через клики/ввод/скриншоты/ОCR.
- Экран 4K (3840x2160). Раскладка:
  - Q1 (0..960 px): **Firefox (Router)** — чат первого роутера. Бот тут ТОЛЬКО отправляет сообщения и читает ответы (OCR).
  - Q2 (960..1920 px): **Operational Chat zone** — зона чтения (OCR) статусов вторичного уровня (не Firefox).
  - Q3+Q4 (1920..3840 px): **Operational Area** — пустая область (резерв), бот может в неё кликать для операций.

Важно: кликер строго использует жёсткие координаты для взаимодействия с Firefox (Router).

## Запуск (Windows)
1) Установи Tesseract OCR (добавь `tesseract.exe` в PATH).
2) Распакуй в `C:\MotionPC\ClickerBot_NoAPI_TwoZones`.
3) В консоли:
   ```cmd
   cd C:\MotionPC\ClickerBot_NoAPI_TwoZones
   run.bat
   ```

## Настройка координат
Редактируй `coords/router_4k_q1.json` (input/send/answer). В интерфейсе есть кнопка логов для проверки.

