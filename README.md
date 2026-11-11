# M-Print: Adaptive Assessment and Learning-Path Prototype

**Research-oriented software prototype · Python / FastAPI · Neo4j · SQLite · browser UI**

M-Print explores a practical question: **how can option-level responses and prerequisite relationships inform the next step of a learning assessment?** The repository contains an exploratory web application—not a validated model of a learner's cognitive state.

> **Status:** research/engineering prototype. No participant study, diagnostic validity assessment, peer-reviewed publication, or deployment-safety certification is claimed.

## What is implemented

| Component | Repository evidence | Role |
| --- | --- | --- |
| Assessment API | [main.py](main.py) | Question requests, response submission, user/session endpoints and response-based routing |
| Scoring prototype | [mprint_engine.py](mprint_engine.py) | Weighted response-label distributions, entropy, heuristic adjustments and summary metrics |
| Prerequisite graph | [graph_query.py](graph_query.py), [graph_loader.py](graph_loader.py), [skills.json](skills.json) | Neo4j skill relationships and graph-based path queries |
| Persistence | [database.py](database.py), [main.py](main.py) | SQLite tables for users, sessions and submitted responses |
| Browser interface | [index.html](index.html) | Standalone HTML/JavaScript frontend using CDN-loaded visual components |
| Sample content | [\*_questions.json](ml_questions.json) | Local question banks used as a fallback |

The optional Google GenAI integration generates question content when configured. API failure is handled by a local-question fallback within the question endpoint; **the code has not been independently smoke-tested for zero-credential startup**.

## Architecture at a glance

\`\`\`text
Browser interface (index.html)
    |
    v
FastAPI (main.py)
    |-- optional AI question generation / local question banks
    |-- assessment responses and accuracy-based routing
    |-- SQLite: users / sessions / responses
    |-- Neo4j: prerequisite graph and learning-path queries
    |
    +-- independent heuristic scoring experiment (mprint_engine.py)
\`\`\`

**Terminology matters.** Labels such as *Activist*, *Reflector*, *Theorist* and *Pragmatist* are **developer-assigned response categories**, not independently established learning styles, cognitive profiles or psychological diagnoses. The source's "confidence" metric is a margin between normalized label scores, **not a statistically calibrated probability**. Correctness and time are observable interface measurements; psychological interpretation remains unvalidated.

## Local exploration

The Python environment and external services must be configured before starting the current API:

1. Clone this repository and create a Python virtual environment.
2. Install the provided [requirements.txt](requirements.txt) (a development-environment snapshot, not a tested minimal dependency lock).
3. Create a local \`.env\` using [the example](.env.example) and set **your own** Gemini API key and Neo4j connection credentials. Never commit credentials.
4. Run a compatible local Neo4j instance and populate its graph using \`python graph_loader.py\`.
5. Start the API with \`uvicorn main:app --reload\`, then open \`http://127.0.0.1:8000/docs\` to inspect its FastAPI endpoints.
6. Serve [index.html](index.html) locally and configure its API origin if necessary.

**These are source-derived setup instructions, not a claim that a clean installation or frontend integration was verified on 11 November 2026.** See [Reproducibility and setup notes](docs/REPRODUCIBILITY.md) for prerequisites, checks and troubleshooting.

## Research boundaries

This repository combines **software exploration** with early-stage assessment questions. It does **not** demonstrate that time taken reveals a learning style, that category scores measure cognition, or that generated questions are psychometrically valid. It contains no verified learner-effectiveness study.

A separate research track on sparse adaptive-assessment identifiability studies a restricted synthetic latent-variable model. That work should not be conflated with the currently public application code; its analyses and test evidence are not included in this checkout.

Read the [research scope and limitations](docs/RESEARCH_SCOPE.md) and [security/deployment caveats](SECURITY.md) before citing or deploying the project.

## Reuse and evaluation

This repository is suitable for **code inspection, further experiments and academic discussion**, not real educational diagnosis or consequential student decisions. Researchers can independently review the API, scoring logic and graph queries, and design new empirical tests. A production service would require authentication/authorization, data protection, model validity, service reliability and security review.

**Project links:** [Research scope](docs/RESEARCH_SCOPE.md) · [Reproducibility](docs/REPRODUCIBILITY.md) · [Portfolio facts](docs/PORTFOLIO_SUMMARY.md)

## License

[Apache License 2.0](LICENSE). Third-party libraries, APIs and sample content remain subject to their own terms.

**Authorship and attribution:** repository history documents code changes; if AI assisted implementation or writing, individual contributions should be represented accurately in CVs and applications. No claims of peer review or original cognitive science theory are implied by this README.
