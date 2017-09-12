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
from scrapy.exporters import JsonItemExporter  # scrapy本身也提供了写入json的机制


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    """
    自定义json文件的导出
    """

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

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipleline(object):
    """
    调用scrapy提供的json export导出json文件
    """

    def __init__(self):
        self.file = open("articleexport.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
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
