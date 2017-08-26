# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.獲取文章列表頁中的文章url並交給scrapy下載後並進行解析
        2.獲取下一頁的url並交給scrapy進行下載，下載完成後交給parse
        """

        # 解析列表頁中的所有文章url並交給scrapy下載後並進行解析
        post_urls = response.css("#archive div.floated-thumb div.post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            """
            若提取的href中沒有域名，則需要提取到當前網頁的域名，並加上當前提取的href組成一個完整的鏈接.
            python3:from urllib import parse 利用urljoin方法通过response.url自动提取域名
            python2:import urlparse
            通过yield关键字将实例好的Request交给scrapy下载
            """
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

            """
            提取下一页的url并交给scrapy下载
            .next.page-numbers：表示它们同级 .next .page-numbers表示它们不同级
            """
            next_url = response.css(".next.page-numbers::attr(href)").extract_first()
            if next_url:
                yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        """
        提取文章的具体字段
        """
        # # extract()[0]等同於extract_first()：意思是先把response的數據解析成list,并取第一個值
        # title = response.xpath('//*[@id="post-112167"]/div[1]/h1/text()').extract_first().strip()
        # create_data = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().replace(
        #     " ·", "")
        # praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first())
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()
        # regex_str = ".*?(\d+).*"
        # match_obj = re.match(regex_str, fav_nums)
        # if match_obj:
        #     fav_nums = int(match_obj.group(1))
        # else:
        #     fav_nums = 0
        #
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        # match_obj = re.match(regex_str, comment_nums)
        # if match_obj:
        #     comment_nums = int(match_obj.group(1))
        # else:
        #     comment_nums = 0
        #
        # content = response.xpath("//div[@class='entry']").extract_first()
        #
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)

        # 通過css選擇器提取字段
        title = response.css(".entry-header h1::text").extract()
        create_data = response.css("p.entry-meta-hide-on-mobile::text").extract_first().replace(" ·", "").strip()
        praise_nums = int(response.css(".vote-post-up h10::text").extract_first())
        fav_nums = response.css("span.bookmark-btn::text").extract_first()
        regex_str = ".*?(\d+).*"
        match_obj = re.match(regex_str, fav_nums)
        if match_obj:
            fav_nums = int(match_obj.group(1))
        else:
            fav_nums = 0

        comment_nums = response.css("a[href='#article-comment'] span::text").extract_first()
        match_obj = re.match(regex_str, comment_nums)
        if match_obj:
            comment_nums = int(match_obj.group(1))
        else:
            comment_nums = 0

        content = response.css("div.entry").extract_first()
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
