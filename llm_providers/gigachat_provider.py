"""
GigaChat LLM Provider - интеграция с GigaChat API (Сбер).
"""

import logging
from typing import Optional

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from core.config import settings
from core.exceptions import LLMError
from core.interfaces import BaseLLMProvider


logger = logging.getLogger(__name__)


class GigaChatProvider(BaseLLMProvider):
    """
    Провайдер GigaChat API от Сбера.
    
    Поддерживает модели GigaChat и GigaChat-Pro.
    """
    
    name = "GigaChat"
    description = "GigaChat API (Сбер)"
    
    def __init__(
        self,
        credentials: Optional[str] = None,
        model: Optional[str] = None,
        scope: Optional[str] = None
    ):
        """
        Инициализация провайдера.
        
        Args:
            credentials: API-ключ (Authorization Key)
            model: Модель (GigaChat или GigaChat-Pro)
            scope: Scope (GIGACHAT_API_PERS или GIGACHAT_API_CORP)
        """
        self.credentials = credentials or settings.gigachat_credentials
        self.model = model or settings.gigachat_model
        self.scope = scope or settings.gigachat_scope
        
        self._client: Optional[GigaChat] = None
        self._validate_credentials()
    
    def _validate_credentials(self) -> None:
        """Проверить наличие API-ключа."""
        if not self.credentials or self.credentials == "your_key_here":
            raise LLMError(
                "API-ключ GigaChat не настроен. "
                "Добавьте GIGACHAT_CREDENTIALS в файл .env",
                provider=self.name
            )
    
    def _get_client(self) -> GigaChat:
        """Получить или создать клиент GigaChat."""
        if self._client is None:
            logger.info(f"Инициализация GigaChat клиента (модель: {self.model})")
            self._client = GigaChat(
                credentials=self.credentials,
                scope=self.scope,
                verify_ssl_certs=False  # Для корректной работы на Windows
            )
        return self._client
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True
    )
    def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> str:
        """
        Отправить запрос к GigaChat.
        
        Args:
            system_prompt: Системный промпт (роль)
            user_prompt: Пользовательский промпт (контент)
            temperature: Температура генерации (0.0-1.0)
            max_tokens: Максимальное количество токенов в ответе
            
        Returns:
            Ответ от GigaChat
            
        Raises:
            LLMError: При ошибке вызова API
        """
        logger.info(f"Отправка запроса к GigaChat ({self.model})...")
        logger.debug(f"System prompt: {system_prompt[:100]}...")
        logger.debug(f"User prompt length: {len(user_prompt)} символов")
        
        try:
            client = self._get_client()
            
            chat = Chat(
                messages=[
                    Messages(
                        role=MessagesRole.SYSTEM,
                        content=system_prompt
                    ),
                    Messages(
                        role=MessagesRole.USER,
                        content=user_prompt
                    )
                ],
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            response = client.chat(chat)
            
            if not response.choices:
                raise LLMError("Пустой ответ от GigaChat", provider=self.name)
            
            result = response.choices[0].message.content
            logger.info(f"Получен ответ: {len(result)} символов")
            
            return result
            
        except LLMError:
            raise
        except Exception as e:
            logger.error(f"Ошибка GigaChat: {e}")
            raise LLMError(str(e), provider=self.name)
    
    def is_available(self) -> bool:
        """
        Проверить доступность GigaChat API.
        
        Returns:
            True если API доступен
        """
        try:
            client = self._get_client()
            # Простой тестовый запрос
            response = client.chat("Привет")
            return bool(response.choices)
        except Exception as e:
            logger.warning(f"GigaChat недоступен: {e}")
            return False

