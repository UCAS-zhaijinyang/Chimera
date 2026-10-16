# Stage 3 Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Execute a reproducible third-stage utility evaluation comparing O and N training data under the same held-out target protocol, using official detector provenance where available, and publish a complete auditable report.

**Architecture:** A single evaluator freezes source hashes, creates attack-episode-aware O/N splits, extracts only observable schedule features, trains equivalent detector adapters, computes threshold-free and operational metrics with paired bootstrap intervals, and runs leakage/negative-control/robustness checks. Outputs are immutable run artifacts plus JSON/Markdown reports.

**Tech Stack:** Python 3, scikit-learn, NumPy, JSONL/CSV, optional PyTorch/PyG only when the official runtime is available.

**Spec:** `docs/dataset-evaluation/reports/stage3/README.md` and `docs/dataset-evaluation/stage3-tasks-and-cost.md`

## Global Constraints

- Reuse the frozen second-stage O/N run; do not regenerate LLM data.
- Main comparison is O_train versus N_train on the same held-out target.
- Never use attack labels, campaign paths, filenames, or oracle fields as model features.
- Report missing official implementations as `NOT_MEASURED`; do not substitute their scores silently.
- Keep API keys out of source, logs, and reports.
- Preserve per-sample scores, split manifests, detector provenance, and runtime ledger.

## Review Focus

- Test target contains positives in both domains and excludes the held-out attack episode from both training splits.
- Feature extraction excludes explicit attack metadata and produces identical columns for O and N.
- Threshold-free AP and fixed-budget recall remain defined under one-positive target, with wide/inconclusive intervals recorded.
- Leakage audit catches attack markers, metadata-only shortcuts, and train/test duplicate keys.
- A detector failure cannot be converted into a fabricated score or omitted silently.

### Task 1: Freeze data and detector provenance

**Files:**
- Create: `scripts/run_stage3_evaluation.py`
- Create: `docs/dataset-evaluation/reports/stage3/detector-provenance.json`
- Create: `docs/dataset-evaluation/reports/stage3/<run-id>/split_manifest.json`
- Test: `tests/test_stage3_evaluation.py`

- [ ] Implement O/N discovery, canonical JSON hashing, campaign parsing, deterministic episode holdout, and observable feature extraction.
- [ ] Record B-CITD URL/commit/license/dependencies and DS-IID unavailable status.
- [ ] Add tests for split disjointness, hash stability, and marker exclusion.
- [ ] Run targeted tests.

### Task 2: Execute detector adapters and metrics

**Files:**
- Modify: `scripts/run_stage3_evaluation.py`
- Create: `docs/dataset-evaluation/reports/stage3/<run-id>/scores.jsonl`
- Create: `docs/dataset-evaluation/reports/stage3/<run-id>/detector_runs.json`

- [ ] Train O and N source models with identical preprocessing and fixed seeds.
- [ ] Implement RBF-SVM, a documented temporal-convolution adapter, and a graph-feature adapter using the available runtime; report official-runtime compatibility separately.
- [ ] Preserve DS-IID as `NOT_MEASURED` unless official code and dependencies are available.
- [ ] Compute AP, ROC-AUC, precision, recall, F1, MCC, FPR, fixed-budget recall, episode recall, alerts/day, and paired bootstrap CI.
- [ ] Run cross-domain matrix O→O, O→N, N→O, N→N.

### Task 3: Leakage, negative controls, robustness, and report

**Files:**
- Modify: `scripts/run_stage3_evaluation.py`
- Create: `docs/dataset-evaluation/reports/stage3/<run-id>/report.json`
- Create: `docs/dataset-evaluation/reports/stage3/<run-id>/README.md`
- Create: `docs/dataset-evaluation/reports/stage3/<run-id>/leakage_audit.json`
- Create: `docs/dataset-evaluation/reports/stage3/<run-id>/runtime_cost.json`

- [ ] Run metadata-only, randomized-label, removed-attack-text, and removed-artifact-field controls.
- [ ] Run missing-time, text masking, and event omission robustness variants where executable.
- [ ] Produce complete report with measured, inconclusive, and not-measured status per metric.
- [ ] Run full relevant test suite and record environment details.

