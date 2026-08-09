import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from database import DatabaseManager
from Telegram_API.keyboards.keyboards import services_keyboard, service_level_3_keyboard, service_level_2_keyboard, service_org_1_3_keyboard
from Telegram_API.utils.common_helpers import log_selection

dp_manager = DatabaseManager()

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    try:
        await dp_manager.save_logs(user.id, message.text or "")
    except Exception as e:
        logging.error(f"Failed to save initial log entry for user {user.id}: {e}")
    try:
        await dp_manager.add_user(user_id=user.id, first_name=user.first_name, username=user.username, role="client")
    # Логирование ошибки
    except Exception as e:
        logging.error(f"Failed to check or add user {user.id}: {e}")

    # Показываем начальное меню услуг (Services -> 1)
    await message.answer(
        f"Привет, {user.first_name}! \nЯ - Маркова Наталья Сергеевна. \nВыбери тип желаемой услуги:",
        reply_markup=services_keyboard()  # Используем общую клавиатуру
    )

@router.callback_query(lambda c: c.data.startswith("menu:"))
async def menu_back(callback: CallbackQuery):
    """Обрабатывает кнопку возврата (сброса)."""
    data = callback.data
    parts = data.split(":")
    selection_key = parts[1].lower()  # Общая категория (order)
    if "back" in selection_key or "back" in data:
        # Если это возврат, мы ничего не логируем, и сразу выходим.
        action_successful = False  # Игнорируем весь остальной код
        message = "⬅️ Вы вернулись назад. Пожалуйста, выберите нужную категорию из меню ниже."
        await callback.message.edit_text(text=message, reply_markup=services_keyboard())
        return  # Завершаем выполнение функции

@router.callback_query(lambda c: c.data.startswith("service:"))
async def services_selected(callback: CallbackQuery):
    """Обрабатывает выбор основной услуги из меню start."""
    service = callback.data.split(":")[1]
    user = callback.message.from_user
    await dp_manager.save_logs(user.id, callback.message.text or "")

    order_id = await dp_manager.create_draft_order(
        user_id=callback.from_user.id,
        service_type=service,
        status="Draft",
        from_where="START",
        username=callback.from_user.username
    )

    try:
        await log_selection(order_id, category="SERVICE", key=service, label=f"Выбранная услуга {service}", value=None)
    except TypeError as e:
        logging.error(f"Failed to save logs due to Type Error in service_entry: {e}")

    if service == "military":
        await callback.message.edit_text(
        f"✅ Вы выбрали услугу: Военные шевроны\n\nДобавьте детали заказа:",
            reply_markup=service_level_3_keyboard(order_id)  # Показываем стартовые опции (Блок 3)
        )
        await callback.answer()
    elif service == "org":
        await callback.message.edit_text(
            f"✅ Вы выбрали услугу: Организация\n\nДобавьте детали заказа:",
            reply_markup=service_org_1_3_keyboard(order_id))  # Показываем стартовые опции (Блок 3)"
        await callback.answer()
    elif service == "general":
        await callback.message.edit_text(
            f"✅ Вы выбрали услугу: Индивидуальный дизайн\n\nДобавьте детали заказа:",
            reply_markup=service_level_2_keyboard(order_id))  # Показываем стартовые опции (Блок 3)"
        await callback.answer()