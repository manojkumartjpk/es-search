# Distributed Document Search Service

A FastAPI-based distributed document search service with Elasticsearch and Redis caching support.

---

## Getting Started

### Prerequisites

* Docker & Docker Compose installed on your machine.

### Start the service

```bash
docker-compose up --build
```

This will build the Docker images and start the service along with Elasticsearch and Redis.

---

## Project Structure

```
├── main.py           # FastAPI application
├── model.py          # Pydantic models (Document etc.)
├── services.py       # Elasticsearch and caching logic
├── db.py             # Elasticsearch and Redis client setup
├── rate_limiter.py   # SlowAPI rate limiting setup
├── docker-compose.yml # Docker configuration
└── README.md         # Project documentation
```

---

## API Endpoints

### 1. Health Check

Check if the service, Elasticsearch, and Redis are running.

```bash
curl http://localhost:8000/health
```

**Response:**

```json
{
  "status": "ok",
  "elasticsearch": true,
  "redis": true
}
```

---

### 2. Create Document

Create a new document in the system.

```bash
curl -X POST http://localhost:8000/documents \
-H "Content-Type: application/json" \
-d '{
  "id": "doc1",
  "title": "First Document",
  "content": "This is a test document.",
  "tenant_id": "tenant1"
}'
```

**Response:**

```json
{
  "status": "success",
  "id": "doc1"
}
```

---

### 3. Read Document

Retrieve a document by ID.

```bash
curl http://localhost:8000/documents/doc1
```

**Response:**

```json
{
  "id": "doc1",
  "title": "First Document",
  "content": "This is a test document.",
  "tenant_id": "tenant1"
}
```

---

### 4. Delete Document

Delete a document by ID.

```bash
curl -X DELETE http://localhost:8000/documents/doc1
```

**Response:**

```json
{
  "status": "deleted",
  "id": "doc1"
}
```

---

### 5. Search Documents

Search for documents by query and tenant.

```bash
curl "http://localhost:8000/search?q=test&tenant=tenant1"
```

**Response:**

```json
[
  {
    "id": "doc1",
    "title": "First Document",
    "content": "This is a test document.",
    "tenant_id": "tenant1",
    "score": 1.23
  }
]
```

---

## Notes

* Ensure that the `tenant_id` field in your requests matches the Pydantic model in `model.py`.
* Rate limiting is applied to the `/search` endpoint (10 requests per minute).
