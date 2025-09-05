"""Базовая интерфейсная часть для мини-приложений (miniapps)."""

from typing import Any


class BaseMiniApp:
    """Контракт миниаппа.

    Методы:
      - setup(dp): регистрирует обработчики на переданный диспетчер.
    """

    name: str = 'base'

    def setup(self, dp: Any):
        """Настроить обработчики в диспетчере `dp`.

        dp — любой объект, предоставляющий API регистрации обработчиков (например, aiogram.Dispatcher).
        """
        raise NotImplementedError()
