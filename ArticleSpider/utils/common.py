# _*_ encoding:utf-8 _*_
__author__ = 'Gaoyp'
__date__ = '17-9-8 下午5:05'

import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    # 加密后的结果用16进制表示
    return m.hexdigest()
