"""
Модели данных приложения.

Pydantic-модели для типизации и валидации данных.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class PageContent(BaseModel):
    """Содержимое веб-страницы."""
    
    url: str = Field(..., description="URL страницы")
    title: Optional[str] = Field(None, description="Заголовок страницы")
    text: str = Field(..., description="Текстовое содержимое")
    html: Optional[str] = Field(None, description="HTML-код (опционально)")
    fetched_at: datetime = Field(
        default_factory=datetime.now,
        description="Время загрузки"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "title": "Example Landing Page",
                "text": "Welcome to our amazing product...",
                "fetched_at": "2026-01-01T12:00:00"
            }
        }


class Recommendation(BaseModel):
    """Одна рекомендация по улучшению."""
    
    number: int = Field(..., ge=1, le=10, description="Номер рекомендации")
    title: str = Field(..., description="Краткий заголовок")
    description: str = Field(..., description="Подробное описание")
    priority: Optional[str] = Field(
        None, 
        description="Приоритет: high, medium, low"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "number": 1,
                "title": "Улучшить CTA-кнопку",
                "description": "Сделайте кнопку призыва к действию более заметной...",
                "priority": "high"
            }
        }


class AnalysisResult(BaseModel):
    """Результат анализа от одного модуля."""
    
    module_name: str = Field(..., description="Название модуля анализа")
    module_description: str = Field(..., description="Описание модуля")
    url: str = Field(..., description="Анализируемый URL")
    recommendations: List[Recommendation] = Field(
        default_factory=list,
        description="Список рекомендаций"
    )
    raw_response: Optional[str] = Field(
        None, 
        description="Сырой ответ от LLM"
    )
    analyzed_at: datetime = Field(
        default_factory=datetime.now,
        description="Время анализа"
    )
    tokens_used: Optional[int] = Field(
        None,
        description="Использовано токенов"
    )
    
    @property
    def recommendations_count(self) -> int:
        """Количество рекомендаций."""
        return len(self.recommendations)
    
    class Config:
        json_schema_extra = {
            "example": {
                "module_name": "UI Designer",
                "module_description": "Анализ дизайна и структуры",
                "url": "https://example.com",
                "recommendations": [],
                "analyzed_at": "2026-01-01T12:00:00"
            }
        }


class FullAnalysisResult(BaseModel):
    """Полный результат анализа от всех модулей."""
    
    url: str = Field(..., description="Анализируемый URL")
    results: List[AnalysisResult] = Field(
        default_factory=list,
        description="Результаты от всех модулей"
    )
    total_recommendations: int = Field(
        default=0,
        description="Общее количество рекомендаций"
    )
    analyzed_at: datetime = Field(
        default_factory=datetime.now,
        description="Время анализа"
    )
    
    def add_result(self, result: AnalysisResult) -> None:
        """Добавить результат модуля."""
        self.results.append(result)
        self.total_recommendations += result.recommendations_count

