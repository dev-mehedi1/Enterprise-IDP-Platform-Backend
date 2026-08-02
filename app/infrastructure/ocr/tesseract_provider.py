from typing import Dict, Any, List
import pytesseract
from PIL import Image
import io
from app.infrastructure.ocr.base import OCRProvider
from app.core.config import settings

class TesseractOCRProvider(OCRProvider):
    def __init__(self):
        if settings.TESSERACT_CMD_PATH:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD_PATH
            
    async def extract_text_from_image(self, image_bytes: bytes) -> str:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
        
    async def get_bounding_boxes(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        image = Image.open(io.BytesIO(image_bytes))
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        boxes = []
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > 0 and data['text'][i].strip() != "":
                boxes.append({
                    "text": data['text'][i],
                    "left": data['left'][i],
                    "top": data['top'][i],
                    "width": data['width'][i],
                    "height": data['height'][i],
                    "confidence": data['conf'][i]
                })
        return boxes
