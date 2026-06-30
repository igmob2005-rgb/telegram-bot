import logging
from typing import Optional
from aiogram import Router
from aiogram.types import InlineKeyboardMarkup
from Telegram_API.keyboards.keyboards import service_level_3_keyboard

router = Router()

def _handle_color_route(selection_key: str, order_id: int) -> Optional[tuple[str, Optional[InlineKeyboardMarkup], bool]]:
    """Обрабатывает все ветвления из блока 'order:color:'."""
    logging.info(f"--- Entering Color Router for selection ({selection_key}) ---")

    if "back" in selection_key or "color:back" in selection_key:
        message = "⬅️ Вы вернулись назад. Пожалуйста, выберите нужную категорию из меню выше."
        Keyboard = service_level_3_keyboard(order_id)
        return message, Keyboard, True

    if "photo" in selection_key:
        # Просто добавили деталь, дальше нет выбора цвета
        return None, False

    elif "custom" in selection_key:  # Свой вариант
        # Предположим, что выбор 'Свой вариант' всегда ведет к детальному вводу.
        # Здесь нужно вывести клавиатуру с полями ввода.
        return None, False

    else:
        logging.warning(f"Неизвестный цветной ключ: {selection_key}")
        return None, False