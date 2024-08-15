from bson.objectid import ObjectId
from pymongo.collection import Collection
from .database import get_collection
from .models import Item

class CRUD:
    def __init__(self, collection_name: str):
        self.collection: Collection = get_collection(collection_name)
    
    def create(self, data: dict):
        return str(self.collection.insert_one(data).inserted_id)
    
    def read(self, item_id: str):
        return self.collection.find_one({"_id": ObjectId(item_id)})
    
    def update(self, item_id: str, data: dict):
        return self.collection.update_one({"_id": ObjectId(item_id)}, {"$set": data}).modified_count
    
    def delete(self, item_id: str):
        return self.collection.delete_one({"_id": ObjectId(item_id)}).deleted_count
    
    def read_all(self, query: dict = {}):
        return list(self.collection.find(query))
