import os
import shutil
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.schemas.document import DocumentChunk, ChunkMetadata

# Strict chunking boundaries to prevent token overflow during embedding
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

async def process_pdf(file: UploadFile) -> tuple[int, int, list[DocumentChunk]]:
    temp_file_path = f"data/{file.filename}"
    
    # Save uploaded file to local disk temporarily
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Load and split
        loader = PyPDFLoader(temp_file_path)
        pages = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(pages)
        
        # Map to strict Pydantic schemas
        processed_chunks = []
        for chunk in chunks:
            meta = ChunkMetadata(
                source=chunk.metadata.get("source", file.filename),
                page=chunk.metadata.get("page", 0)
            )
            processed_chunks.append(DocumentChunk(text=chunk.page_content, metadata=meta))
            
        return len(pages), len(chunks), processed_chunks
        
    finally:
        # Clean up the temporary file immediately
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)