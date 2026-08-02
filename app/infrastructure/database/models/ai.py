from beanie import Document
from pydantic import Field
from typing import Any, Dict, Optional
from datetime import datetime, timezone

class AIRequest(Document):
    document_id: str = Field(indexed=True)
    provider: str # "openai", "gemini", "mock"
    model_version: str
    prompt_used: str
    unresolved_data: Dict[str, Any]
    
    status: str = "PENDING"
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "ai_requests"

class AIResponse(Document):
    ai_request_id: str = Field(indexed=True)
    raw_response: str
    parsed_json: Optional[Dict[str, Any]] = None
    token_count_prompt: int = 0
    token_count_completion: int = 0
    latency_ms: int = 0
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "ai_responses"
