import os
import sys

# Пути: добавить корень репозитория в sys.path чтобы можно было импортировать src
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.miniapps.base import BaseMiniApp


class DummyApp(BaseMiniApp):
    name = 'dummy'

    def setup(self, dp):
        # Простая реализация, возвращаем признак выполнения
        return True


def test_dummy_setup():
    d = DummyApp()
    assert d.setup(None) is True
