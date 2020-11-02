import scrapy
from tutorial.items import QuteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for qute in quotes:
            item = QuteItem()
            item["text"] = qute.xpath('span[@class="text"]/text()').extract()[0]
            item["author"] = qute.xpath('span/small/text()').extract()[0]
            item["tags"] = qute.xpath('div[@class="tags"]/a[@class="tag"]/@href').extract()
            print(item["tags"])
            print("====")
            yield item
        next = response.xpath('//nav/ul/li[@class="next"]/a/@href').extract()[0]
        url = response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse)
