from pydantic import BaseModel
from typing import Optional

class Document(BaseModel):
    id: str
    tenant_id: str
    title: str
    content: str

class SearchResult(BaseModel):
    id: str
    title: str
    content: str