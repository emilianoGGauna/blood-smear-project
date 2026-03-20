from pydantic import BaseModel, Field

from ..schemas.property import PropertyCard


class SearchRequest(BaseModel):
    query: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    bedrooms: int | None = None
    location: str | None = None
    limit: int = Field(default=10, ge=1, le=50)


class SearchResponse(BaseModel):
    summary: str
    property_cards: list[PropertyCard]
    suggestions: list[str] = Field(default_factory=list)
