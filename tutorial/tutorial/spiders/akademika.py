# from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from tutorial.items import AkademikaItem

class AkademikaSpider(CrawlSpider):
	name = "akademika"
	download_delay = 5
	allowed_domains = ["akademika.no"]
	start_urls = [
		"http://www.akademika.no/search/apachesolr_search/?filters=tid:109647"
	]

	rules = (
		Rule (
			SgmlLinkExtractor(restrict_xpaths=("//li[@class='pager-next']"))
		   , callback='parse_start', follow= True),
	)

	def parse_start(self, response):
		hxs = HtmlXPathSelector(response)

		books = hxs.select('//div[contains(@class, "books-teaser")]')
		items = []
		for book in books:
			item = AkademikaItem()
			item['title'] = book.select('.//div[contains(@class, "title")]/a/text()').extract()
			if item['title']:
				item['title'] = item['title'][0]
			item['isbn'] = book.select('.//div[contains(@class, "image")]/a/@href').re('(\d{13})')
			if item['isbn']:
				item['isbn'] = item['isbn'][0]
			item['link'] = book.select('.//div[contains(@class, "image")]/a/@href').extract()
			if item['link']:
				item['link'] =  "http://www.akademika.no" + item['link'][0]
			price = book.select('.//div[contains(@class, "price")]')
			item['ordinaryprice'] = price.select('.//span[contains(@class, "uc-price")]/text()').re('(\d+\.*\d*)')
			if item['ordinaryprice']:
				item['ordinaryprice'] = item['ordinaryprice'][0]
			item['saleprice'] = price.select('.//div/div[contains(@class, "tilbud")]/text()').re('(\d+\.*\d*)')
			if item['saleprice']:
				item['saleprice'] = item['saleprice'][0]
			items.append(item)
		return items

