# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import signals
from scrapy.exceptions import DropItem
import json

class PricePipeline(object):

	def __init__(self):
		self.file = open('items.jl', 'wb')
		self.isbns_seen = set()

	def process_item(self, item, spider):
		if item['isbn'] in self.isbns_seen:
			raise DropItem("Duplicate item found: %s" % item)
		else: 
			self.isbns_seen.add(item['isbn'])
			if item['saleprice'] and item['ordinaryprice']:
				item['price'] = item['saleprice']
				del item['ordinaryprice']
				del item['saleprice']
				line = json.dumps(dict(item)) + "\n"
				self.file.write(line)
				return item
			elif item['saleprice']:
				item['price'] = item['saleprice']
				del item['ordinaryprice']
				del item['saleprice']
				line = json.dumps(dict(item)) + "\n"
				self.file.write(line)
				return item
			elif item['ordinaryprice']:
				item['price'] = item['ordinaryprice']
				del item['ordinaryprice']
				del item['saleprice']
				line = json.dumps(dict(item)) + "\n"
				self.file.write(line)
				return item
			else:
				raise DropItem("Missing price in %s" % item)
