"""Miniapp: обработка данных от Telegram Mini App авторизации.

Этот модуль обрабатывает данные, отправленные из Telegram Mini App
через web_app_data и выполняет авторизацию сотрудников.
"""
import json
import logging
import os
import csv
import io
import urllib.request
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


def validate_employee_code(code: str) -> bool:
    return code.isdigit() and len(code) > 0


def validate_phone(phone: str) -> bool:
    # Ожидаем телефон в формате 8XXXXXXXXXX (11 цифр, начинается с 8)
    if not phone or not phone.isdigit():
        return False
    return len(phone) == 11 and phone.startswith('8')


def find_row_in_sheet_local(csv_text: str, code: str, phone: str) -> Optional[int]:
    """Ищет строку в CSV по обоим полям и возвращает индекс (1-based) строки если найдено."""
    reader = csv.reader(io.StringIO(csv_text))
    for idx, row in enumerate(reader, start=1):
        # Проверяем, есть ли оба значения в одной строке
        if code in row and phone in row:
            return idx
    return None


def try_fetch_public_csv(sheet_id: str) -> Optional[str]:
    """Пытается скачать публичную версию таблицы в CSV (если доступна)."""
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.read().decode('utf-8')
    except Exception:
        return None


def update_sheet_with_gspread(sheet_id: str, row_index: int, telegram_id: int) -> Tuple[bool, str]:
    """Попытаться обновить столбцы D (4) и E (5) указанной строки через gspread.

    Возвращает (успех, сообщение).
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception as e:
        return False, f"gspread не доступен: {e}"

    sa_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE') or os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE') or ''
    if not sa_file or not os.path.exists(sa_file):
        return False, 'Service account JSON не найден. Укажите GOOGLE_SERVICE_ACCOUNT_FILE в env.'

    try:
        creds = Credentials.from_service_account_file(sa_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(sheet_id)
        ws = sh.sheet1
        # Записать в D и E указанной строки
        ws.update_cell(row_index, 4, 'авторизован')
        ws.update_cell(row_index, 5, str(telegram_id))
        return True, 'Обновлено в Google Sheets'
    except Exception as e:
        return False, f'Ошибка при обновлении Google Sheets: {e}'


def append_general_log(message: str):
    try:
        from datetime import datetime
        path = os.path.join(os.getcwd(), 'logs', 'general_log.md')
        with open(path, 'a', encoding='utf-8') as f:
            ts = datetime.now().astimezone().isoformat()
            f.write(f"\n---\nДата: {ts}\nАвтор: Система\nДействие: log\nСообщение: {message}\n---\n")
    except Exception:
        pass


def find_and_mark_authorization(code: str, phone: str, telegram_id: int) -> Tuple[bool, str]:
    """Основная логика: ищем код+телефон и пытаемся пометить авторизацию.

    Возвращает (успех, сообщение для пользователя).
    """
    sheet_id = os.environ.get('SHEET_ID')
    if not sheet_id:
        return False, 'Конфигурация SHEET_ID не найдена.'

    # Попытаться получить публичную CSV
    csv_text = try_fetch_public_csv(sheet_id)
    row_idx = None
    if csv_text:
        row_idx = find_row_in_sheet_local(csv_text, code, phone)

    # Если не найдено в публичной версии, можно попробовать использовать gspread на полной таблице
    if row_idx is None:
        # Если gspread доступен и service account настроен, получить все значения и искать
        try:
            import gspread
            from google.oauth2.service_account import Credentials
            sa_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE')
            if sa_file and os.path.exists(sa_file):
                creds = Credentials.from_service_account_file(sa_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
                gc = gspread.authorize(creds)
                sh = gc.open_by_key(sheet_id)
                ws = sh.sheet1
                all_values = ws.get_all_values()
                for idx, row in enumerate(all_values, start=1):
                    if code in row and phone in row:
                        row_idx = idx
                        break
        except Exception:
            # Не удалось использовать gspread
            pass

    if row_idx is None:
        append_general_log(f'Авторизация не найдена для code={code} phone={phone} telegram_id={telegram_id}')
        return False, 'Пользователь с такими данными не найден'

    # Попытаться обновить через gspread
    ok, msg = update_sheet_with_gspread(sheet_id, row_idx, telegram_id)
    if ok:
        append_general_log(f'Пользователь авторизован: code={code} phone={phone} telegram_id={telegram_id} row={row_idx}')
        return True, 'Вы успешно авторизованы'
    else:
        append_general_log(f'Не удалось обновить Google Sheets: {msg}')
        # Если мы нашли строку, но не можем обновить, всё равно считаем неуспехом для пользователя
        return False, f'Не удалось завершить авторизацию: {msg}'


def parse_webapp_data(data: str) -> Dict[str, Any]:
    """Парсит данные от Telegram Mini App."""
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse webapp data: {data}")
        return {}


def setup(dp):
    try:
        from aiogram import types, F
    except Exception as e:
        logger.error(f"Failed to import dependencies: {e}")
        return

    async def handle_webapp_data(message: types.Message):
        """Обработчик данных от Telegram Mini App."""
        if not message.web_app_data:
            return
        
        try:
            # Парсим данные от Mini App
            webapp_data = parse_webapp_data(message.web_app_data.data)
            
            if not webapp_data:
                await message.reply("❌ Ошибка: не удалось обработать данные авторизации.")
                return
            
            # Извлекаем данные авторизации
            code = webapp_data.get('code')
            phone = webapp_data.get('phone')
            user_id = webapp_data.get('user_id') or message.from_user.id
            first_name = webapp_data.get('first_name') or message.from_user.first_name
            
            if not code or not phone:
                await message.reply("❌ Ошибка: не указан код сотрудника или номер телефона.")
                return
            
            logger.info(f"Mini App auth attempt: user_id={user_id}, code={code}, phone={phone}")
            
            # Выполняем авторизацию
            success, result_message = find_and_mark_authorization(code, phone, user_id)
            
            if success:
                welcome_msg = f"✅ {result_message}\\n\\n"
                welcome_msg += f"Добро пожаловать, {first_name}! 🎉\\n"
                welcome_msg += "Теперь у вас есть доступ к функциям сотрудника."
                
                # Создаем клавиатуру с дополнительными функциями
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text="📊 Мои данные", callback_data="employee_profile")],
                    [types.InlineKeyboardButton(text="🎫 Создать заявку", callback_data="create_ticket")],
                    [types.InlineKeyboardButton(text="📋 Мои заявки", callback_data="my_tickets")]
                ])
                
                await message.reply(welcome_msg, reply_markup=keyboard)
                
            else:
                error_msg = f"❌ {result_message}\\n\\n"
                error_msg += "Проверьте правильность введенных данных и попробуйте снова."
                
                # Кнопка для повторной попытки
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text="🔄 Попробовать снова", callback_data="auth_retry")]
                ])
                
                await message.reply(error_msg, reply_markup=keyboard)
                
        except Exception as e:
            logger.error(f"Error processing webapp data: {e}")
            await message.reply("❌ Произошла ошибка при обработке авторизации. Попробуйте позже.")

    async def handle_auth_retry(callback: types.CallbackQuery):
        """Обработчик повторной попытки авторизации."""
        # Отправляем Mini App снова
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text="🔐 Авторизация сотрудника", 
                web_app=types.WebAppInfo(url="https://synthosaicreativestudio-maker.github.io/marketing/auth.html")
            )]
        ])
        
        await callback.message.edit_text(
            "🔐 Для авторизации откройте форму и введите свои данные:",
            reply_markup=keyboard
        )
        
        await callback.answer()

    async def handle_employee_actions(callback: types.CallbackQuery):
        """Обработчик действий авторизованных сотрудников."""
        action = callback.data
        
        if action == "employee_profile":
            await callback.message.edit_text(
                f"👤 Профиль сотрудника\\n"
                f"ID: {callback.from_user.id}\\n"
                f"Имя: {callback.from_user.first_name or 'Не указано'}\\n"
                f"Username: @{callback.from_user.username or 'Не указан'}\\n"
                f"Статус: ✅ Авторизован"
            )
        
        elif action == "create_ticket":
            await callback.message.edit_text(
                "🎫 Создание заявки\\n\\n"
                "Для создания заявки используйте команду:\\n"
                "/ticket <описание проблемы>\\n\\n"
                "Пример: /ticket Не работает принтер в офисе"
            )
        
        elif action == "my_tickets":
            await callback.message.edit_text(
                "📋 Ваши заявки\\n\\n"
                "Здесь будут отображаться ваши активные заявки.\\n"
                "Пока у вас нет активных заявок."
            )
        
        await callback.answer()

    # Регистрируем обработчики
    dp.message.register(handle_webapp_data, F.web_app_data)
    dp.callback_query.register(handle_auth_retry, lambda c: c.data == "auth_retry")
    dp.callback_query.register(handle_employee_actions, lambda c: c.data in ["employee_profile", "create_ticket", "my_tickets"])