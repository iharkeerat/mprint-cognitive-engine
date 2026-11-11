# Reproducibility and local setup

**Status:** source-derived instructions. The complete stack has **not been independently rebuilt or tested** in the current documentation pass.

## Source inventory
- `main.py`: FastAPI backend, session handling and generation endpoints.
- `mprint_engine.py`: independent heuristic computation module.
- `graph_query.py`: Neo4j graph traversal functions.
- `graph_loader.py` and `skills.json`: example graph data and loading script.
- `database.py`: SQLite schema utility; `main.py` also initialises a database on import.
- `index.html`: standalone browser frontend.
- `*_questions.json`: example local MCQ content.

## Prerequisites
A compatible Python environment, running Neo4j service, credentials, and (for live LLM question generation) a valid Gemini API key. External network and cloud-service usage may incur costs.

## Setup (local development only)
1. Create a Python virtual environment:
   - Linux/macOS: `python -m venv .venv && source .venv/bin/activate`
   - Windows PowerShell: `py -m venv .venv`; then activate the environment.
2. Install dependencies: `python -m pip install -r requirements.txt`.
   The present requirements file is an extensive pinned development snapshot, not a minimal verified dependency specification.
3. Copy `.env.example` to `.env`. Fill in `GEMINI_API_KEY`, `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`, and a randomly generated `SECRET_KEY`.
4. Start the Neo4j instance. Load the example graph: `python graph_loader.py`.
5. Start the API: `uvicorn main:app --reload`. Open `http://127.0.0.1:8000/docs`.
6. Serve `index.html` from a local static server and check the backend URL inside its JavaScript if necessary.

**Potential startup blockers:** the graph driver and GenAI client are initialised during module import. Missing service configuration can prevent startup before the question fallback executes. A successful setup must be confirmed rather than assumed.

## Inspect the scoring module without services
`python mprint_engine.py` runs the example at the bottom of the source using only Python standard-library imports. This is a demonstration, **not** a validated learner model or proof that the rest of the stack is healthy.

## What is not independently demonstrated here
No successful clean-install run, integration test, hosted deployment, CI benchmark, learner outcome study, security assessment or model calibration is claimed by this documentation.

## Privacy and operational safety
The source stores account/session records locally and includes development defaults unsuitable for hosting. Do not upload real learners' information or expose this application on a public server before independent privacy, security and access-control review. See [security notes](../SECURITY.md).

## Reporting checklist
When reproducing or extending the work, record the commit SHA, Python/platform versions, dependency resolution, service versions, configuration (without secrets), datasets and evaluation script. Report exact tests run, rather than inheriting test counts from a different project or offline experiment.
