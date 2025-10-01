from db import es, cache
from model import Document
from typing import List
import json

INDEX_NAME = "documents"

# Index a document
def index_document(doc: Document):
    es.index(index=INDEX_NAME, id=doc.id, document=doc.dict())
    cache.delete(f"search:{doc.tenant_id}")  # Invalidate cache

# Get document by ID
def get_document(doc_id: str) -> dict:
    doc = es.get(index=INDEX_NAME, id=doc_id, ignore=[404])
    if doc and doc.get("found"):
        return doc["_source"]
    return None

# Delete document
def delete_document(doc_id: str):
    es.delete(index=INDEX_NAME, id=doc_id, ignore=[404])

# Search documents
def search_documents(query: str, tenant_id: str) -> List[dict]:
    # Check cache first
    cache_key = f"search:{tenant_id}:{query}"
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"content": query}}
                ],
                "filter": [
                    {"term": {"tenant_id": tenant_id}}
                ]
            }
        }
    }
    resp = es.search(index=INDEX_NAME, body=body)
    results = [hit["_source"] for hit in resp["hits"]["hits"]]

    cache.set(cache_key, json.dumps(results), ex=60)
    return results