
from src.algorithm import AdaptiveModelSelector

def test_classify():
    s = AdaptiveModelSelector()
    assert s.classify("write python code") == "coding"
    assert s.classify("why is this happening") == "reasoning"
    assert s.classify("hello") == "general"
