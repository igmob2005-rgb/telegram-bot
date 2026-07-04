import os
import hashlib
from pathlib import Path

# Токен Бота: Получаем из окружения или используем заглушку для разработки.
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Пароль Администратора и его хеш 
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

# ============================
# Пути к данным (Database Paths)
# ============================

# Используем Path для кроссплатформенного пути.
# Убедитесь, что эта папка существует при запуске бота!
BASE_DIR = Path(__file__).resolve().parent

# Определяем путь к БД в папке 'database'
DB_PATH = BASE_DIR / "database" / "bot_data.db"


# ============================
# 💡 Проверка и валидация конфигурации
# ============================

def validate_config():
    """Проверяет критически важные переменные окружения перед запуском."""
    if not BOT_TOKEN:
        raise ValueError("FATAL ERROR: BOT_TOKEN не установлен. Установите его через переменную окружения.")
    print("✅ Конфигурация успешно загружена.")

# Вызываем проверку при импорте, чтобы сразу знать, готовы ли мы к запуску.
try:
    validate_config()
except ValueError as e:
    print(f"🚨 КОНФИГУРАЦИЯ НЕЗАВЕРШЕНА: {e}")
