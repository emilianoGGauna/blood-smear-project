from pydantic import BaseModel, Field


class PropertyCard(BaseModel):
    id: int
    title: str
    location: str
    price: int
    bedrooms: int
    bathrooms: int
    square_feet: int
    tags: list[str] = Field(default_factory=list)


class PropertyDetail(PropertyCard):
    description: str
    amenities: list[str] = Field(default_factory=list)
