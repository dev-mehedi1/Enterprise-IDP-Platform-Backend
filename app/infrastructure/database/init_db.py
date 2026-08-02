from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings

from app.infrastructure.database.models.user import User, Role
from app.infrastructure.database.models.document import DocumentType, DocumentSchema, UploadedDocument
from app.infrastructure.database.models.extraction import ExtractionResult, OCRResult, LayoutAnalysis
from app.infrastructure.database.models.rules import FieldAlias, ExtractionRule, BusinessDictionary
from app.infrastructure.database.models.ai import AIRequest, AIResponse

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.MONGODB_DB_NAME]
    
    await init_beanie(
        database=database,
        document_models=[
            User, Role,
            DocumentType, DocumentSchema, UploadedDocument,
            ExtractionResult, OCRResult, LayoutAnalysis,
            FieldAlias, ExtractionRule, BusinessDictionary,
            AIRequest, AIResponse
        ]
    )
