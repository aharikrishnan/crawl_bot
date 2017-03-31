# -*- coding: utf-8 -*-
import pymongo
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from crawl_utils import Crawl


class CrawlBotPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self, uri, db_name, collection):
        self.uri = uri
        self.db_name = db_name
        self.collection = collection
        self.client, self.database = None, None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(uri=crawler.settings.get('MONGO_URI'),
                   db_name=crawler.settings.get('MONGO_DATABASE'),
                   collection=crawler.settings.get('MONGO_COLLECTION'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.uri)
        self.database= self.client[self.db_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
      print("Database: {0}, Collection: {1}".format(self.db_name, self.collection))
      if not Crawl.is_crawled(item['uid'], database=self.database, collection=self.collection):
          self.database[self.collection].insert(dict(item))
          return item
      else:
        raise DropItem("item crawled %s" % item)
