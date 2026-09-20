# AGENTS.md

## Repository purpose

This repository contains personal implementations and runnable examples based on
Harvard CS50's Introduction to Artificial Intelligence with Python. The code is
organized by lecture and is intended for learning, comparison, and revision.

## Repository layout

- `lec0_search/`: state-space search and adversarial search.
- `lec2_uncertainty/`: probabilistic models and Viterbi decoding.
- `lec3_optimization/`: local search and constraint satisfaction.
- `lec5_neural_networks/`: TensorFlow/Keras neural-network examples.
- `cs50_ai.py`: convenient public imports for the lecture algorithms.

Each meaningful source directory owns a `README.md`. Lecture-level README files
provide a map of the topic; nested README files explain the concrete algorithms
and code in that directory.

Do not add a repository-root `README.md` until all lecture code has been
organized. When a new lecture or algorithm directory is added, add or update its
local README in the same change.

## Working conventions

- Preserve the lecture-based directory layout and existing public function names
  unless a task explicitly calls for an API change.
- Prefer small, readable teaching implementations over framework-heavy
  abstractions.
- Keep comments and README prose in Chinese; retain standard English algorithm
  names on first mention.
- Describe the code that actually exists. If an implementation is incomplete or
  intentionally simplified, document the limitation rather than implying
  production readiness.
- Do not silently replace handwritten implementations with library calls.
- Do not commit course datasets, trained models, virtual environments, IDE
  metadata, caches, or generated reports unless a task explicitly requires a
  small fixture.

## Python and dependencies

- Target Python 3.10 or newer.
- The handwritten search, probability, and optimization examples should remain
  standard-library-only unless numerical work genuinely requires NumPy.
- Neural-network examples may use NumPy, scikit-learn, and TensorFlow/Keras.
  Keep heavyweight imports inside the runnable entry point when practical so
  helper functions can still be inspected without those packages installed.
- Use `pathlib.Path` for filesystem paths in new code.
- Add deterministic seeds to randomized demonstrations when reproducibility is
  useful.

## Validation

For documentation-only changes, verify that every documented filename and
command exists and that no root README was created prematurely.

For Python changes:

1. Parse or compile every changed Python file.
2. Run the smallest relevant example or focused test.
3. For randomized algorithms, validate invariants rather than one exact output.
4. For neural-network examples, use reduced epochs or data limits for smoke tests;
   do not download large datasets merely to validate unrelated changes.

Before finishing, inspect `git diff` and keep unrelated user changes untouched.
