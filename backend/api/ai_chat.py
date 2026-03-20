from fastapi import APIRouter, Depends

from .dependencies import get_ai_chat_service
from ..schemas.ai import AIChatRequest, AIChatResponse
from ..services.ai_service import AIChatService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=AIChatResponse)
def chat(
    request: AIChatRequest,
    service: AIChatService = Depends(get_ai_chat_service),
) -> AIChatResponse:
    return service.chat(request)
