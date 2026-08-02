from abc import ABC, abstractmethod
from typing import Dict, Any, List
import io

class OCRProvider(ABC):
    """Abstract Base Class for all OCR Providers."""
    
    @abstractmethod
    async def extract_text_from_image(self, image_bytes: bytes) -> str:
        """Extracts text from a single image."""
        pass
        
    @abstractmethod
    async def get_bounding_boxes(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        """Extracts bounding boxes and text from a single image."""
        pass
