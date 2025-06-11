# Структура проекта Ai_service2

## Корень проекта

Ai_service2/ │ ├── main.py # Основной файл FastAPI-сервера, обработка запросов, запуск потоков ├── worker.py # Обработка одной задачи, работа с файлами, запуск нейросети, формирование отчётов ├── tests.py # Скрипт для тестирования API сервера │ ├── storage/ # Временное хранилище загруженных файлов (по сессиям) │ └── <session_id>/audio.mp3 │ ├── results/ # Результаты обработки (по сессиям) │ └── <session_id>/ │ ├── audio.mp3 │ ├── transcript.txt │ ├── ai_result.json │ ├── reasoning.json │ └── summary.xlsx │ ├── metrics/ # Метаданные и шаблоны │ ├── prompt.txt # Шаблон промпта для нейросети │ └── variables.json # Переменные и метрики (очередь, обработанные файлы, настройки) │ ├── logs/ # Логи работы сервера │ ├── api_receive.log │ ├── analysis.log │ ├── errors.log │ └── system.log │ ├── testdata/ # Тестовые mp3-файлы для тестирования API │ └── test*.mp3 │ └── seversdk/ # Внутренняя библиотека (SDK) ├── __init__.py ├── logger_configure.py # Настройка и экспорт логгеров ├── load_metrics.py # Класс Metrics и функции для работы с метриками ├── neuro.py # pipe — интерфейс к Ollama/LLM └── utils.py # Валидация данных, сохранение в Excel и др. утилиты

Ai_service2/ ├── main.py ├── worker.py ├── tests.py ├── storage/ ├── results/ ├── metrics/ │ ├── prompt.txt │ └── variables.json ├── logs/ │ ├── api_receive.log │ ├── analysis.log │ ├── errors.log │ └── system.log ├── testdata/ └── seversdk/ ├── __init__.py ├── logger_configure.py ├── load_metrics.py ├── neuro.py └── utils.py



---

## Описание основных компонентов

- **main.py** — Запуск FastAPI, приём файлов и JSON, валидация, сохранение во `storage/`, передача задачи в обработку.
- **worker.py** — Получение промпта, вызов нейросети, создание папки в `results/`, копирование аудио, сохранение транскрипта, результатов, reasoning, формирование Excel-отчёта, логирование, обработка очереди.
- **tests.py** — Автоматизированная отправка тестовых запросов на сервер.
- **metrics/** — Хранение шаблонов и переменных для работы сервиса.
- **logs/** — Разделение логов по видам событий.
- **seversdk/** — SDK: логгеры, метрики, утилиты, интерфейс к нейросети.

---

## Логика работы

1. **main.py**  
   - Принимает запрос через `/sendHandle/`, валидирует, сохраняет данные и файл.
   - Передаёт задачу в обработку через функцию `handler`.

2. **handler**  
   - Обновляет метрики.
   - Если потоков меньше лимита — запускает `worker` в новом потоке.
   - Иначе — добавляет задачу в очередь.

3. **worker.py**  
   - Читает промпт из `metrics/prompt.txt`, подставляет текст.
   - Отправляет промпт в нейросеть через `pipe`.
   - Создаёт папку в `results/` для сессии.
   - Копирует аудио, сохраняет транскрипт, результат ИИ, reasoning, формирует Excel-отчёт.
   - Логирует результат.
   - Если есть задачи в очереди — берёт следующую и запускает себя рекурсивно.

4. **seversdk/**  
   - Логгеры для разных типов событий.
   - Метрики: очередь, обработанные файлы, лимиты потоков.
   - Валидация данных, работа с Excel.
   - Интерфейс к нейросети (Ollama).

---

## Пример структуры папок и файлов

Ai_service2/ ├── main.py ├── worker.py ├── tests.py ├── storage/ ├── results/ ├── metrics/ │ ├── prompt.txt │ └── variables.json ├── logs/ │ ├── api_receive.log │ ├── analysis.log │ ├── errors.log │ └── system.log ├── testdata/ └── seversdk/ ├── __init__.py ├── logger_configure.py ├── load_metrics.py ├── neuro.py └── utils.py

