from __future__ import annotations

from ..schemas.property import PropertyCard, PropertyDetail
from ..schemas.search import SearchRequest, SearchResponse


class PropertyService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_properties(self) -> list[PropertyCard]:
        details = self.repository.list_properties()
        return [self._to_card(item) for item in details]

    def get_property(self, property_id: int) -> PropertyDetail | None:
        return self.repository.get_property_by_id(property_id)

    def search(self, request: SearchRequest) -> SearchResponse:
        filtered = self._filter_properties(self.repository.list_properties(), request)
        ranked = self._rank_properties(filtered, request)
        limited = ranked[: request.limit]
        cards = [self._to_card(item) for item in limited]

        summary = self._build_summary(cards, request)
        suggestions = self._build_suggestions(cards, request)

        return SearchResponse(summary=summary, property_cards=cards, suggestions=suggestions)

    def _filter_properties(self, properties: list[PropertyDetail], request: SearchRequest) -> list[PropertyDetail]:
        filtered = properties

        if request.min_price is not None:
            filtered = [item for item in filtered if item.price >= request.min_price]
        if request.max_price is not None:
            filtered = [item for item in filtered if item.price <= request.max_price]
        if request.bedrooms is not None:
            filtered = [item for item in filtered if item.bedrooms >= request.bedrooms]
        if request.location:
            query_location = request.location.lower()
            filtered = [item for item in filtered if query_location in item.location.lower()]
        if request.query:
            query = request.query.lower()
            filtered = [
                item
                for item in filtered
                if query in item.title.lower() or query in item.description.lower() or any(query in tag.lower() for tag in item.tags)
            ]

        return filtered

    def _rank_properties(self, properties: list[PropertyDetail], request: SearchRequest) -> list[PropertyDetail]:
        query = (request.query or "").lower()

        def score(item: PropertyDetail) -> int:
            value_score = max(0, 1_000_000 - item.price) // 50_000
            size_score = item.square_feet // 300
            bedroom_score = item.bedrooms * 2
            relevance = 0
            if query:
                if query in item.title.lower():
                    relevance += 6
                if query in item.description.lower():
                    relevance += 4
                relevance += sum(2 for tag in item.tags if query in tag.lower())
            return value_score + size_score + bedroom_score + relevance

        return sorted(properties, key=score, reverse=True)

    def _build_summary(self, cards: list[PropertyCard], request: SearchRequest) -> str:
        if not cards:
            return "No properties match your current filters. Try widening your budget or reducing constraints."

        budget_bits = []
        if request.min_price is not None:
            budget_bits.append(f"from ${request.min_price:,}")
        if request.max_price is not None:
            budget_bits.append(f"up to ${request.max_price:,}")
        budget_text = f" with budget {' '.join(budget_bits)}" if budget_bits else ""
        return f"Found {len(cards)} matching properties{budget_text}. Top options balance value, size, and relevance."

    def _build_suggestions(self, cards: list[PropertyCard], request: SearchRequest) -> list[str]:
        suggestions: list[str] = []
        if request.location is None:
            suggestions.append("Add a preferred city to narrow results.")
        if request.bedrooms is None:
            suggestions.append("Set a minimum bedroom count for better fit.")
        if request.max_price is None:
            suggestions.append("Set a max budget to surface stronger value picks.")
        if cards:
            suggestions.append(f"Compare {cards[0].title} with another nearby option for trade-offs.")
        return suggestions[:3]

    def _to_card(self, item: PropertyDetail) -> PropertyCard:
        return PropertyCard(
            id=item.id,
            title=item.title,
            location=item.location,
            price=item.price,
            bedrooms=item.bedrooms,
            bathrooms=item.bathrooms,
            square_feet=item.square_feet,
            tags=item.tags,
        )
