# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 这是爬虫名
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口URL,扔到调度器去
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # 循环电影条目
        movie_list = response.xpath('//div[@class="article"]//ol[@class="grid_view"]/li')
        for i_item in movie_list:
            # item 文件导进来
            douban_item = DoubanItem()
            # 写详细的xpath，进行数据的解析
            douban_item['seria_number'] = i_item.xpath('.//div[@class="pic"]/em/text()').extract_first()
            douban_item['movie_name'] = i_item.xpath('.//div[@class="hd"]/a/span[1]/text()').extract_first()
            content = i_item.xpath('.//div[@class="bd"]/p[1]/text()').extract()
            contents = i_item.xpath('.//div[@class="bd"]/p[1]/text()').extract()
            # 有多行时，进行数据处理
            for i_content in content:
                douban_item['introduce'] = "".join(i_content.split())
            douban_item['star'] = i_item.xpath('.//div[@class="bd"]/div[@class="star"]/span[2]/text()').extract_first()
            douban_item['evaluate'] = i_item.xpath('.//div[@class="bd"]/div[@class="star"]/span[4]/text()').extract_first()
            douban_item['discribtion'] = i_item.xpath('.//div[@class="bd"]/p[@class="quote"]/span[1]/text()').extract_first()
            # extract()是提取选择器里面的内容，不加则只是一个选择器Selector
            # 最后将数据yield到pipelines里面去
            yield douban_item
            # 解析下一页规则，去后一页的xpath
            next_link=response.xpath('//span[@class="next"]/link/@href').extract()
            next_links=response.xpath('//span[@class="next"]/link/@href').extract_first()

            if next_link:
                next_link=next_link[0]
                yield scrapy.Request('https://movie.douban.com/top250' + next_link, callback=self.parse)

