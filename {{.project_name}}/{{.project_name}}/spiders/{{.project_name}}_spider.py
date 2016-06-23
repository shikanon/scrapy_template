#coding:utf8
import scrapy
from {{.project_name}}.items import {{.project_name}}Item
from scrapy import log

class {{.project_name}}Spider(scrapy.Spider):
    name = "{{.project_name}}"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://baike.baidu.com/renwu"
    ]

    def parse(self, response):
        pass

    def test(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
