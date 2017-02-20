# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from video_url_crawler_demo.spiders.aiqiyi_spider import AiqiyiSpider

if __name__ == '__main__':
	settings = get_project_settings()
	process = CrawlerProcess(settings)

	process.crawl(settings['CRAWLER']['spider'])
	process.start()