"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence
import math

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    tp = sum(1 for h, j in zip(human, judge) if h == POS and j == POS)
    fp = sum(1 for h, j in zip(human, judge) if h != POS and j == POS)
    fn = sum(1 for h, j in zip(human, judge) if h == POS and j != POS)
    tn = sum(1 for h, j in zip(human, judge) if h != POS and j != POS)
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    # TODO M2: precision = tp/(tp+fp), recall = tp/(tp+fn); return 0.0 when the denominator is 0
    cm = confusion(human, judge)
    precision = cm["tp"] / (cm["tp"] + cm["fp"]) if (cm["tp"] + cm["fp"]) > 0 else 0.0
    recall = cm["tp"] / (cm["tp"] + cm["fn"]) if (cm["tp"] + cm["fn"]) > 0 else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    # TODO M2
    cm = confusion(human, judge)
    n = cm["tp"] + cm["fp"] + cm["fn"] + cm["tn"]
    if n == 0:
        raise ValueError("Empty dataset")

    # Observed agreement
    p_o = (cm["tp"] + cm["tn"]) / n

    # Expected agreement by chance
    # Marginals: how often human says FAIL/PASS, how often judge says FAIL/PASS
    human_pos = cm["tp"] + cm["fn"]  # human labeled as POS (FAIL)
    human_neg = cm["fp"] + cm["tn"]  # human labeled as NEG (PASS)
    judge_pos = cm["tp"] + cm["fp"]  # judge predicted POS (FAIL)
    judge_neg = cm["fn"] + cm["tn"]  # judge predicted NEG (PASS)

    p_e = (human_pos * judge_pos + human_neg * judge_neg) / (n * n)

    # Check if kappa is undefined (p_e == 1)
    if p_e == 1.0:
        raise ValueError("Kappa undefined: expected agreement = 1 (constant judge)")

    kappa = (p_o - p_e) / (1.0 - p_e)
    return kappa


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    # TODO M2: (p_obs + spec - 1) / (sens + spec - 1)
    denominator = sensitivity + specificity - 1.0
    if denominator == 0:
        # Judge has no discriminatory power (sens + spec = 1, random classifier)
        return observed_rate  # Cannot correct, return observed
    corrected = (observed_rate + specificity - 1.0) / denominator
    # Clip to [0, 1]
    return max(0.0, min(1.0, corrected))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy import stats as scipy_stats

    # Convert to numpy arrays
    a_arr = np.array(a, dtype=float)
    b_arr = np.array(b, dtype=float)

    # Check if arrays are identical
    if np.array_equal(a_arr, b_arr):
        return (0.0, 0.0, 0.0)

    # Define the statistic: mean difference
    def statistic(x, y, axis=-1):
        return np.mean(x, axis=axis) - np.mean(y, axis=axis)

    # Perform paired bootstrap
    result = scipy_stats.bootstrap(
        (a_arr, b_arr),
        statistic,
        n_resamples=n_resamples,
        paired=True,
        method='percentile',
        confidence_level=confidence,
        random_state=np.random.default_rng(rng)
    )

    # Extract results
    mean_diff = float(np.mean(a_arr) - np.mean(b_arr))
    lo = float(result.confidence_interval.low)
    hi = float(result.confidence_interval.high)

    return (mean_diff, lo, hi)


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    if n <= 0 or k <= 0 or c < 0 or c > n or k > n:
        raise ValueError(f"Invalid arguments for pass_at_k: n={n}, c={c}, k={k}")
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    if n <= 0 or k <= 0 or c < 0 or c > n or k > n:
        raise ValueError(f"Invalid arguments for pass_hat_k: n={n}, c={c}, k={k}")
    if c < k:
        return 0.0
    return math.comb(c, k) / math.comb(n, k)
