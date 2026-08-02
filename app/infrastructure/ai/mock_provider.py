from typing import Dict, Any
from app.infrastructure.ai.base import AIProvider

class MockAIProvider(AIProvider):
    """A mock AI provider for testing and development without API keys."""
    
    async def extract_data(self, text: str, schema: Dict[str, Any], prompt_template: str) -> Dict[str, Any]:
        # Return a mock response matching the schema keys for demonstration
        mock_response = {}
        if "properties" in schema:
            for key, val in schema["properties"].items():
                if val.get("type") == "string":
                    mock_response[key] = f"mock_value_for_{key}"
                elif val.get("type") == "number":
                    mock_response[key] = 123.45
                elif val.get("type") == "integer":
                    mock_response[key] = 10
                elif val.get("type") == "boolean":
                    mock_response[key] = True
                else:
                    mock_response[key] = None
        return mock_response
    
    async def classify_document(self, text: str, categories: list[str]) -> str:
        # Default to the first category
        return categories[0] if categories else "Unknown"
