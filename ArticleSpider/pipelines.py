# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
用来做跟数据存储有关的一个地方
"""

from scrapy.pipelines.images import ImagesPipeline


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


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
