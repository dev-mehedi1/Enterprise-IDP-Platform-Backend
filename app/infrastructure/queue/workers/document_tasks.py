from app.infrastructure.queue.celery_app import celery_app
from app.application.services.pipeline_service import PipelineService
import asyncio
from asgiref.sync import async_to_sync
from app.infrastructure.database.init_db import init_db

# We need to initialize DB connections in the worker process
def run_async(coro):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@celery_app.task(name="process_document_task", bind=True, max_retries=3)
def process_document_task(self, document_id: str):
    """Celery task to run the document processing pipeline asynchronously."""
    
    async def _run():
        await init_db()
        pipeline = PipelineService()
        await pipeline.process_document(document_id)
        
    try:
        run_async(_run())
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
