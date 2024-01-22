
"""
@desc: 日期方法
"""


import calendar
import datetime
import math
import time



def get_now():
    """
    获取当前时间 yyyy-mm-dd
    :return:
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_current_month_days(year, month):
    """
    获取指定年月的天数
    :param year:
    :param month:
    :return:
    """
    return calendar.monthrange(year, month)[1]


def comput_time(start_time, end_time):
    """
    计算时长
    :param start_time: 开始时间，字符串
    :param end_time: 开始时间，字符串
    :return:
    """
    start = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
    end = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
    return round(int(end - start) / 60)


def get_prev_month_first_and_last_date(date_time):
    """
    根据当前时间计算上月的起止时间点
    :param date_time:
    :return:
    """
    prev_last_date = date_time - datetime.timedelta(days=1)
    prev_first_date = prev_last_date.replace(day=1)
    first_date = prev_first_date.strftime("%Y-%m-%d") + " 00:00:00"
    last_date = prev_last_date.strftime("%Y-%m-%d") + " 23:59:59"
    return first_date, last_date


def get_date_list(start=None, end=None):
    """
    获取指定两个日期之间的所有日期，返回一个列表
    :param start: 开始日期datetime对象
    :param end: 结束日期datetime对象
    :return:
    """
    if not start:
        start = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
    if not end:
        end = datetime.datetime.now()

    interval_day = (end - start).days
    if interval_day >= 180:
        raise ValueError("The maximum date that can be calculated is 180 days")

    data = []
    day = datetime.timedelta(days=1)
    for i in range(interval_day):
        date_string = (start + day * i).strftime("%Y-%m-%d %H:%M:%S")
        data.append(date_string)
    return data


def get_day_list(begin_date):
    """
    获取begin_date日期，到当前日期，所有日期，返回一个列表
    """
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def get_day_hour_minute(seconds: int):
    """
    根据间隔秒数， 转换字符串
    :param seconds:
    :return:
    """
    if not seconds:
        return '00 天 00 分 00 秒'
    else:
        day = math.floor(seconds / (60 * 60 * 24))
        hours = math.floor(seconds % (60 * 60 * 24) / (60 * 60))
        minutes = math.floor(seconds % (60 * 60) / 60)
        second = math.floor(seconds % 60)
        return str(day) + ' 天 ' + str(hours) + ' 小时 ' + str(minutes) + ' 分钟 ' + str(second) + ' 秒 '


if __name__ == '__main__':
    start = datetime.datetime.now().replace(year=2024, month=1, day=1)
    print(str(start))
    print(get_date_list(start=start))
    print(get_day_list("2024-01-01"))
    print(get_day_hour_minute(86400))
