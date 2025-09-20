# ALX Task Manager — Capstone Project (Django + AI-native IDE)

## 🔖 Project Title & Description

**Project Title:** Task Manager — Smart Productivity for Developers

**Short Description:**
A modern, secure Task Manager built with Django and Django REST Framework that helps individual developers and small teams track, prioritize, and schedule work. The app includes AI-powered natural-language task creation, smart prioritization, and automated reminders — all developed inside an AI-native IDE (e.g., Trae) to demonstrate an AI-assisted development workflow.

**Who it’s for:**

* Individual developers who want a lightweight, developer-focused task tracker.
* Small teams who need a simple collaborative task board with intelligent suggestions.

**Why it matters:**

* Demonstrates backend engineering fundamentals (REST APIs, auth, background jobs) while integrating AI features that improve UX and developer productivity.
* Serves as a showcase of building production-ready Django apps using AI-native tooling for code generation, testing, and documentation — a perfect capstone for “AI for Developers.”

---

## Tech Stack

**Backend**

* Python 3.11+ (or 3.10+)
* Django 4.x
* Django REST Framework

**Database**

* PostgreSQL (primary)
* Redis (cache + Celery broker)

**Background jobs / async**

* Celery (or Django Q / Dramatiq as alternative)

**Auth & Security**

* djangorestframework-simplejwt (JWT) or Django session auth for web UI
* django-cors-headers for API CORS handling

**AI & Integration**

* Trae (AI-native IDE) for in-IDE code generation and iteration
* OpenAI / Anthropic / local LLM via API for NLP parsing & code assistance

**Dev / Infra**

* Docker + docker-compose (Postgres + Redis + Celery) for local dev
* GitHub repository + GitHub Actions for CI
* Deployment: Railway / Fly.io / Render / Heroku (container-ready)

**Testing**

* pytest + pytest-django
* DRF test client / requests for integration tests

**Optional Frontend**

* Minimal Django templates (MVP) or React (Vite) for richer UI

---

## Core Features (MVP)

* User registration & authentication
* Task CRUD (title, description, due\_date, priority, status)
* Projects/Lists & tags
* Filters: status, priority, due soon
* Pagination & search
* Reminders via background jobs (email/push)
* Natural-language quick-add (AI parser)

**Stretch (post-MVP)**

* Kanban board (drag & drop)
* Collaboration & shared projects
* Smart scheduling suggestions (calendar integration)
* Task subtasks and comments

---

## Data Models (high-level)

* `User` (Django default or custom)
* `Project` — owner, name, description
* `Task` — title, description, owner, project (optional), due\_date, priority, status, is\_recurring
* `Subtask` (optional) — parent Task reference

---

## AI Integration Strategy

This project purposely uses an **AI-native IDE** (Trae) plus external LLMs to accelerate development and demonstrate context-aware AI workflows. Below are the concrete areas and how AI will be used.

### 1) Code generation

**Goals:** scaffold features, speed up boilerplate, and produce tested code patterns.

**How:**

* Use Trae to auto-generate model/serializer/view scaffolds from short prompts.
* Example prompt for Trae (scaffold):

  * `"Create a Django app `tasks` with models: Task (title, description, due_date, priority, status). Add serializers, viewsets (ModelViewSet) with JWT auth, and router registration. Include README usage examples."`
* Use Trae to generate Dockerfile, docker-compose, and Celery config from prompts.
* For sensitive/complex code (auth, payments, security): ask the IDE to provide an explanation + unit tests.

**Safety & QA:** Always review generated code, run linters (flake8, ruff) and static analyzers (bandit) before merging.

---

### 2) Testing (unit & integration)

**Goals:** high test coverage for core business logic and API endpoints.

**How:**

* Use prompts to ask Trae/LLM to produce `pytest` test files for models, serializers, and viewsets.
* Example testing prompt:

  * `"Write pytest tests for Task model: verify default priority, status transitions, and serialization. Include factory fixtures and database rollback."`
* For integration tests: request scenarios that simulate user flows (signup → create task → set reminder → complete task).
* Use the AI to generate property-based tests or fuzz inputs for edge cases.

**Verification:** AI writes tests, developer runs them locally/CI and reviews failures; iterate until green.

---

### 3) Documentation

**Goals:** maintain clear docstrings, inline comments, and keep README updated automatically.

**How:**

* Use Trae to generate and update docstrings for functions and classes based on code context. Prompt examples:

  * `"Generate a concise docstring for this TaskViewSet explaining endpoints and permission model."`
* Use AI to auto-generate README sections from code (e.g., `API Endpoints` list) and to keep changelogs.
* Use docstring templates in prompts to enforce standard format (Args / Returns / Raises / Examples).

**Output:** store generated docs in `docs/` and add a GitHub Action that runs a doc-snippet generator on PR.

---

### 4) Context-aware techniques (feeding context into AI)

**Goals:** make AI suggestions accurate by providing relevant project context.

**How:**

* Feed the AI the project `file tree` when asking it to modify or extend code (so it knows where to place files).
* Provide `API spec` (OpenAPI/Swagger) JSON or `urls.py` outputs when asking the AI to write client code.
* When requesting bug fixes or refactors, pass `git diff` or file contents as part of the prompt so the AI can reason about the change in-situ.
* In Trae, use the IDE's code context window + selection to limit AI's scope.

**Practical examples:**

* Prompt: `"Given this file tree: apps/tasks/models.py, apps/tasks/serializers.py, apps/users/models.py — add a Task serializer field `owner\_email` that is read-only and include tests. Here are the current file contents: <paste>"`
* Prompt for migration-aware changes: include `migrations/` list and model changes so AI can propose migration steps.

---

## Development Plan & Milestones

1. **Week 1 — Project scaffold (MVP foundation)**

   * Create GitHub repo, README (this file), and initial Django project + `tasks` app.
   * Implement User auth and Task model + migrations.
   * Add DRF, router, and ModelViewSet for Task (basic CRUD).

2. **Week 2 — Features & tests**

   * Add Project model, filters, pagination.
   * Add pytest unit tests for models/serializers.
   * Containerize app (Docker + docker-compose with Postgres + Redis).

3. **Week 3 — Background jobs & reminders**

   * Configure Celery + Redis, create reminder tasks.
   * Add simple email or console reminders.
   * Add integration tests for reminder flow.

4. **Week 4 — AI features**

   * Implement text parsing endpoint `/tasks/parse-create/` with LLM integration.
   * Add UI quick-add (or API client example).
   * Add smart-priority suggestion endpoint.

5. **Week 5 — Polish & Deploy**

   * Write CI pipeline, run tests on GitHub Actions.
   * Harden security (CORS, rate-limiting, input sanitization).
   * Deploy to a staging environment (Railway / Fly.io).

6. **Buffer & Presentation**

   * Prepare demo, slides, and short screencast of features + Trae workflow.

---

## CI / CD & Repo Workflow

* **Branches:** `main` (protected), `develop`, feature branches `feat/<name>`
* **PR checks:** linting (ruff/flake8), type checks (mypy), test suite (pytest)
* **GitHub Actions:** run on PRs and merges; job matrix for Python versions.

---

## Local Setup (dev) — commands

```bash
# clone
git clone git@github.com:<your-username>/task-manager.git
cd task-manager

# create virtualenv
python -m venv venv
source venv/bin/activate

# install
pip install -r requirements.txt

# environment
cp .env.example .env  # set DB urls, SECRET_KEY etc

# docker-compose (postgres + redis)
docker-compose up -d

# migrate & run
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**To push README to GitHub root**

```bash
git init
git add README.md
git commit -m "chore: add project README and plan"
git branch -M main
git remote add origin git@github.com:<your-username>/task-manager.git
git push -u origin main
```

---

## Acceptance Checklist (for task 1)

* [ ] Public GitHub repository exists and is named `task-manager` (or your preferred project name)
* [ ] `README.md` is in the repo root and contains this detailed project plan
* [ ] Repo is public and accessible via `https://github.com/<your-username>/task-manager`

---

## Notes & Resources

* OpenAI / Anthropic API docs (for LLM calls and prompt design)
* Django & DRF official docs
* Trae docs for in-IDE workflows and prompt patterns
* Celery docs for background tasks

---

## Next steps I can help with right now

* Generate the initial Django app files (`models.py`, `serializers.py`, `views.py`, `urls.py`) ready to drop into `apps/tasks/`.
* Create a `docker-compose.yml` for Postgres + Redis + Celery + web.
* Write the Trae prompt templates for scaffolding, tests, and docstrings.

Tell me which file you want first and I’ll generate it.
