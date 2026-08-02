# Enterprise Intelligent Document Processing (IDP) Platform

An enterprise-grade, scalable, and AI-provider agnostic backend for Intelligent Document Processing. 

Built with **FastAPI, MongoDB (Beanie), Celery, RabbitMQ, and Redis**. Follows Clean Architecture, SOLID, and Domain-Driven Design (DDD) principles.

## Features
- **Plug-and-Play AI Providers**: Supports any LLM provider (OpenAI, Gemini, Ollama) via Factory Pattern.
- **Plug-and-Play OCR Providers**: Built-in support for Tesseract, highly extensible.
- **Asynchronous Document Pipeline**: High throughput processing powered by Celery & RabbitMQ.
- **Rule Engine**: Pre-process documents deterministically with Regex and Business Dictionaries to save AI token costs.
- **Clean Architecture**: Strong separation of concerns ensuring testability and maintainability.

## Technology Stack
- **API**: FastAPI (Python 3.12+)
- **Database**: MongoDB + Beanie ODM
- **Task Queue**: Celery + RabbitMQ
- **Caching / State**: Redis
- **Dependency Management**: Poetry
- **OCR**: PyTesseract, Pillow
- **Containerization**: Docker & Docker Compose

## Quickstart

### Prerequisites
- Docker & Docker Compose
- Poetry (optional, for local non-docker dev)

### Running with Docker Compose
This is the recommended way to run the entire stack locally.

1. Create your `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the API documentation:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Project Structure
```text
app/
├── api/              # API interface layer (FastAPI endpoints, auth dependencies)
├── application/      # Application layer (Use cases, pipeline orchestrator)
├── core/             # Core settings, exceptions, logging, security
├── domain/           # Enterprise domain logic (Rule engine, core models)
├── infrastructure/   # External integrations (MongoDB Beanie models, AI/OCR factories, Celery)
```

## Scalability
Designed to handle millions of documents per month:
- **Horizontal Scaling**: Simply add more `celery_worker` instances in your deployment.
- **Async I/O**: FastAPI + Motor ensure the API never blocks.
- **Cost Optimization**: AI is only called for unresolved fields after deterministic extraction.
