from typing import Dict, Any
from app.infrastructure.database.models.document import UploadedDocument
from app.infrastructure.database.models.extraction import ExtractionResult
from app.infrastructure.ai.factory import get_ai_provider
from app.infrastructure.ocr.factory import get_ocr_provider
from app.domain.services.rule_engine import RuleEngineService
import structlog
import asyncio

logger = structlog.get_logger(__name__)

class PipelineService:
    def __init__(self):
        self.ai_provider = get_ai_provider()
        self.ocr_provider = get_ocr_provider()
        self.rule_engine = RuleEngineService()

    async def process_document(self, document_id: str) -> None:
        """
        The main orchestration pipeline.
        Steps:
        1. Fetch Document from DB
        2. Read file / PDF extraction
        3. OCR (if scanned)
        4. Apply Rule Engine (Regex, Dictionaries)
        5. Detect unresolved fields
        6. Call AI Provider for unresolved fields
        7. Validate and save ExtractionResult
        """
        logger.info(f"Starting pipeline for document {document_id}")
        
        doc = await UploadedDocument.get(document_id)
        if not doc:
            logger.error(f"Document {document_id} not found.")
            return
            
        doc.status = "PROCESSING"
        await doc.save()
        
        try:
            # Note: For production, we would load the file bytes from storage here.
            # Mocking text extraction for demonstration
            mock_text = f"Sample text extracted from {doc.filename}. Purchase Order Number: 12345."
            
            # 1. OCR (skipped in mock)
            # 2. Rule Engine (Regex matching)
            # 3. AI Extraction
            # We mock the schema
            schema = {"properties": {"purchase_order": {"type": "string"}}}
            ai_data = await self.ai_provider.extract_data(mock_text, schema, "Extract PO")
            
            # 4. Save Results
            result = ExtractionResult(
                document_id=str(doc.id),
                extracted_data=ai_data,
                confidence_scores={"purchase_order": 0.95},
                sources={"purchase_order": "ai"}
            )
            await result.insert()
            
            doc.status = "COMPLETED"
            doc.confidence_score = 0.95
            await doc.save()
            logger.info(f"Pipeline completed for document {document_id}")
            
        except Exception as e:
            logger.error(f"Pipeline failed for document {document_id}", exc_info=True)
            doc.status = "FAILED"
            await doc.save()
            raise e
