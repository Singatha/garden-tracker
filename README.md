# Gardenwise

Gardenwise is a personal garden journal and planning application for keeping
track of what is growing, what needs attention, and what the garden produces.
It brings plantings, growing areas, care tasks, observations, and harvests into
one simple mobile-friendly workspace.

The project is designed for home and backyard gardeners. Its current focus is a
useful local experience and thoughtful garden workflows rather than production
infrastructure or commercial farm management.

## Features

- Account registration, sign-in, and editable profile settings
- Multiple gardens with beds, containers, rows, and greenhouse areas
- Planting records with crop, variety, quantity, method, and lifecycle status
- A focused Today view for overdue and upcoming work
- Garden tasks that can be created and completed
- An activity journal for watering, feeding, pruning, pests, and notes
- Harvest records with dates, quantities, and original measurement units
- Garden-level access isolation
- Responsive navigation with dedicated application routes

## Screens

| Route | Purpose |
| --- | --- |
| `/today` | Current tasks, active plantings, and upcoming harvests |
| `/garden` | Growing areas, planting filters, and lifecycle management |
| `/journal` | Chronological garden activity and observations |
| `/harvests` | Harvest history and quantities |
| `/settings` | Profile information and sign-out |

## Technology

### Backend

- Python 3.12
- FastAPI and Pydantic
- SQLAlchemy 2 with async sessions
- PostgreSQL
- JWT authentication
- pytest and Ruff

### Frontend

- Nuxt 4 and Vue 3
- TypeScript
- shadcn-vue
- Tailwind CSS 4
- Reka UI and Lucide icons

## Run with Docker

Copy the example environment and start the complete stack:

```bash
cp .env.example .env
docker compose up --build
```

Open:

- Gardenwise: [http://localhost:3000](http://localhost:3000)
- OpenAPI documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

PostgreSQL data is stored in the `garden_data` Docker volume. Stop the
application with:

```bash
docker compose down
```

## Local development

### Backend

Python 3.12 or newer is required.

```bash
cd backend
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
DATABASE_URL=sqlite+aiosqlite:///./garden.db .venv/bin/uvicorn app.main:app --reload
```

Run backend checks:

```bash
.venv/bin/pytest
.venv/bin/ruff check .
.venv/bin/ruff format --check .
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Run frontend checks:

```bash
npm run typecheck
npm run build
```

Set `NUXT_PUBLIC_API_BASE` when the API is not available at
`http://localhost:8000/api/v1`.

## Project structure

```text
backend/
  app/
    api/routes/       FastAPI route modules
    models.py         SQLAlchemy domain models
    schemas.py        API request and response schemas
  tests/              API workflow and isolation tests
frontend/
  app/
    components/       Feature and shadcn-vue components
    composables/      Session and API access
    pages/            Nuxt routes
docs/
  design-checklist.md
  roadmap.md
```

## Product direction

Gardenwise is an evolving personal project. Potential next features include
seed inventory, seasonal planting plans, garden photos, recurring tasks,
weather-aware reminders, and harvest summaries.

See [the roadmap](docs/roadmap.md) for the current feature ideas and
[the design checklist](docs/design-checklist.md) for interface quality
standards.

## Contributing

Small improvements and experiments are welcome. Keep garden-owned queries
scoped through an authenticated membership, preserve historical activities as
append-only records, and run the relevant backend and frontend checks before
committing.

