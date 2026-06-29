import logging
from aiogram.types import CallbackQuery
from typing import Optional
from database import (
    save_logs, is_admin, user_exists, add_user,
    create_draft_order, add_order_detail,  # <-- !!! НОВАЯ ФУНКЦИЯ ЛОГИРОВАНИЯ
    get_full_order_details
)

def log_selection(order_id: int, category: str, key: str, label: str, value: Optional[str] = None) -> bool:
    """Универсальная функция логирования выбора в базу данных."""
    try:
        if not isinstance(order_id, int) or order_id <= 0:
            #logging.error("Некорректный или отсутствующий Order ID для логирования.")
            return False, "Ошибка: Некорректный ID Заказа."

        success = add_order_detail(order_id, category, key, label, value)

        if success:
            logging.info(f"✅ Успешно залогировано: {label} ({key}) для заказа {order_id}")
            return True, None
        else:
            message = f"❌ Ошибка при добавлении детали в БД."
            logging.error(f"{message}")
            return False, message

    except Exception as e:
        error_message = f"⚠️ КРИТИЧЕСКАЯ ОШИБКА СОХРАНЕНИЯ: {e.__class__.__name__}. Пожалуйста, повторите выбор."
        logging.critical(f"Критическая ошибка при логировании выбора: {e}")
        # Важно показать пользователю, что произошла ошибка, но не паниковать
        #raise Exception("Не удалось сохранить выбранные данные.") # Выкидываем исключение для обработки выше
        return False, error_message

async def _show_generic_message(callback: CallbackQuery, text: str = "✅ Пункт успешно добавлен в заказ!") -> None:
    """Вспомогательная функция для красивого ответа после логирования."""
    await callback.answer("Успех!", show_alert=True)
    # Используем message.edit_text или просто answer для лучшего UX,
    # но пока оставим простой ответ для совместимости с Telegram API
    await callback.message.edit_text(text)