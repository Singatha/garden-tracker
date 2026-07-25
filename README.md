# Backyard Garden Tracker

A mobile-first garden journal and task tracker built with FastAPI, PostgreSQL,
Nuxt 4, Vue 3, and TypeScript.

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

Open the web app at http://localhost:3000 and API documentation at
http://localhost:8000/docs.

The same workflow is available as:

```bash
make up
```

## Local development

Backend:

```bash
cd backend
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
DATABASE_URL=sqlite+aiosqlite:///./garden.db .venv/bin/uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## MVP capabilities

- Register and sign in
- Create gardens and growing areas
- Track crop plantings and lifecycle status
- Append garden activity history
- Filter plantings and update their lifecycle
- Create, complete, and monitor due tasks
- Record harvest quantities
- View a focused Today dashboard

## Useful commands

```bash
make up         # run the app
make down       # stop it
make logs       # follow container logs
make test       # backend tests
make lint       # backend lint and format check
make typecheck  # frontend TypeScript check
make check      # run all checks and builds
```

This is intentionally a personal project. The current priorities are useful
garden features and a simple local workflow. See [docs/roadmap.md](docs/roadmap.md)
for feature ideas and current direction.
