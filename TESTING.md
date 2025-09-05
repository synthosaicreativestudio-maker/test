# 🧪 Инструкция по тестированию Telegram Bot

## 📋 Быстрый тест

### 1. Локальный запуск бота
```bash
# Убедитесь что токен настроен в файле env
grep "TELEGRAM_TOKEN=" env

# Запуск бота
./run_bot.sh
```

### 2. Тестирование в Telegram
1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Должны появиться:
   - Приветственное сообщение с вашим именем
   - Reply клавиатура с кнопками:
     - 🔐 Пройти авторизацию (Mini App)
     - ℹ️ О системе
     - 📞 Поддержка

### 3. Тестирование Mini App
1. Нажмите кнопку "🔐 Пройти авторизацию"
2. Должен открыться Mini App: https://synthosaicreativestudio-maker.github.io/test/
3. Заполните форму и отправьте
4. Бот должен получить данные и ответить

## ⚙️ Настройка Bot Father

Если у вас еще нет бота:

1. Откройте @BotFather в Telegram
2. Отправьте `/newbot`
3. Выберите имя и username для бота
4. Скопируйте токен в файл `env`:
   ```
   TELEGRAM_TOKEN="your_bot_token_here"
   ```

### Настройка Mini App в боте

1. Отправьте @BotFather команду `/mybots`
2. Выберите вашего бота
3. Нажмите "Bot Settings" → "Menu Button"
4. Выберите "Configure Menu Button"
5. Введите:
   - **Text**: "Авторизация"
   - **URL**: https://synthosaicreativestudio-maker.github.io/test/

## 🔍 Проверка логов

Бот ведет логи в файл `bot.log`:
```bash
# Просмотр логов в реальном времени
tail -f bot.log

# Поиск ошибок
grep "ERROR" bot.log

# Поиск активности пользователей
grep "Пользователь" bot.log
```

## 🐛 Troubleshooting

### Бот не запускается
```bash
# Проверка токена
python3 -c "import os; print('Token found:', bool(os.getenv('TELEGRAM_TOKEN') or open('env').read().find('TELEGRAM_TOKEN=')))"

# Проверка зависимостей
pip list | grep aiogram
```

### Бот не отвечает
1. Проверьте что бот запущен и нет ошибок в логах
2. Убедитесь что токен правильный
3. Проверьте что у бота нет конфликтов с другими запущенными ботами

### Mini App не открывается
1. Проверьте URL в переменной `WEB_APP_AUTH_URL`
2. Убедитесь что GitHub Pages работает: https://synthosaicreativestudio-maker.github.io/test/
3. Настройте Menu Button в @BotFather

## ✅ Что должно работать

- [x] Приветственное сообщение
- [x] Reply клавиатура
- [x] Кнопки "О системе" и "Поддержка"
- [x] Обработка web_app_data
- [x] Логирование активности
- [ ] Интеграция с Google Sheets (в планах)

## 📞 Поддержка

Если что-то не работает:
1. Проверьте логи бота
2. Убедитесь что все зависимости установлены
3. Проверьте конфигурацию в файле `env`