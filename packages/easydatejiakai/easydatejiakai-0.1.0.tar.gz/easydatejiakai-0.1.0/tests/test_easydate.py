# tests/test_easydate.py
from easydatejiakai import get_current_datetime, calculate_days_between, get_weekday

def test_get_current_datetime_format():
    dt = get_current_datetime()
    assert isinstance(dt, str)
    assert len(dt) == 19  # 格式应该是 YYYY-MM-DD HH:MM:SS

def test_calculate_days_between_examples():
    # 通常日期
    assert calculate_days_between("2024-01-01", "2024-01-31") == 30
    # 逆序日期
    assert calculate_days_between("2024-01-31", "2024-01-01") == -30
    # 相同日期
    assert calculate_days_between("2024-01-01", "2024-01-01") == 0
    # 闰年
    assert calculate_days_between("2024-02-28", "2024-03-01") == 2

def test_get_weekday_examples():
    # 测试一周的每一天
    assert get_weekday("2024-01-01") == "Monday"
    assert get_weekday("2024-01-02") == "Tuesday"
    assert get_weekday("2024-01-03") == "Wednesday"
    assert get_weekday("2024-01-04") == "Thursday"
    assert get_weekday("2024-01-05") == "Friday"
    assert get_weekday("2024-01-06") == "Saturday"
    assert get_weekday("2024-01-07") == "Sunday"
