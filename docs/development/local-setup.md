# Local setup

1. Install Python dependencies.
2. Copy `.env.example` to `.env`.
3. Install frontend dependencies.
4. Start PostgreSQL with Docker.
5. Launch the API and web frontend.

Example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm --prefix apps/web install
docker compose up postgres
uvicorn services.api.app.main:app --reload --host 0.0.0.0 --port 8000
npm --prefix apps/web run dev
```
