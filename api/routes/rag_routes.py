from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
from uuid import uuid4

from api.schemas.request_models import QueryRequest
from api.schemas.response_models import QueryResponse
from api.services.rag_services import RAGService

router = APIRouter()
rag_service = RAGService()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_documents(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    thread_id: str = Form(...),
):
    try:
        document_id = str(uuid4())
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Process document
        rag_service.ingest_document(
            file_path=file_path,
            user_id=user_id,
            thread_id=thread_id,
            document_id=document_id,
            source=file.filename,
        )

        return {
            "message": "Document upload and indexed successfully",
            "document_id": document_id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    try:
        answer = rag_service.query(
            user_query=request.query,
            thread_id=request.thread_id,
        )
        return QueryResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))