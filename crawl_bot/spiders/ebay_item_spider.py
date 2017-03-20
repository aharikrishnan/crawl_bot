import json
import time

import scrapy

from crawl_bot.items import EbayItem


class EbayItemSpider(scrapy.Spider):
    name = "ebay-item"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawl_bot.middlewares.IgnoreCrawledMiddleware': 543,
        },
        'ITEM_PIPELINES': {
            'crawl_bot.pipelines.MongoPipeline': 300,
        },
        'MONGO_COLLECTION': 'items_crawl',
        'STAGING_API_ENDPOINT': "http://svcs.sandbox.ebay.com/services/search/FindingService/v1",
        'API_ENDPOINT': "http://svcs.ebay.com/services/search/FindingService/v1"
    }
    
    def __init__(self, categories=None, *args, **kwargs):
        super(EbayItemSpider, self).__init__(*args, **kwargs)
        self.categories = None
        if categories is not None:
            with open(categories) as fo:
                self.categories = fo.read().split("\n")

    def start_requests(self):
        #url = self.settings['STAGING_API_ENDPOINT']
        #appid = self.settings.get('EBAY_STAGING_APP_ID')
        url = self.settings['API_ENDPOINT']
        appid = self.settings.get('EBAY_APP_ID')
        print("API KEY: {0}".format(appid))
        page_number = 1
        per_page = 100
        basic_params = {
            'OPERATION-NAME': 'findItemsByCategory',
            'RESPONSE-DATA-FORMAT': 'JSON',
            'SECURITY-APPNAME': appid,
            'SERVICE-VERSION': '1.12.0',
            'outputSelector': 'CategoryHistogram',
            'paginationInput.entriesPerPage': str(per_page)
        }
        print(self.categories)
        for category in self.categories:
            if len(category) < 1:
                continue
            uid = "{0}-{1}-{2}".format(category, page_number, per_page)
            params = {
                "categoryId": category,
                'paginationInput.pageNumber': str(page_number)
            }
            params.update(basic_params)
            print(params)
            request = scrapy.FormRequest(
                url=url,
                method='GET',
                callback=self.parse,
                formdata=params)
            print(str(request))
            request.meta['uid'] = uid
            yield request

    def parse(self, response):
        json_payload = json.loads(response.body)        
        self.write_to_file(response)
        item = EbayItem()
        item['uid'] = response.meta['uid']
        item['data'] = json_payload
        yield item
        # self.write_to_file(response)
   
    def write_to_file(self, response):
        timestamp = time.strftime("%Y%m%d%H%M%S")
        filename = 'file-item-%s' % timestamp
        with open(filename, 'w') as file:
            file.write(response.body)
        self.log('Saved file %s' % filename)
