from src.miniapps.welcome import format_name


def test_format_name_full():
    assert format_name('Иван', 'Иванов', 'ivan') == 'Иван Иванов'


def test_format_name_first_only():
    assert format_name('Мария', None, None) == 'Мария'


def test_format_name_username_fallback():
    assert format_name(None, None, 'user123') == 'user123'


def test_format_name_empty():
    assert format_name(None, None, None) == 'пользователь'
