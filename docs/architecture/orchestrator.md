# Orchestrator

The orchestrator coordinates incoming requests, classifies task complexity, selects a model, and can run tools before producing a final answer.

## Deterministic first planner

The V0.1 planner is intentionally simple and deterministic. It classifies prompts by keywords and decides whether a calculation or research-oriented workflow is appropriate.

## Future extension

A higher-capability planner can replace the deterministic planner without reworking the API contract.
