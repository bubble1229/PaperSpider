# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from paper.items import PaperItem 
from scrapy.spiders import Rule 
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy import Request
import json
import HTMLParser
import logging

class IeeespiderSpider(scrapy.Spider):
    name = "IEEESpider"
    allowed_domains = ["ieeexplore.ieee.org"]
    start_urls = [
                'http://ieeexplore.ieee.org/Xplore/home.jsp',
        ]

    global dataListUrl,articleDetailUrl,articleAbstractAuthorsUrl,articleKeywordsUrl,articleReferencesUrl
    global pageSize
    global abstractNotExist, authorsNotExist, publishInNotExsit, keywordsNotExist, indexesNotExist
    dataListUrl = "http://ieeexplore.ieee.org/rest/search"
    articleDetailUrl = "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber="
    articleAbstractAuthorsUrl = "http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber="
    articleKeywordsUrl = "http://ieeexplore.ieee.org/xpl/abstractKeywords.jsp?arnumber="
    articleReferencesUrl = "http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?arnumber="
    pageSize = 25
    abstractNotExist = "Abstarct is not available"
    authorsNotExist = 'Authors are not available'
    publishInNotExsit = "Publication is not available"
    keywordsNotExist = "Keywords are not available"
    indexesNotExist = "Indexing are not available"

    def parse(self, response):
        request = Request(dataListUrl,callback = self.parseTotalRecods)
        request.method = "POST"#need post method, if not it will return code 405
        request.headers['Content-Type']="application/json;charset=UTF-8"#if not, it will return 425
        request = request.replace(**{'body':'{"queryText":"(((\'Publication Title\':data mining) OR \'INSPEC Controlled Terms\':data mining) OR \'Author Keywords\':data mining)","matchBoolean":"true","searchField":"Search_All"}'})#the param to transport
        yield request
        
    def parseTotalRecods(self, response):
        request = Request(dataListUrl,callback = self.parse_ajax)
        request.method = "POST"#need post method, if not it will return code 405
        request.headers['Content-Type']="application/json;charset=UTF-8"#if not, it will return 425
       
        data = response.body
        jData = json.loads(data)
        totalRecords = jData['totalRecords']
        pageNos = totalRecords / pageSize if totalRecords % pageSize == 0 else totalRecords / pageSize + 1
        for i in range(1, pageNos + 1):
            bodyParam = '{"queryText":"(((\'Publication Title\':data mining) OR \'INSPEC Controlled Terms\':data mining) OR \'Author Keywords\':data mining)","matchBoolean":"true","searchField":"Search_All","pageNumber":"'+ bytes(i) +'"}'
            request = request.replace(**{'body' : bodyParam})
            yield request 
                

    def parse_ajax(self, response):
        html_parser = HTMLParser.HTMLParser()
        data = response.body
        jData = json.loads(data)
        records = jData['records']
        for record in records:
            article = PaperItem()
            # systemId提取    
            articleNumber = record.get('articleNumber',-1)
            if(-1 != articleNumber):
                article['systemId'] = articleNumber
            # authors提取
            authors = record.get('authors',-1)
            if(-1 == authors):#有些文章中的作者，IEEE没有给出
                article['authors'] = authorsNotExist
            else:
                authorsString = ''
                for author in authors:
                     authorsString = authorsString + html_parser.unescape(author.get ('preferredName')) + " | "#部分内容含有html的转义字符
                article['authors'] = authorsString[0:-3]
            # 出版时间提取
            publishTime = record.get('publicationYear',-1)
            article['publishTime'] = publishTime
            # 提取发表的刊物
            publishIn = record.get('publicationTitle',publishInNotExsit)
            publishIn =  publishIn.replace('[::','')
            publishIn =  publishIn.replace('::]','')
            article['publishIn'] = html_parser.unescape(publishIn)
            # 出版刊物类型
            article['publicationType'] = record.get('contentType',-1)

            yield Request(articleDetailUrl+article['systemId'], meta = {'article': article}, callback = self.parseArticleDetail)

    def parseArticleDetail(self, response):
        sel = Selector(response)
        article = response.meta['article']
        #article['systemId'] = response.url.split('=')[-1]
        article['title'] = sel.xpath('//*[@id="article-page-hdr"]/div[1]/div[2]/h1/text()').extract()[0].strip()
        
        abstractList = sel.xpath('//*[@id="articleDetails"]/div/div[1]/p/text()[1]').extract() 
        if(0 == len(abstractList)):#有些文章的摘要是图片，无法获取摘要信息
            article['abstract'] = abstractNotExist;
        else:
            article['abstract'] = abstractList[0].strip()
          
        #article['publishIn'] = sel.xpath('//*[@id="articleDetails"]/div/div[2]/a/text()').extract()[0].strip() 
        
        yield Request(articleAbstractAuthorsUrl+article['systemId'],meta={'article': article}, callback=self.parseArticleKeywords)   


    def parseArticleKeywords(self, response):
        sel = Selector(response)
        article = response.meta['article']

        keywords = ''#爬取作者的关键词
        if(0 == len(sel.xpath('//*[@id="abstractKeywords"]/div/div/div[1]/div[3]/ul/li/a/text()'))):
            article['keywords'] = keywordsNotExist;
        else:
            for keyword in sel.xpath('//*[@id="abstractKeywords"]/div/div/div[1]/div[3]/ul/li/a/text()').extract():
                keyword = keyword.strip()
                if('' !=  keyword):
                    keywords = keywords + keyword + " | "
            article['keywords'] = keywords[0:-3]

        indexes = ''#爬取页面的控制索引
        try:
            if(0 == len(sel.xpath('//*[@id="abstractKeywords"]/div/div/div[1]/div[1]/ul/li/a/text()'))):
                article['indexes'] = indexesNotExist;
            else:
                for index in sel.xpath('//*[@id="abstractKeywords"]/div/div/div[1]/div[1]/ul/li/a/text()').extract():
                    indexes = indexes + index + " | "
            article['indexes'] = indexes[0:-3]
        except Exception, e:
            logging.error(e)

        yield Request(articleReferencesUrl + article['systemId'], meta = {'article': article}, callback = self.parseReferences)


    def parseReferences(self, response):
        sel = Selector(response)
        article = response.meta['article']

        references = ''
        for li in sel.xpath('//*[@id="abstractReferences"]/div/div/div/ol/li'):#获取所有的li标签（所有的参考文献，有可能含有 'Abstract | Full Text: PDF'字样）
            reference = ''
            for data in li.xpath('./text() | ./i/text()').extract():#将其与子标签的内容连成一个字符串，有些信息在子标签中
                if '' != data.strip():
                    reference = reference + data.strip().replace('\n',' ')
            if '' != reference:
                references = references + reference + " | "
        article['references'] = references[0:-3]

        return article
