import scrapy
import time

class EbayBrowseNodeSpider(scrapy.Spider):
  name = "ebay-browse-node"

  def start_requests(self):
    urls = [
        "http://open.api.sandbox.ebay.com/shopping"
    ]
    api_headers = {
        "X-EBAY-API-APP-ID":"HariA-scarlet-SBX-2bed4d450-767b52f9",
        "X-EBAY-API-SITE-ID":"0",
        "X-EBAY-API-CALL-NAME":"GetCategoryInfo",
        "X-EBAY-API-VERSION":"863",
        "X-EBAY-API-REQUEST-ENCODING":"xml",
        }

    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse, headers=api_headers)

  def parse(self, response):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    filename = 'file-%s' % timestamp
    with open(filename, 'wb') as f:
      f.write(response.body)
    self.log('Saved file %s' % filename)
