# Инструкция по автоматическому деплою проекта

## GitHub Pages (автоматический деплой веб-интерфейса)

### Настройка GitHub Pages
1. В настройках репозитория: Settings → Pages
2. Source: "GitHub Actions"
3. После настройки веб-интерфейс доступен по адресу:
   - **URL**: https://synthosaicreativestudio-maker.github.io/test/
   - **Файлы**: автоматически деплоятся из папки `web_ui/`

### Автоматический деплой веб-интерфейса
При каждом push в `main` ветку:
1. Запускаются тесты
2. Веб-интерфейс (index.html, styles.css, app.js) деплоится на GitHub Pages
3. Telegram Bot получает обновленный URL для Mini App

## Настройка GitHub Actions для автоматического деплоя

### 1. Настройка Secrets в GitHub

В настройках вашего репозитория на GitHub (Settings → Secrets and variables → Actions) добавьте следующие секреты:

#### Обязательные для работы бота:
- `BOT_TOKEN` - токен Telegram бота
- `GOOGLE_SERVICE_ACCOUNT_FILE` - содержимое JSON файла сервисного аккаунта Google
- `SHEET_ID` - ID Google таблицы

#### Опциональные:
- `CONTEXT7_URL` - URL сервера Context7 MCP

#### Для деплоя на сервер (один из вариантов):

**Вариант 1: Деплой на свой сервер через SSH**
- `DEPLOY_HOST` - IP или домен сервера
- `DEPLOY_USER` - пользователь для подключения
- `DEPLOY_KEY` - приватный SSH ключ

**Вариант 2: Деплой на Heroku**
- `HEROKU_API_KEY` - API ключ Heroku
- `HEROKU_APP_NAME` - название приложения в Heroku
- `HEROKU_EMAIL` - email аккаунта Heroku

**Вариант 3: Деплой в Docker Registry**
- `DOCKER_REGISTRY` - адрес Docker registry (например, docker.io)
- `DOCKER_USERNAME` - имя пользователя
- `DOCKER_PASSWORD` - пароль или токен

### 2. Автоматический деплой

После push в ветку `main` GitHub Actions автоматически:
1. Запустит тесты
2. Соберет проект
3. Задеплоит на выбранную платформу

## Ручной деплой на сервер

### Подготовка сервера

```bash
# Установка Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Создание директорий
sudo mkdir -p /opt/marketing_test
sudo mkdir -p /opt/configs/marketing_test
sudo mkdir -p /opt/backups/marketing_test
```

### Настройка конфигурации

```bash
# Создание файла окружения для production
sudo nano /opt/configs/marketing_test/env.prod
```

Содержимое файла:
```
BOT_TOKEN=ваш_токен_бота
GOOGLE_SERVICE_ACCOUNT_FILE=/app/google-credentials.json
SHEET_ID=ваш_sheet_id
CONTEXT7_URL=ваш_context7_url
GITHUB_REPO=https://github.com/synthosaicreativestudio-maker/test
```

```bash
# Копирование Google credentials
sudo cp /path/to/your/google-credentials.json /opt/configs/marketing_test/
```

### Деплой

```bash
# Клонирование или обновление репозитория
cd /opt/marketing_test
sudo git clone https://github.com/synthosaicreativestudio-maker/test.git .
# или для обновления: sudo git pull origin main

# Копирование конфигурации
sudo cp /opt/configs/marketing_test/env.prod env
sudo cp /opt/configs/marketing_test/google-credentials.json .

# Запуск
sudo docker-compose up -d --build
```

### Использование скрипта деплоя

```bash
# Сделать скрипт исполняемым
chmod +x deploy.sh

# Запуск деплоя
sudo ./deploy.sh production
```

## Локальный запуск через Docker

```bash
# Клонирование репозитория
git clone https://github.com/synthosaicreativestudio-maker/test.git
cd test

# Создание файла окружения
cp env.example env
# Отредактируйте env файл с вашими настройками

# Копирование Google credentials (если есть)
cp /path/to/your/google-credentials.json .

# Запуск
docker-compose up -d --build
```

## Доступные сервисы после запуска

- **Telegram Bot** - автоматически подключается к Telegram
- **Web UI (GitHub Pages)** - https://synthosaicreativestudio-maker.github.io/test/ (автоматический деплой)
- **Web UI (локально)** - http://localhost:8000/ (при запуске через Docker)
- **Логи** - http://localhost:8080 (если запущен nginx контейнер)

## Мониторинг и логи

```bash
# Просмотр логов
docker-compose logs -f bot
docker-compose logs -f web

# Статус сервисов
docker-compose ps

# Перезапуск сервиса
docker-compose restart bot
```

## Обновление проекта

### Автоматическое (через GitHub Actions)
Просто сделайте push в ветку `main` - деплой произойдет автоматически.

### Ручное обновление
```bash
cd /opt/marketing_test
sudo git pull origin main
sudo docker-compose up -d --build
```

## Troubleshooting

### Проблемы с правами доступа
```bash
sudo chown -R $USER:$USER /opt/marketing_test
```

### Очистка Docker
```bash
docker system prune -a
docker-compose down --volumes
```

### Просмотр логов в реальном времени
```bash
docker-compose logs -f --tail=100 bot
```