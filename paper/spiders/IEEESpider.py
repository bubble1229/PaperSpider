# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from paper.items import PaperItem 
from scrapy.contrib.spiders import Rule 
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import Request
import json

class IeeespiderSpider(scrapy.Spider):
	name = "IEEESpider"
	allowed_domains = ["ieeexplore.ieee.org"]
	start_urls = [
                'http://ieeexplore.ieee.org/Xplore/home.jsp',
        ]

	rules=[
           #Rule(SgmlLinkExtractor(allow=(r'http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=Data%20Mining&pageNumber=2&newsearch=true'))),
           Rule(SgmlLinkExtractor(allow=(r'http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=\d+&queryText=Data%20Mining&pageNumber=\d+&newsearch=true')),callback="parse_item"),
        ]

	global dataListUrl,articleDetailUrl,articleAbstractAuthorsUrl,articleKeywordsUrl,articleReferencesUrl
        global pageSize
	dataListUrl = "http://ieeexplore.ieee.org/rest/search"
        articleDetailUrl = "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber="
        articleAbstractAuthorsUrl = "http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber="
        articleKeywordsUrl = "http://ieeexplore.ieee.org/xpl/abstractKeywords.jsp?arnumber="
        articleReferencesUrl = "http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?arnumber="
        
        pageSize = 25

	def parse(self, response):
		request = Request(dataListUrl,callback = self.parseTotalRecods)
		request.method = "POST"#need post method, if not it will return code 405
		request.headers['Content-Type']="application/json;charset=UTF-8"#if not, it will return 425
		request = request.replace(**{'body':'{"queryText":"Data Mining","newsearch":"true"}'})#the param to transport
                yield request
                #测试提取作者信息
                #sel = Selector(response)
        
        def parseTotalRecods(self, response):
            request = Request(dataListUrl,callback = self.parse_ajax)
            request.method = "POST"#need post method, if not it will return code 405
            request.headers['Content-Type']="application/json;charset=UTF-8"#if not, it will return 425

            data = response.body
            jData = json.loads(data)
            totalRecords = jData['totalRecords']
            pageNos = totalRecords / pageSize if totalRecords % pageSize == 0 else totalRecords / pageSize + 1
            for i in range(1, pageNos + 1):
                bodyParam = '{"queryText":"Data Mining","pageNumber":"'+ bytes(i) +'","newsearch":"true"}'
                request = request.replace(**{'body' : bodyParam})
                yield request 
                

	def parse_ajax(self, response):
            data = response.body
	    jData = json.loads(data)
	    records = jData['records']
            for record in records:
                articleNumber = record.get('articleNumber',-1)
                yield Request(articleDetailUrl+articleNumber,callback = self.parseArticleDetail)

        def parseArticleDetail(self, response):
            sel = Selector(response)
            article = PaperItem()
            article['systemId'] = response.url.split('=')[-1]
            article['title'] = sel.xpath('//*[@id="article-page-hdr"]/div[1]/div[2]/h1/text()').extract()[0].strip()
            article['abstract'] = sel.xpath('//*[@id="articleDetails"]/div/div[1]/p/text()[1]').extract()[0].strip()
            article['publishIn'] = sel.xpath('//*[@id="articleDetails"]/div/div[2]/a/text()').extract()[0].strip()
            article['publishTime'] = sel.xpath('//*[@id="articleDetails"]/div/div[2]/text()').extract()[3].strip()
            yield Request(articleAbstractAuthorsUrl+article['systemId'],meta={'article': article}, callback=self.parseArticleAbstractAuthors)	

        def parseArticleAbstractAuthors(self,response):
            sel = Selector(response)
            article = response.meta['article']

            authors = ''
            for author in sel.xpath('//*[@id="abstractAuthors"]/div/div/div/a/text()[last()]').extract():
                authors = authors + author.strip( )+ " | "
            article['authors'] = authors[0:-3]
            yield Request(articleKeywordsUrl + article['systemId'], meta = {'article': article},callback = self.parseArticleKeywords)


        def parseArticleKeywords(self, response):
            sel = Selector(response)
            article = response.meta['article']

            keywords = ''
            for keyword in sel.xpath('//*[@id="abstractKeywords"]/div/div/div[1]/div[3]/ul/li/a/text()').extract():
                keyword = keyword.strip()
                if('' !=  keyword):
                    keywords = keywords + keyword + " | "
            article['keywords'] = keywords[0:-3]
            yield Request(articleReferencesUrl + article['systemId'], meta = {'article': article}, callback = self.parseReferences)


        def parseReferences(self, response):
            sel = Selector(response)
            article = response.meta['article']

            referencens = ''
            for li in sel.xpath('//*[@id="abstractReferences"]/div/div/div/ol/li'):#获取所有的li标签（所有的参考文献，有可能含有 'Abstract | Full Text: PDF'字样）
                referencen = ''
                for data in li.xpath('./text() | ./i/text()').extract():#将其与子标签的内容连成一个字符串
                    if '' != data.strip():
                        referencen = referencen + data.strip().replace('\n',' ')
                if '' != referencen:
                    referencens = referencens + referencen + " | "
            #for referencen in sel.xpath('//*[@id="abstractReferences"]/div/div/div/ol/li/text()').extract():
            #    referencen = referencen.strip()
            #    if('' != referencen):
            #        referencens = referencens + referencen + ' | '
            article['referencens'] = referencens[0:-3]

            return article
