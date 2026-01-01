"""
Конфигурация приложения.

Загружает настройки из переменных окружения (.env файла).
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


# Загружаем .env файл
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # GigaChat API
    gigachat_credentials: str = Field(
        default="",
        description="API-ключ GigaChat (Authorization Key)"
    )
    gigachat_model: str = Field(
        default="GigaChat",
        description="Модель GigaChat (GigaChat или GigaChat-Pro)"
    )
    gigachat_scope: str = Field(
        default="GIGACHAT_API_PERS",
        description="Scope для GigaChat API"
    )
    
    # Настройки парсера
    scraper_timeout: int = Field(
        default=10,
        description="Таймаут загрузки страницы в секундах"
    )
    scraper_user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        description="User-Agent для HTTP-запросов"
    )
    
    # Настройки LLM
    llm_timeout: int = Field(
        default=60,
        description="Таймаут запроса к LLM в секундах"
    )
    llm_max_retries: int = Field(
        default=3,
        description="Максимальное количество повторных попыток"
    )
    
    # Настройки вывода
    max_text_length: int = Field(
        default=10000,
        description="Максимальная длина текста для анализа"
    )
    
    # Общие настройки
    debug: bool = Field(
        default=False,
        description="Режим отладки"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()

