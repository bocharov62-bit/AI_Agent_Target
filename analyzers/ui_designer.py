"""
UI Designer Analyzer - анализ дизайна и структуры лендинга.
"""

import re
import logging
from typing import List

from core.interfaces import BaseAnalyzer, BaseLLMProvider
from core.models import PageContent, AnalysisResult, Recommendation


logger = logging.getLogger(__name__)


class UIDesignerAnalyzer(BaseAnalyzer):
    """
    Анализатор дизайна и структуры лендинга.
    
    Роль: опытный UI/UX дизайнер.
    Анализирует: структуру, визуальную иерархию, CTA, навигацию, адаптивность.
    """
    
    name = "UI-дизайнер"
    description = "Анализ дизайна, структуры и пользовательского опыта"
    is_premium = False  # Бесплатный модуль
    
    SYSTEM_PROMPT = """Ты опытный UI/UX дизайнер с 10-летним стажем работы над лендингами и коммерческими сайтами.

Твоя задача — проанализировать содержимое лендинга и дать ровно 5 конкретных, практичных рекомендаций по улучшению дизайна и структуры.

Фокусируйся на:
1. Структуре и расположении блоков (hero-секция, преимущества, CTA)
2. Визуальной иерархии (что привлекает внимание первым)
3. Кнопках и призывах к действию (размер, цвет, расположение, текст)
4. Навигации и удобстве использования
5. Адаптивности под мобильные устройства

Формат ответа:
Каждая рекомендация должна быть в формате:
[Номер]. [Краткий заголовок]
[Подробное описание проблемы и конкретное решение]

Пример:
1. Увеличить размер CTA-кнопки
Главная кнопка призыва к действию слишком мелкая и теряется на фоне. Рекомендую увеличить её минимум до 48px в высоту и использовать контрастный цвет (например, оранжевый или зелёный).

Отвечай на русском языке. Будь конкретен — указывай что именно изменить и как."""

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
                title="Рекомендации по дизайну",
                description=response.strip(),
                priority="medium"
            ))
        
        return recommendations

