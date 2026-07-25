# Repository Guidelines

## Project Structure

- `backend/`: FastAPI, SQLAlchemy 2, and Pydantic API.
- `backend/app/api/routes/`: HTTP routes grouped by garden capability.
- `backend/app/models.py`: SQLAlchemy domain models and enums.
- `backend/app/schemas.py`: request and response schemas.
- `backend/tests/`: pytest API workflow and isolation tests.
- `frontend/`: Nuxt 4, Vue 3, and TypeScript application.
- `frontend/app/components/`: reusable interface components.
- `frontend/app/composables/`: API and session helpers.
- `frontend/app/pages/`: application pages.
- `docs/roadmap.md`: feature ideas and current personal-project priorities.
- `docker-compose.yml`: local PostgreSQL, API, and web stack.

## Development Commands

Run the complete application from the repository root:

```bash
cp .env.example .env
docker compose up --build
```

The web app is available at `http://localhost:3000` and API documentation at
`http://localhost:8000/docs`.

Run backend commands from `backend/`:

```bash
.venv/bin/pytest
.venv/bin/ruff check .
.venv/bin/ruff format --check .
```

Run frontend commands from `frontend/`:

```bash
npm install
npm run dev
npm run typecheck
npm run build
```

## Architecture and Domain Rules

Keep the backend as a modular monolith. HTTP parsing and responses belong in
route modules. Put reusable business workflows in service modules when they
grow beyond a straightforward CRUD operation.

Every garden-owned query must be scoped through an authenticated, active garden
membership. Never accept a garden, growing area, or planting relationship
without verifying that both records belong to the same accessible garden.

Garden activities are append-only history. Planting lifecycle status is
separate from tasks and observations. Preserve the original unit on every
harvest record.

The project currently creates tables automatically for simple local
development. Introduce migrations before making incompatible schema changes or
sharing persistent databases across environments.

## Code Style

Use Python 3.12, four-space indentation, type hints, and async SQLAlchemy
sessions. Keep Pydantic schemas separate from persistence models. Format and
lint Python with Ruff.

Vue components use TypeScript, `<script setup>`, and `PascalCase` filenames.
Keep server data access in API composables. Design mobile-first and retain
accessible labels, keyboard behavior, readable errors, and useful empty states.
Use the code-owned shadcn-vue components in `frontend/app/components/ui/` for
interactive primitives instead of introducing parallel component patterns.
Review UI work against `docs/design-checklist.md`.

Prefer small, direct changes. This is a personal garden project, so prioritize
features that improve everyday use over production infrastructure, premature
abstractions, or operational complexity.

## Testing

Name Python tests `test_*.py`. Add coverage for:

- authentication and validation outcomes;
- cross-account garden isolation;
- parent-child ownership constraints;
- planting lifecycle changes;
- activity, task, and harvest workflows.

Run backend tests and linting plus frontend type checking and building before
finishing a feature. Do not commit `.env`, virtual environments, databases,
`node_modules`, caches, or build output.

## Git Practices

Use concise imperative commit subjects. Keep commits focused on one coherent
feature or cleanup. Update `README.md` or `docs/roadmap.md` when commands,
capabilities, or priorities materially change.
