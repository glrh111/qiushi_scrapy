import scrapy
from ..items import QiushibaikeItem
import time

class QiushibaikeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domins = 'qiushibaike.com'
    start_urls = [
        'http://www.qiushibaike.com/hot/page/1/',
        # 'https://baidu.com/'
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/"
    ]

    # def parse(self, response):
    #     for href in response.xpath('//div[@class="cat-item"]/a/@href'):
    #         url = response.urljoin(href.extract())
    #         yield scrapy.Request(url, callback=self.parse_content)

    def parse(self, response):
        for sel in response.xpath('//div[@class="article block untagged mb15"]'):
            item = QiushibaikeItem()
            item['author'] = sel.xpath('div[@class="author clearfix"]/a/h2/text()').extract()
            item['content'] = map(lambda x:x.strip(), \
                    sel.xpath('div[@class="content"]/text()').extract())
            yield item
        print u'\n Now Preparing for next page...\n'
        time.sleep(3)

        next_page = response.xpath('//ul[@class="pagination"]/li')
        if next_page:
            url = response.urljoin(next_page.xpath('a/@href').extract()[-1])
            yield scrapy.Request(url, self.parse)
