# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
from scrapy.http import Request
import json
import codecs
import MySQLdb
import MySQLdb.cursors
import logging
from scrapy.utils.log import configure_logging

class PaperPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLStorePaperPipline(object):
    def __init__(self):
         self.dbpool = adbapi.ConnectionPool('MySQLdb',
                 host = '127.0.0.1', #settings['MYSQL_HOST'],
                 port = 3306,
                 db = 'paper', #settings['MYSQL_DBNAME'],
                 user = 'root',#settings['MYSQL_USER'],
                 passwd = 'root',#settings['MYSQL_PASSWD'], 
                 cursorclass = MySQLdb.cursors.DictCursor,
                 charset = 'utf8',
                 use_unicode = True
        )

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item,spider)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item, spider):
        tx.execute("select * from paper_basic_info where systemId = %s",(item['systemId'],))
        result=tx.fetchone()
        if result:
            logging.info("Item already stored in db:%s" % item)
        else:
            tx.execute("insert into paper_basic_info(systemId,title,publishTime,publishIn,publicationType,abstract,source) values (%s,%s,%s,%s,%s,%s,%s)",\
                    (item['systemId'], item['title'], item['publishTime'], item['publishIn'], item['publicationType'], item['abstract'], 'IEEE'));
                        
            keywords = item['keywords'].split(' | ')
            for keyword in keywords:
               if('' != keyword.strip()):
                   tx.execute("insert into paper_keywords(systemId, keyword) values(%s,%s)",(item['systemId'], keyword.strip()))
                        
            authors = item['authors'].split(' | ')
            for author in authors:
                if('' != author.strip()):
                    tx.execute("insert into paper_authors(systemId, author) values(%s,%s)",(item['systemId'], author.strip()))

            references = item['references'].split(' | ')
            for reference in references:
                if('' != reference.strip()):
                    tx.execute("insert into paper_references(systemId, reference) values(%s,%s)",(item['systemId'], reference.strip()))
            
            indexes = item['indexes'].split(' | ')
            for index in indexes:
                if('' != index.strip()):
                    tx.execute("insert into paper_indexes(systemId, indexing, type) value(%s, %s, %s)",(item['systemId'], index, "CONTROLLED INDEXING"))

            logging.info('Item already stored in db %s' %item)
                        
    def handle_error(self, e):
        logging.error(e)

