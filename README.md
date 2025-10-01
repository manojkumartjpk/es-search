to start -- > docker-compose up --build
sample api calls
1) healthcheck -- curl http://localhost:8000/health
2) document create 

curl -X POST http://localhost:8000/documents \
-H "Content-Type: application/json" \
-d '{
  "id": "doc1",
  "title": "First Document",
  "content": "This is a test document.",
  "tenant_id": "tenant1"
}'

3) read document. -- curl http://localhost:8000/documents/doc1

4) delete document. -- curl -X DELETE http://localhost:8000/documents/doc1

5) search document -- curl "http://localhost:8000/search?q=test&tenant=tenant1"
