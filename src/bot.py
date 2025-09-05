#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot для авторизации сотрудников
Использует aiogram v3 и Telegram Mini App
Интеграция с Google Sheets для проверки сотрудников
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram import F
import gspread
from google.oauth2.service_account import Credentials

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

# Google Sheets конфигурация
SHEET_ID = '1_SB04LMuGB7ba3aog2xxN6N3g99ZfOboT-vdWXxrh_8'
WORKSHEET_NAME = 'список сотрудников для авторизации'
CREDENTIALS_FILE = 'credentials.json'

# Инициализация Google Sheets клиента
gc = None
worksheet = None

async def init_google_sheets():
    """Инициализация подключения к Google Sheets"""
    global gc, worksheet
    try:
        # Области доступа для Google Sheets API
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Загрузка учетных данных
        credentials = Credentials.from_service_account_file(
            CREDENTIALS_FILE, 
            scopes=scopes
        )
        
        # Авторизация клиента
        gc = gspread.authorize(credentials)
        
        # Открытие таблицы
        sheet = gc.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        
        logger.info(f"✅ Google Sheets подключен: {sheet.title}")
        logger.info(f"📋 Рабочий лист: {WORKSHEET_NAME}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к Google Sheets: {e}")
        return False

async def find_employee(employee_code: str, phone: str) -> Dict[str, Any]:
    """Поиск сотрудника в Google Sheets по коду и телефону"""
    try:
        if not worksheet:
            return {
                'success': False,
                'message': 'Ошибка подключения к базе данных сотрудников'
            }
        
        # Получаем все записи
        records = worksheet.get_all_records()
        logger.info(f"📊 Найдено записей в таблице: {len(records)}")
        
        # Поиск сотрудника
        for i, record in enumerate(records, start=2):  # start=2 т.к. первая строка - заголовки
            # Проверяем код и телефон (приводим к строкам для сравнения)
            record_code = str(record.get('Код сотрудника', '')).strip()
            record_phone = str(record.get('Телефон', '')).strip()
            record_name = str(record.get('Имя', '')).strip()
            record_status = str(record.get('Статус', '')).strip()
            
            logger.info(f"🔍 Проверка записи {i}: код={record_code}, телефон={record_phone}")
            
            if record_code == employee_code and record_phone == phone:
                logger.info(f"✅ Найден сотрудник: {record_name}")
                
                # Обновляем статус авторизации
                try:
                    worksheet.update_cell(i, 4, 'авторизован')  # Колонка D - Статус
                    worksheet.update_cell(i, 5, datetime.now().strftime('%d.%m.%Y %H:%M'))  # Колонка E - Дата авторизации
                    logger.info(f"📝 Обновлен статус для {record_name}")
                except Exception as update_error:
                    logger.error(f"⚠️ Ошибка обновления статуса: {update_error}")
                
                return {
                    'success': True,
                    'employee_name': record_name,
                    'message': f'Авторизация успешна!\n👤 Сотрудник: {record_name}\n📱 Телефон: {phone}\n🆔 Код: {employee_code}'
                }
        
        logger.warning(f"❌ Сотрудник не найден: код={employee_code}, телефон={phone}")
        return {
            'success': False,
            'message': f'Сотрудник с кодом {employee_code} и телефоном {phone} не найден в базе данных.\n\nОбратитесь к администратору для добавления в систему.'
        }
        
    except Exception as e:
        logger.error(f"💥 Ошибка поиска сотрудника: {e}")
        return {
            'success': False,
            'message': f'Ошибка при проверке данных: {str(e)}\n\nПопробуйте позже или обратитесь в поддержку.'
        }

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
        logger.info(f"📱 Получены данные от Mini App: {webapp_data}")
        
        # Парсим JSON данные
        try:
            auth_data = json.loads(webapp_data)
        except json.JSONDecodeError as e:
            logger.error(f"❌ Ошибка парсинга JSON: {e}")
            await message.reply(
                "❌ **Ошибка обработки данных**\n\n"
                "Некорректный формат данных. Попробуйте еще раз.",
                parse_mode="Markdown"
            )
            return
        
        # Извлекаем данные
        employee_code = str(auth_data.get('employee_code', '')).strip()
        phone = str(auth_data.get('phone', '')).strip()
        user_id = auth_data.get('user_id')
        username = auth_data.get('username', '')
        first_name = auth_data.get('first_name', '')
        last_name = auth_data.get('last_name', '')
        
        logger.info(f"👤 Данные авторизации: код={employee_code}, телефон={phone}, user_id={user_id}")
        
        # Валидация данных
        if not employee_code or not phone:
            await message.reply(
                "❌ **Некорректные данные**\n\n"
                "Убедитесь, что заполнены все поля:"
                "\n• Код сотрудника"
                "\n• Номер телефона",
                parse_mode="Markdown"
            )
            return
        
        # Показываем процесс проверки
        processing_msg = await message.reply(
            "🔄 **Проверка данных...**\n\n"
            f"👤 Код сотрудника: `{employee_code}`\n"
            f"📱 Телефон: `{phone}`\n\n"
            "⏳ Поиск в базе данных сотрудников...",
            parse_mode="Markdown"
        )
        
        # Поиск сотрудника в Google Sheets
        result = await find_employee(employee_code, phone)
        
        # Удаляем сообщение о процессе
        await processing_msg.delete()
        
        if result['success']:
            # Успешная авторизация
            await message.reply(
                f"✅ **{result['message']}**\n\n"
                f"🎉 Добро пожаловать в систему!\n"
                f"📅 Время авторизации: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                f"ℹ️ Теперь вы можете пользоваться всеми функциями системы.",
                parse_mode="Markdown"
            )
            
            # Логируем успешную авторизацию
            logger.info(
                f"✅ Успешная авторизация: {result.get('employee_name', 'Unknown')} "
                f"(user_id: {user_id}, код: {employee_code})"
            )
            
        else:
            # Ошибка авторизации
            await message.reply(
                f"❌ **Ошибка авторизации**\n\n"
                f"{result['message']}\n\n"
                f"📞 **Поддержка:** обратитесь к администратору",
                parse_mode="Markdown"
            )
            
            # Логируем неудачную попытку
            logger.warning(
                f"❌ Неудачная авторизация: код={employee_code}, телефон={phone}, "
                f"user_id={user_id}, username={username}"
            )
        
    except Exception as e:
        logger.error(f"💥 Критическая ошибка обработки данных Mini App: {e}")
        await message.reply(
            "💥 **Критическая ошибка**\n\n"
            "Произошла неожиданная ошибка при обработке данных.\n"
            "Попробуйте позже или обратитесь в техническую поддержку.\n\n"
            f"🆔 ID ошибки: `{str(e)[:100]}`",
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
        # Инициализация Google Sheets
        sheets_connected = await init_google_sheets()
        if not sheets_connected:
            logger.error("⚠️ Бот запущен без подключения к Google Sheets")
        
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