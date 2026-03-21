import os
import logging
import uuid
from werkzeug.utils import secure_filename
from config import Config


# ==================== ЛОГИРОВАНИЕ ====================
def setup_logging():
    """Настройка логирования"""
    log_format = '[%(asctime)s] %(levelname)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    log_file = os.path.join(Config.LOGS_DIR, 'app.log')

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def log_info(message):
    logging.info(message)


def log_error(message):
    logging.error(message)


def log_success(message):
    logging.info(f'Успех: {message}')


# ==================== РАБОТА С ФАЙЛАМИ ====================
def ensure_directories():
    """Создаёт необходимые папки, если их нет"""
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.LOGS_DIR, exist_ok=True)
    os.makedirs(Config.BACKUPS_DIR, exist_ok=True)


def get_file_extension(filename):
    """Возвращает расширение файла в нижнем регистре"""
    return os.path.splitext(filename)[1].lower()


def is_allowed_extension(filename):
    """Проверяет, разрешено ли расширение"""
    ext = get_file_extension(filename)
    return ext in Config.ALLOWED_EXTENSIONS


def is_valid_file_size(file_size):
    """Проверяет размер файла"""
    return 0 < file_size <= Config.MAX_CONTENT_LENGTH


def format_file_size(size_bytes):
    """Форматирует размер файла для отображения"""
    if size_bytes < 1024:
        return f'{size_bytes} B'
    elif size_bytes < 1024 * 1024:
        return f'{size_bytes / 1024:.2f} KB'
    else:
        return f'{size_bytes / (1024 * 1024):.2f} MB'


def generate_unique_filename(original_filename):
    """Генерирует уникальное имя файла"""
    ext = get_file_extension(original_filename)
    unique_id = str(uuid.uuid4())
    return f'{unique_id}{ext}'


def save_file(filename, file_content):
    """Сохраняет файл на диск"""
    try:
        original_name = secure_filename(filename)
        new_filename = generate_unique_filename(original_name)
        file_path = os.path.join(Config.UPLOAD_FOLDER, new_filename)

        with open(file_path, 'wb') as f:
            f.write(file_content)

        log_success(f'Файл сохранён: {new_filename} (оригинал: "{original_name}")')
        return True, new_filename
    except Exception as error:
        error_msg = f'Ошибка сохранения файла: {error}'
        log_error(error_msg)
        return False, error_msg


def delete_file(filename):
    """Удаляет файл с диска"""
    try:
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        log_error(f'Ошибка удаления файла: {e}')
        return False