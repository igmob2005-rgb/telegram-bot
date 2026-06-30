from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from database import (
    save_logs, is_admin, user_exists, add_user,
    create_draft_order, add_order_detail,
    get_full_order_details
)
from Telegram_API.keyboards.keyboards import services_keyboard, service_level_3_keyboard, service_level_2_keyboard, service_org_1_3_keyboard
from Telegram_API.utils.common_helpers import log_selection

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    save_logs(user.id, message.text or "")
    if not user_exists(user.id):
        add_user(user_id=user.id, first_name=user.first_name, username=user.username, role="client")

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
    # ... (Остается без изменений, так как работает правильно)
    service = callback.data.split(":")[1]

    order_id = create_draft_order(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        service_type=service
    )

    log_selection(order_id, category="SERVICE", key=service, label=f"Выбранная услуга {service}", value=None)

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