import logging
from typing import Optional, Tuple
from aiogram.types import InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from Telegram_API.handlers.complex_components import Form
from Telegram_API.handlers.service_entry import services_keyboard
from Telegram_API.keyboards.keyboards import (service_level_6_1_keyboard,
                                              service_level_6_2_keyboard,
                                              service_level_6_3_keyboard,
                                              service_level_5_1_3_keyboard)

async def _handle_deg_sl_route(selection_key: str, order_id: int, state: FSMContext) ->Optional[Tuple[str, Optional[InlineKeyboardMarkup], bool]] :
    """
    Обрабатывает все ветвления из блока 'order:unit:'.
    Это замена для огромного IF/ELIF по блоку Военные части.
    """
    logging.info(f"--- Entering Military Router for unit selection ({selection_key}) ---")

    if "back" in selection_key or selection_key == "menu:back":
        message = "⬅️ Вы вернулись назад. Пожалуйста, выберите нужную категорию из меню ниже."
        return message, services_keyboard(), True
    elif "poi" in selection_key:
        message = f"✅ Заказ {order_id} Вы успешно добавили . Пожалуйста, выберите тип комплектации:"
        return message, service_level_6_1_keyboard(order_id), False  # или вызов специализированного обработчика для дежурных
    elif "shevron" in selection_key:
        message = f"✅ Заказ {order_id} Выбраны Дежурные службы. Пожалуйста, уточните детали комплектации"  # Оставляем пустым для обработки в главном диспетчере.
        return message, service_level_6_1_keyboard(order_id), False  # или вызов специализированного обработчика для дежурных

    elif "ops_duty" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "duty_dept" in selection_key:
        message = f"✅ Заказ {order_id} Выбраны Дежурные службы. Пожалуйста, уточните детали комплектации"  # Оставляем пустым для обработки в главном диспетчере.
        return message, service_level_6_2_keyboard(order_id), False  # или вызов специализированного обработчика для дежурных
    elif "assistant" in selection_key:
        message = f"✅ Заказ {order_id} Выбраны Дежурные службы. Пожалуйста, уточните детали комплектации"  # Оставляем пустым для обработки в главном диспетчере.
        return message, service_level_6_3_keyboard(order_id), False  # или вызов специализированного обработчика для дежурных
    elif "dnevnik" in selection_key:
        message = f"✅ Заказ {order_id} Выбраны Дежурные службы. Пожалуйста, уточните детали комплектации"  # Оставляем пустым для обработки в главном диспетчере.
        return message, service_level_6_4_keyboard(
            order_id), False  # или вызов специализированного обработчика для дежурных
    elif "rukvod" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False

    elif "parts" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "battalion" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "canteen" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "park" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "cpp1" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "cpp2" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "division" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "polygon" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False

    elif "pom_cpp1" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "pom_cpp2" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "pom_division" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "pom_polygon" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "ops_duty" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False

    elif "dnevnik_squad" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False
    elif "park" in selection_key:
        await state.set_state(Form.lens)
        await state.update_data(order_id=order_id)
        message = f"✅ Заказ {order_id} укажите количество:"
        return message, service_level_5_1_3_keyboard(order_id), False



    elif "shevron" in selection_key:
        # Дежурные службы - может сразу перекидывать на Level 6
        message = f"✅ Заказ {order_id} Выбраны Дежурные службы. Пожалуйста, уточните детали комплектации"  # Оставляем пустым для обработки в главном диспетчере.
        return message, service_level_6_1_keyboard(order_id), False  # или вызов специализированного обработчика для дежурных
    elif "shevron" in selection_key:
        # Дежурные службы - может сразу перекидывать на Level 6
        message = f"✅ Заказ {order_id} Выбраны Дежурные службы. Пожалуйста, уточните детали комплектации"  # Оставляем пустым для обработки в главном диспетчере.
        return message, service_level_6_1_keyboard(order_id), False  # или вызов специализированного обработчика для дежурных
    elif "shevron" in selection_key:
        # Дежурные службы - может сразу перекидывать на Level 6
        message = f"✅ Заказ {order_id} Выбраны Дежурные службы. Пожалуйста, уточните детали комплектации"  # Оставляем пустым для обработки в главном диспетчере.
        return message, service_level_6_1_keyboard(order_id), False  # или вызов специализированного обработчика для дежурных

    else:
        logging.warning(f"Неизвестный ключ юнита в блоке Военных частей: {selection_key}")
        return None, None, False
