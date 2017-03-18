class Crawl(object):
    @classmethod
    def get_crawl_by_uid(self, uid, database, collection):
        row = database[collection].find_one({"uid": str(uid)})
        return row

    @classmethod
    def is_crawled(self, uid, database, collection):
        row = database[collection].find_one({"uid": str(uid)}, {"uid": 1, "_id":0})
        return row is not None

