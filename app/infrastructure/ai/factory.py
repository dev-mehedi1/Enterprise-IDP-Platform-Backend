from app.infrastructure.ai.base import AIProvider
from app.infrastructure.ai.mock_provider import MockAIProvider
from app.core.config import settings
from app.core.exceptions import AIProviderError
import logging

logger = logging.getLogger(__name__)

def get_ai_provider() -> AIProvider:
    provider_name = settings.AI_PROVIDER.lower()
    
    if provider_name == "mock":
        return MockAIProvider()
    elif provider_name == "openai":
        # from app.infrastructure.ai.openai_provider import OpenAIProvider
        # return OpenAIProvider(api_key=settings.OPENAI_API_KEY)
        raise NotImplementedError("OpenAI provider not fully implemented in this phase.")
    elif provider_name == "gemini":
        raise NotImplementedError("Gemini provider not fully implemented in this phase.")
    else:
        logger.error(f"Unknown AI provider specified: {provider_name}")
        raise AIProviderError(f"Unknown provider {provider_name}")
