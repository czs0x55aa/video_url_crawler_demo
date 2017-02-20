# -*- encoding: utf-8 -*-

import time
import scrapy
from selenium import webdriver
from scrapy.utils.project import get_project_settings
from ..items import AlbumItem, ContentItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class AiqiyiSpider(scrapy.Spider):
	name = "aiqiyi"

	def __init__(self):
		scrapy.spiders.Spider.__init__(self)

		self.global_settings = get_project_settings()
		if self.global_settings['PLATFORM'] == 'win':
			self.driver = webdriver.PhantomJS(executable_path= self.global_settings['PHANTOMJS_PATH'])
		elif self.global_settings['PLATFORM'] == 'linux':
			self.driver = webdriver.PhantomJS()
		self.driver.set_page_load_timeout(30)
		self.driver.implicitly_wait(10)

		self.type_id = 2

	def __del__(self):
		self.driver.quit()
		scrapy.spiders.Spider.__del__(self)

	def set_type_id(type_id):
		self.type_id = type_id

	def __aiqiyi_url(self, type_id):
		def get_url(data_key):
			return 'http://list.iqiyi.com/www/%s/-------------11-%s-1-iqiyi--.html'%(type_id, data_key)
		return get_url

	def start_requests(self):
		self.get_tv_url = self.__aiqiyi_url(self.type_id)
		urls = []
		urls.append(self.get_tv_url(1))
		for url in urls:
			yield scrapy.Request(url=url, callback=self.main_list_parse, errback=self.errback_httpbin)

	def main_list_parse(self, response):
		# for sel in response.xpath('//div[@class="wrapper-piclist"]/ul/li'):
		# 	item = AlbumItem()
		# 	item['level'] = 1
		# 	item['title'] = sel.xpath('div[2]/div[1]/p/a/text()').extract_first()
		# 	item['img_url'] = sel.xpath('div[1]/a/img/@src').extract_first()
		# 	item['main_url'] = sel.xpath('div[2]/div[1]/p/a/@href').extract_first()
		# 	item['type_id'] = self.type_id
		# 	update_status = sel.xpath('div[1]/a/div/div/p/span/text()').extract_first().strip()
		# 	item['status'] = 1 if update_status[0] == u'共' else 0

		# 	if item['title'] is not None and item['main_url'] is not None:
		# 		yield item
		# 		yield scrapy.Request(response.urljoin(item['main_url']), callback=self.video_list_parse, errback=self.errback_httpbin)
		
		no_page = response.xpath('//span[@class="curPage"]/following-sibling::span[@class="noPage"]').extract_first()
		# to crawl next page
		if no_page is None:
			next_page_url = response.xpath('//div[@class="mod-page"]/a[last()]/@href').extract_first()
			print 'visit next page url: ', next_page_url
			yield scrapy.Request(response.urljoin(next_page_url), callback=self.main_list_parse, errback=self.errback_httpbin)


	def video_list_parse(self, response):
		title = response.xpath('//div[@class="crumb-item"]/a[last()]/strong/text()').extract_first()
		if title is not None:
			level = 2
			for li in response.xpath('//*[@id="block-I"]/div/div/ul/li'):
				item = ContentItem()
				item['level'] = level
				item['title'] = title
				item['set_name'] = li.xpath('div[2]/p[2]/a/text()').extract_first()
				item['set_url'] = li.xpath('div[2]/p[2]/a/@href').extract_first()
				yield item

			link_list = response.xpath('//div[@class="mod-album_tab_num fl"]/a/text()')
			if len(link_list) > 1:
				link_name_list = [item.extract() for item in link_list[1:]]
				self.driver.get(response.url)
				time.sleep(2)
				for link_name in link_name_list:
					page_link = self.driver.find_element_by_link_text(link_name)
					page_link.click()
					time.sleep(3)
					# li_list = self.driver.find_elements_by_xpath('//p[@class="site-piclist_info_title fs12"]/a')
					li_list = self.driver.find_elements_by_xpath('//*[@id="block-I"]/div/div/ul/li')
					for li in li_list:
						item = ContentItem()
						item['level'] = level
						item['title'] = title
						xpath_element = li.find_element_by_xpath('div[2]/p[2]/a')
						item['set_name'] = xpath_element.text
						item['set_url'] = xpath_element.get_attribute("href")
						yield item

	def errback_httpbin(self, failure):
		# log all failures
		self.logger.error(repr(failure))

		# in case you want to do something special for some errors,
		# you may need the failure's type:

		if failure.check(HttpError):
			# these exceptions come from HttpError spider middleware
			# you can get the non-200 response
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)

		elif failure.check(DNSLookupError):
			# this is the original request
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)

		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)