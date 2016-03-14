# -*- coding: utf-8 -*-
import scrapy


class AcmspiderSpider(scrapy.Spider):
    name = "AcmSpider"
    allowed_domains = ["dl.acm.org"]
    start_urls = (
        'http://www.dl.acm.org/',
    )

    def parse(self, response):
        pass
