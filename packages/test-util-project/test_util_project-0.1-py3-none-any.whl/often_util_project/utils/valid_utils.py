#! -*- coding:utf-8 -*
"""
@desc: 校验方法
"""

import re


def validate_phone_number(number):
    pattern = r'^1[3-9]\d{9}$'
    if re.match(pattern, number):
        return True
    else:
        return False


def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


def is_str_ip_v4(ip_str):
    """
    判断字符串是不是ipv4
    """
    if ip_str is None:
        return False
    v4_regex = "^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]?\d)" \
               "(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]?\d)){3}$"
    return re.match(v4_regex, ip_str) is not None

