# video_url_crawler_demo
爱奇艺视频信息的爬虫。
两年多前刚学python没多久写的，现在回头看看感觉写的很烂，只是勉强能运行的demo。
鉴于偶尔还有朋友点星，因而在py3检查了时隔两年爬虫还是能运行的，后期应该不会考虑更新维护了。

# 依赖
- python
- scrapy 1.3
- selenium
- pymongo
- [PhantomJS](http://phantomjs.org/download.html)
- [MongoDB](https://www.mongodb.com/download-center)

# 使用
在settings.py文件中填写相应的配置信息
### 1.填写PhantomJS配置
根据实际的系统环境和文件路径配置以下两项
```python
PLATFORM = 'win'	# 'win' or 'linux' or 'mac'
PHANTOMJS_PATH = 'D:/Program Files/Anaconda2/Scripts/phantomjs.exe'
```
### 2.填写数据库配置
如果开启了用户认证，需要将'auth'字段设置成True，并填写用户名和密码
```python
# MongoDB database configure
DATABASE = {
	'server': 'localhost',
	'port': 27017,
	'auth': False,
	'user': '',
	'passwd': '',
	'db': 'video_box',	# database name
	'collection': 'aiqiyi',
}
```
### 3.配置爬虫信息
```python
CRAWLER = {
	'spider': 'aiqiyi',
	'type_id_list': [2, 3],
	're_type_id': 'http://list.iqiyi.com/www/(\d+)/',
	'url_template': 'http://list.iqiyi.com/www/%s/-------------11-%s-1-iqiyi--.html'
}
```
spider: 爬虫的名字  
type_id: 爱奇艺的视频类型,1:电影,2:电视剧,3:纪录片,4:动漫...  
re_type_id：使用正则从URL中提取type_id  
url_template: 爱奇艺的视频列表页面的通用URL，第一个%s为视频类型，第二个%s为页码  
URL和类型码详见 [爱奇艺视频列表页面](http://list.iqiyi.com/www/2/-------------11-1-1-iqiyi--.html)
### 4.启动程序
```python
python launch.py
```
爬虫会抓取爱奇艺指定类型下的所有（从第一页到最后一页）的视频

# 运行结果
数据的存储结构如下：
```python
{
	'title': 视频项的标题,
	'img_url': 视频的封面图地址,
	'main_url': 视频的抓取地址,
	'type_id': 爱奇艺的视频类型码,
	'status': 视频状态,0:还在更新,1:全集,
	'vedio_list': [
		{'set_name': 视频名称, 'set_url': 视频地址},
		......
	]
}
```

# 可供参考的文档
- [Scrapy 1.3 documentation](https://doc.scrapy.org/en/1.3/index.html)
- [Selenium with Python](http://selenium-python.readthedocs.io/)
- [PyMongo 3.4.0 Documentation](http://api.mongodb.com/python/current/)

# Bugs
- 异常处理存在问题
- 部分特殊页面的数据无法抓取