#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot для авторизации сотрудников
Использует aiogram v3 и Telegram Mini App
"""

import asyncio
import logging
import os
import sys
from typing import Any, Dict

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram import F

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Получение конфигурации из переменных окружения
def load_env_var(var_name: str, default_value: str = None) -> str:
    """Загружает переменную окружения из файла env или системных переменных"""
    try:
        # Пробуем загрузить из файла env
        if os.path.exists('env'):
            with open('env', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        if key.strip() == var_name:
                            # Убираем кавычки если есть
                            value = value.strip().strip('"\'')
                            return value
    except Exception as e:
        logger.warning(f"Ошибка чтения файла env: {e}")
    
    # Fallback к системным переменным
    return os.getenv(var_name, default_value)

# Конфигурация
BOT_TOKEN = load_env_var('TELEGRAM_BOT_TOKEN') or load_env_var('TELEGRAM_TOKEN')
WEB_APP_AUTH_URL = load_env_var('WEB_APP_AUTH_URL', 'https://synthosaicreativestudio-maker.github.io/test/')

if not BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не найден в переменных окружения!")
    sys.exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def format_name(first_name: str, last_name: str, username: str) -> str:
    """Форматирует имя пользователя для отображения"""
    parts = []
    if first_name:
        parts.append(first_name)
    if last_name:
        parts.append(last_name)
    
    if parts:
        result = ' '.join(parts)
        if username:
            result += f" (@{username})"
        return result
    elif username:
        return f"@{username}"
    else:
        return "Пользователь"

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start с приветственным сообщением"""
    user = message.from_user
    user_name = format_name(
        user.first_name, 
        user.last_name, 
        user.username
    )
    
    # Приветственное сообщение
    welcome_text = f"👋 Добро пожаловать, {user_name}!\n\n"
    welcome_text += "🔐 **Система авторизации сотрудников**\n\n"
    welcome_text += "Для использования системы необходимо пройти авторизацию.\n"
    welcome_text += "Нажмите кнопку ниже для открытия формы авторизации."
    
    # Создание reply клавиатуры с кнопкой Mini App
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🔐 Пройти авторизацию",
                web_app=WebAppInfo(url=WEB_APP_AUTH_URL)
            )],
            [KeyboardButton(text="ℹ️ О системе")],
            [KeyboardButton(text="📞 Поддержка")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие..."
    )
    
    await message.reply(
        welcome_text, 
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
    logger.info(f"Пользователь {user.id} ({user_name}) запустил бота")

@dp.message(F.text == "ℹ️ О системе")
async def info_about_system(message: types.Message):
    """Информация о системе"""
    info_text = (
        "📋 **О системе авторизации**\n\n"
        "Эта система предназначена для авторизации сотрудников "
        "с использованием современных технологий:\n\n"
        "🔹 Telegram Mini App интерфейс\n"
        "🔹 Валидация в реальном времени\n"
        "🔹 Безопасная передача данных\n"
        "🔹 Интеграция с Google Sheets\n\n"
        "Для авторизации используйте кнопку **'🔐 Пройти авторизацию'**"
    )
    
    await message.reply(info_text, parse_mode="Markdown")

@dp.message(F.text == "📞 Поддержка")
async def support_info(message: types.Message):
    """Информация о поддержке"""
    support_text = (
        "📞 **Техническая поддержка**\n\n"
        "Если у вас возникли проблемы с авторизацией:\n\n"
        "1️⃣ Проверьте правильность ввода кода сотрудника\n"
        "2️⃣ Убедитесь в корректности номера телефона\n"
        "3️⃣ Обратитесь к администратору системы\n\n"
        "💡 Код сотрудника должен содержать только цифры\n"
        "💡 Номер телефона: 11 цифр, начинающихся с 8"
    )
    
    await message.reply(support_text, parse_mode="Markdown")

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    """Обработчик данных от Telegram Mini App"""
    try:
        # Получаем данные от Mini App
        webapp_data = message.web_app_data.data
        logger.info(f"Получены данные от Mini App: {webapp_data}")
        
        # Здесь будет обработка данных авторизации
        # Пока что просто подтверждаем получение
        await message.reply(
            "✅ Данные получены!\n\n"
            "🔄 Обработка авторизации...\n"
            "📋 Проверка данных сотрудника в системе...",
            parse_mode="Markdown"
        )
        
        # TODO: Добавить интеграцию с Google Sheets
        # TODO: Добавить валидацию данных
        # TODO: Добавить обновление статуса авторизации
        
    except Exception as e:
        logger.error(f"Ошибка обработки данных Mini App: {e}")
        await message.reply(
            "❌ **Ошибка обработки данных**\n\n"
            "Попробуйте еще раз или обратитесь в поддержку.",
            parse_mode="Markdown"
        )

@dp.message()
async def handle_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    help_text = (
        "🤔 Не понимаю эту команду.\n\n"
        "Используйте кнопки меню:\n"
        "🔹 **🔐 Пройти авторизацию** - для входа в систему\n"
        "🔹 **ℹ️ О системе** - информация о системе\n"
        "🔹 **📞 Поддержка** - помощь и инструкции\n\n"
        "Или введите /start для начала работы."
    )
    
    await message.reply(help_text, parse_mode="Markdown")

async def main():
    """Основная функция запуска бота"""
    logger.info("🚀 Запуск Telegram бота...")
    logger.info(f"🔗 Mini App URL: {WEB_APP_AUTH_URL}")
    
    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        logger.info(f"✅ Бот запущен: @{bot_info.username} ({bot_info.first_name})")
        
        # Запускаем бота
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        sys.exit(1)