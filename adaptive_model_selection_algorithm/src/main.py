
from algorithm import AdaptiveModelSelector

selector = AdaptiveModelSelector()

while True:
    q = input("\nEnter query (or 'exit'): ")
    if q.lower() == "exit":
        break

    intent = selector.classify(q)
    model = selector.select_model(intent)

    print(f"Intent: {intent}")
    print(f"Selected Model: {model}")
