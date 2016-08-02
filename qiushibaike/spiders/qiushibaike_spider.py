import scrapy
from ..items import QiushibaikeItem

class QiushibaikeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domins = 'qiushibaike.com'
    start_urls = [
        # 'http://www.qiushibaike.com/hot/page/3/'
        # 'https://baidu.com/'
        "http://www.dmoz.org/Computers/Programming/Languages/Python/"
    ]

    def parse(self, response):
        for href in response.xpath('//div[@class="cat-item"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_content)

    def parse_content(self, response):
        for sel in response.xpath('//div[@class="title-and-desc"]'):
            item = QiushibaikeItem()
            item['href'] = sel.xpath('a/@href').extract()
            item['book'] = sel.xpath('a/div/text()').extract()
            item['content'] = map(lambda x:x.strip(), sel.xpath('div/text()').extract())
            yield item