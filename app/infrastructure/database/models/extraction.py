from beanie import Document
from pydantic import Field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

class ExtractionResult(Document):
    document_id: str = Field(indexed=True)
    extracted_data: Dict[str, Any]
    confidence_scores: Dict[str, float]
    sources: Dict[str, str] # mapping of field to source (e.g. "regex", "ai")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "extraction_results"

class OCRResult(Document):
    document_id: str = Field(indexed=True)
    page_number: int
    raw_text: str
    bounding_boxes: List[Dict[str, Any]]
    
    class Settings:
        name = "ocr_results"

class LayoutAnalysis(Document):
    document_id: str = Field(indexed=True)
    page_number: int
    tables: List[Dict[str, Any]]
    images: List[Dict[str, Any]]
    paragraphs: List[Dict[str, Any]]
    
    class Settings:
        name = "layout_analysis"
