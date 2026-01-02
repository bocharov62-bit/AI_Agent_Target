"""
HTML-парсер для извлечения контента из веб-страниц.
"""

import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup

from core.config import settings
from core.exceptions import ScraperError
from core.interfaces import BaseScraper
from core.models import PageContent
from core.utils import clean_text, truncate_text


logger = logging.getLogger(__name__)


class HTMLParser(BaseScraper):
    """
    Парсер HTML-страниц.
    
    Использует requests для загрузки и BeautifulSoup для парсинга.
    """
    
    name = "HTML Parser"
    description = "Парсер HTML-страниц с извлечением текста"
    
    def __init__(
        self,
        timeout: Optional[int] = None,
        user_agent: Optional[str] = None
    ):
        """
        Инициализация парсера.
        
        Args:
            timeout: Таймаут запроса в секундах
            user_agent: User-Agent для HTTP-запросов
        """
        self.timeout = timeout or settings.scraper_timeout
        self.user_agent = user_agent or settings.scraper_user_agent
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Создать HTTP-сессию с настроенными заголовками."""
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0",
        })
        return session
    
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
        logger.info(f"Загрузка страницы: {url}")
        
        try:
            response = self.session.get(
                url,
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Определяем кодировку
            response.encoding = response.apparent_encoding or "utf-8"
            
            logger.info(f"Страница загружена: {len(response.text)} символов")
            return response.text
            
        except requests.exceptions.Timeout:
            raise ScraperError(
                f"Превышен таймаут ({self.timeout} сек)", 
                url=url
            )
        except requests.exceptions.ConnectionError:
            raise ScraperError(
                "Не удалось подключиться к серверу", 
                url=url
            )
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_messages = {
                401: "Сайт требует авторизации или блокирует автоматические запросы (401 Unauthorized)",
                403: "Доступ запрещён - сайт блокирует запросы (403 Forbidden)",
                404: "Страница не найдена (404 Not Found)",
                500: "Внутренняя ошибка сервера (500)",
                503: "Сервис временно недоступен (503 Service Unavailable)"
            }
            message = error_messages.get(status_code, f"HTTP ошибка: {status_code}")
            raise ScraperError(message, url=url)
        except requests.exceptions.RequestException as e:
            raise ScraperError(str(e), url=url)
    
    def parse(self, html: str, url: str = "") -> PageContent:
        """
        Извлечь контент из HTML.
        
        Args:
            html: HTML-код страницы
            url: URL страницы (опционально)
            
        Returns:
            PageContent с извлечённым контентом
        """
        logger.info("Парсинг HTML...")
        
        soup = BeautifulSoup(html, "lxml")
        
        # Удаляем ненужные теги
        for tag in soup(["script", "style", "meta", "link", "noscript", "header", "footer", "nav"]):
            tag.decompose()
        
        # Извлекаем заголовок
        title = None
        if soup.title:
            title = soup.title.get_text(strip=True)
        
        # Извлекаем текст
        text = soup.get_text(separator="\n", strip=True)
        text = clean_text(text)
        text = truncate_text(text, settings.max_text_length)
        
        logger.info(f"Извлечено: {len(text)} символов текста")
        
        return PageContent(
            url=url,
            title=title,
            text=text,
            html=html[:50000] if len(html) > 50000 else html  # Ограничиваем HTML
        )
    
    def fetch_and_parse(self, url: str) -> PageContent:
        """
        Загрузить и распарсить страницу.
        
        Args:
            url: URL страницы
            
        Returns:
            PageContent с контентом страницы
        """
        html = self.fetch(url)
        return self.parse(html, url=url)

