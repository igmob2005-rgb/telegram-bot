from aiogram import Router#, types
from aiogram.types import CallbackQuery#, #Message

from Telegram_API.handlers.Deg_sluzhba import _handle_deg_sl_route
from Telegram_API.handlers.input_routes import handle_incoming_text_input
#from aiogram.types.message import Message
#from pyexpat.errors import messages

from Telegram_API.handlers.military_routes import _handle_military_route
from Telegram_API.utils.common_helpers import log_selection
from Telegram_API.handlers.complex_components import _handle_complex_component_route, _handle_complex_variety
from Telegram_API.handlers.color_routes import _handle_color_route
from Telegram_API.handlers.org_routes import _handle_org_route

router = Router()

@router.callback_query(lambda c: c.data.startswith("order:"))
async def handle_order_details_selection(callback: CallbackQuery, state):
    """
    УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК для всех кликов по кнопкам в меню заказа.
    Теперь он действует как Диспетчер, направляя управление в специализированные функции.
    """
    data = callback.data
    parts = data.split(":")



    try:
        selected_category = parts[1].lower()  # Общая категория (order)
        selection_key = parts[2].lower()  # Конкретный ключ (unit, color, complex и т.д.)
        order_id = int(parts[-1])  # ID заказа

    except ValueError:
        await callback.answer("Ошибка данных: Неверный ID Заказа.")
        #return

    next_keyboard = None
    message_text = ""
    is_navigation_return = False
    action_successful = False

    if "back" in selection_key or "back" in data:
        message_text, next_keyboard, is_navigation_return = _handle_military_route(selection_key, order_id)
        action_successful = False # Игнорируем весь остальной код
    else:
        is_navigation_return = False
        log_success, db_message = log_selection(order_id, selected_category, selection_key, "Общий выбор пункта", None)
    # 1. Логирование выбранного элемента 
        # 2. МАРШРУТИЗАЦИЯ (Dispatching)

        if selected_category == "unit":
            result = await _handle_military_route(selection_key, order_id, state)
            message_text, next_keyboard, is_navigation_return = result if result else ("", None, True)
            action_successful = bool(result and not is_navigation_return)
        elif selected_category == "form":
            result = _handle_complex_variety(selection_key, order_id)
            message_text, next_keyboard, is_navigation_return = result if result else ("", None, True)
            action_successful = bool(result and not is_navigation_return)
        elif selected_category == "color":
            result = _handle_color_route(selection_key, order_id)
            message_text, next_keyboard, is_navigation_return = result if result else ("", None, True)
            action_successful = bool(result and not is_navigation_return)
        elif selected_category == "org":
            result = _handle_org_route(selection_key, order_id)
            message_text, next_keyboard, is_navigation_return = result if result else ("", None, True)
            action_successful = bool(result and not is_navigation_return)
        elif selected_category == "complex":
            result = await _handle_complex_component_route(selection_key, order_id, state)
            message_text, next_keyboard, is_navigation_return = result if result else ("", None, True)
            action_successful = bool(result and not is_navigation_return)
        elif selected_category == "input":
            result = await _handle_complex_component_route(selection_key, order_id, state)
            message_text, next_keyboard, is_navigation_return = result if result else ("", None, True)
            action_successful = bool(result and not is_navigation_return)
        elif selected_category == "epaulettes":
            result = await _handle_deg_sl_route(selection_key, order_id, state)
            message_text, next_keyboard, is_navigation_return = result if result else ("", None, True)
            action_successful = bool(result and not is_navigation_return)
        elif selected_category == "kepka":
            result = await handle_incoming_text_input()
            message_text, next_keyboard, is_navigation_return = result if result else ("", None, True)
            action_successful = bool(result and not is_navigation_return)

    if is_navigation_return:
        # ⭐ СЦЕНАРИЙ ВОЗВРАТА ⭐
        await callback.answer("Навигация:", show_alert=True)
        await callback.message.edit_text(text=message_text, reply_markup=next_keyboard or None)
        return

    elif action_successful:
        try:
            await callback.message.edit_text(text=message_text, reply_markup=next_keyboard)
            await callback.answer("✅ Выбор принят! Ожидайте следующего шага.")
        except ValueError:
            await callback.answer("Продолжайте.....")
            # return
    elif db_message and not is_navigation_return:
        # Сценарий C1: Логирование ПРОВАЛИЛОСЬ 
        await callback.answer(db_message, show_alert=True)
        return # Ничего не рисуем на экране, только предупреждение!

    elif not action_successful and not is_navigation_return:
        # Сценарий D: Неизвестный ключ (Не было ни возврата, ни выбора).
        await callback.answer("❌ Выбран элемент, который пока не имеет детальной обработки в системе.")
        return
    else:
        await callback.message.edit_text(text=message_text, reply_markup=next_keyboard)
        await callback.answer("✅ Пункт успешно добавлен в заказ! Ожидайте дальнейших действий.")

    if next_keyboard:
        await callback.message.edit_text(text=message_text, reply_markup=next_keyboard)
    elif message_text:
        await callback.message.edit_text(text=message_text)
    else:
        # Просто уведомляем через всплывающее окошко (callback.answer).
        await callback.answer("✅ Пункт успешно добавлен в заказ! Ожидаем дальнейших действий.")
