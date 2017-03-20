import pymongo
import pandas

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
    def open_connection(cls, uri):
        conn = pymongo.MongoClient(uri)
        return conn

    @classmethod
    def close_connection(cls, conn):
        # Yet to implement
        conn.close()
        
class DB(object):
    
    
    @classmethod
    def query(cls, docs, query={}, columns=[], exclude_columns=["_id"], limit=None, engine='mongodb'):
        if engine == 'mongodb':
            projection = None
            if columns != []:
                projection = {}
                for column in columns:
                    projection[column]=1
            if exclude_columns is not None:
                projection = projection or  {}
                for column in exclude_columns:
                    projection[column]= 0
            print("({0}, {1})".format(query, projection))
            cursor = docs.find(query, projection)
            if limit is not None:
                cursor = cursor.limit(limit)
            return cursor
        else:
            raise "Unsupported db engine '{0}'".format(engine)
            
    @classmethod
    def to_dataframe(cls, *args, **kwargs):
        cursor = cls.query(*args, **kwargs)
        df = pandas.DataFrame(list(cursor))
        return df

