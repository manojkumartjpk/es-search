
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from model import Document
from services import index_document, get_document, delete_document, search_documents
from rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from db import es, cache

app = FastAPI(title="Distributed Document Search Service")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"message": "Rate limit exceeded"})

# POST /documents
@app.post("/documents")
def create_document(doc: Document):
    index_document(doc)
    return {"status": "success", "id": doc.id}

# GET /documents/{id}
@app.get("/documents/{doc_id}")
def read_document(doc_id: str):
    doc = get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

# DELETE /documents/{id}
@app.delete("/documents/{doc_id}")
def remove_document(doc_id: str):
    delete_document(doc_id)
    return {"status": "deleted", "id": doc_id}

# GET /search?q=&tenant=
@app.get("/search")
@limiter.limit("10/minute")
def search(request: Request, q: str, tenant: str):
    results = search_documents(q, tenant)
    return results

# Health check
@app.get("/health")
def health():
    es_status = False
    redis_status = False
    try:
        es_status = es.ping()
        print("es_status", es_status, es.info())
    except Exception as e:
        print("elasticsearchexception", e)
        pass
    try:
        redis_status = cache.ping()
    except Exception:
        pass
    return {"status": "ok", "elasticsearch": es_status, "redis": redis_status}