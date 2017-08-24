# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
用来做跟数据存储有关的一个地方
"""

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
