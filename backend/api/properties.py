from fastapi import APIRouter, Depends, HTTPException

from .dependencies import get_property_service
from ..schemas.property import PropertyCard, PropertyDetail
from ..services.property_service import PropertyService

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("", response_model=list[PropertyCard])
def list_properties(service: PropertyService = Depends(get_property_service)) -> list[PropertyCard]:
    return service.list_properties()


@router.get("/{property_id}", response_model=PropertyDetail)
def get_property(property_id: int, service: PropertyService = Depends(get_property_service)) -> PropertyDetail:
    result = service.get_property(property_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return result
