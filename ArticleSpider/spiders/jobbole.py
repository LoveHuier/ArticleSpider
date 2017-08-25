# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/112265/']

    def parse(self, response):
        title = response.xpath('//*[@id="post-112265"]/div[1]/h1/text()').extract()[0].strip()
        create_data = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace(
            " ·", "")
        pass
