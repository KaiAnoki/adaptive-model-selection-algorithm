# Adaptive model selection algorithm

A small Python reference implementation for routing requests among model profiles. It classifies a request with token-based signals, scores available models for quality, speed, and cost efficiency, then returns the selected model with the complete score breakdown.

## What it demonstrates

- Deterministic intent classification without external services
- Configurable model profiles
- Weighted model selection with explainable scores
- Input validation and unit tests
- A command-line interface that returns JSON

## Run it

```bash
python -m src.main "Write a Python API for inventory updates"
```

## Test it

```bash
python -m pip install -e ".[dev]"
pytest -q
```

## Project layout

```text
src/algorithm.py        routing policy and data models
src/main.py             command-line entry point
tests/test_algorithm.py unit tests
```

This project intentionally uses a transparent rule-based policy. It does not claim to benchmark or call real language models.
