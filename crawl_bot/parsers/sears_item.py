import pymongo
from scrapy.utils.project import get_project_settings
from crawl_bot.crawl_utils import Crawl


def parse_items():
    settings = get_project_settings()
    uri = settings.get("MONGO_URI")
    db_name = 'sears'
    collection = 'items_crawl'
    item_collection = 'items'
    conn = Crawl.open_connection(uri)
    database = conn[db_name]

    print("uri: #{0}, db: #{1}, collection: #{2}".format(uri, db_name,
                                                         collection))
    item_docs = database[item_collection]
    print("To process " + str(database[collection].count()))
    docs = database[collection].find()
    for doc in docs:
        try:
              node = doc['data']
              item = get_item(node)
              if item is not None:
                  try:
                      item_docs.insert(item)
                  except pymongo.errors.DuplicateKeyError, e:
                      print("EEEEEEEEE KEY ERROR" + str(e))
        except:
            print("Erro")
            items = []

def get_item(node):
    record = {}
    if not (("data" in node) and ("product" in node["data"])):
        print node
        return None
    d = node["data"]
    p = d["product"]
    record = {
        'bn': d["productmapping"],
        'id': p["id"],
        'title': p["name"],
        'seo': p['seo'],
        'brand': p['brand']['name'],
        'model': p['mfr']['modelNo']
    }
    print(str(record))
    return record


parse_items()
