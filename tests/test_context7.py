import asyncio
from unittest.mock import patch

from src.mcp.context7_client import Context7Client


class DummyResp:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data


class DummyAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, json=None):
        return DummyResp(200, {"results": ["doc1", "doc2"]})

    async def get(self, url):
        return DummyResp(200, {"id": url})


def test_search_monkeypatch(monkeypatch):
    monkeypatch.setattr('httpx.AsyncClient', DummyAsyncClient)

    async def run():
        client = Context7Client('https://example.com')
        res = await client.search('test')
        assert 'results' in res

    asyncio.get_event_loop().run_until_complete(run())


def test_get_doc_monkeypatch(monkeypatch):
    monkeypatch.setattr('httpx.AsyncClient', DummyAsyncClient)

    async def run():
        client = Context7Client('https://example.com')
        res = await client.get_doc('abc')
        assert res and 'id' in res

    asyncio.get_event_loop().run_until_complete(run())
