from pydantic import BaseModel, Field

from ..schemas.property import PropertyCard


class AIChatRequest(BaseModel):
    message: str = Field(min_length=1)
    context_property_ids: list[int] = Field(default_factory=list)


class AIChatResponse(BaseModel):
    summary: str
    property_cards: list[PropertyCard]
    suggestions: list[str] = Field(default_factory=list)
    answer: str
