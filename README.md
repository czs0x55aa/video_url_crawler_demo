# video_url_crawler_demo
视频网站的URL爬虫，使用MongoDB存储抓取到的数据  
目前只支持爱奇艺
代码还在调试阶段

# 依赖组件
- python 2.7
- scrapy 1.3
- selenium
- PhantomJS
- pymongo

# 使用
在settings.py文件中填写相应的配置信息
### 1.填写PhantomJS配置
```python
PLATFORM = 'win'	# 'win' or 'linux'
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
### 3.启动程序
```python
python launch.py
```
默认会抓取爱奇艺的所有电视剧

# Bugs
...
