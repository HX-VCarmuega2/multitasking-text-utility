from dataclasses import dataclass
from openai import OpenAI


@dataclass
class ModerationResult:
    allowed: bool
    flagged: bool
    categories: list[str]
    max_score: float
    reason: str | None = None


class ModerationMiddleware:
    def __init__(
        self,
        client: OpenAI,
        threshold: float = 0.70,
    ):
        self.client = client
        self.threshold = threshold

    def check(self, text: str) -> ModerationResult:
        """
        Checks whether a text can continue through the application.
        """

        response = self.client.moderations.create(
            model="omni-moderation-latest",
            input=text,
        )

        moderation = response.results[0]

        category_scores = moderation.category_scores.model_dump()

        detected_categories = [
            category
            for category, score in category_scores.items()
            if score >= self.threshold
        ]

        max_score = max(category_scores.values(), default=0.0)

        allowed = len(detected_categories) == 0

        return ModerationResult(
            allowed=allowed,
            flagged=moderation.flagged,
            categories=detected_categories,
            max_score=max_score,
            reason=(
                None
                if allowed
                else "The content exceeded the moderation threshold."
            ),
        )