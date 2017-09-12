# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
用来做跟数据存储有关的一个地方
"""
import codecs  # 与open最大的差别就是文件的编码，可以避免很多编码的繁杂工作
import json

from scrapy.pipelines.images import ImagesPipeline


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        """
        处理item的关键方法，将item写入到文件中
        :param item:
        :param spider:
        :return:
        """
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"  # dumps将dict转化为str
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()


class ArticleImagePipeline(ImagesPipeline):
    """
    自定义图片通道，用于下载，处理图片，继承自ImagesPipeline
    """

    def item_completed(self, results, item, info):
        """

        :param results:一个存放着tuple的list
        :param item: 保存数据的一个item对象
        :param info:
        :return: 返回item，以便于其它通道处理
        """
        for ok, value in results:
            image_file_path = value['path']
            item["front_image_path"] = image_file_path

        return item
