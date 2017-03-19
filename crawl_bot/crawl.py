class Crawl(object):
    @classmethod
    def get_crawl_by_uid(cls, uid, database, collection):
        row = database[collection].find_one({"uid": str(uid)})
        return row

    @classmethod
    def is_crawled(cls, uid, database, collection):
        row = database[collection].find_one({"uid": str(uid)}, {"uid": 1, "_id":0})
        return row is not None

    @classmethod
    def open_connection(cls):
        # Yet to implement
        return None

    def close_connection(cls):
        # Yet to implement
        return None
