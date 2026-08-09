RU
🚀 Название Бота: BetaListToDo_bot
License Python Version

📋 Обзор проекта
Этот бот является системой для взаимодействия с пользователями, позволяя им проходить многоступенчатый процесс заказа услуг через Telegram API. Система автоматически сохраняет все этапы сессии и выбранные детали в локальную базу данных SQLite. Бот реализует архитектуру "Service-Oriented Backend" (Сервисно-ориентированный бэкенд), где логика разделена на чистый репозиторий данных (database.py) и обработчики команд бота (service_entry.py).

✨ Функционал
✅ Автоматическая регистрация пользователей: Новый пользователь автоматически регистрируется в БД.
🛒 Многоэтапный процесс заказа: Пользователь последовательно выбирает услуги, подкатегории и детали, получая структурированный черновик заказа.
💾 Постоянное хранение данных: Все шаги сессии записываются в order_details, что позволяет восстанавливать заказ даже при выходе из бота.
🔑 Администрирование (В перспективе): Механизмы для администраторов и логирования действий пользователя.
🏗️ Технический стек
Компонент	Технология / Библиотека	Назначение
Язык программирования	Python 3.12+	Основной язык реализации.
Telegram API	aiogram (v3)	Обработка сообщений и колбэков от Telegram.
База данных	aiosqlite / SQLite	Асинхронная работа с локальной базой данных.
Конфигурация	python-dotenv (или переменные окружения)	Безопасное управление секретами (токены, пароли).
⚙️ Настройка проекта (Setup & Installation)
Следуйте этим шагам в терминале для полной настройки рабочего окружения.

1. Предварительные условия
Установленный Python 3.12+.
Доступ к рабочему каталогу проекта.
2. Создание и активация виртуального окружения (Virtual Environment)
Создайте изолированную среду для проекта, чтобы зависимости не конфликтовали с системным Python:

# Создаем venv
python -m venv venv

# Активируем venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1 

# Если вы используете Linux/macOS: source venv/bin/activate
3. Установка зависимостей
Установите все необходимые библиотеки для работы бота и базы данных:

pip install aiogram aiosqlite pathlib python-dotenv
(Если у вас есть файл requirements.txt, просто используйте pip install -r requirements.txt)

🔒 Конфигурация Секретов (Crucial Step!)
Важно: Никогда не храните токены и пароли прямо в коде! Используем переменные окружения.

Перед запуском бота вы должны установить все необходимые ключи в текущей сессии терминала.

В PowerShell (Windows):

$env:MY_TELEGRAM_BOT_TOKEN = "ВАШ_РЕАЛЬНЫЙ_ТОКЕН" 
# Устанавливаем пароли админов, если они используются
$env:ADMIN_PASSWORD = "ваш_админ_пароль"
🚀 Запуск Бота (Running the Bot)
После того как вы выполнили все шаги выше, вам нужно запустить главный файл из активированного виртуального окружения.

В терминале введите:

python main.py
Если всё успешно — бот должен подключиться к Telegram API и начать работать!

📁 Структура проекта (File Structure)
Понимание, где что находится, критически важно для дальнейшей разработки.

config.py: Центр управления. Содержит пути к БД и получает все секретные ключи из окружения.
database.py: Репозиторий данных. Здесь находится весь код взаимодействия с aiosqlite. В этом файле нет ни одной функции Telegram API — только SQL.
service_entry.py: Логика бота. Обрабатывает входящие сообщения и колбэки, вызывает методы из database.py, но ничего не знает о структуре БД (только о типах данных).
main.py: Точка входа. Инициализирует бот, подключает роутеры (dp.include_router(router)) и запускает цикл работы бота.
📚 Дальнейшее развитие (Future Scope)
 Реализация механизма администрирования через команды /admin и /user.
 Добавление рассылки уведомлений о завершении заказа.
 Интеграция с внешними API (например, для расчета стоимости услуги).

En
🚀 Project Name: BetaListToDo_bot (or the actual bot name)
License Python Version Status

📋 Overview
This project is a robust bot system designed to interact with users via the Telegram API, facilitating a multi-step service ordering process. The core feature is the ability to capture and persist all user choices and order details into a local SQLite database asynchronously. This structure implements a clear "Service-Oriented Backend" (SOB), cleanly separating the data layer from the bot's business logic.

✨ Key Features
✅ Automatic User Registration: New users are automatically registered in the DB upon first interaction.
🛒 Multi-Stage Workflow: Users select services, subcategories, and details sequentially, which builds a structured draft order record.
💾 Persistent State Management: All session steps are logged into order_details, ensuring that even if the bot restarts, the user's progress is saved and can be resumed.
🔑 Admin & Logging System: Includes mechanisms for administrators and comprehensive logging of user actions (currently implemented in key files).
🏗️ Technology Stack
Component	Technology / Library	Purpose
Language	Python 3.12+	Core implementation language.
Telegram API	aiogram (v3)	Handling Telegram messages, callbacks, and state management.
Database	aiosqlite / SQLite	Asynchronous database interaction for persistence.
Configuration	python-dotenv / Env Vars	Secure handling of sensitive credentials (tokens, passwords).
⚙️ Getting Started Guide
Follow these steps in your terminal to set up the working environment.

1. Prerequisites
Python 3.12+ installed on your system.
Access to a command-line terminal (PowerShell/Bash/CMD).
2. Setting up the Virtual Environment
It is highly recommended to use a virtual environment to prevent dependency conflicts with your global Python installation.

# Create the venv directory
python -m venv venv

# Activate the environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1 

# If using Linux/macOS: source venv/bin/activate
3. Installing Dependencies
Install all required libraries into your clean virtual environment:

pip install aiogram aiosqlite pathlib python-dotenv
🔒 Configuration Secrets (CRITICAL!)
SECURITY WARNING: NEVER hardcode tokens or passwords directly in your source code! Use environment variables always.

Before running the bot, you must set up all required keys in your terminal session.

Example for PowerShell (Windows): (Replace placeholders with your actual secrets)

$env:MY_TELEGRAM_BOT_TOKEN = "YOUR_REAL_BOT_TOKEN" 
# Set admin credentials if used by the bot logic
$env:ADMIN_PASSWORD = "your_admin_password"
🚀 Running the Bot
Once all steps are completed, you can start the bot from your activated terminal session.

In the terminal, run:

python main.py
If successful, the console should print logs confirming startup and successful connection to Telegram API.

📁 Project Structure & Architecture
Understanding the separation of concerns is key for development.

config.py: Configuration Hub. Handles loading paths (DB_PATH) and fetching all sensitive secrets from environment variables at startup time.
database.py: The Repository Layer. Contains all database interaction logic using aiosqlite. This module has zero knowledge of Telegram API calls—it only knows SQL queries.
service_entry.py: Business Logic/Controller. Handles the actual request/response cycle from the user (processing callbacks). It interprets the workflow and delegates data persistence to methods in database.py.
main.py: Entry Point. Initializes the bot, includes all routers (dp.include_router(router)), handles startup events, and initiates the long-running polling loop (await dp.start_polling(bot)).
🔭 Future Scope (Roadmap)
The following features are planned for future development:

 Implement full Admin Panel functionality via dedicated Telegram commands.
 Integrate external APIs (e.g., pricing calculators, calendar services).
 Develop advanced reporting and analytics based on stored logs.