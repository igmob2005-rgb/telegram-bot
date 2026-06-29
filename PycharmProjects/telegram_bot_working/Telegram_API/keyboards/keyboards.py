from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Tuple

# --- CORE KEYBOARDS (General Order Actions) ---

def order_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Основная клавиатура действий с заказом."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Описание", callback_data=f"order:add_desc:{order_id}")],
            [InlineKeyboardButton(text="📅 Дедлайн", callback_data=f"order:add_deadline:{order_id}")],
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"order:confirm:{order_id}")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data=f"order:cancel:{order_id}")],
        ]
    )

# --- LEVEL 1 (INITIAL SERVICE CHOICE) ---

def services_keyboard() -> InlineKeyboardMarkup:
    """Обрабатывает выбор основного типа услуги (текст для кнопки 'start')."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # Индивидуальный -> 2
            [InlineKeyboardButton(text="Индивидуал.", callback_data="service:general:2")],
            # Воинская часть -> 3
            [InlineKeyboardButton(text="Военная часть", callback_data="service:military:3")],
            # Организация -> 1.3
            [InlineKeyboardButton(text="Организация (ФГУ)", callback_data="service:org:1.3")]
        ]
    )

def service_level_2_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Кнопки для общего этапа 2: Детали заказа (Фото, Размеры, Расцветка)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🖼️ Добавить фото", callback_data=f"order:details:photo:{order_id}")],
            [InlineKeyboardButton(text="📏 Указать размеры", callback_data=f"order:details:size:{order_id}")],
            # Указать расцветку -> 2.1
            [InlineKeyboardButton(text="🌈 Указать расцветку", callback_data=f"order:details:color_start:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

def service_level_2_1_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 2.1: Выбор варианта цвета."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎨 Как на фото", callback_data=f"order:color:photo:{order_id}")],
            [InlineKeyboardButton(text="✨ Свой вариант", callback_data=f"order:color:custom:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )


# --- LEVEL 1.3 (Specific Organizations/Colleges) ---

def service_org_1_3_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Кнопки для выбора конкретной организации из списка 1.3."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Школа Рейдово", callback_data=f"order:org:reydovo:{order_id}")],
            [InlineKeyboardButton(text="Школа Горячие Ключи", callback_data=f"order:org:gor_klyuch :{order_id}")],
            [InlineKeyboardButton(text="Пожарная организация", callback_data=f"order:org:firedept:{order_id}")],
            [InlineKeyboardButton(text="ФССП", callback_data=f"order:org:fssp:{order_id}")],
            [InlineKeyboardButton(text="Котельная", callback_data=f"order:org:boiler:{order_id}")],
            [InlineKeyboardButton(text="Военная прокуратура", callback_data=f"order:org:prosecutor:{order_id}")],
            [InlineKeyboardButton(text="Полевой банк", callback_data=f"order:org:bank_field:{order_id}")],
            # Кнопка для возврата к основному меню или завершения выбора
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

# --- LEVEL 1. (Military Unit Options) ---
# ==============================================
# [НОВОЕ] Блок 3: Главная стартовая клавиатура после выбора услуги
# Это заменяет старую "placeholder" функцию и содержит все ветки 3.
# ==============================================

def service_level_3_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Основной экран выбора подразделения/элемента униформы из блока 3."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # Коды подразделений (Самые важные идентификаторы)
            [InlineKeyboardButton(text="05812", callback_data=f"order:unit:05812:{order_id}")],
            [InlineKeyboardButton(text="71436", callback_data=f"order:unit:71436:{order_id}")],
            [InlineKeyboardButton(text="Бастион", callback_data=f"order:unit:bastion:{order_id}")],
            # Места и предметы (Запускают разные ветки)
            [InlineKeyboardButton(text="Летная комендатура ➡️", callback_data=f"order:unit:lta_komendatura:{order_id}")], # -> 3.1
            [InlineKeyboardButton(text="На полевую кепку", callback_data=f"order:unit:kepka:{order_id}")],
            [InlineKeyboardButton(text="Петлицы (Штанга)", callback_data=f"order:unit:petlitsy:{order_id}")], # -> 3.2
            [InlineKeyboardButton(text="Дежурные службы", callback_data=f"order:unit:duty_services:{order_id}")],
            # Кнопка для возврата
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data=f"menu:back")]
        ]
    )

# --- LEVEL 3.1 (Technical Equipment Branch) ---

def service_level_3_1_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Блок 3.1: Особенности технического оборудования."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # 4.1 - По типу формы (Ветка, которая ведет к самому выбору формы)
            [InlineKeyboardButton(text="На техничку", callback_data=f"order:unit:tehno:{order_id}")],
            # Логика из файла подразумевает, что выбор "4.1" здесь - это общая категория форм
            [InlineKeyboardButton(text="⚙️ Полевая расцветка", callback_data=f"order:form:field:{order_id}")],
            [InlineKeyboardButton(text="👔 На офисную", callback_data=f"order:form:office:{order_id}")],
            [InlineKeyboardButton(text="🎖️ На парадную", callback_data=f"order:form:parade:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")]
        ]
    )

def service_level_3_1_1_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Указать звание", callback_data=f"order:technichka:zvanie:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")]
        ]
    )

# --- LEVEL 3.2 (Stripe/Badge Branch) ---

def service_level_3_2_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Блок 3.2: Выбор элементов, связанных с петлицами."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # Указать номер на фото -> 3.2.1
            [InlineKeyboardButton(text="🆔 Указать номер (Фото)", callback_data=f"order:badge:photo:{order_id}")],
            # Свой вариант - род войск (Переход к общим выборам)
            [InlineKeyboardButton(text="<0xF0><0x9F><0x97><0x82>️ Род войск", callback_data=f"order:badge:military:{order_id}")],
            # Индивидуальный -> 2. Перезапуск процесса выбора цвета/деталей
            [InlineKeyboardButton(text="🎨 Начать с нуля (По цвету)", callback_data=f"service:general:2")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

def service_level_3_2_1_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 3.2.1: Выбор цвета для элемента (Номера)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟡 Офисная расцветка", callback_data=f"order:color:office:{order_id}")],
            [InlineKeyboardButton(text="🟢 Полевая расцветка", callback_data=f"order:color:field:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data=f"menu:back")]
        ]
    )

# --- LEVEL 4 (General Color Choices) ---
def service_level_4_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Блок 4: Общие выборы расцветки."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛡️ Стандартная расцветка (4.1)", callback_data=f"order:color:standard:{order_id}")], # -> 4.1
            [InlineKeyboardButton(text="🎨 Индивидуальная расцветка (2.1)", callback_data=f"order:color:individual:{order_id}")],# -> 2.1
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

def service_level_4_1_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 4.1: Выбор формы."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟢 На полевую форму", callback_data=f"order:form:field:{order_id}")],
            [InlineKeyboardButton(text="👔 На офисную", callback_data=f"order:form:office:{order_id}")],
            [InlineKeyboardButton(text="🎖️ На парадную", callback_data=f"order:form:parade:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data=f"menu:back")]
        ]
    )

# --- LEVEL 5 (Complex Components - Straps/Patches) ---

def service_level_5_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Блок 5: Основные компоненты комплекта."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎒 Комплект (Общий)", callback_data=f"order:complex:set:{order_id}")], # -> 5.1
            [InlineKeyboardButton(text="🛡️ Левый нарукавный", callback_data=f"order:complex:left_arm:{order_id}")],
            [InlineKeyboardButton(text="🛡️ Правый нарукавный", callback_data=f"order:complex:right_arm:{order_id}")],
            [InlineKeyboardButton(text="🏷️ Нагрудный ФИО", callback_data=f"order:complex:fio_start:{order_id}")], # -> 5.1
            [InlineKeyboardButton(text="🎖️ Нагрудный ВСР", callback_data=f"order:complex:vsr_start:{order_id}")], # Общая ветка для нагрудника с ВС
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )
def service_level_5_1_keyboard(order_id: int) ->InlineKeyboardMarkup:
    """Подраздел 5.1: Ввод персональных данных."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Ввести фамилию и инициалы", callback_data=f"order:input:fio1:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

def service_level_5_1_2_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 5.1.2: Изменение или подтверждение персональных данных."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Изменить фамилию и инициалы", callback_data=f"order:input:rename:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

def service_level_5_1_3_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 5.1.3: Изменение количества необходимых шевронов."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

def service_level_5_2_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 5.2: Нагрудный со званием и ФИО (Пример из логики)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👨‍✈️ С званием и ФИО", callback_data=f"order:complex:rank_fio:{order_id}")],
            [InlineKeyboardButton(text="🎖️ Нагрудный с ВСР (Альтернатива)", callback_data=f"order:complex:vsr2:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]

        ]
    )


# --- LEVEL 6 (Epaulettes/Stripes) ---

def service_level_6_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Основная клавиатура выбора элементов Эполет/Шевронов."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏷️ Повязка", callback_data=f"order:epaulettes:poi:{order_id}")], # Нет order_id, если это общая категория
            [InlineKeyboardButton(text="📐 Шеврон (Сложные)", callback_data=f"order:epaulettes:shevron:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

def service_level_6_1_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 6.1: Общая структура дежурств."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧭 Оперативный (Дежурный)", callback_data=f"order:epaulettes:ops_duty:{order_id}")], # -> 6.2
            [InlineKeyboardButton(text="🚨 Дежурный по:", callback_data=f"order:epaulettes:duty_dept:{order_id}")], # -> 6.3
            [InlineKeyboardButton(text="🧑‍🏫 Помощник", callback_data=f"order:epaulettes:assistant:{order_id}")], # -> 6.2 (В некоторых системах, может быть общим блоком)
            [InlineKeyboardButton(text="🧹 Дневальный по:", callback_data=f"order:epaulettes:dnevnik:{order_id}")], # -> 6.4
            [InlineKeyboardButton(text="P Руководитель занятий", callback_data=f"order:epaulettes:rukvod:{order_id}")], # -> 6.4
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

# --- LEVEL 6.2 (Unit Locations/Types) ---
def service_level_6_2_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 6.2: Выбор местоположения или подразделения."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Дежурный по Части", callback_data=f"order:epaulettes:parts:{order_id}")],
            [InlineKeyboardButton(text="🚁 Дежурный по Батальону", callback_data=f"order:epaulettes:battalion:{order_id}")],
            [InlineKeyboardButton(text="🍽️ Дежурный по Столовой", callback_data=f"order:epaulettes:canteen:{order_id}")],
            [InlineKeyboardButton(text="🌳 Дежурный по Парку", callback_data=f"order:epaulettes:park:{order_id}")],
            [InlineKeyboardButton(text="🚧 Дежурный по КПП", callback_data=f"order:epaulettes:cpp1:{order_id}")],
            [InlineKeyboardButton(text="🚧 Дежурный по КПП 2", callback_data=f"order:epaulettes:cpp2:{order_id}")],
            [InlineKeyboardButton(text="🏞️ Дежурный по Дивизиону", callback_data=f"order:epaulettes:division:{order_id}")],
            [InlineKeyboardButton(text="⚙️ Дежурный по Полигону", callback_data=f"order:epaulettes:polygon:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

# --- LEVEL 6.3 (Department Duty) ---

def service_level_6_3_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 6.3: Выбор конкретного дежурного или специалиста."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚧 Пом.дежурного по КПП", callback_data=f"order:epaulettes:pom_cpp1:{order_id}")],
            [InlineKeyboardButton(text="🚧 Пом.дежурного по КПП 2", callback_data=f"order:epaulettes:pom_cpp2:{order_id}")],
            [InlineKeyboardButton(text="🏞️ Пом.дежурного по Дивизиону", callback_data=f"order:epaulettes:pom_division:{order_id}")],
            [InlineKeyboardButton(text="⚙️ Пом.дежурного по Полигону", callback_data=f"order:epaulettes:pom_polygon:{order_id}")],
            [InlineKeyboardButton(text="🧭 Пом.оперативного дежурного", callback_data=f"order:epaulettes:ops_duty:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

def service_level_6_3_1_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 6.3.1: Детализация места для дежурного."""                              #не используется!!!!
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚧 КПП", callback_data=f"order:epaulettes:cpp:{order_id}")],
            [InlineKeyboardButton(text="🚧 КПП 2", callback_data=f"order:epaulettes:cpp2:{order_id}")],
            [InlineKeyboardButton(text="🏠 Части", callback_data=f"order:epaulettes:parts:{order_id}")],
            [InlineKeyboardButton(text="🏞️ Дивизиону", callback_data=f"order:epaulettes:division:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

# --- LEVEL 6.4 (Specific Duty Type) ---

def service_level_6_4_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Подраздел 6.4: Дневальный по """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌳 Дневальный по Роте", callback_data=f"order:epaulettes:dnevnik_squad:{order_id}")],
            [InlineKeyboardButton(text="🏞️ Дневальный по Парку", callback_data=f"order:epaulettes:park:{order_id}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору услуг", callback_data="menu:back")]
        ]
    )

# =========================================
# END OF KEYBOARDS.PY
# ВАЖНО: Требуется максимальное расширение handlers.py для обработки всех этих новых колбэков.
