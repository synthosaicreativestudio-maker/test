"""Miniapp: обработка данных от Telegram Mini App авторизации.

Этот модуль обрабатывает данные, отправленные из Telegram Mini App
через web_app_data и выполняет авторизацию сотрудников.
"""
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


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
        from src.miniapps.auth import find_and_mark_authorization
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