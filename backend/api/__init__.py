from .ai_chat import router as ai_chat_router
from .health import router as health_router
from .properties import router as properties_router
from .search import router as search_router

__all__ = [
    "health_router",
    "properties_router",
    "search_router",
    "ai_chat_router",
]
