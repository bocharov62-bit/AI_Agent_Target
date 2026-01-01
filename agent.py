#!/usr/bin/env python3
"""
Landing Redesign Assistant - AI-агент для анализа лендингов.

Точка входа приложения (CLI).
Запуск: py -3.12 agent.py [url] [--role ui|content|all] [--output file.txt]
"""

import argparse
import logging
import sys
import io
from typing import List, Optional

# Исправление кодировки для Windows консоли
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from core.config import settings
from core.exceptions import LandingAssistantError, ScraperError, LLMError
from core.models import AnalysisResult
from core.utils import validate_url

from scrapers.html_parser import HTMLParser
from llm_providers.gigachat_provider import GigaChatProvider
from analyzers.ui_designer import UIDesignerAnalyzer
from analyzers.content_manager import ContentManagerAnalyzer
from outputs.console_output import ConsoleOutput
from outputs.txt_output import TxtOutput


# Настройка логирования
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Доступные модули анализа
ANALYZERS = {
    "ui": {
        "class": UIDesignerAnalyzer,
        "name": "UI-дизайнер",
        "description": "Анализ дизайна и структуры",
        "premium": False
    },
    "content": {
        "class": ContentManagerAnalyzer,
        "name": "Контент-менеджер", 
        "description": "Анализ текстов и копирайтинга",
        "premium": False
    }
}


def show_banner() -> None:
    """Показать баннер приложения."""
    banner = """
+--------------------------------------------------------------+
|                                                              |
|   [*]  LANDING REDESIGN ASSISTANT                            |
|                                                              |
|   AI-агент для анализа лендингов                             |
|   Powered by GigaChat                                        |
|                                                              |
+--------------------------------------------------------------+
    """
    print(banner)


def show_menu() -> str:
    """
    Показать интерактивное меню выбора роли.
    
    Returns:
        Выбранная роль: 'ui', 'content' или 'all'
    """
    print("\n[i] Доступные модули анализа:\n")
    print("   [1] UI-дизайнер        (бесплатно)")
    print("       Анализ дизайна, структуры и UX")
    print()
    print("   [2] Контент-менеджер   (бесплатно)")
    print("       Анализ текстов, заголовков и CTA")
    print()
    print("   [3] Оба модуля         (бесплатно)")
    print("       Комплексный анализ")
    print()
    
    while True:
        choice = input("   Ваш выбор [1/2/3]: ").strip()
        
        if choice == "1":
            return "ui"
        elif choice == "2":
            return "content"
        elif choice == "3":
            return "all"
        else:
            print("   [!] Неверный выбор. Введите 1, 2 или 3.")


def get_url_input() -> str:
    """
    Запросить URL у пользователя.
    
    Returns:
        Валидный URL
    """
    print("\n[?] Введите URL лендинга для анализа:")
    
    while True:
        url = input("   URL: ").strip()
        
        if not url:
            print("   [!] URL не может быть пустым.")
            continue
        
        # Добавляем https:// если не указан протокол
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        if validate_url(url):
            return url
        else:
            print("   [!] Некорректный URL. Попробуйте снова.")


def run_analysis(
    url: str,
    role: str,
    llm_provider: GigaChatProvider
) -> List[AnalysisResult]:
    """
    Запустить анализ лендинга.
    
    Args:
        url: URL для анализа
        role: Роль ('ui', 'content' или 'all')
        llm_provider: LLM-провайдер
        
    Returns:
        Список результатов анализа
    """
    results = []
    
    # Определяем какие анализаторы использовать
    if role == "all":
        analyzer_keys = ["ui", "content"]
    else:
        analyzer_keys = [role]
    
    # Загружаем страницу
    print("\n[...] Загрузка страницы...")
    scraper = HTMLParser()
    content = scraper.fetch_and_parse(url)
    print(f"   [OK] Загружено: {len(content.text)} символов")
    
    # Анализируем каждым модулем
    for key in analyzer_keys:
        analyzer_info = ANALYZERS[key]
        print(f"\n[...] Анализ: {analyzer_info['name']}...")
        
        analyzer = analyzer_info["class"](llm_provider)
        result = analyzer.analyze(content)
        results.append(result)
        
        print(f"   [OK] Получено {len(result.recommendations)} рекомендаций")
    
    return results


def ask_save_to_file() -> Optional[str]:
    """
    Спросить о сохранении в файл.
    
    Returns:
        Имя файла или None
    """
    print("\n[?] Сохранить результаты в файл?")
    choice = input("   [y/n]: ").strip().lower()
    
    if choice in ("y", "yes", "д", "да"):
        filename = input("   Имя файла (Enter для автоматического): ").strip()
        return filename if filename else None
    
    return None


def main() -> int:
    """
    Главная функция приложения.
    
    Returns:
        Код возврата (0 = успех)
    """
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Landing Redesign Assistant - AI-агент для анализа лендингов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  py -3.12 agent.py                              # Интерактивный режим
  py -3.12 agent.py https://example.com          # Анализ с меню выбора роли
  py -3.12 agent.py https://example.com --role ui  # Только UI-анализ
  py -3.12 agent.py https://example.com --role all --output result.txt
        """
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="URL лендинга для анализа"
    )
    parser.add_argument(
        "--role", "-r",
        choices=["ui", "content", "all"],
        help="Роль агента: ui (дизайн), content (тексты), all (оба)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Сохранить результаты в файл"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Отключить цветной вывод"
    )
    
    args = parser.parse_args()
    
    try:
        # Показываем баннер
        show_banner()
        
        # Получаем URL
        url = args.url
        if not url:
            url = get_url_input()
        elif not validate_url(url):
            # Добавляем https:// если не указан
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            if not validate_url(url):
                print(f"[ERROR] Некорректный URL: {url}")
                return 1
        
        # Получаем роль
        role = args.role
        if not role:
            role = show_menu()
        
        print(f"\n[>] Анализируем: {url}")
        print(f"   Режим: {ANALYZERS.get(role, {}).get('name', 'Все модули')}")
        
        # Инициализируем LLM-провайдер
        try:
            llm_provider = GigaChatProvider()
        except LLMError as e:
            print(f"\n[ERROR] Ошибка настройки GigaChat: {e}")
            print("\n[TIP] Добавьте ваш API-ключ в файл .env:")
            print("   GIGACHAT_CREDENTIALS=ваш_ключ_здесь")
            return 1
        
        # Запускаем анализ
        results = run_analysis(url, role, llm_provider)
        
        # Выводим результаты
        console = ConsoleOutput(use_colors=not args.no_color)
        console.output_full(results)
        
        # Сохраняем в файл
        output_file = args.output
        if output_file is None and not args.url:
            # Интерактивный режим - спрашиваем
            save_filename = ask_save_to_file()
            if save_filename is not None:
                output_file = save_filename if save_filename else None
        
        if output_file is not None or (args.output == ""):
            txt_output = TxtOutput()
            filepath = txt_output.output_full(results, output_file if output_file else None)
            print(f"\n[SAVED] Результаты сохранены в: {filepath}")
        
        return 0
        
    except ScraperError as e:
        print(f"\n[ERROR] Ошибка загрузки страницы: {e}")
        return 1
    except LLMError as e:
        print(f"\n[ERROR] Ошибка GigaChat: {e}")
        return 1
    except LandingAssistantError as e:
        print(f"\n[ERROR] Ошибка: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\n[!] Прервано пользователем.")
        return 130
    except Exception as e:
        logger.exception("Неожиданная ошибка")
        print(f"\n[ERROR] Неожиданная ошибка: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
