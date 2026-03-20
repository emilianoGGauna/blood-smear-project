from ..schemas.ai import AIChatRequest, AIChatResponse
from ..schemas.property import PropertyCard
from ..services.property_service import PropertyService


class AIChatService:
    def __init__(self, property_service: PropertyService) -> None:
        self.property_service = property_service

    def chat(self, request: AIChatRequest) -> AIChatResponse:
        cards = self._resolve_context_cards(request.context_property_ids)
        summary = self._build_summary(request.message, cards)
        suggestions = self._build_suggestions(cards)
        answer = self._build_answer(request.message, cards, suggestions)

        return AIChatResponse(
            summary=summary,
            property_cards=cards,
            suggestions=suggestions,
            answer=answer,
        )

    def _resolve_context_cards(self, property_ids: list[int]) -> list[PropertyCard]:
        cards: list[PropertyCard] = []
        for property_id in property_ids[:3]:
            detail = self.property_service.get_property(property_id)
            if detail:
                cards.append(
                    PropertyCard(
                        id=detail.id,
                        title=detail.title,
                        location=detail.location,
                        price=detail.price,
                        bedrooms=detail.bedrooms,
                        bathrooms=detail.bathrooms,
                        square_feet=detail.square_feet,
                        tags=detail.tags,
                    )
                )
        return cards

    def _build_summary(self, message: str, cards: list[PropertyCard]) -> str:
        if cards:
            return f"Responding to: '{message}'. Included {len(cards)} referenced properties for context."
        return f"Responding to: '{message}'. No property context was provided."

    def _build_suggestions(self, cards: list[PropertyCard]) -> list[str]:
        if not cards:
            return [
                "Share preferred city and budget for personalized recommendations.",
                "Ask for trade-offs between price and square footage.",
            ]
        return [
            "Ask for a side-by-side mortgage estimate.",
            f"Request neighborhood pros/cons for {cards[0].location}.",
            "Ask which option has the best value per square foot.",
        ]

    def _build_answer(self, message: str, cards: list[PropertyCard], suggestions: list[str]) -> str:
        if not cards:
            return (
                "I can help refine your search. "
                f"You said: '{message}'. Start by sharing budget, location, and bedroom needs. "
                f"Try this next: {suggestions[0]}"
            )

        spotlight = ", ".join(f"{card.title} (${card.price:,})" for card in cards)
        return (
            f"Based on your question '{message}', I reviewed: {spotlight}. "
            "These listings are strong candidates; I can now compare commute, value, and amenities in more detail."
        )
