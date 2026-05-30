from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import logging
from pathlib import Path
from uuid import uuid4

from api.schemas.request_models import QueryRequest
from api.schemas.response_models import QueryResponse
from api.services.rag_services import RAGService

router = APIRouter()
rag_service = None
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("data/uploads")
SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


def get_rag_service() -> RAGService:
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service


@router.post("/upload")
async def upload_documents(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    thread_id: str = Form(...),
):
    try:
        original_filename = Path(file.filename or "upload").name
        file_extension = Path(original_filename).suffix.lower()
        if file_extension not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload a PDF or TXT file.",
            )

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        document_id = str(uuid4())
        file_path = UPLOAD_DIR / f"{document_id}{file_extension}"

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Process document
        get_rag_service().ingest_document(
            file_path=str(file_path),
            user_id=user_id,
            thread_id=thread_id,
            document_id=document_id,
            source=original_filename,
        )

        return {
            "message": "Document upload and indexed successfully",
            "document_id": document_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Document upload failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    try:
        result = get_rag_service().query(
            user_query=request.query,
            thread_id=request.thread_id,
        )
        return QueryResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
