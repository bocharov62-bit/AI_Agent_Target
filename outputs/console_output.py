"""
Console Output - вывод результатов в консоль.
"""

from typing import List

from core.interfaces import BaseOutput
from core.models import AnalysisResult


class ConsoleOutput(BaseOutput):
    """
    Вывод результатов анализа в консоль.
    
    Форматирует результаты для читаемого отображения в терминале.
    """
    
    name = "Console Output"
    description = "Вывод результатов в консоль"
    
    # Цвета для терминала (ANSI escape codes)
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
    }
    
    def __init__(self, use_colors: bool = True):
        """
        Инициализация.
        
        Args:
            use_colors: Использовать цветной вывод
        """
        self.use_colors = use_colors
    
    def _color(self, text: str, color: str) -> str:
        """Добавить цвет к тексту."""
        if not self.use_colors:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
    
    def _print_header(self, text: str) -> None:
        """Напечатать заголовок."""
        line = "=" * 60
        print(f"\n{self._color(line, 'cyan')}")
        print(self._color(f"  {text}", 'bold'))
        print(f"{self._color(line, 'cyan')}\n")
    
    def _print_subheader(self, text: str) -> None:
        """Напечатать подзаголовок."""
        print(f"\n{self._color('-' * 50, 'blue')}")
        print(self._color(f"  {text}", 'magenta'))
        print(f"{self._color('-' * 50, 'blue')}\n")
    
    def output(self, result: AnalysisResult) -> None:
        """
        Вывести результат анализа одного модуля.
        
        Args:
            result: Результат анализа
        """
        self._print_subheader(f"[*] {result.module_name}")
        print(f"   {self._color(result.module_description, 'yellow')}")
        print(f"   URL: {result.url}")
        print()
        
        if not result.recommendations:
            print("   Рекомендации не найдены.")
            return
        
        for rec in result.recommendations:
            print(f"   {self._color(f'{rec.number}.', 'green')} "
                  f"{self._color(rec.title, 'bold')}")
            
            # Форматируем описание с отступом
            lines = rec.description.split('\n')
            for line in lines:
                if line.strip():
                    print(f"      {line.strip()}")
            print()
    
    def output_full(self, results: List[AnalysisResult]) -> None:
        """
        Вывести результаты от нескольких модулей.
        
        Args:
            results: Список результатов анализа
        """
        if not results:
            print("Нет результатов для отображения.")
            return
        
        url = results[0].url if results else "Unknown"
        total_recommendations = sum(len(r.recommendations) for r in results)
        
        self._print_header(f"[ANALYSIS] АНАЛИЗ ЛЕНДИНГА")
        print(f"   URL: {self._color(url, 'cyan')}")
        print(f"   Модулей: {len(results)}")
        print(f"   Рекомендаций: {total_recommendations}")
        
        for result in results:
            self.output(result)
        
        # Итоговая линия
        print(f"\n{self._color('=' * 60, 'cyan')}")
        print(self._color(f"  [OK] Анализ завершен. Всего рекомендаций: {total_recommendations}", 'green'))
        print(f"{self._color('=' * 60, 'cyan')}\n")
