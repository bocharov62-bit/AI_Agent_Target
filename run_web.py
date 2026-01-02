#!/usr/bin/env python3
"""
Запуск веб-сервера Landing Redesign Assistant.

Использование:
    python run_web.py
    python run_web.py --port 8080
    python run_web.py --host 0.0.0.0 --port 8000
"""

import argparse
import sys
import os

# Добавляем корневую папку в путь для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn


def main():
    parser = argparse.ArgumentParser(description="Запуск веб-сервера Landing Redesign Assistant")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Хост для запуска сервера (по умолчанию: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Порт для запуска сервера (по умолчанию: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Автоматическая перезагрузка при изменении кода (для разработки)"
    )
    
    args = parser.parse_args()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🚀  LANDING REDESIGN ASSISTANT                             ║
║                                                              ║
║   Веб-интерфейс запущен!                                     ║
║                                                              ║
║   Откройте в браузере:                                       ║
║   http://{args.host}:{args.port}                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()

