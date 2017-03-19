# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json

import pymongo
from scrapy import signals
from scrapy.http import TextResponse

from crawl import Crawl


class CrawlBotSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#
# ignore files that are already crawled in DB using UID


class IgnoreCrawledMiddleware(object):
    def __init__(self, uri, db_name, collection):
        self.uri = uri
        self.db_name = db_name
        self.collection = collection
        self.client, self.database = None, None

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(uri=crawler.settings.get('MONGO_URI'),
                db_name=crawler.settings.get('MONGO_DATABASE'),
                collection=crawler.settings.get('MONGO_COLLECTION'))
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def process_request(self, request, spider):
        uid = request.meta['uid']
        crawl = Crawl.get_crawl_by_uid(uid, database=self.database, collection=self.collection)
        if crawl is not None:
            reason = "$$$$$$$$ Crawl exists: ignoring crawl request"
            print(reason)
            # raise IgnoreRequest(reason)
            body = json.dumps(crawl["data"])
            return TextResponse(url=request.url, body=body, request=request)

    def spider_opened(self, spider):
        self.client = pymongo.MongoClient(self.uri)
        self.database = self.client[self.db_name]

    def spider_closed(self, spider):
        if self.client is not None:
            self.client.close()
