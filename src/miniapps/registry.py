"""Регистрация всех мини-приложений."""


def register_all(dp):
    """Зарегистрировать доступные миниаппы в диспетчере.

    Добавляйте новые модули миниаппов в этот файл.
    """
    # Импортировать и вызывать setup каждого миниаппа
    # Регистрируем миниаппы по очереди. Каждый миниапп аккуратно обрабатывает отсутствие aiogram.
    for module in ('echo', 'welcome', 'auth'):
        try:
            mod = __import__(f'src.miniapps.{module}', fromlist=['*'])
            if hasattr(mod, 'setup'):
                mod.setup(dp)
        except Exception:
            # Не падаем при импорте — логируем и продолжаем
            import traceback
            traceback.print_exc()
