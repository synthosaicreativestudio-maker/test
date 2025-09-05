from src.miniapps.auth import validate_employee_code, validate_phone


def test_validate_employee_code():
    assert validate_employee_code('123')
    assert not validate_employee_code('abc')
    assert not validate_employee_code('')


def test_validate_phone():
    assert validate_phone('89827701055')
    assert not validate_phone('987701055')
    assert not validate_phone('a9827701055')
