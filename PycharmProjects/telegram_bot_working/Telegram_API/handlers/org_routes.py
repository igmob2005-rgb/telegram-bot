from typing import Optional, Tuple
from aiogram.types import InlineKeyboardMarkup
from Telegram_API.handlers.service_entry import services_keyboard

def _handle_org_route(selection_key: str, order_id: int) -> Optional[Tuple[str, Optional[InlineKeyboardMarkup], bool]]:
    """
        Обрабатывает все ветвления из блока 'order:org:'.
        """
    if "back" in selection_key or selection_key == "menu:back":
        message = "⬅️ Вы вернулись назад. Пожалуйста, выберите нужную категорию из меню выше."
        return message, services_keyboard(), True

    if "reydovo" in selection_key:
        message = f"Заказ {order_id} Укажите количество необходимых шевронов"
        return message, None, False

    elif "gor_klyuch" in selection_key:
        message = f"Заказ {order_id} Укажите количество необходимых шевронов"
        return message, None, False

    elif "firedept" in selection_key:
        message = f"Заказ {order_id} Укажите количество необходимых шевронов"
        return message, None, False

    elif "fssp" in selection_key:
        message = f"Заказ {order_id} Укажите количество необходимых шевронов"
        return message, None, False

    elif "boiler" in selection_key:
        message = f"Заказ {order_id} Укажите количество необходимых шевронов"
        return message, None, False

    elif "prosecutor" in selection_key:
        message = "Заказ {order_id} Пока недоступно"
        return message, None, False

    elif "bank_field" in selection_key:
        message = "Заказ {order_id} Пока недоступно"
        return message, None, False