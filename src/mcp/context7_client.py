"""Простой HTTP-клиент для Context7 MCP Server.

Описание:
- Клиент предоставляет минимальный метод `search(query)` для отправки запроса в
  Context7 MCP сервер по HTTP и получения JSON-ответа.
- Реализован осторожный перебор популярных конечных точек (`/search`, `/query`, `/mcp/v1/search`).
- Используется `httpx.AsyncClient` для асинхронных запросов.

Этот модуль не жестко зависит от специфики Context7 и служит простой обёрткой.
"""
from typing import Any, Dict, Optional
import httpx


class Context7Client:
    def __init__(self, base_url: str, timeout: int = 10):
        if not base_url:
            raise ValueError('base_url должен быть указан')
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    async def search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Отправить запрос поиска в Context7 и вернуть JSON-ответ.

        Пытается несколько стандартных путей и возвращает первый успешный ответ.
        """
        if not query:
            raise ValueError('query не может быть пустым')

        endpoints = [
            f"{self.base_url}/search",
            f"{self.base_url}/query",
            f"{self.base_url}/mcp/v1/search",
        ]

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for url in endpoints:
                try:
                    resp = await client.post(url, json={"q": query, "top_k": top_k})
                    if resp.status_code == 200:
                        return resp.json()
                except httpx.HTTPError:
                    # Переходим к следующему эндпойнту
                    continue

        raise RuntimeError('Не удалось получить ответ от Context7 по указанным эндпойнтам')

    async def get_doc(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Попытка получить конкретный документ по id (если поддерживается сервером)."""
        if not doc_id:
            raise ValueError('doc_id не может быть пустым')
        url = f"{self.base_url}/doc/{doc_id}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    return resp.json()
            except httpx.HTTPError:
                return None
        return None
