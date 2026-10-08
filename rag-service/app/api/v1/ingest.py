from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.document import IngestionResponse
from app.services.ingestion import process_pdf

router = APIRouter()

@router.post("/upload", response_model=IngestionResponse, tags=["Ingestion"])
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Strictly accepting PDF files only.")
        
    try:
        pages, chunk_count, chunks = await process_pdf(file)
        return IngestionResponse(
            filename=file.filename,
            total_pages=pages,
            total_chunks=chunk_count,
            chunks=chunks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))