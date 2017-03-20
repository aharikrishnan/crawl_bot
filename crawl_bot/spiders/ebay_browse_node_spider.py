import json
import time

import scrapy

from crawl_bot.items import EbayBrowseNodeItem


class EbayBrowseNodeSpider(scrapy.Spider):
    name = "ebay-browse-node"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawl_bot.middlewares.IgnoreCrawledMiddleware': 543,
        },

        'ITEM_PIPELINES': {
            'crawl_bot.pipelines.MongoPipeline': 300,
        }
    }

    def start_requests(self):
        yield self.enqueue_category("-1")

    def parse(self, response):
        json_payload = json.loads(response.body)        
        self.write_to_file(response)
        sub_cat_ids = [
            cat['CategoryID'] for cat in json_payload['CategoryArray']['Category'] if cat['LeafCategory'] != True
            ]
        item = EbayBrowseNodeItem()
        item['uid'] = response.meta['uid']
        item['data'] = json_payload
        yield item
        # self.write_to_file(response)
        for sub_cat_id in sub_cat_ids:
            yield self.enqueue_category(sub_cat_id)

    def enqueue_category(self, cat_id):
        # url = self.settings['EBAY_STAGING_SHOPPING_API_ENDPOINT']
        url = self.settings['EBAY_SHOPPING_API_ENDPOINT']
        # appid = self.settings.get('EBAY_STAGING_APP_ID')
        appid = self.settings['EBAY_APP_ID']
        basic_params = {
            "appid": appid,
            "siteid": "0",
            "callname": "GetCategoryInfo",
            "version": "863",
            "responseencoding": "JSON"
        }
        params = {"CategoryID": cat_id, "IncludeSelector": "ChildCategories"}
        params.update(basic_params)
        request = scrapy.FormRequest(
            url=url,
            method='GET',
            callback=self.parse,
            formdata=params)
        request.meta['uid'] = cat_id
        return request

    def write_to_file(self, response):
        timestamp = time.strftime("%Y%m%d%H%M%S")
        filename = 'file-%s' % timestamp
        with open(filename, 'w') as file:
            file.write(response.body)
        self.log('Saved file %s' % filename)
