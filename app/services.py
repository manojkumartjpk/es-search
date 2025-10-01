from db import es, cache
from model import Document
from typing import List, Dict
import json

INDEX_NAME = "documents"

# ---------------------------
# Index a document
# ---------------------------
def index_document(doc: Document):
    try:
        es.index(index=INDEX_NAME, id=doc.id, document=doc.dict())
        cache.delete(f"search:{doc.tenant_id}")  # Invalidate cache for tenant
    except Exception as e:
        raise RuntimeError(f"Failed to index document: {e}")


# ---------------------------
# Get document by ID
# ---------------------------
def get_document(doc_id: str) -> dict:
    try:
        doc = es.get(index=INDEX_NAME, id=doc_id, ignore=[404])
        if doc and doc.get("found"):
            return doc["_source"]
        return None
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve document: {e}")


# ---------------------------
# Delete document
# ---------------------------
def delete_document(doc_id: str):
    try:
        es.delete(index=INDEX_NAME, id=doc_id, ignore=[404])
    except Exception as e:
        raise RuntimeError(f"Failed to delete document: {e}")


# ---------------------------
# Search documents with advanced features
# ---------------------------
def search_documents(query: str, tenant_id: str, page: int = 0, size: int = 10) -> Dict:
    try:
        # Check cache first
        cache_key = f"search:{tenant_id}:{query}:{page}:{size}"
        cached = cache.get(cache_key)
        if cached:
            return json.loads(cached)

        # Elasticsearch query with fuzzy, highlighting, and faceted search
        body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"content": {"query": query, "fuzziness": "AUTO"}}}
                    ],
                    "filter": [
                        {"term": {"tenant_id": tenant_id}}
                    ]
                }
            },
            "highlight": {
                "fields": {
                    "content": {}
                }
            },
            "aggs": {
                "categories": {"terms": {"field": "category.keyword"}}  # Example facet
            },
            "from": page * size,
            "size": size
        }

        resp = es.search(index=INDEX_NAME, body=body)
        results = []
        for hit in resp["hits"]["hits"]:
            results.append({
                "id": hit["_id"],
                "score": hit["_score"],
                "highlight": hit.get("highlight", {}),
                "source": hit["_source"]
            })

        facets = resp.get("aggregations", {})
        response = {"results": results, "facets": facets}

        # Cache the response for 60 seconds
        cache.set(cache_key, json.dumps(response), ex=60)
        return response

    except Exception as e:
        raise RuntimeError(f"Search operation failed: {e}")
