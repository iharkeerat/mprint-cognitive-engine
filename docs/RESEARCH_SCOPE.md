# Research scope and evidence boundaries

## Question and motivation
M-Print is an exploration of **adaptive assessment and prerequisite-based routing**. It asks whether observable item responses can help select a useful next question or prerequisite topic. It is not intended as a clinical, psychological or high-stakes educational diagnostic.

## What the current repository supports

| Observed/code element | Supported statement | Unsupported extrapolation |
| --- | --- | --- |
| Option correctness and response time | The API can record response-level measurements | Timing proves a personality or learning style |
| Accuracy thresholds in `main.py` | Routing branches depend on measured accuracy | Those cutoffs are empirically optimal |
| Prerequisite graph queries | A graph can return paths based on declared edges | The returned path maximizes learning |
| Normalized label scores | A heuristic profile can be calculated from assigned labels | The score is a validated cognitive trait or calibrated confidence |
| Generated MCQs | A configured external LLM may produce questions | Every generated item is valid, unbiased and reliable |

The four style labels are legacy **response-category names** in the code. They should not be presented as a verified educational or psychological classification.

## Research questions worth testing
- Can a prerequisite-aware routing policy outperform a non-adaptive baseline under a pre-specified learning metric?
- How sensitive are inferred scores to item wording, response timing, missing data and unbalanced question exposure?
- What can a model *actually identify* when its next item depends on previous responses?
- Which evidence would be necessary before real student data were used?

These are research directions, not findings established by the current checkout.

## Separate work: sparse adaptive-assessment identifiability
A related offline research investigation examines exact identifiability in a **restricted synthetic multiple-choice latent-state model**, with assumptions about conditional independence, observed path support and response kernels. Its manuscript and experiment package are **not part of this public application repository**, so numerical theorems and test results from that work should not be attributed to this codebase.

## Evidence status
- Existing backend, graph-query, UI and scoring code are inspectable.
- No independently replicated clean-install demonstration or current CI result is supplied by this branch.
- No human-subject learning-effectiveness data or prospective psychometric evaluation is supplied.
- Generated questions, path heuristics and scores must not be used for consequential learner decisions.

## Suggested reproducible next study
Freeze an item bank and sample; define a non-adaptive comparator; pre-register accuracy/learning outcomes and missingness rules; run a controlled evaluation with appropriate consent and data safeguards; report unsuccessful results as well as successful results.

For the implementation assumptions, see [reproducibility notes](REPRODUCIBILITY.md). For public presentation, see [portfolio summary](PORTFOLIO_SUMMARY.md).
