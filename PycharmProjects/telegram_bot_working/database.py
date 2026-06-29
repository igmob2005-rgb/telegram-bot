import sqlite3
import os
from Telegram_API.config import DB_PATH
from datetime import datetime
from typing import Optional, List, Tuple  # Импортируем список для возврата данных


# --- Инициализация Базы Данных (Обновление) ---
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Таблица Users, Orders (Остаются прежними)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        from_where TEXT,
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        role TEXT DEFAULT 'client',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_where TEXT,
            user_id INTEGER NOT NULL,
            service_type TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'draft',
            deadline DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. НОВЫЙ: Таблица для хранения ВСЕХ выбранных деталей заказа (Исторический лог выбора)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            category TEXT NOT NULL,      -- Общая категория выбора (e.g., 'COLOR', 'LOCATION', 'COMPONENT')
            selection_key TEXT NOT NULL, -- Ключ выбора из UI/Логики (e.g., 'field', 'cpp2', 'reydovo')
            human_label TEXT NOT NULL,    -- Красивое имя для вывода пользователю (e.g., 'Полевая расцветка')
            value TEXT,                   -- Дополнительное значение (например, ФИО или код)
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message_text TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Таблица Admins (Остается прежней)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        authorized_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# --- Функции добавления/извлечения данных (Обновление и Добавление) ---

def add_user(user_id: int, username: str | None, first_name: str, role: str):
    # ... (Остается без изменений)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
    """, (user_id,
          username or "",
          first_name or ""))
    conn.commit()
    conn.close()


def user_exists(user_id: int) -> bool:
    # ... (Остается без изменений)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def save_logs(user_id: int, message_text: str):
    # ... (Остается без изменений)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO logs (user_id, message_text)
        VALUES (?, ?)
    """, (user_id,
          message_text))
    conn.commit()
    conn.close()


def is_admin(user_id: int) -> bool:
    # ... (Остается без изменений)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM admins WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result is not None


def remove_admin(user_id: int):
    # ... (Остается без изменений)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def get_last_logs(limit=10):
    # ... (Остается без изменений)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def create_draft_order(user_id: int, username: str, service_type: str) -> int:
    """Создает черновик заказа и возвращает его ID."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders (user_id, service_type, status)
            VALUES (?, ?, 'draft')
            """,
                    (user_id, service_type)
                    )
        return cur.lastrowid


def add_order_detail(order_id: int, category: str, key: str, label: str, value: Optional[str] = None):
    """
    НОВЫЙ ФУНКЦИОНАЛ: Записывает ОДИН выбранный пункт в лог деталей заказа.
    Этот вызов должен происходить при каждом клике пользователя по кнопке меню/callback.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO order_details (order_id, category, selection_key, human_label, value)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, category, key, label, value))
            conn.commit()
            return True  # Успешное добавление детализации
        except Exception as e:
            print(f"Ошибка при добавлении детали в заказ {order_id}: {e}")
            return False


def create_order(from_where: str, user_id: int, username: str, service_type: str, description: Optional[str],
                 status: str, deadline: Optional):
    """
    Финальный этап. Используется для закрытия заказа и сохранения всех деталей.
    Поскольку все детали уже записаны в order_details, здесь только финальная запись.
    """
#    for text, user_id in list;



    if isinstance(deadline, datetime):
        deadline = deadline.isoformat(sep=' ', timespec='seconds')

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Если мы просто завершаем заказ, нам достаточно перезаписать основную запись (order)
    cur.execute("""
    INSERT INTO orders (from_where, user_id, service_type, description, status, deadline)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (from_where,
          user_id,
          service_type,
          description,
          status,
          deadline))
    conn.commit()
    conn.close()


def get_full_order_details(order_id: int) -> Tuple[Optional[dict], List[dict]]:
    """
    НОВЫЙ ФУНКЦИОНАЛ: Получает полный набор данных о заказе.
    Возвращает словарь с общей информацией (из 'orders') и список всех деталей (из 'order_details').
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Получаем общую информацию о заказе
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    main_data = cur.fetchone()

    # 2. Получаем все выбранные детали по order_id
    cur.execute("""
        SELECT category, selection_key, human_label, value, timestamp 
        FROM order_details WHERE order_id = ? ORDER BY timestamp ASC
    """, (order_id,))
    detail_rows = cur.fetchall()
    conn.close()

    # Преобразование в удобные структуры для Python
    full_summary = {
        "general": main_data[1] if main_data else "N/A",  # user_id
        "service_type": main_data[3] if main_data else "Н/Д",
        "status": main_data[4] if main_data else "draft",
        "description": main_data[2] if main_data and main_data[2] else None,
        # ... можно добавить другие поля из orders: 0=id, 1=from_where, 3=service_type и т.д.
    }

    detailed_list = []
    for row in detail_rows:
        detailed_list.append({
            "category": row[0],
            "selection_key": row[1],
            "human_label": row[2],
            "value": row[3] if row[3] else "Нет данных",
            "timestamp": row[4]
        })

    return full_summary, detailed_list


def get_orders():
    # ... (Остается без изменений)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    conn.close()
    return rows


def update_order_field(order_id: int, field: str, value):
    # ... (Остается без изменений)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders SET {} = ? WHERE id = ?
        """.format(field), (value, order_id))

