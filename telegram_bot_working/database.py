import aiosqlite
import os
from Telegram_API.config import DB_PATH
from datetime import datetime
from typing import Optional, List, Tuple, Dict, Any, Union    # Импортируем список для возврата данных


class DatabaseManager:
    """
    Асинхронный Репозиторий данных для работы с SQLite.
    Отвечает ТОЛЬКО за взаимодействие с БД. Никакой бизнес-логики!
    """

    def __init__(self):
        # Просто инициализируем класс, не подключаемся к БД здесь.
        pass

    async def initialize_db(self):
        """
        ВАЖНО: Создает все необходимые таблицы в асинхронном режиме.
        Должен быть вызван ПЕРВЫМ (await db_manager.initialize_db()) при запуске бота.
        """
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        print("⚙️ Database schema initialization started...")

        try:
            # async with обеспечивает, что соединение будет закрыто автоматически, даже если ошибка произойдет
            async with aiosqlite.connect(DB_PATH) as db:
                # 1. Users
                await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    role TEXT DEFAULT 'client'
                    )
                """)
                # 2. Orders
                await db.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_where TEXT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    service_type TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'draft',
                    deadline DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # 3. order_details (Лог выбора)
                await db.execute("""
                CREATE TABLE IF NOT EXISTS order_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    selection_key TEXT NOT NULL,
                    human_label TEXT NOT NULL,
                    value TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
                )
                """)

                # 4. Logs
                await db.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    message_text TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                await db.commit()

        except aiosqlite.Error as e:
            print(f"🔴 FATAL ASYNC DB ERROR during initialization: {e}")
            exit()

    # ==============================
    # 👤 Управление прайслистом (Pricelist CRUD)
    # ==============================


        async with aiosqlite.connect(DB_PATH) as db:
            try:
                # Использование транзакции для атомарной и быстрой вставки данных
                await db.execute("BEGIN TRANSACTION;")

                await db.commit()
                print("[✅] Price list population complete! Successfully synchronized catalog.")

            except Exception as e:
                await db.rollback()  # Откатываем все изменения при любой ошибке
                print(f"[❌] CRITICAL ERROR during price list population: {e}")

    # ==============================
    # 👤 Управление Пользователями (User Profile CRUD)
    # ==============================

    async def save_logs(self, user_id: int, message_text: Optional[str]):
        """Сохраняет лог сообщения пользователя."""
        query = """
        INSERT INTO logs (user_id, message_text)
        VALUES (?, ?)
        """
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(query, (user_id, message_text))
            await db.commit()

    async def is_admin(self, user_id: int) -> bool:
        """Проверяет, является ли пользователь администратором."""
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT 1 FROM admins WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            return row is not None

    async def add_user(self, user_id: int, username: Optional[str], first_name: str, role: str):
        """Добавляет или обновляет данные пользователя."""
        query = """
        INSERT INTO users (user_id, username, first_name, role)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            role = excluded.role;
        """
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(query, (user_id, username or "", first_name, role))
            await db.commit()

    async def user_exists(self, user_id: int) -> bool:
        """Проверяет существование пользователя по ID."""
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            return row is not None

    # ... [Здесь должны быть другие методы для админов, логов и т.д.] ...


    # ==============================
    # 🛒 Управление Заказами (Core Logic)
    # ==============================

    async def create_draft_order(self, user_id: int, service_type: str, status: str, from_where: str, username: str) -> int:
        """Создает черновик заказа и возвращает его ID."""
        query = """
            INSERT INTO orders (user_id, service_type, status, from_where, username)
            VALUES (?, ?, 'draft', ?, ?)
        """
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(query, (user_id, service_type, from_where, username))
            await db.commit()
            return cursor.lastrowid

    async def add_order_detail(self, order_id: int, category: str, key: str, label: str, value: Optional[str] = None) -> bool:
        """
        Записывает один выбранный пункт в лог деталей заказа (КЛЮЧЕВАЯ ФУНКЦИЯ).
        """
        query = """
        INSERT INTO order_details (order_id, category, selection_key, human_label, value)
        VALUES (?, ?, ?, ?, ?)
        """
        async with aiosqlite.connect(DB_PATH) as db:
            try:
                await db.execute(query, (order_id, category, key, label, value))
                await db.commit()
                return True
            except Exception as e:
                print(f"ASync Error adding detail in order {order_id}: {e}")
                return False

    async def finalize_order(self, from_where: str, user_id: int, service_type: str, description: Optional[str],
                            status: str, deadline: Optional[Union[datetime, str]]):
        """Финальный этап: сохраняет или обновляет основную запись заказа."""
        if isinstance(deadline, datetime):
            deadline_str = deadline.isoformat(sep=' ', timespec='seconds')
        else:
            deadline_str = str(deadline) if deadline else None

        query = """
            INSERT INTO orders (from_where, user_id, service_type, description, status, deadline)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(query, (
                from_where,
                user_id,
                service_type,
                description,
                status,
                deadline_str
            ))
            await db.commit()


    async def get_full_order_details(self, order_id: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Получает полный набор данных о заказе."""
        async with aiosqlite.connect(DB_PATH) as db:
            # 1. Получаем общую информацию о заказе
            cursor = await db.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            main_row = await cursor.fetchone()

            # 2. Получаем все выбранные детали
            cursor = await db.execute("""
                SELECT category, selection_key, human_label, value, timestamp 
                FROM order_details WHERE order_id = ? ORDER BY timestamp ASC
            """, (order_id,))
            detail_rows = await cursor.fetchall()

        # Обработка данных: ручная сборка словарей из кортежей.
        full_summary: Dict[str, Any] = {}
        if main_row:
             # Предполагая порядок колонок: 0=id, 1=from_where, 2=user_id и т.д.
            full_summary = {
                "id": main_row[0],
                "from_where": main_row[1] if main_row[1] else "N/A",
                "user_id": main_row[2] if main_row[2] else None,
                "service_type": main_row[3] if main_row[3] else "Н/Д",
                "status": main_row[4] if main_row[4] else "draft",
            }

        detailed_list: List[Dict[str, Any]] = []
        for row in detail_rows:
            detailed_list.append({
                "category": row[0],
                "selection_key": row[1],
                "human_label": row[2],
                "value": row[3] if row[3] else "Нет данных",
                "timestamp": row[4]
            })

        return full_summary, detailed_list