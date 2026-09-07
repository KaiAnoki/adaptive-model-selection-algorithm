from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


TOKEN_RE = re.compile(r"[a-z0-9_+#.-]+")


@dataclass(frozen=True, slots=True)
class ModelProfile:
    """A model option and the traits used by the routing policy."""

    name: str
    intents: frozenset[str]
    quality: float
    speed: float
    cost_efficiency: float

    def __post_init__(self) -> None:
        for field_name in ("quality", "speed", "cost_efficiency"):
            value = getattr(self, field_name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field_name} must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class Selection:
    intent: str
    model: str
    confidence: float
    model_scores: dict[str, float]


DEFAULT_MODELS = (
    ModelProfile("fast-general", frozenset({"general"}), quality=0.70, speed=0.95, cost_efficiency=0.95),
    ModelProfile("code-specialist", frozenset({"coding"}), quality=0.92, speed=0.70, cost_efficiency=0.65),
    ModelProfile("reasoning-specialist", frozenset({"reasoning"}), quality=0.95, speed=0.55, cost_efficiency=0.50),
)

INTENT_SIGNALS = {
    "coding": {"api", "bug", "c++", "code", "debug", "function", "java", "javascript", "python", "sql"},
    "reasoning": {"analyze", "compare", "explain", "how", "plan", "reason", "tradeoff", "why"},
}


class AdaptiveModelSelector:
    """Select a model with a small, deterministic scoring policy."""

    def __init__(self, models: Iterable[ModelProfile] = DEFAULT_MODELS) -> None:
        self.models = tuple(models)
        if not self.models:
            raise ValueError("at least one model profile is required")

    def classify(self, query: str) -> str:
        tokens = self._tokens(query)
        scores = {intent: len(tokens & signals) for intent, signals in INTENT_SIGNALS.items()}
        best_intent, best_score = max(scores.items(), key=lambda item: (item[1], item[0] == "coding"))
        return best_intent if best_score else "general"

    def select_model(self, intent: str) -> str:
        return max(self._score_models(intent).items(), key=lambda item: item[1])[0]

    def route(self, query: str) -> Selection:
        intent = self.classify(query)
        scores = self._score_models(intent)
        model, top_score = max(scores.items(), key=lambda item: item[1])
        total = sum(scores.values()) or 1.0
        return Selection(
            intent=intent,
            model=model,
            confidence=round(top_score / total, 3),
            model_scores={name: round(score, 3) for name, score in scores.items()},
        )

    @staticmethod
    def _tokens(query: str) -> set[str]:
        if not query or not query.strip():
            raise ValueError("query must contain text")
        return set(TOKEN_RE.findall(query.lower()))

    def _score_models(self, intent: str) -> dict[str, float]:
        normalized = intent if intent in {"general", "coding", "reasoning"} else "general"
        return {
            model.name: (
                (0.60 if normalized in model.intents else 0.0)
                + (0.25 * model.quality)
                + (0.10 * model.speed)
                + (0.05 * model.cost_efficiency)
            )
            for model in self.models
        }
