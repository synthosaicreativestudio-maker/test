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
        from aiogram.filters.command import Command
    except Exception:
        return

    async def cmd_start(message: types.Message):
        u = message.from_user
        name = format_name(getattr(u, 'first_name', None), getattr(u, 'last_name', None), getattr(u, 'username', None))
        text = f"Добро пожаловать, {name}! 👋\n\nДля работы с системой необходимо пройти авторизацию сотрудника."
        
        # Создаем клавиатуру с Mini App кнопкой
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🔐 Авторизация сотрудника", 
                web_app=types.WebAppInfo(url="https://synthosaicreativestudio-maker.github.io/marketing/auth.html")
            )],
            [InlineKeyboardButton(text="ℹ️ О системе", callback_data="info")],
            [InlineKeyboardButton(text="📞 Поддержка", callback_data="support")]
        ])
        
        await message.reply(text, reply_markup=kb)

    async def handle_info(callback: types.CallbackQuery):
        """Обработчик информации о системе."""
        info_text = (
            "📋 **О системе**\n\n"
            "Это система авторизации и управления заявками для сотрудников.\n\n"
            "**Возможности:**\n"
            "• 🔐 Безопасная авторизация сотрудников\n"
            "• 🎫 Создание и отслеживание заявок\n"
            "• 📊 Просмотр статистики\n"
            "• 📱 Удобный интерфейс Mini App\n\n"
            "Для начала работы пройдите авторизацию сотрудника."
        )
        
        await callback.message.edit_text(info_text, parse_mode="Markdown")
        await callback.answer()

    async def handle_support(callback: types.CallbackQuery):
        """Обработчик поддержки."""
        support_text = (
            "📞 **Служба поддержки**\n\n"
            "Если у вас возникли проблемы с авторизацией или работой системы, "
            "обратитесь к администратору:\n\n"
            "📧 Email: support@company.com\n"
            "📱 Телефон: +7 (XXX) XXX-XX-XX\n\n"
            "Мы поможем решить любые вопросы! 🤝"
        )
        
        await callback.message.edit_text(support_text, parse_mode="Markdown")
        await callback.answer()

    dp.message.register(cmd_start, Command(commands=['start']))
    dp.callback_query.register(handle_info, lambda c: c.data == "info")
    dp.callback_query.register(handle_support, lambda c: c.data == "support")
