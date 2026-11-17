# Lab 9 — Evaluation & Failure Analysis: Implementation Plan

**Status:** Analysis Complete (No Code Changes Yet)  
**Date:** 2026-11-17  
**Lab Duration:** 13:30–17:00 (M0–M4 Core 60 points)  
**Extension:** After 17:00 to 23:59 (M5–M7 Advanced/Expert 40 points)

---

## A. Repository Structure Analysis

### Day 8 (Current Directory: `K5-L3A-Day08-Vibeforlife-From-Workflows-to-Agents-main`)

```
src/
├── lab8/
│   ├── shapes/
│   │   ├── workflow.py        (TODO M1–M2: implement CP2/CP3)
│   │   ├── single.py          (TODO M1–M2: implement CP2/CP3)
│   │   ├── orchestrator.py    (TODO M1–M2: implement CP2/CP3)
│   │   ├── swarm_reference.py (PROVIDED: reference shape D)
│   │   └── common.py          (Shared utilities)
│   ├── metrics.py             (LOCKED: cannot modify)
│   ├── durability.py          (LOCKED: cannot modify)
│   ├── policy.py              (LOCKED: cannot modify)
│   ├── mock_llm.py            (Available for reference)
│   ├── compensation.py        (Available for reference)
│   ├── app.py                 (Main orchestration)
│   ├── benchmark.py           (Benchmarking)
│   ├── crash_test.py          (Crash testing)
│   └── [other files]          (LOCKED)
├── config/
│   └── *.yaml                 (LOCKED: cannot modify)
├── data/
│   └── *.jsonl                (LOCKED: cannot modify)
├── tests/
├── requirements.txt
└── reports/
    └── (generated outputs)

docs/
├── business_rules.md          (Day 8 spec)
├── contracts.md               (Day 8 spec)
└── [other Day 8 files]

report/
├── team/
│   ├── group_report.md
│   ├── decision_adr.md
│   ├── research_card.md
│   ├── MSSV_HoTen.md          (Template)
│   └── (individual reports)
```

### Day 9 (Starter: `K5-Day9-Evaluation-and-Failure-Analysis`)

```
src/
├── lab9/                      (NEW: evaluation module)
│   ├── smoke.py               (Smoke test)
│   ├── evalset.py             (TODO M1: eval set management)
│   ├── trace_case.py          (Trace analysis)
│   ├── graders.py             (TODO M3: assertion graders)
│   ├── stats.py               (TODO M2, M4: calibration, bootstrap)
│   ├── judge.py               (Judge replay)
│   ├── eval.py                (Evaluation runner)
│   ├── gate.py                (TODO M4: gate logic)
│   ├── variants.py            (Test variants)
│   ├── variant_agent.py       (Variant agent)
│   ├── mutation.py            (Mutation testing)
│   ├── traps.py               (Integrity traps)
│   ├── ci_check.py            (CI validation)
│   └── __init__.py
├── config/                    (NEW: evaluation config)
│   ├── metric_spec.yaml       (TODO M2–M4: define metrics)
│   ├── metric_spec_v2.yaml    (TODO M5–M6: advanced metrics)
│   └── fm_map.yaml            (TODO M5: failure mode mapping)
├── data/
│   └── eval/                  (NEW: evaluation data)
│       ├── judge_tone_public.csv     (Judge labels)
│       ├── judge_helpful_public.csv  (Judge labels)
│       └── adversarial_v2.json       (Adversarial cases)
├── tests/
│   ├── test_lab9_*.py         (NEW: evaluation tests)
└── requirements-lab9.txt      (NEW: lab9 deps)

docs/
├── eval_card.md               (NEW: evaluation template)
├── failure_taxonomy.md        (TODO M1: failure modes)
├── PRD_v1.1.md               (NEW: PRD update)
├── judge_audit.md            (NEW: judge audit template)
├── trace_case.md             (NEW: trace analysis guide)

.github/workflows/
├── eval-gate.yml             (NEW: CI evaluation gate)
└── ci.yml                    (Day 8: existing)
```

---

## B. Files to Copy (Overlay)

### From Day 9 starter to Day 8 repo:

```bash
cp -R src/lab9/                src/      # New evaluation module
cp -R src/config/              src/      # New config: metric_spec*.yaml, fm_map.yaml
cp -R src/data/eval/           src/data/ # New: judge CSVs, adversarial cases
cp -R src/tests/test_lab9_*    src/tests/
cp -R src/requirements-lab9.txt src/
cp -R docs/eval_card.md        docs/
cp -R docs/failure_taxonomy.md docs/
cp -R docs/PRD_v1.1.md         docs/
cp -R docs/judge_audit.md      docs/
cp -R docs/trace_case.md       docs/
cp -R .github/workflows/eval-gate.yml .github/workflows/
```

**DO NOT copy:**
- README.md, CHECKPOINTS.md, RUBRIC.md, SUBMISSION.md (read directly from Day 9 starter)
- .gitignore (would overwrite Day 8's)
- src/lab8/ files (LOCKED)
- src/requirements.txt (keep Day 8's)

---

## C. Execution Plan by Checkpoint

### M0 (13:30) — Environment Setup

**Deliverables:**
- Overlay copied to Day 8 repo
- Virtual environment configured
- Dependencies installed
- Smoke test passes

**Commands:**
```bash
cd src
python -m lab9.smoke
python -m lab9.evalset --build
# Check: exit 0 for both
```

**Expected Output:**
- `M0 PASS` from smoke
- `eval_set_v1.jsonl` and `labels_v1.json` created
- All items have empty `failure_modes`

**Files to Check:**
- `src/lab9/smoke.py` ✓
- `src/requirements-lab9.txt` ✓
- `src/config/metric_spec.yaml` ✓

---

### M1 (13:45) — Taxonomy (12 points)

**Deliverables:**
- `docs/failure_taxonomy.md` with ≥5 failure modes (FM)
- Each FM has: definition, layer, ≥1 trace/claim evidence, grader type
- 5 anchor FMs matched to instructor key
- `evalset --check` = 0 problems

**TODO Items:**
1. Analyze trace_case.md for failure patterns
2. Extract 5+ failure modes from swarm shape traces
3. Assign `failure_modes` in eval set items
4. Document in `docs/failure_taxonomy.md`

**Commands:**
```bash
python -m lab9.evalset --check      # Verify 0 problems
python -m lab9.trace_case          # Extract failure cases
```

**Expected Output:**
- ≥5 FM defined with 1-sentence definition
- Each FM tagged with layer: model/prompt | tool/schema | retrieval | orchestration/state | guardrail/approval
- Trace evidence linked from `src/traces/`
- Grader type specified: code | judge | human

**Files to Create/Modify:**
- `docs/failure_taxonomy.md` (CREATE)

**Files to Check (Locked):**
- `src/lab9/evalset.py` (read to understand structure)
- `docs/trace_case.md` (reference for extraction)

---

### M2 (14:30) — Judge Calibration (12 points)

**Deliverables:**
- `stats.py` functions pass tests
- Judge tone: κ≈0.757, P≈0.857, R≥0.8 (PASS)
- Judge helpful: explanation of why NOT usable as gate (FAIL by design)
- Audit table: ≥5 disagreements with resolution

**TODO Items:**
1. Implement stats functions: kappa, P/R, Rogan-Gladen correction
2. Run judge replay on `data/eval/judge_tone_public.csv`
3. Analyze tone judge → PASS floor
4. Analyze helpful judge → explain failure
5. Create audit table of 5+ disagreements

**Commands:**
```bash
python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5
python -m pytest -q -m student -o addopts= -k "test_stats"
```

**Expected Output:**
```
Judge Tone:
  κ ≈ 0.757 ✓ (pass floor ≥0.6)
  P ≈ 0.857 ✓ (pass floor ≥0.8)
  R ≈ 0.8   ✓ (pass floor ≥0.7)
  Rogan-Gladen correction: x%

Judge Helpful:
  FAIL (κ too low OR P/R miss floor)
  Reason: [explain why not suitable for gate]

Audit: 5+ rows with (claim_id, grader_tone, grader_helpful, resolution)
```

**Files to Create/Modify:**
- `src/lab9/stats.py` (implement TODO functions)
- `docs/judge_audit.md` (CREATE: audit table)

---

### M3 (15:15) — Trajectory Assertions (12 points)

**Deliverables:**
- 2 grader assertions implemented: `ApprovalBypass`, `RefundAmountCorrect`
- Detection rate ≥80%, false positive rate ≤10% on `fixed` variant
- 1 new metric for FM-08 (refund amount mismatch)
- Tests pass

**TODO Items:**
1. Implement `ApprovalBypass` grader: detects approval violations
2. Implement `RefundAmountCorrect` grader: validates refund amounts
3. Add FM-08 metric: detects when agent reply differs from ledger
4. Run on variants to measure detection/FP rates

**Commands:**
```bash
python -m pytest -q -m student -o addopts= -k "lab9 and not advanced"
python -m lab9.eval --shape fixed --out reports/eval_fixed.json
python -m lab9.eval --shape seeded_regression --out reports/eval_seeded_regression.json
```

**Expected Output:**
```
ApprovalBypass: 80%+ detection on actual violations, ≤10% FP on fixed
RefundAmountCorrect: 80%+ detection on mismatches, ≤10% FP on fixed
FM-08 metric: triggers on reply/ledger mismatch
```

**Files to Create/Modify:**
- `src/lab9/graders.py` (implement TODO graders)
- `src/config/metric_spec.yaml` (add FM-08 metric)

---

### M4 (16:00) — Bootstrap Gate (15 points)

**Deliverables:**
- Paired bootstrap CI calculated correctly (Δ ≤0.01 from reference)
- Gate blocks `seeded_regression` (exit 1)
- Gate allows `fixed` (exit 0)
- CI job `eval-gate` passes
- `baseline_v1.json` committed

**TODO Items:**
1. Implement `gate.py` bootstrap logic
2. Generate baseline from swarm on public eval set
3. Verify gate blocks regression variant
4. Verify gate allows fixed variant
5. Commit baseline for CI

**Commands:**
```bash
cd src
python -m lab9.eval --shape swarm --out reports/baseline_v1.json
python -m lab9.eval --shape fixed --out reports/eval_fixed.json
python -m lab9.gate --pr reports/eval_fixed.json --baseline reports/baseline_v1.json
# Exit 0 expected

python -m lab9.eval --shape seeded_regression --out reports/eval_seeded_regression.json
python -m lab9.gate --pr reports/eval_seeded_regression.json --baseline reports/baseline_v1.json
# Exit 1 expected
```

**Expected Output:**
```
Fixed vs Baseline:
  pass_rate: Δ ≥ -0.05 (good)
  CI: [−0.05, +0.10] (positive trend, no regression)
  Gate: PASS (exit 0)

Seeded_regression vs Baseline:
  pass_rate: Δ ≈ −0.271
  CI: [−0.500, −0.057] (clearly negative)
  Gate: BLOCK (exit 1)
```

**Files to Create/Modify:**
- `src/lab9/gate.py` (implement bootstrap + CI logic)
- `src/reports/baseline_v1.json` (CREATE: generate & commit)
- `.github/workflows/eval-gate.yml` (verify CI configuration)

---

## D. Core Testing Checklist

| Checkpoint | Test Command | Expected Result | Must Pass |
|---|---|---|---|
| M0 | `python -m lab9.smoke` | Exit 0, prints "M0 PASS" | ✓ |
| M0 | `python -m lab9.evalset --build` | Exit 0, 14 items with empty failure_modes | ✓ |
| M1 | `python -m lab9.evalset --check` | Exit 0, 0 problems | ✓ |
| M2 | `python -m pytest -q -m student -k test_stats` | All pass, κ/P/R meet floors | ✓ |
| M2 | `python -m lab9.judge --csv data/eval/judge_tone_public.csv` | PASS on tone, FAIL on helpful | ✓ |
| M3 | `python -m pytest -q -m student -k "lab9 and not advanced"` | All pass | ✓ |
| M3 | `python -m lab9.eval --shape fixed` | Exit 0, eval_fixed.json valid | ✓ |
| M4 | `python -m lab9.gate --pr reports/eval_fixed.json --baseline reports/baseline_v1.json` | Exit 0 (allow) | ✓ |
| M4 | `python -m lab9.gate --pr reports/eval_seeded_regression.json --baseline reports/baseline_v1.json` | Exit 1 (block) | ✓ |
| M4 | CI workflow `eval-gate.yml` | Pass on fixed, fail on seeded_regression | ✓ |

---

## E. Files That Must NOT Be Modified

**Day 8 Core (LOCKED):**
```
src/lab8/shapes/workflow.py          (Day 8 assignment)
src/lab8/shapes/single.py            (Day 8 assignment)
src/lab8/shapes/orchestrator.py      (Day 8 assignment)
src/lab8/shapes/swarm_reference.py   (Reference)
src/lab8/shapes/common.py
src/lab8/metrics.py
src/lab8/durability.py
src/lab8/policy.py
src/lab8/compensation.py
src/lab8/mock_llm.py
src/lab8/db.py
src/lab8/*.py                        (All Day 8 modules)
src/config/                          (Day 8 config, except new lab9 configs)
src/data/                            (Day 8 data, except new lab9 data)
src/requirements.txt                 (Keep Day 8's, add to requirements-lab9.txt)
```

**Reports (DO NOT HAND-EDIT):**
```
src/reports/baseline_v1.json         (Must be generated)
src/reports/eval_*.json              (Must be generated)
src/reports/crash.json               (Generated in Day 8)
```

**Templates (PRESERVE):**
```
report/team/MSSV_HoTen.md            (Keep for copying)
```

---

## F. Risk Assessment & Known Pitfalls

### High-Risk Items (Potential Point Loss)

| Risk | Mitigation | Penalty |
|---|---|---|
| **Modify lab8/** | Verify with `git diff src/lab8/` | −10 points |
| **Hand-edit reports/** | Generate via commands only | −20 points |
| **Nesting metrics** | Check metric_spec.yaml syntax | Grader crash |
| **Judge disagreement** | Explain why helpful=fail, not fix to pass | −5 points (audit) |
| **Wrong baseline** | Commit `baseline_v1.json` from `main`, not `PR` | CI failure |
| **Missing trace** | Ensure trace format matches contract | −10 points (C5 equivalent) |
| **Ratcheting spec** | Only tighten thresholds, never loosen | −10 points |
| **Missing FM in taxonomy** | ≥5 FMs required, <5 = partial credit | Rubric fail |
| **Inline labels in eval set** | Keep labels in separate `labels_v1.json` | −5 points (M1) |
| **Wrong CI config** | Verify `eval-gate.yml` references correct baseline | CI fail |

### Known Tricky Cases

1. **Judge helpful MUST fail** — This is intentional. Do NOT try to make it pass by tweaking thresholds. Document why in audit table.

2. **Baseline must be from `main`** — `eval-gate.yml` CI job reads `baseline_v1.json` from the branch, so it must be committed to `main` BEFORE opening PR.

3. **Paired bootstrap requires identical items** — Items in `reports/eval_fixed.json` and `reports/baseline_v1.json` must have same IDs, or CI pairing fails.

4. **Trace sanitization** — Trace must not leak `CANARY_SECRET_*` or PII. Check both `src/traces/` AND stdout during eval.

5. **MockLLM seed determinism** — Seed `11,22,33,44,55` hardcoded; changing seeds breaks reproducibility.

---

## G. Deliverables Checklist (for SUBMISSION)

**Core (M0–M4) Must-Have:**
```
src/lab9/                          (Overlay from starter)
src/requirements-lab9.txt          (Dependencies)
src/config/metric_spec.yaml        (Metrics + thresholds)
src/config/fm_map.yaml             (Failure mode→code mapping)
src/reports/baseline_v1.json       (Committed to repo)
src/reports/eval_fixed.json        (Generated, shows gate PASS)
src/reports/eval_seeded_regression.json (Generated, shows gate BLOCK)

docs/failure_taxonomy.md           (≥5 FMs with evidence)
docs/eval_card.md                  (Filled with numbers)
docs/PRD_v1.1.md                   (Updated from starter)
docs/judge_audit.md                (≥5 disagreements + resolution)

.github/workflows/eval-gate.yml    (CI configuration)

report/team/group_report.md        (Baseline decision & findings)
report/team/decision_adr.md        (Shape choice, commit hash, run_id, metrics)
report/team/research_card.md       (R1–R4, ablation results)
```

**Advanced/Expert (M5–M7) Optional:**
```
src/config/metric_spec_v2.yaml     (Slices + pass_hat_5)
src/reports/baseline_v2.json
src/reports/eval_slice_regression.json
report/team/bonus_report.md
```

---

## H. Next Steps

### Immediate (M0 — 13:30)
1. ✓ Analyze both repositories (DONE)
2. **Copy overlay** from Day 9 starter to Day 8 repo
3. **Install dependencies**: `pip install -r requirements.txt -r requirements-lab9.txt`
4. **Run smoke**: `python -m lab9.smoke` → expect "M0 PASS"
5. **Build eval set**: `python -m lab9.evalset --build` → expect 14 items

### Phase 1 (M1 — 13:45–14:30)
1. Read `docs/trace_case.md` to understand failure extraction
2. Analyze swarm traces for patterns
3. Define ≥5 failure modes in `docs/failure_taxonomy.md`
4. Tag items with failure_modes in eval set
5. Run `evalset --check` → expect 0 problems

### Phase 2 (M2 — 14:30–15:15)
1. Implement stats functions (kappa, P/R, Rogan-Gladen)
2. Run judge replay on tone → confirm PASS
3. Run judge replay on helpful → confirm FAIL
4. Create audit table with 5+ disagreements
5. Document resolution for each disagreement

### Phase 3 (M3 — 15:15–16:00)
1. Implement `ApprovalBypass` grader
2. Implement `RefundAmountCorrect` grader
3. Add FM-08 metric to spec
4. Test on `fixed` and `seeded_regression` variants
5. Verify detection ≥80%, FP ≤10%

### Phase 4 (M4 — 16:00–17:00)
1. Generate baseline from swarm
2. Implement bootstrap + CI logic in gate
3. Test gate on `fixed` → expect PASS (exit 0)
4. Test gate on `seeded_regression` → expect BLOCK (exit 1)
5. Commit `baseline_v1.json`
6. Fill eval card and decision ADR

### Extension (M5–M7 — 17:00–23:59, if time permits)
1. Create `fm_map.yaml` mapping codebase mechanisms to failure modes
2. Build eval set v2 with adversarial cases
3. Implement pass@k / pass^k metrics
4. Add slice gates (money_movement, adversarial)
5. Test against mutation variants and traps

---

## Summary

**Current Status:** ✓ Analysis Complete

**Ready to Proceed:** Yes, awaiting confirmation to:
1. Copy overlay files to Day 8 repo
2. Install Lab9 dependencies
3. Begin M0 environment setup
4. Execute checkpoints M1–M4 in sequence

**Total Core Points at Stake:** 60  
**Total Advanced/Expert Points:** 40 (if time permits)  
**Deadline:** 23:59 same day (GMT+7)
