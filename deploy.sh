#!/bin/bash
# Скрипт развертывания Landing Redesign Assistant на сервере

set -e  # Остановка при ошибке

echo "=== Развертывание Landing Redesign Assistant ==="

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "Docker не установлен. Установка..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Проверка Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose не установлен. Установка..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Создание директории проекта
PROJECT_DIR="$HOME/landing-assistant"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Клонирование репозитория (если еще не клонирован)
if [ ! -d ".git" ]; then
    echo "Клонирование репозитория..."
    git clone https://github.com/bocharov62-bit/AI_Agent_Target.git .
    cd landing_redesign_assistant
else
    cd landing_redesign_assistant
    echo "Обновление репозитория..."
    git pull
fi

# Создание .env файла (если не существует)
if [ ! -f ".env" ]; then
    echo "Создание .env файла..."
    cp .env.example .env
    echo "⚠️  ВАЖНО: Отредактируйте .env файл и добавьте ваш GIGACHAT_CREDENTIALS!"
    echo "   nano .env"
    read -p "Нажмите Enter после редактирования .env файла..."
fi

# Создание директории для результатов
mkdir -p output

# Остановка существующих контейнеров
echo "Остановка старых контейнеров..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

# Сборка и запуск
echo "Сборка и запуск контейнеров..."
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Проверка статуса
echo "Ожидание запуска (10 секунд)..."
sleep 10

# Проверка работоспособности
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "✅ Сервис успешно запущен!"
    echo ""
    echo "=== Информация ==="
    echo "Веб-интерфейс: http://$(hostname -I | awk '{print $1}'):8000"
    echo ""
    echo "Полезные команды:"
    echo "  Просмотр логов: docker-compose -f docker-compose.prod.yml logs -f"
    echo "  Остановка:      docker-compose -f docker-compose.prod.yml down"
    echo "  Перезапуск:     docker-compose -f docker-compose.prod.yml restart"
    echo "  Статус:         docker-compose -f docker-compose.prod.yml ps"
else
    echo "❌ Ошибка запуска. Проверьте логи:"
    echo "   docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi

