from pymongo import MongoClient
from helper.config import ConfigSingleton

class MongoDBService:
    def __init__(self, collection_name=None):
        config = ConfigSingleton()
        self.client = MongoClient(config.mongodb_uri)
        self.db = self.client.get_default_database()
        self.collection_name = collection_name or config.job_collection_name
        self.collection = self.db[self.collection_name]

    def insert_one(self, data):
        return self.collection.insert_one(data)

    def find(self, query=None, limit=100):
        query = query or {}
        cursor = self.collection.find(query).limit(limit)
        return list(cursor)

    def insert_many(self, data_list):
        return self.collection.insert_many(data_list)

    def update_one(self, query, update):
        return self.collection.update_one(query, {"$set": update})

    def delete_one(self, query):
        return self.collection.delete_one(query)

    def set_collection(self, collection_name):
        self.collection_name = collection_name
        self.collection = self.db[collection_name]
