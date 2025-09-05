"""Миниапп: приветствие и простая регистрация.

Обработчик `/start` отправляет пользователю сообщение:
"Уважаемый <имя>, пройдите простую регистрацию"

Функция `format_name` выделена для тестирования и гарантирует безопасную подстановку имени.
"""

def format_name(first_name: str = None, last_name: str = None, username: str = None) -> str:
    """Вернуть предпочтительное отображаемое имя пользователя."""
    parts = []
    if first_name:
        parts.append(first_name)
    if last_name:
        # Если last_name совпадает с first_name или пуст, не дублируем
        if last_name not in parts:
            parts.append(last_name)
    if parts:
        return ' '.join(parts)
    if username:
        return username
    return 'пользователь'


def setup(dp):
    try:
        from aiogram import types
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    except Exception:
        return

    async def cmd_start(message: types.Message):
        u = message.from_user
        name = format_name(getattr(u, 'first_name', None), getattr(u, 'last_name', None), getattr(u, 'username', None))
        text = f"Уважаемый {name}, пройдите простую регистрацию"
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Авторизоваться', callback_data='auth_start')]])
        await message.reply(text, reply_markup=kb)

    dp.message.register(cmd_start, commands=['start'])
