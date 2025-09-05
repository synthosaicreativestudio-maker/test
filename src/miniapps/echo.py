"""Пример миниаппа: простая команда /echo."""


def setup(dp):
    try:
        from aiogram import types
    except Exception:
        return

    async def echo_cmd(message: types.Message):
        # В aiogram v3 заменяем get_args
        args = ''
        if message.text:
            parts = message.text.split(maxsplit=1)
            args = parts[1] if len(parts) > 1 else ''
        text = args or message.text or 'Echo'
        await message.reply(text)

    dp.message.register(echo_cmd, commands=['echo'])
