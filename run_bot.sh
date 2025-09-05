#!/bin/bash

# Скрипт запуска Telegram бота
# Автоматически устанавливает зависимости и запускает бота

echo "🚀 Запуск Telegram бота для авторизации сотрудников..."
echo "📅 $(date)"
echo

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8 или выше."
    exit 1
fi

# Проверка наличия файла env
if [ ! -f "env" ]; then
    echo "⚠️  Файл env не найден."
    echo "📝 Скопируйте env.example в env и заполните TELEGRAM_BOT_TOKEN"
    exit 1
fi

# Проверка токена бота
if ! grep -q "TELEGRAM_BOT_TOKEN=" env || (grep "TELEGRAM_BOT_TOKEN=" env | grep -q "TELEGRAM_BOT_TOKEN=$\|TELEGRAM_BOT_TOKEN=\"\"\|TELEGRAM_BOT_TOKEN=your_bot_token_here"); then
    echo "❌ TELEGRAM_BOT_TOKEN не настроен в файле env"
    echo "🔧 Получите токен у @BotFather и добавьте в файл env:"
    echo "   TELEGRAM_BOT_TOKEN=your_bot_token_here"
    exit 1
fi

# Создание виртуального окружения если не существует
if [ ! -d ".venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv .venv
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source .venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install -r requirements.txt

# Запуск бота
echo "🤖 Запуск бота..."
echo "💡 Для остановки нажмите Ctrl+C"
echo

python3 src/bot.py