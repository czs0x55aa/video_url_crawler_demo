# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoUrlCrawlerDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AlbumItem(scrapy.Item):
	level = scrapy.Field()
	title = scrapy.Field()
	img_url = scrapy.Field()
	main_url = scrapy.Field()
	type_id = scrapy.Field()
	status = scrapy.Field()

class ContentItem(scrapy.Item):
	level = scrapy.Field()
	title = scrapy.Field()
	set_order = scrapy.Field()
	set_name = scrapy.Field()
	set_url = scrapy.Field()