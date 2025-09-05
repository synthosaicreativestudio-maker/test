"""Миниапп: приветствие и Mini App авторизация.

Обработчик `/start` отправляет пользователю приветствие с кнопкой
запуска Telegram Mini App для авторизации сотрудников.
"""
import os

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


def load_env_var(key: str, default: str = "") -> str:
    """Загружает переменную из env файла или окружения."""
    # Сначала пробуем из переменных окружения
    value = os.environ.get(key)
    if value:
        return value
    
    # Если нет, читаем из env файла
    try:
        with open('env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith(f'{key}='):
                    return line.split('=', 1)[1].strip('"\'')
    except FileNotFoundError:
        pass
    
    return default


def setup(dp):
    try:
        from aiogram import types
        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
        from aiogram.filters.command import Command
    except Exception:
        return

    async def cmd_start(message: types.Message):
        u = message.from_user
        name = format_name(getattr(u, 'first_name', None), getattr(u, 'last_name', None), getattr(u, 'username', None))
        
        # Получаем URL Mini App из конфигурации
        miniapp_url = load_env_var('WEB_APP_AUTH_URL', 'https://synthosaicreativestudio-maker.github.io/marketing/auth_universal.html')
        
        text = f"Добро пожаловать, {name}! 👋\n\n"
        text += "🔐 Для работы с системой необходимо пройти авторизацию сотрудника.\n\n"
        text += "Нажмите кнопку ниже для открытия формы авторизации."
        
        # Создаем reply клавиатуру с Mini App кнопкой
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(
                    text="🔐 Авторизация сотрудника",
                    web_app=WebAppInfo(url=miniapp_url)
                )],
                [KeyboardButton(text="ℹ️ О системе")],
                [KeyboardButton(text="📞 Поддержка")]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
        
        await message.reply(text, reply_markup=keyboard)

    async def handle_text_messages(message: types.Message):
        """Обработчик текстовых сообщений для reply кнопок."""
        text = message.text
        
        if text == "ℹ️ О системе":
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
            await message.reply(info_text, parse_mode="Markdown")
            
        elif text == "📞 Поддержка":
            support_text = (
                "📞 **Служба поддержки**\n\n"
                "Если у вас возникли проблемы с авторизацией или работой системы, "
                "обратитесь к администратору:\n\n"
                "📧 Email: support@company.com\n"
                "📱 Телефон: +7 (XXX) XXX-XX-XX\n\n"
                "Мы поможем решить любые вопросы! 🤝"
            )
            await message.reply(support_text, parse_mode="Markdown")

    dp.message.register(cmd_start, Command(commands=['start']))
    dp.message.register(handle_text_messages, lambda message: message.text in ["ℹ️ О системе", "📞 Поддержка"])
