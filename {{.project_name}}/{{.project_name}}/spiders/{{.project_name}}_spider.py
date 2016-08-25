#coding:utf8
import scrapy
from {{.project_name}}.items import {{.project_name}}Item
from scrapy import log

class {{.project_name}}Spider(scrapy.Spider):
    name = "{{.project_name}}"
    allowed_domains = ["xxx.com"]
    start_urls = [
        ""
    ]

##    post方法
##    def start_requests(self):
##        payload = None
##        return [scrapy.http.FormRequest(url=start_url,formdata=payload,
##                    callback=self.parse, dont_filter=True) for start_url in self.start_urls]

    def parse(self, response):
        pass

    def test(self, response):
        '''测试方法，回调进入交互式测试'''
        from scrapy.shell import inspect_response
        inspect_response(response, self)
