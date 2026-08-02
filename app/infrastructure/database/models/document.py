from beanie import Document
from pydantic import Field, AnyUrl
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

class DocumentType(Document):
    name: str = Field(unique=True) # e.g. "Purchase Order", "Invoice"
    description: Optional[str] = None
    
    class Settings:
        name = "document_types"

class DocumentSchema(Document):
    document_type: str = Field(unique=True)
    schema_definition: Dict[str, Any] # JSON Schema definition
    
    class Settings:
        name = "document_schemas"

class UploadedDocument(Document):
    filename: str
    original_filename: str
    file_hash: str = Field(unique=True)
    mime_type: str
    size_bytes: int
    storage_path: str
    
    # Processing states: UPLOADED -> CLASSIFIED -> OCR_COMPLETED -> EXTRACTION_COMPLETED -> VALIDATED -> HUMAN_REVIEW -> DONE
    status: str = Field(default="UPLOADED") 
    
    document_type_id: Optional[str] = None
    confidence_score: float = 0.0
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "uploaded_documents"
