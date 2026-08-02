from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from app.infrastructure.database.models.document import UploadedDocument
from app.infrastructure.database.models.user import User
from app.api.dependencies.auth import get_current_active_user
from app.infrastructure.queue.workers.document_tasks import process_document_task
import hashlib
import os
import shutil

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    # current_user: User = Depends(get_current_active_user) # Commented for local test
):
    # 1. Read file and calculate hash for duplicate detection
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()
    
    # 2. Check duplicate
    existing = await UploadedDocument.find_one(UploadedDocument.file_hash == file_hash)
    if existing:
        return {"message": "Document already exists", "document_id": str(existing.id), "status": existing.status}
        
    # 3. Store file locally (In prod, upload to S3)
    os.makedirs("./uploads", exist_ok=True)
    file_path = f"./uploads/{file_hash}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(content)
        
    # 4. Save metadata to DB
    doc = UploadedDocument(
        filename=file.filename,
        original_filename=file.filename,
        file_hash=file_hash,
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=len(content),
        storage_path=file_path,
        status="UPLOADED"
    )
    await doc.insert()
    
    # 5. Trigger Celery Task
    process_document_task.delay(str(doc.id))
    
    return {"message": "Document uploaded and processing started", "document_id": str(doc.id)}

@router.get("/{document_id}/status")
async def get_status(document_id: str):
    from bson import ObjectId
    if not ObjectId.is_valid(document_id):
        raise HTTPException(status_code=400, detail="Invalid Document ID format")
    
    doc = await UploadedDocument.get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    return {"document_id": str(doc.id), "status": doc.status, "confidence": doc.confidence_score}
