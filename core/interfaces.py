"""
Базовые интерфейсы (абстрактные классы) для модулей.

Все модули должны наследоваться от соответствующих базовых классов.
Это обеспечивает единый интерфейс и возможность замены модулей.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from core.models import PageContent, AnalysisResult, Recommendation


class BaseScraper(ABC):
    """
    Базовый класс для парсеров веб-страниц.
    
    Все парсеры должны реализовать методы fetch и parse.
    """
    
    name: str = "Base Scraper"
    description: str = "Базовый парсер"
    
    @abstractmethod
    def fetch(self, url: str) -> str:
        """
        Загрузить HTML-код страницы.
        
        Args:
            url: URL страницы для загрузки
            
        Returns:
            HTML-код страницы
            
        Raises:
            ScraperError: При ошибке загрузки
        """
        pass
    
    @abstractmethod
    def parse(self, html: str) -> PageContent:
        """
        Извлечь контент из HTML.
        
        Args:
            html: HTML-код страницы
            
        Returns:
            PageContent с извлечённым контентом
        """
        pass
    
    def fetch_and_parse(self, url: str) -> PageContent:
        """
        Загрузить и распарсить страницу.
        
        Args:
            url: URL страницы
            
        Returns:
            PageContent с контентом страницы
        """
        html = self.fetch(url)
        content = self.parse(html)
        content.url = url
        return content


class BaseLLMProvider(ABC):
    """
    Базовый класс для LLM-провайдеров.
    
    Все провайдеры должны реализовать метод call.
    """
    
    name: str = "Base LLM Provider"
    description: str = "Базовый LLM-провайдер"
    
    @abstractmethod
    def call(
        self, 
        system_prompt: str, 
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> str:
        """
        Отправить запрос к LLM.
        
        Args:
            system_prompt: Системный промпт (роль)
            user_prompt: Пользовательский промпт (контент)
            temperature: Температура генерации (0.0-1.0)
            max_tokens: Максимальное количество токенов в ответе
            
        Returns:
            Ответ от LLM
            
        Raises:
            LLMError: При ошибке вызова API
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Проверить доступность провайдера.
        
        Returns:
            True если провайдер доступен
        """
        pass


class BaseAnalyzer(ABC):
    """
    Базовый класс для анализаторов контента.
    
    Все анализаторы должны реализовать методы analyze и get_prompt.
    """
    
    name: str = "Base Analyzer"
    description: str = "Базовый анализатор"
    is_premium: bool = False  # Платный ли модуль
    
    def __init__(self, llm_provider: BaseLLMProvider):
        """
        Инициализация анализатора.
        
        Args:
            llm_provider: Провайдер LLM для генерации рекомендаций
        """
        self.llm_provider = llm_provider
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Получить системный промпт для LLM.
        
        Returns:
            Системный промпт, определяющий роль LLM
        """
        pass
    
    @abstractmethod
    def parse_response(self, response: str) -> List[Recommendation]:
        """
        Распарсить ответ LLM в список рекомендаций.
        
        Args:
            response: Сырой ответ от LLM
            
        Returns:
            Список рекомендаций
        """
        pass
    
    def analyze(self, content: PageContent) -> AnalysisResult:
        """
        Провести анализ контента.
        
        Args:
            content: Контент страницы для анализа
            
        Returns:
            Результат анализа с рекомендациями
        """
        system_prompt = self.get_system_prompt()
        user_prompt = self._build_user_prompt(content)
        
        response = self.llm_provider.call(system_prompt, user_prompt)
        recommendations = self.parse_response(response)
        
        return AnalysisResult(
            module_name=self.name,
            module_description=self.description,
            url=content.url,
            recommendations=recommendations,
            raw_response=response
        )
    
    def _build_user_prompt(self, content: PageContent) -> str:
        """
        Построить пользовательский промпт.
        
        Args:
            content: Контент страницы
            
        Returns:
            Промпт для анализа
        """
        return f"""Проанализируй следующий лендинг:

URL: {content.url}
Заголовок: {content.title or 'Не определён'}

Содержимое страницы:
{content.text[:10000]}  # Ограничиваем длину
"""


class BaseOutput(ABC):
    """
    Базовый класс для модулей вывода.
    
    Все модули вывода должны реализовать метод output.
    """
    
    name: str = "Base Output"
    description: str = "Базовый вывод"
    
    @abstractmethod
    def output(self, result: AnalysisResult) -> None:
        """
        Вывести результат анализа.
        
        Args:
            result: Результат анализа для вывода
        """
        pass
    
    @abstractmethod
    def output_full(self, results: List[AnalysisResult]) -> None:
        """
        Вывести результаты от нескольких модулей.
        
        Args:
            results: Список результатов анализа
        """
        pass

