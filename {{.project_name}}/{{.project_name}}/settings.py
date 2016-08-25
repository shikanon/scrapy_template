# -*- coding: utf-8 -*-

# Scrapy settings for crawler project


BOT_NAME = '{{.project_name}}'

SPIDER_MODULES = ['{{.project_name}}.spiders']
NEWSPIDER_MODULE = '{{.project_name}}.spiders'

# 日志等级
LOG_LEVEL = "INFO"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# 爬虫速度限制
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# 关闭cookies
COOKIES_ENABLED = False

#Ajax Crawlable Pages
AJAXCRAWL_ENABLED = True

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'baike.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#加入随机USER-AGENT
DOWNLOADER_MIDDLEWARES = {
    'common.downloadermiddleware.useragent.RandomPCAgent': 543,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

# 开启HTTP缓存
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 写入jsonline
FEED_URI = "file:///home/crawler/crawler/baike_export.json"
FEED_FORMAT = "jsonlines"

# 调用redis做调度器
# pip install scrapy-redis
# 用docker安装redis
# docker pull redis
# docker run --name scrapy-redis -p 6379:6379 -v /docker/host/dir:/data -d redis
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 爬虫持久化运行命令
# scrapy crawl {{.project_name}} -s JOBDIR=crawls/somespider-1
