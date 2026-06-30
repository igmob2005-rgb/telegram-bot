import logging
from typing import Optional
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from Telegram_API.keyboards.keyboards import (service_level_4_keyboard,
                                              service_level_5_keyboard,
                                              service_level_5_1_keyboard,
                                              service_level_5_1_2_keyboard,
                                              service_level_5_1_3_keyboard)

router = Router()

class Form(StatesGroup):
    zvanie = State()
    lens = State()
    familia = State()
    initsialy = State()


async def _handle_complex_component_route(selection_key: str, order_id: int, state: FSMContext) -> Optional[tuple[str, Optional[InlineKeyboardMarkup], bool]]:
    """
    Обрабатывает все ветвления из блока 'order:complex:'.
    Сюда попадают вещи типа ФИО, ВСР и т.д.
    """
    logging.info(f"--- Entering Complex Component Router for selection ({selection_key}) ---")

    if "back" in selection_key or selection_key == "complex:back":
        message = "⬅️ Вы вернулись назад. Пожалуйста, выберите нужную категорию из меню выше."
        keyboard = service_level_5_keyboard(order_id)
        return message, keyboard, True

    elif "fio_start" in selection_key or "set" in selection_key:  # Начало ввода ФИО (Блок 5.1)
        await state.set_state(Form.familia)
        await state.update_data(order_id=order_id)
        message = f"Заказ {order_id}"
        return message, service_level_5_1_keyboard(order_id), False

    elif "fio1" or "rename" in selection_key: # Начало ввода ФИО (Блок 5.1)
        await state.set_state(Form.familia)
        await state.update_data(order_id=order_id)
        message = f"Заказ {order_id} Введите вашу фамилию"
        return message, service_level_5_1_3_keyboard(order_id), False

    elif "vsr_start" in selection_key or "vsr2" in selection_key:  # Ввод ВСР
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"🎉 Заказ {order_id} Количество:"
        # Здесь должна быть логика, которая ведет к выбору текста или файла для ВСР.
        return message, service_level_5_1_3_keyboard(order_id), False


    else:
        logging.warning(f"Неизвестный ключ компонента в блоке комплектации: {selection_key}")
        return None, False

def _handle_complex_variety(selection_key: str, order_id: int) -> Optional[tuple[str, Optional[InlineKeyboardMarkup], bool]]:
    """Обрабатывает все ветвления из блока 'order:form:'."""
    logging.info(f"--- Entering Complex Router for selection ({selection_key}) ---")

    if "back" in selection_key or "form:back" in selection_key:
        message = "⬅️ Вы вернулись назад. Пожалуйста, выберите нужную категорию из меню выше."
        return message, service_level_4_keyboard(order_id), True

    if selection_key in "order:form:field":
        message = f"Заказ {order_id} Вы успешно выбрали тип формы!"
        return message, service_level_5_keyboard(order_id), False
    elif selection_key in "order:form:office":
        message = f"Заказ {order_id} Вы успешно выбрали тип формы!"
        return message, service_level_5_keyboard(order_id), False
    elif selection_key in "order:form:parade":
        message = f"Заказ {order_id} Вы успешно выбрали тип формы!"
        return message, service_level_5_keyboard(order_id), False

    else:
        logging.info(f"--- Ветка ({selection_key}) проигнорирована как элемент навигации назад или общая категория.")
        return None, None, False