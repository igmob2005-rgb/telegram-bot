from typing import Optional
import logging
from aiogram import Router
from aiogram import types
from aiogram.types import message

# ВАЖНО: Импортируйте ваше состояние (Form) из complex_components или отдельного места
from .complex_components import Form  # Убедитесь, что путь к состоянию верен
from aiogram.fsm.context import FSMContext
from Telegram_API.keyboards.keyboards import service_level_5_1_2_keyboard, service_level_5_keyboard, \
                                                service_level_5_1_3_keyboard

router = Router()


@router.message(lambda message: True)  # Использование общего фильтра для всех текстовых сообщений в контексте заказа
async def handle_incoming_text_input(message: types.Message, state: FSMContext):
    """
    Универсальный обработчик всего входящего текста от пользователя,
    когда он находится в режиме ввода данных (FSM).

    ВАЖНО: Вам нужно реализовать логику ветвления внутри этой функции,
    проверяя текущее состояние.
    """
    user_input = message.text

    if not user_input:
        await message.answer("Пожалуйста, введите текст.")
        return

    # --- 1. Получение текущего состояния (Определение контекста ввода) ---
    current_state: Optional[Form] = await state.get_state()
    user_data = await state.get_data()
    order_id = user_data.get('order_id')

    if current_state is None:
        # Если мы не знаем, в каком блоке введен текст (ошибка или сбой),
        await message.answer("Ошибка: Невозможно обработать ваш ввод. Пожалуйста, выберите действие в меню.")
        return

    logging.info(f"Пользователь вошел в состояние {current_state} и ввел: '{user_input}'")

    # --- 2. БЛОК ВЕТВЛЕНИЯ (Логика, что делать с текстом) ---
    await state.update_data(family=user_input)
    if current_state == Form.familia:
        try:
            await state.set_state(Form.initsialy)
            messag = f"✅ Фамилия '{user_input}' успешно сохранена.\nТеперь, пожалуйста, введите ваши ИНИЦИАЛЫ."
            next_keyboard = service_level_5_1_2_keyboard(order_id=order_id)  # Нужно передать order_id!
            await message.answer(messag, reply_markup=next_keyboard)

        except Exception as e:
            logging.error(f"Ошибка при сохранении ФИО: {e}")
            await state.set_state(Form.familia)

            await message.answer("Произошла ошибка при записи данных.")


    elif current_state == Form.initsialy:
        try:
            await state.update_data(initials=user_input)
            messag = f"🎉 Заказ {order_id} Инициалы '{user_input}' успешно введены! Количество:"
            await message.answer(messag, reply_markup=service_level_5_1_2_keyboard(order_id))
            await state.set_state(Form.lens)
        except Exception as e:
            logging.error(f"Ошибка при сохранении инициалов: {e}")
            await message.answer("Произошла ошибка.")
    elif current_state == Form.lens:
        try:
            if int(user_input)>0:
                await state.update_data(lens=user_input)
                messag = f"🎉 Заказ {order_id} Количество '{user_input}' успешно введены! далее оплата: Можете оплатить... :::"
                await message.answer(messag, reply_markup=service_level_5_1_3_keyboard(order_id))
                await state.set_state(Form.lens)
        except Exception as e:
            if "with base 10" in str(e):
                messag = f"🎉 Заказ {order_id} Введите Количество числом! Пример: 10"
                await message.answer(messag, reply_markup=service_level_5_1_3_keyboard(order_id))
                await state.set_state(Form.lens)
            else:
                logging.error(f"Ошибка при сохранении количества: {e}")
                await message.answer("Произошла ошибка.")
    elif current_state == Form.zvanie:
        try:
            await state.update_data(zvanie=user_input)
            messag = f"🎉 Заказ {order_id} Звание '{user_input}' успешно введено! Введите фамилию"
            await message.answer(messag, reply_markup=service_level_5_1_3_keyboard(order_id))
            await state.set_state(Form.familia)
        except Exception as e:
            logging.error(f"Ошибка при сохранении звания: {e}")
            await message.answer("Произошла ошибка.")

    else:
        # Если состояние не распознано или нет логики для этого состояния
        await message.answer(
            f"В текущем состоянии ({current_state.__name__}) ввод текста не ожидается. Пожалуйста, используйте кнопки меню.")











@router.message()  # Обрабатывает ВСЕ текстовые сообщения, которые попадают в этот роутер
async def handle_incoming_text_input(message: types.Message, state: FSMContext):
    """Ловит любой текст и решает, что с ним делать, основываясь на текущем состоянии."""
    user_input = message.text

    # 1. Получаем актуальное состояние после поступления сообщения (важно!)
    current_state = await state.get_state()
    user_data = await state.get_data()
    order_id = user_data.get('order_id')

    if current_state == Form.familia:
        await process_input_familia(user_input, state,order_id)
    elif current_state == Form.initsialy:
        await process_input_initials(user_input, state, order_id)
    else:
        # Если мы в состоянии, не предназначенном для ввода текста (например, просто "общий выбор"),
        # или состояние неизвестно - игнорируем сообщение.
        logging.warning(f"Получено лишнее текстовое сообщение в состоянии {current_state}. Игнорирование.")
        await message.answer("Пожалуйста, используйте меню для выбора действия.",
                             reply_markup=service_level_5_keyboard(...))


async def process_input_familia(user_input: str, state: FSMContext, order_id: int):
    # 1. Валидация: Проверить формат (например, должно содержать буквы и пробелы?)
    if not user_input or len(user_input) < 2:
        await message.answer("Пожалуйста, введите корректную фамилию.")
        return

    # 2. Сохранение в FSM
    await state.update_data(familia=user_input)

    # 3. Изменение состояния и сообщение
    new_message = f"✅ Фамилия {user_input} сохранена."
    next_keyboard = service_level_5_1_2_keyboard(order_id=order_id)  # !!! Убедитесь, что order_id передается
    await message.answer(new_message, reply_markup=next_keyboard)


async def process_input_initials(user_input: str, state: FSMContext, order_id: int):
    # ... (Аналогично обработка инициалов и переход на следующий этап)
    pass