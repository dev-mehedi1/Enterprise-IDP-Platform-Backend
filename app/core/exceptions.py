from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Any

class BaseIDPException(Exception):
    """Base exception for the IDP platform."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class DocumentProcessingError(BaseIDPException):
    """Raised when document processing fails."""
    def __init__(self, message: str = "Document processing failed."):
        super().__init__(message, status_code=422)

class ResourceNotFoundError(BaseIDPException):
    """Raised when a resource is not found."""
    def __init__(self, resource: str, resource_id: str):
        super().__init__(f"{resource} with ID {resource_id} not found.", status_code=404)

class AIProviderError(BaseIDPException):
    """Raised when an AI Provider fails."""
    def __init__(self, message: str):
        super().__init__(f"AI Provider Error: {message}", status_code=502)

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseIDPException)
    async def idp_exception_handler(request: Any, exc: BaseIDPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.__class__.__name__, "message": exc.message}
        )
