# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/112265/']

    def parse(self, response):
        title = response.xpath('//*[@id="post-112265"]/div[1]/h1/text()').extract()[0].strip()
        create_data = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace(
            " ·", "")
        praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        regex_str = ".*(\d+).*"
        match_obj = re.match(regex_str, fav_nums)
        if match_obj:
            fav_nums = match_obj.group(1)

        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_obj = re.match(regex_str, comment_nums)
        if match_obj:
            comment_nums = match_obj.group(1)

        content = response.xpath("//div[@class='entry']").extract()[0]

        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
