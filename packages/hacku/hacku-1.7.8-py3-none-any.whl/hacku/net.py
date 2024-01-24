# coding=utf-8

import random
import socket
import struct

from loguru import logger

from hacku.ip2region import Ip2Region


def query_ip_location(ip):
    """
    查询IP归属地信息
    """
    searcher = Ip2Region()
    if searcher.conn_obj is False:
        logger.error(f'初始化连接IP位置数据库失败')
        return

    if not searcher.isip(ip):
        logger.error(f'IP：{ip} 地址格式有误，请从新输入')

    data = searcher.btreeSearch(ip)
    region = data["region"].decode('utf-8')
    searcher.close()
    split_data = str(region).split('|') if '|' in region else ["", "", "", ""]

    return {
        "info": region,
        "country": split_data[0] if str(split_data[0]) != "0" else "",
        "city": split_data[3] if str(split_data[3]) != "0" else ""
    }


def gen_random_ip(rand_list):
    """
    从指定的CIDR地址段内随机生成IP
    @rand_list: [xx.xx.xx.xx/x]
    """
    str_ip = rand_list[random.randint(0, len(rand_list) - 1)]
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mask = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I', socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    for i in range(31, 31 - int(str_ip_mask), -1):
        mask = mask | (1 << i)
    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))


def is_valid_ip(ip):
    try:
        # 尝试将 IP 地址转换为二进制格式
        socket.inet_aton(ip)
        return True
    except:
        # 转换失败说明 IP 地址不合法
        return False
