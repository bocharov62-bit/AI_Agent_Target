# 🐳 Docker Guide
# Landing Redesign Assistant

Руководство по использованию Docker контейнеров.

---

## 📦 Docker образы на GitHub Container Registry

### Основной образ (CLI)

```
ghcr.io/bocharov62-bit/ai_agent_target:latest
```

### Веб-интерфейс

```
ghcr.io/bocharov62-bit/ai_agent_target:web-latest
```

---

## 🚀 Быстрый старт

### 1. Установка Docker

**Windows:**
- Скачайте [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Установите и запустите

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. Получение образа

**Автоматическая сборка:**
Образы автоматически собираются при каждом push в `main` или `develop` ветку.

**Ручная сборка:**
```bash
git clone https://github.com/bocharov62-bit/AI_Agent_Target.git
cd AI_Agent_Target/landing_redesign_assistant
docker build -t landing-assistant .
```

---

## 💻 Использование CLI образа

### Базовое использование

```bash
docker run --rm \
  --env-file .env \
  ghcr.io/bocharov62-bit/ai_agent_target:latest \
  https://example.com --role all
```

### С сохранением результатов

```bash
docker run --rm \
  --env-file .env \
  -v $(pwd)/output:/app/output \
  ghcr.io/bocharov62-bit/ai_agent_target:latest \
  https://example.com --role ui --output result.txt
```

### Интерактивный режим

```bash
docker run -it --rm \
  --env-file .env \
  ghcr.io/bocharov62-bit/ai_agent_target:latest
```

---

## 🌐 Использование веб-интерфейса

### Базовый запуск

```bash
docker run -d \
  --name landing-assistant-web \
  -p 8000:8000 \
  --env-file .env \
  ghcr.io/bocharov62-bit/ai_agent_target:web-latest
```

Откройте в браузере: `http://localhost:8000`

### С сохранением результатов

```bash
docker run -d \
  --name landing-assistant-web \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/output:/app/output \
  ghcr.io/bocharov62-bit/ai_agent_target:web-latest
```

### Остановка и удаление

```bash
docker stop landing-assistant-web
docker rm landing-assistant-web
```

---

## 🐙 GitHub Container Registry

### Авторизация

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

Или используйте Personal Access Token с правами `write:packages`.

### Просмотр образов

Перейдите на: `https://github.com/bocharov62-bit/AI_Agent_Target/pkgs/container/ai_agent_target`

---

## 📝 Docker Compose

### CLI режим

```yaml
# docker-compose.yml
version: '3.8'
services:
  agent:
    image: ghcr.io/bocharov62-bit/ai_agent_target:latest
    env_file:
      - .env
    volumes:
      - ./output:/app/output
```

Запуск:
```bash
docker-compose run agent https://example.com --role all
```

### Веб-интерфейс

```yaml
# docker-compose.web.yml
version: '3.8'
services:
  web:
    image: ghcr.io/bocharov62-bit/ai_agent_target:web-latest
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./output:/app/output
    restart: unless-stopped
```

Запуск:
```bash
docker-compose -f docker-compose.web.yml up -d
```

---

## 🔧 Переменные окружения

Создайте файл `.env`:

```env
GIGACHAT_CREDENTIALS=your_key_here
GIGACHAT_MODEL=GigaChat
GIGACHAT_SCOPE=GIGACHAT_API_PERS
SCRAPER_TIMEOUT=10
LLM_TIMEOUT=60
DEBUG=False
```

---

## 🛠 Локальная разработка

### Сборка образа

```bash
docker build -t landing-assistant:local .
```

### Запуск с перезагрузкой (для разработки)

```bash
docker run -it --rm \
  --env-file .env \
  -v $(pwd):/app \
  -p 8000:8000 \
  landing-assistant:local \
  python run_web.py --reload
```

---

## 📊 Мониторинг

### Просмотр логов

```bash
docker logs landing-assistant-web
docker logs -f landing-assistant-web  # в реальном времени
```

### Использование ресурсов

```bash
docker stats landing-assistant-web
```

---

## 🔒 Безопасность

- ✅ Образ запускается от непривилегированного пользователя
- ✅ Минимальный базовый образ (python:3.12-slim)
- ✅ Секреты передаются через `.env` файл (не в образе!)
- ✅ Регулярные обновления базового образа

---

## ❓ Решение проблем

### Ошибка: "Cannot connect to Docker daemon"

**Решение:** Убедитесь, что Docker Desktop запущен.

### Ошибка: "Permission denied"

**Решение (Linux):**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Ошибка: "Image not found"

**Решение:** Проверьте, что образ собран или загружен:
```bash
docker images | grep landing-assistant
```

---

## 📚 Дополнительные ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Compose](https://docs.docker.com/compose/)

---

*Последнее обновление: 02.01.2026*

