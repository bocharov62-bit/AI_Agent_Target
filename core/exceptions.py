"""
Кастомные исключения приложения.
"""


class LandingAssistantError(Exception):
    """Базовое исключение приложения."""
    pass


class ScraperError(LandingAssistantError):
    """Ошибка при парсинге страницы."""
    
    def __init__(self, message: str, url: str = ""):
        self.url = url
        super().__init__(f"Ошибка парсинга{f' ({url})' if url else ''}: {message}")


class LLMError(LandingAssistantError):
    """Ошибка при вызове LLM API."""
    
    def __init__(self, message: str, provider: str = ""):
        self.provider = provider
        super().__init__(f"Ошибка LLM{f' ({provider})' if provider else ''}: {message}")


class AnalyzerError(LandingAssistantError):
    """Ошибка при анализе контента."""
    
    def __init__(self, message: str, analyzer: str = ""):
        self.analyzer = analyzer
        super().__init__(f"Ошибка анализа{f' ({analyzer})' if analyzer else ''}: {message}")


class ConfigError(LandingAssistantError):
    """Ошибка конфигурации."""
    pass


class ValidationError(LandingAssistantError):
    """Ошибка валидации данных."""
    pass

