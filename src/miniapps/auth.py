"""Миниапп: авторизация сотрудников через Google Sheets.

Поток:
- Пользователь нажимает кнопку 'Авторизоваться' (inline или команда) -> бот начинает FSM
- Запрашивает код сотрудника (только цифры)
- Запрашивает номер телефона: автоматически предлагает начать с '8' и ожидает ещё 10 цифр (итого 11 цифр)
- После получения данных ищет строку в Google Sheets по совпадению кода и номера.
- Если найдено — обновляет столбец D значением 'авторизован' и столбец E телеграм id, отправляет сообщение об успехе.
- Если не найдено — отправляет сообщение о неудаче.

Примечание: обновление Google Sheets возможно только при наличии service account JSON, путь к которому указывается в `env` (GOOGLE_SERVICE_ACCOUNT_FILE). Без него бот уведомит о невозможности обновления и запишет ошибку в `logs/general_log.md`.
"""
from typing import Optional, Tuple
import os
import csv
import io
import urllib.request


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


def setup(dp):
    try:
        from aiogram import types
        from aiogram.fsm.context import FSMContext
        from aiogram.fsm.state import StatesGroup, State
    except Exception:
        return

    class AuthStates(StatesGroup):
        waiting_code = State()
        waiting_phone = State()

    async def start_auth_cb(callback: types.CallbackQuery):
        await callback.message.answer('Введите код сотрудника (только цифры):')
        await AuthStates.waiting_code.set()

    async def cmd_start(message: types.Message):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('Авторизоваться', callback_data='auth_start'))
        u = message.from_user
        name = (getattr(u, 'first_name', '') or getattr(u, 'username', '') or 'пользователь')
        await message.reply(f'Уважаемый {name}, пройдите простую регистрацию', reply_markup=kb)

    async def handle_code(message: types.Message, state: FSMContext):
        code = message.text.strip()
        if not validate_employee_code(code):
            await message.reply('Код должен состоять только из цифр. Повторите ввод:')
            return
        await state.update_data(code=code)
        await message.reply("Введите номер телефона. Введите 10 цифр после первой '8' (например 89827701055):")
        await AuthStates.waiting_phone.set()

    async def handle_phone(message: types.Message, state: FSMContext):
        phone = message.text.strip()
        if phone.startswith('+'):
            phone = phone[1:]
        if phone.isdigit() and len(phone) == 10:
            phone = '8' + phone
        if not validate_phone(phone):
            await message.reply("Неверный формат телефона. Ожидается 11 цифр, начинается с 8. Попробуйте снова:")
            return
        data = await state.get_data()
        code = data.get('code')
        tg_id = message.from_user.id
        ok, user_msg = find_and_mark_authorization(code, phone, tg_id)
        await message.reply(user_msg)
        await state.clear()

    dp.message.register(cmd_start, commands=['start'])
    dp.callback_query.register(start_auth_cb, lambda c: c.data == 'auth_start')
    dp.message.register(handle_code, state=AuthStates.waiting_code)
    dp.message.register(handle_phone, state=AuthStates.waiting_phone)
