# Landing Redesign Assistant

AI-агент для анализа лендингов и генерации рекомендаций по улучшению дизайна и контента.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GigaChat](https://img.shields.io/badge/LLM-GigaChat-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

## Описание

Landing Redesign Assistant — это AI-агент, который анализирует лендинги (посадочные страницы) и выдаёт конкретные рекомендации по улучшению. Агент работает в двух режимах:

- **UI-дизайнер** — анализ структуры, визуальной иерархии, CTA-кнопок и адаптивности
- **Контент-менеджер** — анализ заголовков, текстов, УТП и призывов к действию

## Возможности

- Анализ любого лендинга по URL
- Два режима анализа (дизайн / контент / оба)
- 5 конкретных рекомендаций от каждого модуля
- Сохранение результатов в TXT-файл
- Интерактивное меню или работа через аргументы
- Docker-контейнеризация
- Модульная архитектура для расширения

## Установка

### Требования

- Python 3.12+
- API-ключ GigaChat ([получить здесь](https://developers.sber.ru/studio))

### Локальная установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/bocharov62-bit/AI_Agent_Target.git
cd AI_Agent_Target
```

2. **Создайте виртуальное окружение:**

```bash
py -3.12 -m venv venv
.\venv\Scripts\activate
```

3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

4. **Настройте API-ключ:**

```bash
copy .env.example .env
```

Откройте `.env` и вставьте ваш API-ключ GigaChat.

### Docker установка

```bash
docker build -t landing-assistant .
```

## Использование

### Интерактивный режим

```bash
python agent.py
```

### Командная строка

```bash
# Анализ с выбором режима
python agent.py https://example.com

# Только UI-анализ
python agent.py https://example.com --role ui

# Только контент-анализ
python agent.py https://example.com --role content

# Полный анализ с сохранением в файл
python agent.py https://example.com --role all --output result.txt
```

### Docker

```bash
docker run --env-file .env landing-assistant https://example.com --role all
```

### Параметры

| Параметр | Описание |
|----------|----------|
| `url` | URL лендинга для анализа |
| `--role`, `-r` | Режим: `ui`, `content` или `all` |
| `--output`, `-o` | Сохранить результаты в файл |
| `--no-color` | Отключить цветной вывод |

## Структура проекта

```
landing_redesign_assistant/
├── agent.py              # Точка входа (CLI)
├── core/                 # Ядро системы
│   ├── config.py         # Конфигурация
│   ├── interfaces.py     # Базовые классы
│   ├── models.py         # Модели данных
│   └── exceptions.py     # Исключения
├── scrapers/             # Модули парсинга
│   └── html_parser.py    # HTML-парсер
├── analyzers/            # Модули анализа
│   ├── ui_designer.py    # UI-анализ
│   └── content_manager.py # Контент-анализ
├── llm_providers/        # LLM-провайдеры
│   └── gigachat_provider.py
├── outputs/              # Модули вывода
│   ├── console_output.py # Вывод в консоль
│   └── txt_output.py     # Сохранение в TXT
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Docker Compose
└── web/                  # Веб-интерфейс (в разработке)
```

## Конфигурация

Настройки хранятся в файле `.env`:

```env
GIGACHAT_CREDENTIALS=your_key_here
GIGACHAT_MODEL=GigaChat
GIGACHAT_SCOPE=GIGACHAT_API_PERS
SCRAPER_TIMEOUT=10
DEBUG=False
```

## Архитектура

Проект построен на модульной архитектуре:

- **Scrapers** — загрузка и парсинг веб-страниц
- **Analyzers** — анализ контента (расширяемые модули)
- **LLM Providers** — интеграция с языковыми моделями
- **Outputs** — вывод результатов в разных форматах

## Roadmap

- [x] MVP — консольный агент
- [x] Два модуля анализа (UI, контент)
- [x] Сохранение в TXT
- [x] Docker
- [ ] Веб-интерфейс
- [ ] Дополнительные модули (SEO, конкуренты)
- [ ] Генерация изображений

## Лицензия

MIT License

## Автор

**Bocharov62**

---

*Powered by GigaChat*

