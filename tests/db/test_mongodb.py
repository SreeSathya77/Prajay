import pytest
from datetime import datetime
from typing import Dict, Any
from src.utils.db_client import MongoDBClient

class TestMongoDB:
    @pytest.fixture(scope="class")
    def db_client(self):
        client = MongoDBClient()
        assert client.check_connection(), "MongoDB connection failed"
        return client
        
    @pytest.fixture
    def test_account(self) -> Dict[str, Any]:
        return {
            "accountType": "PERSONAL",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "createdAt": datetime.utcnow(),
            "status": "ACTIVE"
        }
        
    def test_database_connection(self, db_client):
        """Test MongoDB connection"""
        assert db_client.check_connection()
        
    def test_insert_and_find_document(self, db_client, test_account):
        """Test inserting and retrieving a document"""
        # Insert document
        doc_id = db_client.insert_document(
            db_name="accounts_db",
            collection_name="users",
            document=test_account
        )
        assert doc_id is not None
        
        # Find document
        found_doc = db_client.find_document(
            db_name="accounts_db",
            collection_name="users",
            query={"email": test_account["email"]}
        )
        assert found_doc is not None
        assert found_doc["firstName"] == test_account["firstName"]
        
    def test_update_document(self, db_client, test_account):
        """Test updating a document"""
        # First insert a document
        db_client.insert_document(
            db_name="accounts_db",
            collection_name="users",
            document=test_account
        )
        
        # Update the document
        update_result = db_client.update_document(
            db_name="accounts_db",
            collection_name="users",
            query={"email": test_account["email"]},
            update={"status": "INACTIVE"}
        )
        assert update_result == 1
        
        # Verify update
        updated_doc = db_client.find_document(
            db_name="accounts_db",
            collection_name="users",
            query={"email": test_account["email"]}
        )
        assert updated_doc["status"] == "INACTIVE"
        
    def test_delete_document(self, db_client, test_account):
        """Test deleting a document"""
        # First insert a document
        db_client.insert_document(
            db_name="accounts_db",
            collection_name="users",
            document=test_account
        )
        
        # Delete the document
        delete_result = db_client.delete_document(
            db_name="accounts_db",
            collection_name="users",
            query={"email": test_account["email"]}
        )
        assert delete_result == 1
        
        # Verify deletion
        deleted_doc = db_client.find_document(
            db_name="accounts_db",
            collection_name="users",
            query={"email": test_account["email"]}
        )
        assert deleted_doc is None
        
    def test_collection_stats(self, db_client):
        """Test retrieving collection statistics"""
        stats = db_client.get_collection_stats(
            db_name="accounts_db",
            collection_name="users"
        )
        assert "ns" in stats
        assert "count" in stats
        assert "size" in stats