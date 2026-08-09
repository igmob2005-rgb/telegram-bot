import aiosqlite
import os
from datetime import datetime
from typing import Optional, List, Tuple, Dict, Any, Union
from Telegram_API.config import Pricelist_PATH

class PricelistManager:
    """
    Асинхронный Репозиторий данных для работы с SQLite.
    Отвечает ТОЛЬКО за взаимодействие с БД. Никакой бизнес-логики!
    """
    def __int__(self):
        pass
    async def initialize_pricelist_db(self):
        os.makedirs(os.path.dirname(Pricelist_PATH), exist_ok=True)
        print("⚙️ Pricelist schema initialization started...")
        try:
            # async with обеспечивает, что соединение будет закрыто автоматически, даже если ошибка произойдет
            async with aiosqlite.connect(Pricelist_PATH) as db:
                # 1. Pricelist
                await db.execute("""
                CREATE TABLE IF NOT EXISTS COMPLEX (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    service_key TEXT,  
                    usluga TEXT,
                    color TEXT DEFAULT 'green',
                    category_key TEXT NOT NULL,
                    detail_key TEXT NOT NULL,
                    price REAL DEFAULT 0.0,
                    is_active BOOL DEFAULT TRUE,
                    amount INTEGER DEFAULT 1,
                    description TEXT,
                    petlitsa_type TEXT OPTIONAL,
                    complex_type TEXT OPTIONAL
                    )
                """)
                await db.execute("""
                CREATE TABLE IF NOT EXISTS PETLICY (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_key TEXT,
                    usluga TEXT,
                    color TEXT DEFAULT 'green',
                    category_key TEXT NOT NULL,
                    detail_key TEXT NOT NULL,
                    price REAL DEFAULT 0.0,
                    is_active BOOL DEFAULT TRUE,
                    amount INTEGER DEFAULT 1,
                    description TEXT,
                    petlitsa_type TEXT OPTIONAL,
                    complex_type TEXT OPTIONAL
                    )
                """)
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS OTHER (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        service_key TEXT,
                        usluga TEXT,
                        color TEXT DEFAULT 'green',
                        category_key TEXT NOT NULL,
                        detail_key TEXT NOT NULL,
                        price REAL DEFAULT 0.0,
                        is_active BOOL DEFAULT TRUE,
                        amount INTEGER DEFAULT 1,
                        description TEXT,
                        petlitsa_type TEXT OPTIONAL,
                        complex_type TEXT OPTIONAL
                        )
                    """)

                await db.commit()
        except aiosqlite.Error as e:
            print(f"🔴 FATAL ASYNC DB ERROR during initialization: {e}")

    # ==============================
    # 👤 Управление прайслистом (Pricelist CRUD)
    # ==============================

    async def populate_initial_data(self):
        """
        *** СПЕЦИАЛЬНАЯ ФУНКЦИЯ ***
        Заполняет таблицу pricelist базовыми данными и ценами.
        Должна запускаться ОДИН РАЗ при старте бота.
        """
        print("\n[📚] Attempting to populate price list...")

        # 1. Структура данных: Список кортежей, где каждый кортеж - это одна запись.
        # Порядок в кортеже должен строго соответствовать порядку колонок в таблице!
        data_complex = [
            # (service_key, category_key, detail_key, color, price, is_active, description, amount, petlitsa_type, complex_type)

            # --- ОСНОВНЫЕ УСЛУГИ ПО ПОЛКУ (BASE SERVICE) ---
            ('complex', 'SERVICE', 'base', 'green', 2000.0, True, 1, "Комплект шевронов зелёный", None, 'Polk'),
            ('complex', 'SERVICE', 'base', 'multicolor', 2000.0, True, 1, "Комплект шевронов цветная", None, 'Polk'),
            ('fio', 'SERVICE', 'base', 'green', 500.0, True, 1, "ФИО клиента для именного шеврона зелёная", None, 'Polk'),
            ('fio', 'SERVICE', 'base', 'multicolor', 500.0, True, 1, "ФИО клиента для именного шеврона цветная", None, 'Polk'),
            ('right_arm', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Шеврон нарукавный правый зелёный", None, 'Polk'),
            ('right_arm', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Шеврон нарукавный правый цветной", None, 'Polk'),
            ('left_arm', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Шеврон нарукавный левый зелёный", None, 'Polk'),
            ('left_arm', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Шеврон нарукавный левый цветной", None, 'Polk'),
            ('vsr', 'SERVICE', 'base', 'green', 500.0, True, 1, "Шеврон ВСР зелёный", None, 'Polk'),
            ('vsr', 'SERVICE', 'base', 'multicolor', 500.0, True, 1, "Шеврон ВСР цветной", None, 'Polk'),
            #('general', 'SERVICE', 'base', 'red', 800.0, True, "Базовая цена индивидуального дизайна.", 1),
        ]

        data_petlicy = [

            # --- ОПЦИИ (DETAILS) ---
            # Эта опция универсальна: может быть добавлена к любой услуге
            #(None, 'DETAIL', 'PANTONE', 'yellow', 300.0, True, "Изготовление по выбранному коду Pantone."),
            #(None, 'DETAIL', 'EXPEDITE', 'orange', 500.0, True, "Ускоренная доставка (за дополнительную плату)."),

            # --- ПЕТЛИЦЫ (PETLICY) ---
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная Артиллерии", 'Artillery', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная Артиллерии", 'Artillery', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная Сухопутных войск", 'ground_forces', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная Сухопутных войск", 'ground_forces', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная ПВО", 'air_defence', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная ПВО", 'air_defence', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная автомобильных", 'automobile', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная автомобильных", 'automobile', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная танковых", 'tank', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная танковых", 'tank', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная инженерные",
             'inzh', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная инженерные",
             'inzh', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная РХБЗ",
             'RHBZ', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная РХБЗ",
             'RHBZ', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная связные",
             'svyaz', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная связные",
             'svyaz', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная оркестровые",
             'orkestr', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная оркестровые",
             'orkestr', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, True, 1, "Пара петлиц зелёная юридические",
             'juridich', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, True, 1, "Пара петлиц цветная юридические",
             'juridich', None),
            ('petlicy', 'SERVICE', 'optional', 'green', 500.0, False, 1, "Пара петлиц зелёная ...",
             '', None),
            ('petlicy', 'SERVICE', 'optional', 'multicolor', 500.0, False, 1, "Пара петлиц цветная ...",
             '', None),
            ]

        data_other = [

            # --- ДРУГОЕ (OTHER) ---
            ('other', 'SERVICE', 'optional', 'green', 400.0, True, 1, "Шеврон на кепку зелёный", None, None),
            ('other', 'SERVICE', 'optional', 'multicolor', 1000.0, False, 1, "Уникальный дизаин нашивки (шеврона)", None, None) # На доработку

            # Пример неактивной цены: если цена была повышена или услуга снята с продажи
            #('military', 'SERVICE', 'base', None, 1200.0, False, "СТАРЫЙ ЦЕННИК - Не использовать!"),
        ]

        async with aiosqlite.connect(Pricelist_PATH) as db:
            try:
                # Использование транзакции для атомарной и быстрой вставки данных
                await db.execute("BEGIN TRANSACTION;")

                # Шаблон SQL-запроса с использованием плейсхолдеров (?)
                query_complex = """
                INSERT OR IGNORE INTO COMPLEX (service_key, category_key, detail_key, color, price, is_active, 
                amount, description, petlitsa_type, complex_type) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                query_petlicy = """INSERT OR IGNORE INTO PETLICY (service_key, category_key, detail_key, color, price, is_active, 
                amount, description, petlitsa_type, complex_type) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                query_other = """INSERT OR IGNORE INTO OTHER (service_key, category_key, detail_key, color, price, is_active, 
                                amount, description, petlitsa_type, complex_type) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                # executemany выполняет один и тот же запрос для всего списка кортежей
                await db.executemany(query_complex, data_complex)
                await db.executemany(query_petlicy, data_petlicy)
                await db.executemany(query_other, data_other)

                await db.commit()
                print("[✅] Price list population complete! Successfully synchronized catalog.")

            except Exception as e:
                await db.rollback()  # Откатываем все изменения при любой ошибке
                print(f"[❌] CRITICAL ERROR during price list population: {e}")
                exit()

    #==================
    #
    #==================

    async def get_service_details(self, service_key: str) -> Optional[Dict[str, Any]]:
        """
        Извлекает все доступные детали и варианты для заданного ключевого слова услуги.

        Args:
            service_key (str): Ключ услуги, например 'complex' или 'fio'.

        Returns:
            Optional[Dict[str, Any]]: Словарь с полной структурированной информацией о услуге
                                      или None, если услуга не найдена.
        """
        print(f"🔍 Поиск деталей для service_key: '{service_key}'...")

        async with aiosqlite.connect(Pricelist_PATH) as db:
            try:
                # Запрос всех полей, отфильтрованный только по нужному ключу услуги.
                query = f"""
                            SELECT id, usluga, color, price, is_active, amount, description, 
                                category_key, detail_key, petlitsa_type, complex_type 
                            FROM COMPLEX 
                            WHERE service_key = ? AND is_active = TRUE

                            UNION ALL

                            SELECT id, usluga, color, price, is_active, amount, description, 
                                category_key, detail_key, petlitsa_type, complex_type 
                            FROM PETLICY 
                            WHERE service_key = ? AND is_active = TRUE

                            UNION ALL

                            SELECT id, usluga, color, price, is_active, amount, description, 
                                category_key, detail_key, petlitsa_type, complex_type 
                            FROM OTHER 
                            WHERE service_key = ? AND is_active = TRUE;
                            """
                # Запускаем запрос с параметром key трижды
                cursor = await db.execute(query, (service_key, service_key, service_key))
                rows = await cursor.fetchall()

            except aiosqlite.Error as e:
                print(f"🔴 Ошибка при запросе деталей для '{service_key}': {e}")
                return None

            # Если строк нет, значит, услуга не активна или не существует.
            if not rows:
                return None

            # --- Структурирование данных (самая важная часть!) ---

            all_details = []

            # Итерируемся по каждой найденной записи и собираем информацию в словари.
            for row in rows:
                detail = {
                    "id": row[0],
                    "usluga": row[1],        # Человекочитаемое название услуги
                    "color": row[2] if row[2] else None, # Цвет
                    "price": row[3],         # Цена
                    "is_active": row[4],     # Активна ли (проверка на стороне БД)
                    "amount": row[5],        # Сколько это стоит в базовой единице
                    "description": row[6],  # Полное описание для вывода пользователю
                    "category_key": row[7], # Группа услуги: SERVICE, DETAIL, PETLICY и т.д.
                    "detail_key": row[8] if row[8] else None,
                    "petlitsa_type": row[9] if row[9] else None,
                    "complex_type": row[10] if row[10] else None # Все эти поля могут быть пустыми (None)
                }
                all_details.append(detail)

            # Создаем итоговый словарь для возврата:
            return {
                "service_key": service_key,
                "overall_category": "SERVICE" if any(r["category_key"] == 'SERVICE' for r in all_details) else None,
                "all_variants": all_details # Возвращаем список всех найденных вариантов услуги.
            }

    async def calculate_total_cost(self, service_key: str, user_id: int, desired_quantity: int) -> Optional[Tuple[float, Dict]]:
        """
        РАЗДЕЛОЧНАЯ СТРУКТУРА (СИМПЛ ПЛЮС):
        Рассчитывает итоговую стоимость всего комплекта услуг, просто суммируя базовые цены.

        Args:
            service_key (str): Ключ услуги для расчета.
            user_id (int): ID пользователя (сейчас используется только для сохранения структуры).

        Returns:
            Optional[Tuple[final_total_price, breakdown_details]]
        """
        print(f"\n🚀 Начало расчета итоговой стоимости для {service_key}...")

        service_data = await self.get_service_details(service_key)

        if not service_data:
            print("[❌] Ошибка расчета: Не удалось получить данные по услуге.")
            return None

        all_variants = service_data["all_variants"]
        total_cost = 0.0
        breakdown_details = []

        # 2. Итерация и простое суммирование (Симплификация)
        for variant in all_variants:
            base_price = float(variant['price']) if variant.get('price') is not None else 0.0
            amount = variant['amount'] or 1
            try:
                amount = int(amount) if amount is not None else 1
            except ValueError:
                amount = 1

            component_cost = base_price * desired_quantity
            total_cost += component_cost

            breakdown_details.append({
                "variant": variant["usluga"],
                "base_price_unit": base_price,
                "component_used_qty": 1,
                "calculated_cost": component_cost
            })

        # Возвращаем итоговую сумму и полную разбивку расчета
        return (total_cost, {"breakdown": breakdown_details})
