import pymongo
from scrapy.utils.project import get_project_settings
from crawl_bot.crawl_utils import Crawl


def parse_items():
    settings = get_project_settings()
    uri = settings.get("MONGO_URI")
    db_name = settings.get('MONGO_DATABASE')
    collection = 'items_crawl'
    item_collection = 'items'
    conn = Crawl.open_connection(uri)
    database = conn[db_name]

    print("uri: #{0}, db: #{1}, collection: #{2}".format(uri, db_name, collection))
    item_docs = database[item_collection]
    print("To process "+ str(database[collection].count()))
    docs = database[collection].find()
    for doc in docs:
        try:
            bns = [get_item(node) for node in doc['data']['findItemsByCategoryResponse'][0]['searchResult'][0]['item']]
        except:
            bns = []
        
        for bn in bns:
            try:
                item_docs.insert(bn)
            except pymongo.errors.DuplicateKeyError, e:
                print("EEEEEEEEE KEY ERROR"+ str(e))


def get_item(node):
    record =  {
        'id': node['itemId'],
        'name': node['title'],
        'primaryCategory' : node['primaryCategory']
    }
    print(str(record))
    return record

parse_items()