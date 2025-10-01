import unittest
import requests
import uuid
import time

BASE_URL = "http://localhost"

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        """Setup resources before each test."""
        self.doc_id = str(uuid.uuid4())  # Generate a unique document ID for each test
        self.payload = {
            "id": self.doc_id,
            "title": "Test Document",
            "content": "This is a test document.",
            "tenant_id": "tenant1"
        }

    def tearDown(self):
        """Clean up resources after each test."""
        # Attempt to delete the document if it exists
        requests.delete(f"{BASE_URL}/documents/{self.doc_id}")

    def test_1_health_check(self):
        response = requests.get(f"{BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("elasticsearch", response.json())
        self.assertIn("redis", response.json())

    def test_2_create_document(self):
        response = requests.post(f"{BASE_URL}/documents", json=self.payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "success")
        self.assertEqual(response.json().get("id"), self.doc_id)

    def test_3_read_document(self):
        # Ensure the document exists
        requests.post(f"{BASE_URL}/documents", json=self.payload)
        response = requests.get(f"{BASE_URL}/documents/{self.doc_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), self.doc_id)
        self.assertEqual(response.json().get("title"), "Test Document")

    def test_4_delete_document(self):
        # Ensure the document exists
        requests.post(f"{BASE_URL}/documents", json=self.payload)
        response = requests.delete(f"{BASE_URL}/documents/{self.doc_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "deleted")
        self.assertEqual(response.json().get("id"), self.doc_id)

    def test_5_search_documents(self):
        # Ensure the document exists
        requests.post(f"{BASE_URL}/documents", json=self.payload)
        time.sleep(1)  # Wait for Elasticsearch to index the document
        response = requests.get(f"{BASE_URL}/search?q=test&tenant=tenant1")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        # Filter results to ensure the correct document is found
        matching_docs = [doc for doc in response.json()["results"] if doc.get("id") == self.doc_id]
        self.assertTrue(matching_docs, "Document not found in search results")
        self.assertEqual(matching_docs[0].get("id"), self.doc_id)

if __name__ == "__main__":
    unittest.main()