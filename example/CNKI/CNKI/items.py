# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    institutions = scrapy.Field()
    summary = scrapy.Field()
    keywords = scrapy.Field()
    journal_zh = scrapy.Field()
    journal_en = scrapy.Field()

class JournalItem(scrapy.Item):
    name = scrapy.Field()
    base_info = scrapy.Field()
    pub_info = scrapy.Field()
    evaluation = scrapy.Field()
    level = scrapy.Field()