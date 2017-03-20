# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlBotItem(scrapy.Item):
    uid = scrapy.Field()
    data = scrapy.Field()

EbayBrowseNodeItem = CrawlBotItem
EbayItem = CrawlBotItem