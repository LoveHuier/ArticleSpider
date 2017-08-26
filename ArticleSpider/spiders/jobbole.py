# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/112167/']

    def parse(self, response):
        # extract()[0]等同於extract_first()：意思是先把response的數據解析成list,并取第一個值
        title = response.xpath('//*[@id="post-112167"]/div[1]/h1/text()').extract_first().strip()
        create_data = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().replace(
            " ·", "")
        praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first())
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()
        regex_str = ".*?(\d+).*"
        match_obj = re.match(regex_str, fav_nums)
        if match_obj:
            fav_nums = match_obj.group(1)

        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        match_obj = re.match(regex_str, comment_nums)
        if match_obj:
            comment_nums = match_obj.group(1)

        content = response.xpath("//div[@class='entry']").extract_first()

        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        # 通過css選擇器提取字段
        title = response.css(".entry-header h1::text").extract()
        create_data = response.css("p.entry-meta-hide-on-mobile::text").extract_first().replace(" ·", "").strip()
        praise_nums = int(response.css(".vote-post-up h10::text").extract_first())
        fav_nums = response.css("span.bookmark-btn::text").extract_first()
        regix_str = ".*?(\d*).*"
        match_obj = re.match(regix_str, fav_nums)
        if match_obj:
            fav_nums = match_obj.group(1)

        comment_nums = response.css("a[href='#article-comment'] span::text").extract_first()
        match_obj = re.match(regex_str, comment_nums)
        if match_obj:
            comment_nums = match_obj.group(1)

        content = response.css("div.entry").extract_first()
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
