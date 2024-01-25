# 导入 datetime 模块
from datetime import datetime

def get_current_datetime():
    # 获取当前日期和时间
    now = datetime.now()
    # 将日期和时间转换为易读的字符串格式
    return now.strftime("%Y-%m-%d %H:%M:%S")

def calculate_days_between(d1, d2):
    # 将字符串日期转换为 datetime 对象
    date1 = datetime.strptime(d1, "%Y-%m-%d")
    date2 = datetime.strptime(d2, "%Y-%m-%d")
    # 计算两个日期之间的差值
    delta = date2 - date1
    # 返回天数差
    return delta.days

def get_weekday(date):
    # 将字符串日期转换为 datetime 对象
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    # 获取星期几的名称
    return date_obj.strftime("%A")