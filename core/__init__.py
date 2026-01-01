"""
Core module - ядро системы Landing Redesign Assistant.

Содержит базовые классы, интерфейсы, модели данных и конфигурацию.
"""

from core.config import settings
from core.models import PageContent, AnalysisResult, Recommendation
from core.interfaces import BaseAnalyzer, BaseScraper, BaseLLMProvider, BaseOutput

__all__ = [
    "settings",
    "PageContent",
    "AnalysisResult", 
    "Recommendation",
    "BaseAnalyzer",
    "BaseScraper",
    "BaseLLMProvider",
    "BaseOutput",
]

