from pymongo.collection import Collection
from .database import get_collection

class CRUD:
    def __init__(self, collection_name: str):
        self.collection: Collection = get_collection(collection_name)
    
    def create(self, data: dict):
        return str(self.collection.insert_one(data).inserted_id)
    
    def read(self, query: dict):
        return self.collection.find_one(query)
    
    def update(self, query: dict, data: dict):
        return self.collection.update_one(query, {"$set": data}).modified_count
    
    def delete(self, query: dict):
        return self.collection.delete_one(query).deleted_count
    
    def read_all(self, query: dict = {}):
        return list(self.collection.find(query))
