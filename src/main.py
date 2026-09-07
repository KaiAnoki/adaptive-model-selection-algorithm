from __future__ import annotations

import argparse
import json

from src.algorithm import AdaptiveModelSelector


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a request to a model profile.")
    parser.add_argument("query", help="Request to classify and route")
    args = parser.parse_args()
    result = AdaptiveModelSelector().route(args.query)
    print(json.dumps({
        "intent": result.intent,
        "model": result.model,
        "confidence": result.confidence,
        "model_scores": result.model_scores,
    }, indent=2))


if __name__ == "__main__":
    main()
