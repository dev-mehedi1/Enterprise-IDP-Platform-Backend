from abc import ABC, abstractmethod
from typing import Dict, Any

class AIProvider(ABC):
    """Abstract Base Class for all AI Providers."""
    
    @abstractmethod
    async def extract_data(self, text: str, schema: Dict[str, Any], prompt_template: str) -> Dict[str, Any]:
        """
        Sends the text to the AI provider and asks it to extract data matching the provided JSON schema.
        Returns the parsed JSON dictionary.
        """
        pass
    
    @abstractmethod
    async def classify_document(self, text: str, categories: list[str]) -> str:
        """
        Given the document text and a list of categories, returns the best matching category.
        """
        pass
