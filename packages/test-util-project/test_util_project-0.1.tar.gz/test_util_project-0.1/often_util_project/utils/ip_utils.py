#! -*- coding:utf-8 -*
"""
@desc: ip方法
"""

import ipaddress


def is_subnet_of(a, b):
    """
    Returns True if network a is a subnet of network b.
    网络a是网络b的子网，返回true
    @param a: 子网
    @param b: 父网
    @return:  bool
    """

    try:
        # 将前缀转换为IP网络对象
        a_network = ipaddress.ip_network(a, strict=True)
        b_network = ipaddress.ip_network(b, strict=True)
        return (a_network.network_address >= b_network.network_address and
                a_network.broadcast_address <= b_network.broadcast_address)
    except Exception as e:
        print(e)
        return False


def count_ips(prefix: str, ip_type) -> int:
    """
    计算前缀的ip数
    @param prefix: 前缀地址
    @param ip_type: 前缀类型
    @return: 有效ip数
    """
    # 子网掩码
    subnet_mask = int(prefix.split("/")[-1])
    if ip_type == "ipv4":
        net_mask = 32
        valid_ips = 1 if subnet_mask == net_mask else (2 ** (net_mask - subnet_mask)) - 2
    else:
        net_mask = 128
        valid_ips = 1 if subnet_mask == net_mask else 2 ** (net_mask - subnet_mask)
    return valid_ips


def identify_ip_network(ip: str) -> (bool, str):
    """
    校验前缀合法性、类型
    @param ip: ipv4/ipv6的前缀
    @return:
    """
    ip_type = "无效前缀"

    # 192.168.1.1会被解释为192.168.1.1/32
    if '/' not in ip:
        # 没有掩码
        return False, ip_type

    try:
        network = ipaddress.ip_network(ip, strict=True)
    except ValueError:
        return False, ip_type

    # 查询ip类型
    if isinstance(network, ipaddress.IPv4Network):
        return True, "ipv4"
    elif isinstance(network, ipaddress.IPv6Network):
        return True, "ipv6"
    else:
        return False, ip_type

if __name__ == '__main__':
    print(is_subnet_of("5.8.0.0/16", "5.5.0.0/17"))
    print(count_ips("2001:0db8::/32", "ipv6"))
    print(count_ips("1.1.1.4/24", "ipv4"))