"""
Content Manager Analyzer - анализ текстового контента лендинга.
"""

import re
import logging
from typing import List

from core.interfaces import BaseAnalyzer, BaseLLMProvider
from core.models import PageContent, AnalysisResult, Recommendation


logger = logging.getLogger(__name__)


class ContentManagerAnalyzer(BaseAnalyzer):
    """
    Анализатор текстового контента лендинга.
    
    Роль: опытный контент-менеджер и копирайтер.
    Анализирует: заголовки, УТП, CTA-тексты, читаемость, убедительность.
    """
    
    name = "Контент-менеджер"
    description = "Анализ текстов, заголовков и призывов к действию"
    is_premium = False  # Бесплатный модуль
    
    SYSTEM_PROMPT = """Ты опытный контент-менеджер и копирайтер с 10-летним стажем работы над продающими текстами для лендингов.

Твоя задача — проанализировать текстовое содержимое лендинга и дать ровно 5 конкретных, практичных рекомендаций по улучшению контента.

Фокусируйся на:
1. Заголовках и подзаголовках (привлекают ли внимание, понятны ли)
2. Уникальном торговом предложении (УТП) — чётко ли оно сформулировано
3. Призывах к действию (CTA-тексты) — мотивируют ли они к действию
4. Читаемости и структуре текста (абзацы, списки, акценты)
5. Убедительности и аргументации (доказательства, выгоды, социальные подтверждения)

Формат ответа:
Каждая рекомендация должна быть в формате:
[Номер]. [Краткий заголовок]
[Подробное описание проблемы и конкретное решение]

Пример:
1. Усилить заголовок главной секции
Текущий заголовок "Добро пожаловать" не несёт ценности для посетителя. Рекомендую заменить на заголовок с выгодой: "Увеличьте продажи на 30% за 2 недели" или "Решение [проблемы] за [время]".

Отвечай на русском языке. Будь конкретен — приводи примеры улучшенных формулировок."""

    def get_system_prompt(self) -> str:
        """Получить системный промпт."""
        return self.SYSTEM_PROMPT
    
    def parse_response(self, response: str) -> List[Recommendation]:
        """
        Распарсить ответ LLM в список рекомендаций.
        
        Args:
            response: Сырой ответ от LLM
            
        Returns:
            Список рекомендаций
        """
        recommendations = []
        
        # Ищем паттерн: "N. Заголовок\nОписание"
        pattern = r'(\d+)\.\s*(.+?)(?:\n|$)([\s\S]*?)(?=\d+\.|$)'
        matches = re.findall(pattern, response)
        
        if matches:
            for match in matches[:5]:  # Максимум 5 рекомендаций
                number = int(match[0])
                title = match[1].strip()
                description = match[2].strip()
                
                if title and description:
                    recommendations.append(Recommendation(
                        number=number,
                        title=title,
                        description=description,
                        priority="medium"
                    ))
        
        # Если не удалось распарсить, создаём одну общую рекомендацию
        if not recommendations:
            logger.warning("Не удалось распарсить ответ, сохраняем как есть")
            recommendations.append(Recommendation(
                number=1,
                title="Рекомендации по контенту",
                description=response.strip(),
                priority="medium"
            ))
        
        return recommendations

