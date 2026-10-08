from pydantic import BaseModel
from typing import List

class ChunkMetadata(BaseModel):
    source: str
    page: int

class DocumentChunk(BaseModel):
    text: str
    metadata: ChunkMetadata

class IngestionResponse(BaseModel):
    filename: str
    total_pages: int
    total_chunks: int
    chunks: List[DocumentChunk]