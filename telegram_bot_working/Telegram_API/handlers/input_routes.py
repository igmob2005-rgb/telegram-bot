from typing import Optional
import logging
from aiogram import Router
from aiogram import types
from aiogram.types import message
from .complex_components import Form
from aiogram.fsm.context import FSMContext
from Telegram_API.keyboards.keyboards import service_level_5_1_2_keyboard, service_level_5_keyboard, \
    service_level_5_1_3_keyboard, services_keyboard
from Pricelist import PricelistManager

router = Router()
pm = PricelistManager()

@router.message(lambda message: True)  # Универсальный обработчик для всех текстовых сообщений в контексте заказа
async def handle_incoming_text_input(message: types.Message, state: FSMContext):
    """
    Универсальный обработчик всего входящего текста от пользователя.
    Определяет логику ветвления только на основе текущего состояния (current_state).
    """
    user_input = message.text

    if not user_input:
        await message.answer("Пожалуйста, введите текст.")
        return

    # --- 1. Получение контекста ---
    current_state: Optional[Form] = await state.get_state()
    user_data = await state.get_data()
    order_id = user_data.get('order_id')

    if current_state is None:
        await message.answer("Ошибка: Невозможно обработать ваш ввод. Пожалуйста, выберите действие в меню.")
        return services_keyboard()

    logging.info(f"Пользователь вошел в состояние {current_state} и ввел: '{user_input}'")

    # --- 2. БЛОК ВЕТВЛЕНИЯ (Используем ELIF для исключения конфликтов) ---

    if current_state == Form.lens:
        await process_handling_lens(message, user_input, state, order_id)

    elif current_state == Form.initsialy:
        await process_handling_initsialy(message, user_input, state, order_id)

    elif current_state == Form.zvanie:
        await process_handling_zvanie(message, user_input, state, order_id)

    elif current_state == Form.familia:
        await process_handling_familia(message, user_input, state, order_id)

    else:
        # Состояние неизвестно или ввод текста не ожидается
        await message.answer(
            f"В текущем состоянии ({current_state.__name__}) ввод текста не ожидается. Пожалуйста, используйте кнопки меню.")


# --- ФУНКЦИИ ОБРАБОТЧИКОВ (Clean Separation of Concerns) ---

async def process_handling_familia(message: types.Message, user_input: str, state: FSMContext, order_id: int):
    """Обработка ввода Фамилии."""
    try:
        # 1. Сохраняем данные в контекст
        await state.update_data(familia=user_input)
        # 2. Переводим пользователя на следующий шаг (Инициалы)
        await state.set_state(Form.initsialy)
        messag = f"✅ Фамилия '{user_input}' успешно сохранена.\nТеперь, пожалуйста, введите ваши ИНИЦИАЛЫ."
        next_keyboard = service_level_5_1_2_keyboard(order_id=order_id)
        await message.answer(messag, reply_markup=next_keyboard)

    except Exception as e:
        logging.error(f"Ошибка при сохранении ФИО: {e}")
        await state.set_state(Form.familia) # Возвращаем в текущее состояние в случае ошибки
        await message.answer("Произошла ошибка при записи данных.")


async def process_handling_initsialy(message: types.Message, user_input: str, state: FSMContext, order_id: int):
    """Обработка ввода Инициалов."""
    try:
        # 1. Сохраняем данные в контекст
        await state.update_data(initsialy=user_input)
        messag = (f"🎉 Заказ {order_id} Инициалы '{user_input}' успешно введены! \n"
                  f"Введите количество:")
        await message.answer(messag, reply_markup=service_level_5_1_2_keyboard(order_id))
        # 2. Переводим пользователя на следующий шаг (Количество)
        await state.set_state(Form.lens)

    except Exception as e:
        logging.error(f"Ошибка при сохранении инициалов: {e}")
        await message.answer("Произошла ошибка.")


async def process_handling_zvanie(message: types.Message, user_input: str, state: FSMContext, order_id: int):
    """Обработка ввода Звания."""
    try:
        # 1. Сохраняем данные в контекст
        await state.update_data(zvanie=user_input)
        messag = f"🎉 Заказ {order_id} Звание '{user_input}' успешно введено! Введите фамилию."
        await message.answer(messag, reply_markup=service_level_5_1_3_keyboard(order_id))
        # 2. Переводим пользователя на следующий шаг (Фамилия)
        await state.set_state(Form.familia)

    except Exception as e:
        logging.error(f"Ошибка при сохранении звания: {e}")
        await message.answer("Произошла ошибка.")


async def process_handling_lens(message: types.Message, user_input: str, state: FSMContext, order_id: int):
    """Обработка ввода Количества и завершение заказа."""
    try:
        user_input_count = user_input.strip()

        # 1. Валидация ввода (проверяем, является ли ввод числом > 0)
        if not user_input_count or not str(user_input_count).isdigit() or int(user_input_count) <= 0:
            messag = (f"⚠️ Количество должно быть положительным целым числом. Попробуйте снова.")
            await message.answer(messag, reply_markup=service_level_5_1_3_keyboard(order_id))
            return

        # 2. Получение всех данных из контекста
        data = await state.get_data()
        familia = data.get('familia')
        initsialy = data.get('initsialy')

        calculated_service_key = data.get('primary_service_key') # Получаем ключ услуги из контекста

        if not familia or not initsialy:
            error_msg = "⚠️ Критическая ошибка: Не удалось собрать данные клиента. Пожалуйста, начните ввод с фамилии."
            await message.answer(error_msg)
            return

        # 3. Обновление и сохранение данных (использование int для количества)
        new_count = int(user_input_count)  # Преобразуем строку в целое число
        await state.update_data(lens=new_count)  # Сохраняем правильный тип данных

        # 4. Расчёт стоимости (ДИНАМИЧЕСКИЙ ВЫЗОВ ФУНКЦИИ РАСЧЕТА)
        if not calculated_service_key:
            error_msg = "⚠️ Неизвестный ключ услуги. Пожалуйста, начните процесс заказа заново."
            await message.answer(error_msg)
            return

        # Расчёт стоимости
        cost_result = await pm.calculate_total_cost(
            service_key=calculated_service_key,
            user_id=order_id,
            desired_quantity=new_count
        )

        if cost_result is None:
            messag = "⚠️ Не удалось рассчитать стоимость из-за ошибки в базе данных."
            await message.answer(messag, reply_markup=service_level_5_1_3_keyboard(order_id))
            return
        final_cost = cost_result[0]

        # 5. Формирование сообщения с корректными данными
        fullname = f"{str(familia)} {str(initsialy)}"
        messag = (f"🎉 Заказ {order_id} \n\n"
                  f"ФИО {fullname} в количестве {new_count} штук. \n" 
                  f"\n ИТОГОВАЯ СТОИМОСТЬ: {final_cost:.2f} руб.\n"
                  f"Далее оплата: Можете оплатить.")
        await message.answer(messag, reply_markup=service_level_5_1_3_keyboard(order_id))

    except Exception as e:
        logging.error(f"Ошибка при обработке количества: {e}")
        # Если ошибка не связана с валидацией (catch-all)
        await message.answer("Произошла необработанная системная ошибка.")


@router.message()  # Обрабатывает ВСЕ текстовые сообщения, которые попадают в этот роутер
async def handle_incoming_text_input(message: types.Message, state: FSMContext):
    """
    Вся логика перенесена сюда и работает по принципу IF/ELIF.
    Все остальные вспомогательные функции (process_input_familia, process_input_initsialy) были удалены, так как их логика встроена выше.
    """
    user_input = message.text

    if not user_input:
        await message.answer("Пожалуйста, введите текст.")
        return

    # --- Основная ветка (Исправлено с if/elif) ---
    current_state: Optional[Form] = await state.get_state()
    user_data = await state.get_data()
    order_id = user_data.get('order_id')

    if current_state == Form.lens:
        await process_handling_lens(message, user_input, state, order_id)

    elif current_state == Form.initsialy:
        await process_handling_initsialy(message, user_input, state, order_id)

    elif current_state == Form.zvanie:
        await process_handling_zvanie(message, user_input, state, order_id)

    elif current_state == Form.familia:
        await process_handling_familia(message, user_input, state, order_id)

