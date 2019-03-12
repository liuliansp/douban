# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from douban.settings import mongo_host,mongo_port,mongo_dbname,mongo_docname
import pymongo
class DoubanPipeline(object):
    def __init__(self):
        host=mongo_host
        port=mongo_port
        dbname=mongo_dbname
        docname=mongo_docname
        Client=pymongo.MongoClient(host=host,port=port)
        mydb=Client[dbname]
        self.post=mydb[docname]
    def process_item(self, item, spider):
        data=dict(item)
        self.post.insert(data)
        return item
