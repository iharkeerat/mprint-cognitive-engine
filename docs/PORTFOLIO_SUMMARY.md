# M-Print — portfolio fact sheet

**Type:** Research-oriented software prototype  
**Areas:** Adaptive assessment · Educational technology · Python/FastAPI · Prerequisite graphs · Data interpretation

## Verified from repository inspection
- Implemented source code for FastAPI assessment endpoints, a SQLite-backed session model and Neo4j prerequisite queries.
- A heuristic response-scoring module computes label distributions and summary statistics.
- An HTML/JavaScript interface and sample question banks are included.
- Model and learner-outcome validity are **not established**.

## Short public description
> M-Print is an exploratory adaptive-assessment prototype combining response logging, accuracy-based routing, prerequisite graphs and optional generated MCQs. The repository documents implemented functionality and limitations; it does not claim validated cognitive diagnosis or measured improvements in student learning.

## CV description — customize only after verifying your personal contributions
> **M-Print — Adaptive Assessment Prototype** | Python, FastAPI, Neo4j, SQLite  
> Worked on [specific module you personally built or reviewed], investigating [specific research question you can explain]. The public repository documents an experimental question-routing system and its limitations.

Replace bracketed text with **your own verified work**. Do not claim you independently wrote components created mainly with AI assistance, tested the full stack when you did not, conducted human studies, or published peer-reviewed results.

## Research limitations to disclose
The current code uses developer-defined heuristic categories, not calibrated cognitive traits. The complete integrated system has not been independently tested in this documentation pass. Related offline mathematical research on sparse assessment paths lives outside this repository and must be cited separately if used.

**Repository:** https://github.com/iharkeerat/mprint-cognitive-engine  
**Setup:** [docs/REPRODUCIBILITY.md](REPRODUCIBILITY.md)  
**Scope:** [docs/RESEARCH_SCOPE.md](RESEARCH_SCOPE.md)
