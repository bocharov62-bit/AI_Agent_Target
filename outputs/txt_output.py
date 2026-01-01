"""
TXT Output - сохранение результатов в текстовый файл.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from core.interfaces import BaseOutput
from core.models import AnalysisResult
from core.utils import get_file_timestamp


class TxtOutput(BaseOutput):
    """
    Сохранение результатов анализа в TXT-файл.
    
    Формат: UTF-8, читаемый текст.
    """
    
    name = "TXT Output"
    description = "Сохранение результатов в текстовый файл"
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Инициализация.
        
        Args:
            output_dir: Директория для сохранения файлов
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
    
    def _generate_filename(self, url: str) -> str:
        """Сгенерировать имя файла."""
        timestamp = get_file_timestamp()
        # Извлекаем домен из URL для имени файла
        domain = url.replace("https://", "").replace("http://", "")
        domain = domain.split("/")[0].replace(".", "_")
        return f"analysis_{domain}_{timestamp}.txt"
    
    def _format_result(self, result: AnalysisResult) -> str:
        """Форматировать результат одного модуля."""
        lines = []
        lines.append(f"\n{'─' * 50}")
        lines.append(f"📊 {result.module_name}")
        lines.append(f"   {result.module_description}")
        lines.append(f"{'─' * 50}\n")
        
        if not result.recommendations:
            lines.append("   Рекомендации не найдены.\n")
            return "\n".join(lines)
        
        for rec in result.recommendations:
            lines.append(f"{rec.number}. {rec.title}")
            lines.append(f"   {rec.description}")
            lines.append("")
        
        return "\n".join(lines)
    
    def output(self, result: AnalysisResult, filename: Optional[str] = None) -> str:
        """
        Сохранить результат анализа в файл.
        
        Args:
            result: Результат анализа
            filename: Имя файла (опционально)
            
        Returns:
            Путь к сохранённому файлу
        """
        if filename is None:
            filename = self._generate_filename(result.url)
        
        filepath = self.output_dir / filename
        
        content = []
        content.append("=" * 60)
        content.append("  АНАЛИЗ ЛЕНДИНГА")
        content.append("=" * 60)
        content.append(f"\nURL: {result.url}")
        content.append(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        content.append(self._format_result(result))
        content.append("\n" + "=" * 60)
        content.append("  Сгенерировано: Landing Redesign Assistant")
        content.append("=" * 60)
        
        text = "\n".join(content)
        
        filepath.write_text(text, encoding="utf-8")
        
        return str(filepath)
    
    def output_full(self, results: List[AnalysisResult], filename: Optional[str] = None) -> str:
        """
        Сохранить результаты от нескольких модулей.
        
        Args:
            results: Список результатов анализа
            filename: Имя файла (опционально)
            
        Returns:
            Путь к сохранённому файлу
        """
        if not results:
            return ""
        
        url = results[0].url
        if filename is None:
            filename = self._generate_filename(url)
        
        filepath = self.output_dir / filename
        
        total_recommendations = sum(len(r.recommendations) for r in results)
        
        content = []
        content.append("=" * 60)
        content.append("  АНАЛИЗ ЛЕНДИНГА")
        content.append("=" * 60)
        content.append(f"\nURL: {url}")
        content.append(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        content.append(f"Модулей анализа: {len(results)}")
        content.append(f"Всего рекомендаций: {total_recommendations}")
        
        for result in results:
            content.append(self._format_result(result))
        
        content.append("\n" + "=" * 60)
        content.append("  Сгенерировано: Landing Redesign Assistant")
        content.append("=" * 60)
        
        text = "\n".join(content)
        
        filepath.write_text(text, encoding="utf-8")
        
        return str(filepath)

