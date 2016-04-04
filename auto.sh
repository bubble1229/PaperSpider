#! /bin/sh                                                                                                                                            

export PATH=$PATH:/usr/local/bin

cd /mydata/workspace/python/paper

scrapy crawl IEEESpider -o IEEEData.json
