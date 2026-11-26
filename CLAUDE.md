# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**legre** is a digital library ("Tu biblioteca digital") REST API built with FastAPI, SQLAlchemy 2.x (sync, `Mapped`/`mapped_column` style), Pydantic v2, and PostgreSQL 16 (via `psycopg` v3). Code, identifiers, and docs are in **Spanish** (`usuarios`, `crear_usuario`, `guardar_usuario`, …); follow that convention for new code.

The planned domain model is described in [docs/README.md](docs/README.md) and [docs/modelo_relacional.md](docs/modelo_relacional.md): `Usuario` is a superclass specialized into `Lector` and `Administrador` (shared PK `id_usuario`), plus `Libro`, `Autor`, and the junction tables `Autor_Libro` and `Lector_Libro`. Only `Usuario` is implemented so far.

## Commands

```bash
# Full stack (API on :8000 with ./app bind-mounted, Postgres on host port 5433)
cp .env.example .env   # set POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_DB
docker compose up --build

# Run the API locally against the compose DB (needs DATABASE_URL in .env)
#   DATABASE_URL=postgresql+psycopg://<user>:<pass>@localhost:5433/<db>
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Interactive API docs: http://localhost:8000/docs

There is no test suite, linter, or formatter configured yet.

## Architecture

All application code lives in `app/`. Each domain feature is a package (currently `app/usuarios/`) with a fixed layering:

- `models.py` — SQLAlchemy ORM model inheriting `app.infra.database.Base`.
- `schema.py` — Pydantic request/response models (`XCrear`, `XActualizar`, `XRespuesta` with `from_attributes=True`).
- `repository.py` — data access on an injected `Session`. Uses `add`/`flush`/`refresh`/`delete` but **never commits**.
- `service.py` — business logic; owns the **transaction boundary** (`session.commit()` on success, `rollback()` on exception). Receives both the repository and the same `Session`.
- `router.py` — `APIRouter` with a `get_service_dependency(session: DBSession)` factory that wires repo → service, exposed as an `Annotated[..., Depends(...)]` alias. Endpoints convert ORM objects with `XRespuesta.model_validate(...)`.

Shared plumbing:
- `app/core/config.py` — `pydantic-settings` `Settings`; only `DATABASE_URL`, read from env or the repo-root `.env`.
- `app/infra/database.py` — engine, `Base`, `sessionmaker`, and the `get_db_session` generator dependency.
- `app/common/dependencies.py` — `DBSession` annotated dependency.
- `app/common/models.py` — imports every ORM model so they are registered on `Base.metadata`. **Add new models here.**

When adding a feature: create the package with the layers above, import its model in `app/common/models.py`, and `include_router` it in `app/main.py`.

## Database schema / migrations

Tables are currently created at startup by `Base.metadata.create_all(bind=engine)` in `app/main.py` (create-only; it won't alter existing tables). Alembic is initialized but **not wired up**: `alembic/env.py` has `target_metadata = None`, `alembic.ini` still holds the placeholder `sqlalchemy.url`, and there is no `alembic/versions/` directory. Hooking it up requires pointing `target_metadata` at `app.infra.database.Base.metadata` (after importing `app.common.models`) and loading the URL from `app.core.config.settings`.

## Gotchas

- The top-level `common/` and `usuarios/` directories are stale leftovers from before the move into `app/` (they use absolute imports like `from usuarios.models ...` and are not imported anywhere). Edit code under `app/`, not these.
- The Dockerfile only copies `app/`; anything outside it isn't in the image.
- `.venv_libri/` is committed to git; `.venv_legre/` is the git-ignored local venv.
- Passwords are stored and returned in plain text (`schema.py` marks this `#temporal`).
- `UsuarioRepositorio.cargar_usuario` raises `ValueError` for missing ids and there's no exception handler mapping it to 404, so unknown ids currently yield a 500.

## Answer Style
- Always prioritize a teaching style. Instead of just giving me the code, explain from first principles and use examples.
- Make questions to confirm im understanding, you can even challenge me to do stuff alongisde you to test me, or to make changes to something you made, etc, use real, pedagogical methods for making me a better software engineer.

## Workflow
You will follow this unless instructed otherwise
- Im using github for this project. So, when dicussing a new feature, you will speak in terms of the  current working branch, and will try and synthesize in issue format your suggestions for work. Follow the basic following issue structure: Conext, Tasks, Definition of done. And write them in spanish. 
- Do not make an issue for every answer, only if i ask for it
