# _*_ encoding:utf-8 _*_
__author__ = 'Gaoyp'
__date__ = '17-8-24 下午5:25'

"""
自定义调试工具
"""

from scrapy.cmdline import execute  # scrapy自带的调试命令行

import sys
import os

# __file__当前py文件
current_file_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(current_file_path))  # 设置工程目录后，调用execute才会生效

#執行爬蟲的命令
execute(["scrapy", "crawl", "jobbole"])
