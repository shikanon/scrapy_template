#coding:utf8
import scrapy
import json
import requests
import logging
from six.moves.urllib.parse import urlparse
from CNKI.items import ArticleItem, JournalItem
from scrapy_splash import SplashRequest
from CNKI.spiders import script


logger = logging.getLogger(__name__)


class CNKISpider(scrapy.Spider):
    name = "CNKI"
    allowed_domains = ["cnki.net"]
    start_urls = [
        "http://epub.cnki.net/kns/oldnavi/n_Navi.aspx?NaviID=1&Flg="
    ]
    reqeusts_headers = {"Host":"navi.cnki.net",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",}

    def parse(self, response):
        urls = [response.urljoin(url) for url in response.css(".list>li>a::attr(href)").extract()]
        subject = response.css(".list>li>a::text").extract()
        data = dict(zip(subject,urls))
        for sub in data:
            if sub in [u"电子信息科学综合",u"无线电电子学",u"电信技术",u"计算机硬件技术",u"互联网技术",u"自动化技术"]:
                logger.info("the crawler of subject %s is start!"%sub)
                yield scrapy.Request(data[sub], callback=self.frist_journal_list)

    def frist_journal_list(self, response):
        # 抓取子页面
        journal_urls = response.css(".colPic>p>a::attr(href)").extract()    
        for url in journal_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.journal)
        # 翻页
        total_page = int(response.css("#lblPageCount2::text").extract_first())
        for page in range(2, total_page + 1):
            yield SplashRequest(response.url, callback=self.journal_list, endpoint='execute',
                args={'lua_source': script.to_page(page)}, dont_filter=True, meta={"save_data_page":page})

    def journal_list(self, response):
        # 判断是否失败,如果获取当前页码不正确则重新获取
        is_again = True
        # 期待页
        anticipate_page = int(response.meta["save_data_page"])
        if response.css("#txtPageGoTo::attr(value)").extract_first():
            current_page = int(response.css("#txtPageGoTo::attr(value)").extract_first())
            if current_page == anticipate_page:
                logger.debug("%d is success!"%current_page)
                is_again =False
                # 检验通过，则抓取子页面
                journal_urls = response.css(".colPic>p>a::attr(href)").extract()
                for url in journal_urls:
                    yield scrapy.Request(response.urljoin(url), callback=self.journal)
        # 翻页
        if is_again:
            logger.warning("the page of %d is failed!\n url is %s"%(anticipate_page, response.url))
            yield SplashRequest(response.url, callback=self.journal_list, endpoint='execute',
                args={'lua_source': script.to_page(anticipate_page)}, dont_filter=True, meta={"save_data_page":anticipate_page})

    def journal(self, response):
        journal_item = JournalItem()
        # 期刊信息
        journal_item["name"] = response.css(".titbox::text").extract_first().strip()
        base_info = self.iter_extract(response, ".list01 .hostUnit")
        journal_item["base_info"] = dict(info.split(u"：") for info in base_info if len(info.split(u"："))==2)
        pub_info = self.iter_extract(response, ".list02 .hostUnit")
        journal_item["pub_info"] = dict(info.split(u"：") for info in pub_info if len(info.split(u"："))==2)
        evaluation = self.iter_extract(response, ".list03 .hostUnit")
        journal_item["evaluation"] = dict(info.split(u"：") for info in evaluation if len(info.split(u"："))==2)
        journal_item["level"] = response.css(".journalType span::text").extract()
        yield journal_item
        # 获取期刊所的刊号个数
        for year in range(1996, 2017):
            year = str(year)
            urlpath = urlparse(response.url).path.split("/")
            issues_payload = {"year":year,"type":"0","productId":urlpath[-2],"baseId":urlpath[-1]}
            reqeust_issues = requests.post("http://navi.cnki.net/KNavi/Journal/Issues", data=issues_payload, timeout=8, headers=self.reqeusts_headers)
            if json.loads(reqeust_issues.content):
                issues = json.loads(reqeust_issues.content)[0]["Item"]
                logger.info("jouranl:%s; years:%s GET!"%(journal_item["name"],year))
                logger.debug("issues num is %s"%issues)
                # 获取文章链接
                article_payload = {"year":year, "issue":issues, "productId":urlpath[-2], "baseId":urlpath[-1], "type":"yq", "page": "1"}
                yield scrapy.FormRequest("http://navi.cnki.net/KNavi/Journal/CatalogPaging", formdata=article_payload,
                dont_filter=True, callback=self.get_article_urls)
            else:
                logger.info("jouranl %s in %s years is null or failed!"%(journal_item["name"],year))

    def get_article_urls(self, response):
        article_urls = response.css(".name>a::attr(href)").extract()
        for url in article_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.article_info)

    def article_info(self, response):
        article_item = ArticleItem()
        article_item["title"] = response.css("h1>span::text").extract_first().strip()
        article_item["authors"] = response.css("p:nth-child(1) .KnowledgeNetLink::text").extract()
        article_item["institutions"] = response.css("p+ p .KnowledgeNetLink::text").extract()
        article_item["summary"] = response.css("#ChDivSummary::text").extract_first()
        article_item["keywords"] = response.css("#ChDivKeyWord .KnowledgeNetLink::text").extract()
        article_item["journal_zh"] = response.css(".detailLink a::text").extract()[0].strip()
        article_item["journal_en"] = response.css(".detailLink a::text").extract()[1].strip()
        logger.info(article_item["title"])
        yield article_item

    def save_to_file(self, response):
        if response.meta.has_key("save_data_page"):
            page = response.meta["save_data_page"]
            logger.info(page)
            with open("test%d.html"%page,"w") as f:
                f.write(response.body)
        else:
            with open("test.html","w") as f:
                f.write(response.body)

    def iter_extract(self, response, css):
        # 循环迭代解析,不需要::text和extract（）
        return ["".join(element.root.itertext()) for element in response.css(css)]

    def test(self, response):
        '''测试方法，回调进入交互式测试'''
        from scrapy.shell import inspect_response
        inspect_response(response, self)
