#!/bin/bash

# Скрипт для деплоя marketing_test проекта
# Использование: ./deploy.sh [production|staging]

set -e

ENVIRONMENT=${1:-production}
PROJECT_DIR="/opt/marketing_test"
BACKUP_DIR="/opt/backups/marketing_test"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🚀 Начинаю деплой marketing_test (окружение: $ENVIRONMENT)"

# Создание бэкапа
echo "📦 Создаю бэкап..."
mkdir -p $BACKUP_DIR
if [ -d "$PROJECT_DIR" ]; then
    tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" -C "$PROJECT_DIR" .
    echo "✅ Бэкап создан: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
fi

# Остановка сервисов
echo "⏹️  Останавливаю сервисы..."
docker-compose down || true

# Обновление кода
echo "📥 Обновляю код..."
if [ ! -d "$PROJECT_DIR" ]; then
    git clone https://github.com/synthosaicreativestudio-maker/test.git $PROJECT_DIR
else
    cd $PROJECT_DIR
    git fetch origin
    git reset --hard origin/main
fi

cd $PROJECT_DIR

# Копирование файлов окружения
echo "⚙️  Настраиваю окружение..."
if [ "$ENVIRONMENT" = "production" ]; then
    cp /opt/configs/marketing_test/env.prod env
else
    cp /opt/configs/marketing_test/env.staging env
fi

# Копирование Google credentials
cp /opt/configs/marketing_test/google-credentials.json . || echo "⚠️  Google credentials не найдены"

# Сборка и запуск
echo "🔨 Собираю и запускаю контейнеры..."
docker-compose build --no-cache
docker-compose up -d

# Проверка здоровья
echo "🔍 Проверяю состояние сервисов..."
sleep 10

if docker-compose ps | grep -q "Up"; then
    echo "✅ Деплой успешно завершен!"
    
    # Отправка уведомления (опционально)
    if [ ! -z "$WEBHOOK_URL" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"✅ Marketing Test успешно задеплоен на $ENVIRONMENT\"}" \
            $WEBHOOK_URL
    fi
else
    echo "❌ Ошибка при запуске сервисов!"
    
    # Восстановление из бэкапа
    echo "🔄 Восстанавливаю из бэкапа..."
    docker-compose down
    cd /
    rm -rf $PROJECT_DIR
    mkdir -p $PROJECT_DIR
    tar -xzf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" -C "$PROJECT_DIR"
    cd $PROJECT_DIR
    docker-compose up -d
    
    exit 1
fi

# Очистка старых бэкапов (оставляем последние 5)
echo "🧹 Очищаю старые бэкапы..."
cd $BACKUP_DIR
ls -t backup_*.tar.gz | tail -n +6 | xargs -r rm

echo "🎉 Деплой завершен успешно!"