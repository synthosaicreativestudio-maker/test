# Marketing Test Project v1.0.0

[![Deploy to GitHub Pages](https://github.com/synthosaicreativestudio-maker/test/actions/workflows/deploy.yml/badge.svg)](https://github.com/synthosaicreativestudio-maker/test/actions/workflows/deploy.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen?logo=github)](https://synthosaicreativestudio-maker.github.io/test/)
[![Website Status](https://img.shields.io/website?url=https%3A%2F%2Fsynthosaicreativestudio-maker.github.io%2Ftest%2F)](https://synthosaicreativestudio-maker.github.io/test/)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/synthosaicreativestudio-maker/test)
[![Mobile Ready](https://img.shields.io/badge/Mobile-100%25%20Compatible-brightgreen)](https://synthosaicreativestudio-maker.github.io/test/)
[![Auto Deploy](https://img.shields.io/badge/Deploy-Automatic-brightgreen)](https://github.com/synthosaicreativestudio-maker/test/actions)

**Production-ready** проект для автоматизации маркетинга с интеграцией Telegram бота, Context7 MCP, Google Sheets и веб-интерфейсом.

## 🚀 **Live Demo & Deployment**

### 🌐 **Доступные ресурсы:**
- **🎯 Веб-интерфейс**: [https://synthosaicreativestudio-maker.github.io/test/](https://synthosaicreativestudio-maker.github.io/test/)
- **📱 Telegram Mini App**: Авторизация через веб-интерфейс
- **📋 Документация**: [DEPLOYMENT.md](DEPLOYMENT.md) - полное руководство по деплою
- **🔄 CI/CD Status**: Автоматический деплой при каждом push в `main`

### ✅ **Статус развертывания:**
- **Автоматические тесты**: ✅ Проходят при каждом коммите
- **GitHub Pages**: ✅ Автоматический деплой веб-интерфейса  
- **Mobile compatibility**: ✅ 100% совместимость с мобильными устройствами
- **Real-time updates**: ✅ Обновления в реальном времени

## 🚀 Быстрый старт и деплой

**[📋 Полная инструкция по деплою](DEPLOYMENT.md)** - настройка GitHub Actions, Docker, автоматический и ручной деплой

## Функциональность

### Журналы проекта и утилита добавления записей

В репозитории добавлены журналы и скрипт для удобной работы с ними:

- `logs/rules_log.md` — журнал правил проекта
- `logs/project_log.md` — журнал проекта (changelog, milestones)
- `logs/bot_functions_log.md` — журнал основных функций бота
- `scripts/add_log.py` — утилита для добавления записей в любой из журналов
- `logs/general_log.md` — общий лог для оперативных заметок и решений

### Файлы окружения и секреты

Файл `env` используется для хранения указаний на логи и настроек проекта (включая URL репозитория). По умолчанию в `env` указана ссылка на репозиторий:

```
GITHUB_REPO=https://github.com/synthosaicreativestudio-maker/test
```

Файл `env` не должен коммититься в публичные репозитории. В репозитории также добавлен `env.example` — используйте его как шаблон и заполните реальные токены локально.

### Google Sheets и авторизация

Для автоматической записи статуса авторизации в Google Sheets требуется сервисный аккаунт с правами на редактирование таблицы. Поместите JSON учетных данных в файл и укажите путь в `env`:

```
GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
SHEET_ID=1_SB04LMuGB7ba3aog2xxN6N3g99ZfOboT-vdWXxrh_8
```

### Context7 MCP Integration

Проект использует Context7 как MCP-сервер для обогащения подсказок актуальной документацией.
Вместо установки Node.js-пакета, мы используем HTTP-интеграцию. Добавлен модуль `src/mcp/context7_client.py`.

Чтобы включить интеграцию:
1) Укажите URL вашего Context7 сервера в `env` переменной `CONTEXT7_URL`.
2) Установите зависимости: `pip install -r requirements.txt` (включён `httpx`).
3) Используйте в коде:

```python
from src.mcp.context7_client import Context7Client
client = Context7Client(CONTEXT7_URL)
res = await client.search('how to use aiogram')
```

### Local MCP

Если вы поместили реализацию MCP в проект (например `mcp_context_v7.py`), используйте обёртку `src/mcp/local_context.py` для взаимодействия:

```python
from src.mcp.local_context import create_thread_for_user, append_message, get_context_summary
tid = create_thread_for_user('telegram_123')
append_message(tid, 'user', 'Привет')
print(get_context_summary(tid))
```

### 📱 Telegram Mini App авторизация

Проект использует Telegram Mini App для удобной авторизации сотрудников:

- **Reply клавиатура** с кнопкой запуска Mini App
- **URL конфигурируется** через `WEB_APP_AUTH_URL` в `env`
- **Автоматическая обработка** данных через `webapp.py` модуль
- **Валидация в реальном времени** кода сотрудника и телефона
- **Интеграция с MainButton** Telegram для улучшенного UX

По умолчанию используется: `https://synthosaicreativestudio-maker.github.io/test/`

### Web UI

Добавлена папка `web_ui` с готовыми стилями `styles.css` и примером страницы авторизации `index.html`.
Это можно использовать как миниапп-страницу Telegram Web App или как отдельную страницу авторизации.

Чтобы запустить локально:

```bash
python3 scripts/serve_web.py --port 8000
# затем открыть http://localhost:8000/
```

## Примеры использования

```bash
python3 scripts/add_log.py --log logs/project_log.md --author "Иван" --type add --message "Добавил начальный план"
```

## Рекомендации

# test
>>>>>>> 6eff3e320eb9a623ac3081f83ad6576dc10ef955
# Test auto deploy
- Используйте читаемые и структурированные записи.
- Не храните секреты в журналах в репозитории.
- Версионируйте изменения через Git.

## 🚀 Автоматический деплой

Проект настроен на автоматический деплой:

- **✅ Тесты**: Автоматически запускаются при каждом push
- **🌐 GitHub Pages**: Веб-интерфейс автоматически деплоится
- **🔄 CI/CD**: GitHub Actions workflow для непрерывной интеграции

Подробнее в **[📋 DEPLOYMENT.md](DEPLOYMENT.md)**

## 🎨 Архитектура проекта

### 📱 **Telegram Mini App + Веб-интерфейс**
- **Frontend**: HTML5 + CSS3 + JavaScript (Адаптивный дизайн)
- **Telegram SDK**: WebApp API для интеграции с Mini App
- **Real-time validation**: Проверка форм в реальном времени

### 🤖 **Telegram Bot (Python)**
- **Framework**: aiogram v3.15.0 (Современный async framework)
- **Модульная система**: Miniapps архитектура
- **Авторизация**: Google Sheets API интеграция

### 🌐 **MCP (Model Context Protocol)**
- **Context7 интеграция**: Управление контекстом
- **Локальный контекст**: Сохранение состояния диалогов

### 📦 **Компоненты проекта**
```
┌── web_ui/                 # Веб-интерфейс (дубликат)
├── src/miniapps/          # Модули бота
│   ├── echo.py           # Эхо модуль
│   ├── welcome.py        # Приветствие + Mini App
│   └── webapp.py         # Обработка авторизации
├── src/mcp/               # MCP интеграция  
├── .github/workflows/     # CI/CD конфигурация
├── index.html             # Главная страница (деплой)
├── app.js                 # Mini App логика
└── styles.css             # Стили интерфейса
```

### 🔄 **CI/CD Pipeline**
- **Тестирование**: pytest автотесты (9 тестов)
- **Деплой**: GitHub Pages автоматический деплой
- **Мониторинг**: Status badges и отчеты

```
# 🔐 Telegram Mini App - Авторизация сотрудников

[![Deploy Status](https://github.com/synthosaicreativestudio-maker/test/actions/workflows/deploy.yml/badge.svg)](https://github.com/synthosaicreativestudio-maker/test/actions/workflows/deploy.yml)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://synthosaicreativestudio-maker.github.io/test/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](./CHANGELOG.md)
[![Telegram](https://img.shields.io/badge/platform-Telegram-blue)](https://core.telegram.org/bots/webapps)
[![Mobile Friendly](https://img.shields.io/badge/mobile-friendly-brightgreen)](#)

Современное приложение для авторизации сотрудников через Telegram Mini App с интеграцией в Google Sheets.

## ✨ Особенности

- 🚀 **Современный дизайн** - адаптивный интерфейс с поддержкой тем Telegram
- 📱 **Полная интеграция** - использует Telegram Web App SDK
- ✅ **Валидация в реальном времени** - мгновенная проверка введенных данных
- 🔄 **Автокоррекция номеров** - автоматическое исправление формата телефона
- 💫 **Хаптическая обратная связь** - тактильные ощущения при взаимодействии
- 🎨 **Темная/светлая тема** - поддержка системных настроек Telegram

## 🛠 Технологии

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Integration**: Telegram Web App SDK
- **Styling**: CSS Custom Properties (для поддержки тем)
- **Validation**: Real-time форм валидация
- **Deployment**: GitHub Pages

## 📚 Документация

### 📋 Основные документы
- **[📋 CHANGELOG.md](./CHANGELOG.md)** - История всех изменений по версиям
- **[✅ TODO.md](./TODO.md)** - Текущие задачи и планы

### 📁 Проектная документация
- **[📋 RULES.md](./docs/RULES.md)** - Правила разработки и стандарты
- **[🗺️ ROADMAP.md](./docs/ROADMAP.md)** - План развития проекта
- **[🏗️ ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Архитектура системы

### 📊 Логи проекта
- **[📋 project.md](./logs/project.md)** - Основной лог всех изменений
- **[🛠️ development.md](./logs/development.md)** - Технические детали разработки
- **[🚀 deployment.md](./logs/deployment.md)** - История деплоев и инфраструктуры

## 🚀 Деплой

Приложение автоматически деплоится на GitHub Pages:
- **URL**: https://synthosaicreativestudio-maker.github.io/test/

## 📋 Функционал

### Авторизация
- Ввод кода сотрудника (только цифры)
- Ввод номера телефона (с автокоррекцией формата)
- Валидация данных в реальном времени
- Отправка данных через Telegram Bot API

### Интерфейс
- Отображение информации о пользователе Telegram
- Статус подключения к Telegram Web App
- Адаптивный дизайн для всех устройств
- Анимации и переходы

### Обработка ошибок
- Информативные сообщения об ошибках
- Визуальная индикация статуса полей
- Fallback для тестирования вне Telegram

## 💻 Локальная разработка

Для локального тестирования откройте `index.html` в браузере или используйте локальный HTTP сервер:

```bash
# Python 3
python -m http.server 8000

# Node.js
npx serve .

# PHP
php -S localhost:8000
```

## 📁 Структура проекта

```
marketing_test/
├── index.html              # 🚀 Главный файл Mini App
├── README.md               # 📖 Основная документация
├── CHANGELOG.md            # 📋 История изменений
├── TODO.md                 # ✅ Список задач
├── .gitignore              # 🛡️ Исключенные файлы
├── env.example             # 📝 Шаблон переменных
├── docs/                   # 📚 Документация
│   ├── RULES.md           # 📋 Правила проекта
│   ├── ROADMAP.md         # 🗺️ План развития
│   └── ARCHITECTURE.md    # 🏗️ Архитектура
├── logs/                   # 📊 Логи проекта
│   ├── project.md         # 📋 Основной лог
│   ├── development.md     # 🛠️ Лог разработки
│   └── deployment.md      # 🚀 Лог деплоя
├── .github/workflows/      # ⚙️ GitHub Actions
│   └── deploy.yml         # 🚀 Автодеплой
├── env                     # 🔐 Переменные окружения (локально)
└── credentials.json        # 🔐 Google Sheets (локально)
```

## 🔧 Настройка

1. Скопируйте `env.example` в `env` и заполните переменные
2. Добавьте `credentials.json` для интеграции с Google Sheets
3. Настройте Telegram Bot через @BotFather
4. Укажите URL Mini App в настройках бота

## 📱 Использование

1. Откройте бота в Telegram
2. Нажмите на кнопку "Авторизация" или используйте команду
3. Введите код сотрудника и номер телефона
4. Подтвердите отправку данных

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature ветку
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

---

> 💡 **Примечание**: Файлы `env` и `credentials.json` содержат секретные данные и не должны попадать в публичный репозиторий.
