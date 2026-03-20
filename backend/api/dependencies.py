from __future__ import annotations

import os

from ..data.repository import PostgresPropertyRepository, SQLitePropertyRepository
from ..services.ai_service import AIChatService
from ..services.property_service import PropertyService


_repository = None
_property_service = None
_ai_chat_service = None


def get_repository():
    global _repository
    if _repository is None:
        backend_type = os.getenv("PROPERTY_DB_BACKEND", "sqlite").lower()
        if backend_type == "postgres":
            dsn = os.getenv("PROPERTY_POSTGRES_DSN", "")
            if not dsn:
                raise ValueError("PROPERTY_POSTGRES_DSN must be set when PROPERTY_DB_BACKEND=postgres")
            _repository = PostgresPropertyRepository(dsn=dsn)
        else:
            db_path = os.getenv("PROPERTY_SQLITE_PATH", "backend/data/properties.db")
            _repository = SQLitePropertyRepository(db_path=db_path)
    return _repository


def get_property_service() -> PropertyService:
    global _property_service
    if _property_service is None:
        _property_service = PropertyService(repository=get_repository())
    return _property_service


def get_ai_chat_service() -> AIChatService:
    global _ai_chat_service
    if _ai_chat_service is None:
        _ai_chat_service = AIChatService(property_service=get_property_service())
    return _ai_chat_service
