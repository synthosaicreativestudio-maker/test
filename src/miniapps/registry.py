"""Регистрация всех мини-приложений."""


def register_all(dp):
    """Зарегистрировать доступные миниаппы в диспетчере.

    Добавляйте новые модули миниаппов в этот файл.
    """
    # Импортировать и вызывать setup каждого миниаппа
    # Регистрируем миниаппы по очереди. Каждый миниапп аккуратно обрабатывает отсутствие aiogram.
    for module in ('echo', 'welcome', 'auth', 'webapp'):
        try:
            mod = __import__(f'src.miniapps.{module}', fromlist=['*'])
            if hasattr(mod, 'setup'):
                mod.setup(dp)
                print(f'✅ Миниапп {module} загружен')
        except Exception:
            # Не падаем при импорте — логируем и продолжаем
            import traceback
            print(f'❌ Ошибка загрузки миниаппа {module}:')
            traceback.print_exc()
