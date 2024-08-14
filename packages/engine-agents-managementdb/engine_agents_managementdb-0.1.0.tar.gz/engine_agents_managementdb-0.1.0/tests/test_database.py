import unittest
from pymongo import MongoClient
from managementdb.database import get_collection
from managementdb.config import MONGO_URI, DATABASE_NAME

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup a connection to the test database
        cls.client = MongoClient(MONGO_URI)
        cls.db = cls.client[DATABASE_NAME]
        cls.collection_name = "test_collection"
        cls.collection = get_collection(cls.collection_name)

    def test_get_collection(self):
        # Test if the get_collection method returns a valid collection object
        self.assertIsNotNone(self.collection)
        self.assertEqual(self.collection.name, self.collection_name)
        self.assertEqual(self.collection.database.name, DATABASE_NAME)

    def test_insert_and_find(self):
        # Insert a document into the collection and verify it can be retrieved
        test_data = {"name": "test_document", "value": 42}
        insert_result = self.collection.insert_one(test_data)
        self.assertIsNotNone(insert_result.inserted_id)
        
        # Find the document by name
        found_document = self.collection.find_one({"name": "test_document"})
        self.assertIsNotNone(found_document)
        self.assertEqual(found_document["value"], 42)
        
        # Clean up by deleting the inserted document
        delete_result = self.collection.delete_one({"_id": insert_result.inserted_id})
        self.assertEqual(delete_result.deleted_count, 1)

    @classmethod
    def tearDownClass(cls):
        # Clean up test collection
        cls.db.drop_collection(cls.collection_name)
        cls.client.close()

if __name__ == '__main__':
    unittest.main()
