from app.infrastructure.ocr.base import OCRProvider
from app.infrastructure.ocr.tesseract_provider import TesseractOCRProvider
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_ocr_provider() -> OCRProvider:
    provider_name = settings.OCR_PROVIDER.lower()
    
    if provider_name == "tesseract":
        return TesseractOCRProvider()
    else:
        logger.error(f"Unknown OCR provider specified: {provider_name}. Falling back to Tesseract.")
        return TesseractOCRProvider()
