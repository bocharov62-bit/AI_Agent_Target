"""
FastAPI веб-приложение для Landing Redesign Assistant.
"""

import logging
from typing import List, Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from pydantic import HttpUrl
import os

from core.config import settings
from core.exceptions import ScraperError, LLMError
from core.models import AnalysisResult
from core.utils import validate_url

from scrapers.html_parser import HTMLParser
from llm_providers.gigachat_provider import GigaChatProvider
from analyzers.ui_designer import UIDesignerAnalyzer
from analyzers.content_manager import ContentManagerAnalyzer
from outputs.txt_output import TxtOutput


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI(
    title="Landing Redesign Assistant",
    description="AI-агент для анализа лендингов",
    version="1.0.0"
)

# Статические файлы и шаблоны
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Jinja2 templates
env = Environment(loader=FileSystemLoader(templates_dir))

def render_template(template_name: str, context: dict, request: Request):
    """Рендерит Jinja2 шаблон."""
    template = env.get_template(template_name)
    context["request"] = request
    return HTMLResponse(content=template.render(context))

# Доступные модули анализа
ANALYZERS = {
    "ui": {
        "class": UIDesignerAnalyzer,
        "name": "UI-дизайнер",
        "description": "Анализ дизайна и структуры",
        "premium": False
    },
    "content": {
        "class": ContentManagerAnalyzer,
        "name": "Контент-менеджер",
        "description": "Анализ текстов и копирайтинга",
        "premium": False
    }
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница с формой анализа."""
    return render_template("index.html", {
        "analyzers": ANALYZERS
    }, request)


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    url: str = Form(...),
    role: str = Form(...)
):
    """
    Обработка запроса на анализ лендинга.
    
    Args:
        request: FastAPI Request
        url: URL для анализа
        role: Роль ('ui', 'content' или 'all')
    """
    try:
        # Валидация URL
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        if not validate_url(url):
            raise HTTPException(status_code=400, detail="Некорректный URL")
        
        # Валидация роли
        if role not in ["ui", "content", "all"]:
            raise HTTPException(status_code=400, detail="Некорректная роль")
        
        logger.info(f"Анализ запрошен: {url}, роль: {role}")
        
        # Инициализация LLM-провайдера
        try:
            llm_provider = GigaChatProvider()
        except LLMError as e:
            logger.error(f"Ошибка GigaChat: {e}")
            return render_template("error.html", {
                "error": f"Ошибка настройки GigaChat: {e}"
            }, request)
        
        # Загрузка страницы
        scraper = HTMLParser()
        content = scraper.fetch_and_parse(url)
        
        # Определение модулей анализа
        if role == "all":
            analyzer_keys = ["ui", "content"]
        else:
            analyzer_keys = [role]
        
        # Анализ
        results = []
        for key in analyzer_keys:
            analyzer_info = ANALYZERS[key]
            analyzer = analyzer_info["class"](llm_provider)
            result = analyzer.analyze(content)
            results.append(result)
        
        # Отображение результатов
        return render_template("results.html", {
            "url": url,
            "results": results,
            "total_recommendations": sum(len(r.recommendations) for r in results)
        }, request)
        
    except ScraperError as e:
        logger.error(f"Ошибка парсинга: {e}")
        return render_template("error.html", {
            "error": f"Ошибка загрузки страницы: {e}"
        }, request)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Неожиданная ошибка")
        return render_template("error.html", {
            "error": f"Неожиданная ошибка: {e}"
        }, request)


@app.post("/download")
async def download_results(
    url: str = Form(...),
    role: str = Form(...)
):
    """
    Скачать результаты анализа в TXT-файле.
    
    Args:
        url: URL анализируемой страницы
        role: Роль анализа
    """
    try:
        # Восстанавливаем результаты (в реальном приложении лучше хранить в сессии/БД)
        # Для MVP - перезапрашиваем анализ
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        llm_provider = GigaChatProvider()
        scraper = HTMLParser()
        content = scraper.fetch_and_parse(url)
        
        if role == "all":
            analyzer_keys = ["ui", "content"]
        else:
            analyzer_keys = [role]
        
        results = []
        for key in analyzer_keys:
            analyzer_info = ANALYZERS[key]
            analyzer = analyzer_info["class"](llm_provider)
            result = analyzer.analyze(content)
            results.append(result)
        
        # Сохранение в файл
        txt_output = TxtOutput(output_dir="output")
        filepath = txt_output.output_full(results)
        
        return FileResponse(
            filepath,
            media_type="text/plain",
            filename=f"analysis_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.txt"
        )
        
    except Exception as e:
        logger.exception("Ошибка при создании файла")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

