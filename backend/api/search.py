from fastapi import APIRouter, Depends

from .dependencies import get_property_service
from ..schemas.search import SearchRequest, SearchResponse
from ..services.property_service import PropertyService

router = APIRouter(tags=["search"])


@router.post("/search", response_model=SearchResponse)
def search_properties(
    request: SearchRequest,
    service: PropertyService = Depends(get_property_service),
) -> SearchResponse:
    return service.search(request)
