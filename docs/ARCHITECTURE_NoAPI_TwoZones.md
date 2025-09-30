# Архитектура ClickerBot (No API, Two Zones)

## Назначение
Windows-приложение с UI и кликер-ботом. Все действия через клики в Firefox.
Экран 4K (3840x2160) поделен:
- Q1 (0..960) — Router (Firefox)
- Q2 (960..1920) — Operational Chat (OCR)
- Q3+Q4 (1920..3840) — Operational Area (резерв)

Бот работает с Firefox только в Q1.

## Потоки
1. Пользователь → Router: ввод сообщения в UI → вставка и клик Send в Q1.
2. Router-OCR: каждые N сек скан answer-области, ищем «Для пользователя».
3. Задачи/результаты через файлы task/exec_cmd/notice в репозитории.

## Компоненты
- UI (PySide6)
- Clicker Core
- Router Worker
- Coords Profiles
- (будущее) Ops Executor
- Git Integration
- Virtual Desktop Metadata
- Logging
