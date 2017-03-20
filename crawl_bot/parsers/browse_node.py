from scrapy.utils.project import get_project_settings
from crawl_bot.crawl_utils import Crawl


def parse_browse_nodes():
    settings = get_project_settings()
    uri = settings.get("MONGO_URI")
    db_name = settings.get('MONGO_DATABASE')
    collection = settings.get('MONGO_COLLECTION')
    bn_collection = settings.get('MONGO_BROWSE_NODE')
    conn = Crawl.open_connection(uri)
    database = conn[db_name]

    print("uri: #{0}, db: #{1}, collection: #{2}".format(uri, db_name, collection))
    bn_docs = database[bn_collection]
    docs = database[collection].find()
    for doc in docs:
        bns = [get_browse_node(cat) for cat in doc['data']['CategoryArray']['Category']]
        bn_docs.insert_many(bns)


def get_browse_node(cat):
    if cat['LeafCategory']:
        kind = 'leaf'
    else:
        if cat['CategoryLevel'] != 0:
            kind = 'branch'
        else:
            kind= 'root'

    node =  {
        'id': cat['CategoryID'],
        'name': cat['CategoryName'],
        'kind': kind,
        'level': cat.get('CategoryLevel',None),
        'path_ids': cat.get('CategoryIDPath', None),
        'path_names': cat.get('CategoryNamePath',None),
        'parent_id': cat.get('CategoryParentID',None)
    }
    print(str(node))
    return node

parse_browse_nodes()