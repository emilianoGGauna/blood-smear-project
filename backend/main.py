from fastapi import FastAPI

from .api import ai_chat_router, health_router, properties_router, search_router

app = FastAPI(title="Property Search API", version="0.1.0")

app.include_router(health_router)
app.include_router(properties_router)
app.include_router(search_router)
app.include_router(ai_chat_router)
