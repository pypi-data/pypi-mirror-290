from pymongo.collection import Collection
from .database import get_collection

class CRUD:
    def __init__(self, collection_name: str):
        self.collection: Collection = get_collection(collection_name)
    
    def create(self, data: dict):
        # Insert the document into the collection
        insert_result = self.collection.insert_one(data)    
        # Retrieve the inserted document using the inserted_id
        inserted_document = self.collection.find_one({"_id": insert_result.inserted_id})
        # Return the full inserted document
        return inserted_document
    
    def read(self, query: dict):
        return self.collection.find_one(query)
    
    def update(self, query: dict, data: dict):
        return self.collection.update_one(query, {"$set": data}).modified_count
    
    def delete(self, query: dict):
        return self.collection.delete_one(query).deleted_count
    
    def read_all(self, query: dict = {}):
        return list(self.collection.find(query))
