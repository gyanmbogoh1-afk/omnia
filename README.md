# OMNIA

OMNIA is a modular research and general-purpose intelligence system intended to become a general-purpose research and problem-solving platform.

This repository contains the V0.1 foundation: configuration, database schema, backend API, model provider abstraction, orchestrator, memory persistence, tool system, agents, observability, tests, Docker setup, and documentation.

## Quick start

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Start the local stack:
   ```bash
   docker compose up --build
   ```
3. Open the app:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000/docs
   - PostgreSQL: localhost:5432

## Repository layout

- `apps/web` - Next.js frontend
- `services/api` - FastAPI backend
- `services/orchestrator` - planning and task execution
- `services/models` - provider interfaces and registry
- `services/memory` - working/episodic/semantic/procedural/project memory
- `services/tools` - calculator, sandbox, filesystem and validation
- `services/knowledge` - document and retriever skeleton
- `services/agents` - agent abstraction and initial agents
- `database/migrations` - database schemas
- `tests` - unit and integration tests
- `docs` - design and operations docs

## Core principles

- No fake functionality: all major subsystems have interfaces
- No arbitrary host execution: Python execution is sandboxed
- Secrets stay server-side and are read from environment variables only
- Observability is built in: activity events and structured logs are first-class
- No monolithic implementation: features are isolated modules

## Local development

### Python backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn services.api.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd apps/web
npm install
npm run dev
```

### Tests

```bash
pytest -q
```

## Environment variables

See `.env.example` for the required values.

## Architecture summary

User -> API Gateway -> Orchestrator -> Model Router -> Model Provider -> Tool System -> Memory System -> Response Synthesizer

## What is implemented in V0.1

- backend service skeleton
- model provider abstraction with a working in-memory provider
- orchestrator with deterministic planning
- activity logging
- memory service and persistence abstraction
- calculator tool and sandbox abstraction
- agent abstraction with General, Research, Coding, Math, Critic agents
- basic API endpoints and chat route
- Next.js frontend skeleton
- Docker Compose local environment
- docs and tests

## Known limitations

- the project is intentionally a production-grade foundation rather than a fully autonomous research platform
- remote model providers are configured via abstraction, but the concrete provider must be configured in `.env`
- semantic embeddings are prepared but not fully deployed without a configured embedding backend
- sandbox execution is isolated in the design and can be backed by Docker in production

## Next recommended step

Implement the complete SQLAlchemy database schema and provider-specific adapters, then connect the frontend to the APIs and enable end-to-end streaming responses.
