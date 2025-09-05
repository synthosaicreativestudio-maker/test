"""Обёртка для локального MCP (mcp_context_v7.py).

Предназначена для использования внутри бота как единственный экземпляр контекста.
"""
from typing import Optional, List, Tuple
import logging

from mcp_context_v7 import MCPContextV8

logger = logging.getLogger(__name__)


# Singleton instance
mcp_local = MCPContextV8()


def create_thread_for_user(user_key: str) -> str:
    return mcp_local.create_thread(user_key)


def register_thread(thread_id: str, user_key: str) -> None:
    return mcp_local.register_thread(thread_id, user_key)


def append_message(thread_id: str, role: str, text: str) -> None:
    return mcp_local.append_message(thread_id, role, text)


def get_messages(thread_id: str) -> List[Tuple[str, str, float]]:
    return mcp_local.get_messages(thread_id)


def get_context_summary(thread_id: str, max_chars: int = 1000) -> str:
    return mcp_local.get_context_summary(thread_id, max_chars=max_chars)


def cleanup_and_save():
    return mcp_local.cleanup_and_save()
