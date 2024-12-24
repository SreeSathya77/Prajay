from typing import Dict, Any, List
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDBClient:
    def __init__(self):
        self.host = os.getenv('MONGODB_HOST', '10.10.10.56')
        self.port = int(os.getenv('MONGODB_PORT', '27017'))
        self.client = MongoClient(host=self.host, port=self.port)
        
    def get_database(self, db_name: str) -> Database:
        return self.client[db_name]
        
    def get_collection(self, db_name: str, collection_name: str) -> Collection:
        return self.get_database(db_name)[collection_name]
        
    def insert_document(self, db_name: str, collection_name: str, document: Dict[str, Any]) -> str:
        collection = self.get_collection(db_name, collection_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)
        
    def find_document(self, db_name: str, collection_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
        collection = self.get_collection(db_name, collection_name)
        return collection.find_one(query)
        
    def update_document(self, db_name: str, collection_name: str, 
                       query: Dict[str, Any], update: Dict[str, Any]) -> int:
        collection = self.get_collection(db_name, collection_name)
        result = collection.update_one(query, {'$set': update})
        return result.modified_count
        
    def delete_document(self, db_name: str, collection_name: str, query: Dict[str, Any]) -> int:
        collection = self.get_collection(db_name, collection_name)
        result = collection.delete_one(query)
        return result.deleted_count
        
    def get_collection_stats(self, db_name: str, collection_name: str) -> Dict[str, Any]:
        db = self.get_database(db_name)
        return db.command('collstats', collection_name)
        
    def check_connection(self) -> bool:
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False