import logging
from typing import Optional, Tuple
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from Telegram_API.handlers.complex_components import Form
from Telegram_API.handlers.service_entry import services_keyboard
from Telegram_API.keyboards.keyboards import (service_level_3_1_keyboard, service_level_3_2_keyboard,
                                              service_level_4_1_keyboard, service_level_5_1_3_keyboard,
                                              service_level_6_keyboard)

async def _handle_military_route(selection_key: str, order_id: int, state: FSMContext) ->Optional[Tuple[str, Optional[InlineKeyboardMarkup], bool]] :
    """
    Обрабатывает все ветвления из блока 'order:unit:'.
    Это замена для огромного IF/ELIF по блоку Военные части.
    """
    logging.info(f"--- Entering Military Router for unit selection ({selection_key}) ---")

    if "back" in selection_key or selection_key == "menu:back":
        message = "⬅️ Вы вернулись назад. Пожалуйста, выберите нужную категорию из меню ниже."
        return message, services_keyboard(), True

    elif "05812" in selection_key:
        # Пример: Тут можно вызвать специализированную логику для 05812
        message = f"✅ Заказ {order_id} Вы успешно добавили гос. код 05812. Пожалуйста, выберите тип комплектации:"
        return message, service_level_4_1_keyboard(order_id), False

    elif "71436" in selection_key:
        message = f"✅ Заказ {order_id} Вы успешно добавили 71436. Пожалуйста, выберите тип комплектации:"
        return message, service_level_4_1_keyboard(order_id), False

    elif "bastion" in selection_key:
        message = f"✅ Заказ {order_id} Вы успешно добавили Бастион. Пожалуйста, выберите тип комплектации:"
        return message, service_level_4_1_keyboard(order_id), False

    elif "lta_komendatura" in selection_key:  # Ищем общий ключ для 3.1
        # Здесь должна быть логика перехода на страницу технички (Level 3.1)
        message = f"✅ Заказ {order_id} Выбрана комплектация для 'Комендатура'. Пожалуйста, выберите техническое оснащение:"
        return message, service_level_3_1_keyboard(order_id), False

    elif "kepka" in selection_key:  # Блок Петлицы
        #Это триггер для блока 3.2 (Штанга/Петлицы)
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} Выбран шеврон на полевую кепку. Пожалуйста, укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False

    elif "tehno" in selection_key:  # Блок Петлицы
        # Это триггер для блока 3.2 (Штанга/Петлицы)
        await state.set_state(Form.zvanie)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} Выбраны шеврон на техничку. Пожалуйста, укажите Звание:"
        return message, service_level_5_1_3_keyboard(order_id), False

    elif "petlitsy" in selection_key:  # Блок Петлицы
        #Это триггер для блока 3.2 (Штанга/Петлицы)
        message = f"✅ Заказ {order_id} Выбраны Петлицы. Пожалуйста, уточните детали комплектации (Штанга/Петлицы):"
        return message, service_level_3_2_keyboard(order_id), False

    elif "duty_services" in selection_key:
        # Дежурные службы - может сразу перекидывать на Level 6
        message = f"✅ Заказ {order_id} Выбраны Дежурные службы. Пожалуйста, уточните детали комплектации"  # Оставляем пустым для обработки в главном диспетчере.
        return message, service_level_6_keyboard(order_id), False  # или вызов специализированного обработчика для дежурных

    else:
        logging.warning(f"Неизвестный ключ юнита в блоке Военных частей: {selection_key}")
        return None, None, False