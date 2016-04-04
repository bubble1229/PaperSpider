# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    systemId = Field();#在对应系统的ID（可以查重）
    title = Field();#标题
    publishTime = Field();#发表时间
    publishIn = Field();#发表期刊
    publicationType = Field();#发表期刊的类型（会议、杂志等）
    abstract = Field();#摘要
    authors = Field();#作者
    keywords = Field()#关键词
    indexes = Field();#索引标签
    references = Field();#参考文献
    source = Field();#来源，例如IEEE ACM等

