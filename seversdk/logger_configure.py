import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str,
                 log_file: str = 'app.log',
                 level: int = logging.INFO,
                 max_bytes: int = 10*1024*1024,
                 backup_count: int = 5) -> logging.Logger:
    """
    Создаёт и возвращает настроенный логгер.
    - name: имя логгера (обычно __name__)
    - log_file: путь к файлу лога
    - level: минимальный уровень логов
    - max_bytes + backup_count: параметры ротации файла
    """
    os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)

    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Файловый обработчик с ротацией
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger

loggerApiReceive = setup_logger("api-receive", log_file='logs/api_receive.log', level=logging.DEBUG)
loggerAnalysis = setup_logger("analyzes", log_file='logs/analysis.log', level=logging.DEBUG)
loggerErrors = setup_logger("errors", log_file='logs/errors.log', level=logging.DEBUG)
loggerSystem = setup_logger("system", log_file='logs/system.log', level=logging.DEBUG)