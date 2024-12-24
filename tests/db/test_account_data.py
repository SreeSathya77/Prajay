import pytest
from datetime import datetime
from typing import Dict, Any
from src.utils.db_client import MongoDBClient

class TestAccountData:
    @pytest.fixture(scope="class")
    def db_client(self):
        return MongoDBClient()
        
    def test_account_schema_validation(self, db_client):
        """Test account document schema validation"""
        collection = db_client.get_collection("accounts_db", "users")
        
        # Get collection validation rules
        db = db_client.get_database("accounts_db")
        validation_rules = db.command("listCollections", 
                                    filter={"name": "users"})
        
        assert validation_rules is not None
        
    def test_account_indexes(self, db_client):
        """Test required indexes exist"""
        collection = db_client.get_collection("accounts_db", "users")
        indexes = collection.list_indexes()
        
        index_names = [index["name"] for index in indexes]
        assert "email_1" in index_names  # Assuming email should be indexed
        
    def test_account_data_integrity(self, db_client):
        """Test data integrity constraints"""
        collection = db_client.get_collection("accounts_db", "users")
        
        # Check for duplicate emails
        pipeline = [
            {"$group": {
                "_id": "$email",
                "count": {"$sum": 1}
            }},
            {"$match": {
                "count": {"$gt": 1}
            }}
        ]
        
        duplicates = list(collection.aggregate(pipeline))
        assert len(duplicates) == 0, "Duplicate email addresses found"
        
    def test_account_status_values(self, db_client):
        """Test valid status values"""
        collection = db_client.get_collection("accounts_db", "users")
        
        valid_statuses = ["ACTIVE", "INACTIVE", "SUSPENDED", "PENDING"]
        invalid_statuses = collection.find({
            "status": {"$nin": valid_statuses}
        })
        
        assert len(list(invalid_statuses)) == 0, "Invalid status values found"