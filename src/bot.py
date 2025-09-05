"""Запуск бота и регистрация мини-приложений (miniapps).

Принята архитектура: каждый миниапп предоставляет функцию `setup(dp)` — она
регистрирует обработчики на переданный диспетчер.

Запуск:
  - Установите зависимости `pip install -r requirements.txt`
  - Поместите токен в файл `env` или в переменную окружения TELEGRAM_BOT_TOKEN
  - Запустите: `python3 -m src.bot`
"""
import os
import sys
import asyncio


def load_env(path='env'):
    data = {}
    if not os.path.exists(path):
        return data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                data[k.strip()] = v.strip()
    return data


def main():
    env = load_env('env')
    token = env.get('TELEGRAM_BOT_TOKEN') or os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print('Токен Telegram не найден. Установите TELEGRAM_BOT_TOKEN в env или в переменных окружения.')
        sys.exit(1)

    try:
        from aiogram import Bot, Dispatcher
        from aiogram.fsm.storage.memory import MemoryStorage
    except Exception:
        print('Не удалось импортировать aiogram v3. Установите зависимости: pip install -r requirements.txt')
        raise

    storage = MemoryStorage()
    bot = Bot(token=token)
    dp = Dispatcher(bot=bot, storage=storage)

    # Регистрация миниаппов
    from src.miniapps.registry import register_all
    register_all(dp)

    print('Запуск polling...')
    # Запускаем polling в asyncio
    try:
        # Используем встроенный run_polling (блокирующий) у Dispatcher
        dp.run_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        print('Остановлен')


if __name__ == '__main__':
    main()
