import pytest

from src.algorithm import AdaptiveModelSelector, ModelProfile


@pytest.fixture
def selector() -> AdaptiveModelSelector:
    return AdaptiveModelSelector()


@pytest.mark.parametrize(("query", "intent"), [
    ("Write a Python API", "coding"),
    ("Why did this design fail?", "reasoning"),
    ("Hello, how is the weather?", "reasoning"),
    ("Hello there", "general"),
])
def test_classify(selector: AdaptiveModelSelector, query: str, intent: str) -> None:
    assert selector.classify(query) == intent


def test_keyword_matching_uses_tokens(selector: AdaptiveModelSelector) -> None:
    assert selector.classify("capital cities") == "general"


def test_route_selects_code_specialist(selector: AdaptiveModelSelector) -> None:
    result = selector.route("Debug this Java function")
    assert result.intent == "coding"
    assert result.model == "code-specialist"
    assert 0.0 < result.confidence <= 1.0
    assert set(result.model_scores) == {"fast-general", "code-specialist", "reasoning-specialist"}


def test_empty_query_is_rejected(selector: AdaptiveModelSelector) -> None:
    with pytest.raises(ValueError, match="query must contain text"):
        selector.route("   ")


def test_invalid_profile_score_is_rejected() -> None:
    with pytest.raises(ValueError, match="quality"):
        ModelProfile("bad", frozenset({"general"}), quality=2.0, speed=0.5, cost_efficiency=0.5)
