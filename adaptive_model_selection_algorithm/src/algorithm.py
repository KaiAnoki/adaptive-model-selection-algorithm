
class AdaptiveModelSelector:
    def __init__(self):
        self.models = ["general", "coding", "reasoning"]

    def classify(self, query: str) -> str:
        q = query.lower()
        if any(k in q for k in ["code", "python", "algorithm"]):
            return "coding"
        elif any(k in q for k in ["why", "explain", "reason"]):
            return "reasoning"
        return "general"

    def select_model(self, intent: str) -> str:
        # Internal selection logic abstracted
        return intent if intent in self.models else "general"
