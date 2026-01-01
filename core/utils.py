"""
Вспомогательные функции.
"""

import re
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """
    Проверить корректность URL.
    
    Args:
        url: URL для проверки
        
    Returns:
        True если URL корректен
    """
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False


def clean_text(text: str) -> str:
    """
    Очистить текст от лишних пробелов и символов.
    
    Args:
        text: Исходный текст
        
    Returns:
        Очищенный текст
    """
    # Удаляем множественные пробелы
    text = re.sub(r'\s+', ' ', text)
    # Удаляем множественные переносы строк
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Убираем пробелы в начале и конце
    text = text.strip()
    return text


def truncate_text(text: str, max_length: int = 10000) -> str:
    """
    Обрезать текст до максимальной длины.
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
        
    Returns:
        Обрезанный текст
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def get_timestamp() -> str:
    """
    Получить текущую метку времени.
    
    Returns:
        Строка с датой и временем
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_file_timestamp() -> str:
    """
    Получить метку времени для имени файла.
    
    Returns:
        Строка без спецсимволов
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_number(number: int) -> str:
    """
    Форматировать число с разделителями тысяч.
    
    Args:
        number: Число
        
    Returns:
        Отформатированная строка
    """
    return f"{number:,}".replace(",", " ")

