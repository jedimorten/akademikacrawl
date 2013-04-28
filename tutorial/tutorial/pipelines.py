# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import sys
import MySQLdb
import hashlib
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.http import Request

class PricePipeline(object):

	def __init__(self):
		self.conn = MySQLdb.connect(user='drupal', '16bitlove', 'drupal7', 'localhost', charset="utf8", use_unicode=True)
    	self.cursor = self.conn.cursor()
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
				store_item(self, item)
				return item
			elif item['saleprice']:
				item['price'] = item['saleprice']
				del item['ordinaryprice']
				del item['saleprice']
				store_item(self, item)
				return item
			elif item['ordinaryprice']:
				item['price'] = item['ordinaryprice']
				del item['ordinaryprice']
				del item['saleprice']
				store_item(self, item)
				return item
			else:
				raise DropItem("Missing price in %s" % item)


	def store_item(self, item):
		try:
	        self.cursor.execute("""INSERT INTO pricescraper (isbn, title, link, price)  
	                        VALUES (%s, %s, %s, %s)""", 
	                       (item['isbn'].encode('utf-8'), 
	                       	item['title'].encode('utf-8'),
	                       	item['link'].encode('utf-8'),
	                        item['price'].encode('utf-8')))

	        self.conn.commit()


	    except MySQLdb.Error, e:
	        print "Error %d: %s" % (e.args[0], e.args[1])
