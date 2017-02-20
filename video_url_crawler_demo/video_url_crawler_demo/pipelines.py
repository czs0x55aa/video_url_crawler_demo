# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo

class FilterPipeline(object):
	def process_item(self, item, spider):
		if item['level'] == 2 and item['set_name'] is None:
			raise DropItem('set name is empty')
		return item

class MongoDBPipeline(object):

	def __init__(self, config):
		db_url = "mongodb://" + \
			('%s:%s@'%(config['user'], config['passwd']) if config['auth'] else '') + \
			('%s:%s/%s' % (config['server'], config['port'], config['db']))
		print db_url
		self.client = pymongo.MongoClient(db_url)
		self.db = self.client[config['db']]
		self.collection = self.db[config['collection']]

	@classmethod  
	def from_crawler(cls, crawler):
		return cls(crawler.settings['DATABASE'])

	def open_spider(self, spider):
		pass

	def process_item(self, item, spider):
		if item['level'] == 1 and self.__insert_vedio(item):
			return item
		elif item['level'] == 2 and self.__update_vedio(item):
			return item
		raise DropItem('fail to store data')

	def close_spider(self, spider):
		self.client.close()

	def __insert_vedio(self, item):
		""" 插入视频条目 """
		find_result = self.collection.find_one({'title': item['title']})
		if find_result is None:
			self.collection.insert_one({
					'title': item['title'],
					'img_url': item['img_url'],
					'main_url': item['main_url'],
					'type_id': item['type_id'],
					'status': item['status'],
					'vedio_list': []
				})
			print 'insert: {title: %s}' % item['title']
			return True
		return False

	def __update_vedio(self, item):
		""" 更新单集视频 """
		find_result = self.collection.find_one({'title': item['title']})
		if find_result is not None:
			self.collection.find_one_and_update(
				{'title': item['title']},
				{'$addToSet': {'vedio_list': {'set_name': item['set_name'], 'set_url': item['set_url']}}}
			)
			print 'update: {title: %s, set_name: %s}' % (item['title'], item['set_name'])
			return True
		return False


	