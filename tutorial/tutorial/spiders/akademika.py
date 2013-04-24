from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from tutorial.items import AkademikaItem

class AkademikaSpider(BaseSpider):
    name = "akademika"
    allowed_domains = ["akademika.no"]
    start_urls = [
        "http://www.akademika.no/search/apachesolr_search/?filters=tid:109647"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        books = hxs.select('//div[contains(@class, "books-teaser")]')
        items = []
        for book in books:
        	item = AkademikaItem()
        	item['title'] = book.select('.//div[contains(@class, "title")]/a/text()').extract()
        	item['isbn'] = book.select('.//div[contains(@class, "image")]/a/@href').re('(\d{13})')
        	item['link'] = "http://www.akademika.no" + book.select('.//div[contains(@class, "image")]/a/@href').extract()[0]
        	price = book.select('.//div[contains(@class, "price")]')
        	item['ordinaryprice'] = price.select('.//span[contains(@class, "uc-price")]/text()').re('(\d+)')
        	item['saleprice'] = price.select('.//div/div[contains(@class, "tilbud")]/text()').re('(\d+)')
        	items.append(item)
        return items