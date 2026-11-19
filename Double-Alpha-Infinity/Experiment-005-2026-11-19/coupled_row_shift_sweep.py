#!/usr/bin/env python3
"""Exploratory sweep for the specified 16-state two-thread row-shift family.

This is a numerical check of one ad hoc matrix family, not a general theorem
about coupling, a model of the Time Loom, or a physical prediction.
"""
from __future__ import annotations

import argparse
import csv
import json
import platform
from pathlib import Path

import numpy as np


def single_chain(eps: float) -> np.ndarray:
    return np.array(
        [
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, eps, 1.0 - eps],
            [1.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )


def coupled_matrix(eps: float, gamma: float) -> tuple[np.ndarray, np.ndarray]:
    """Return M0=P⊗P and Mγ after moving γε² from (∞,∞) to (r,r)."""
    p = single_chain(eps)
    m0 = np.kron(p, p)
    m = m0.copy()
    row = 2 * 4 + 2  # source state (∞,∞) with pair index a*4+b
    col_ii = 2 * 4 + 2
    col_rr = 3 * 4 + 3
    delta = gamma * eps * eps
    m[row, col_ii] -= delta
    m[row, col_rr] += delta
    return m0, m


def slem(matrix: np.ndarray) -> tuple[float, float]:
    """Return SLEM (largest modulus after removing one eigenvalue nearest 1)
    and spectral radius. At reducible/periodic endpoints, any additional unit
    eigenvalues remain and therefore correctly yield SLEM 1.
    """
    vals = np.linalg.eigvals(matrix)
    perron_idx = int(np.argmin(np.abs(vals - 1.0)))
    other = np.delete(vals, perron_idx)
    return float(np.max(np.abs(other))), float(np.max(np.abs(vals)))


def marginal_drift(m0: np.ndarray, m: np.ndarray) -> float:
    """Maximum single-coordinate marginal change over all source rows."""
    max_change = 0.0
    for source in range(16):
        delta = m[source] - m0[source]
        for coord in (0, 1):
            groups = [0.0, 0.0, 0.0, 0.0]
            for target, mass in enumerate(delta):
                state = target // 4 if coord == 0 else target % 4
                groups[state] += mass
            max_change = max(max_change, max(abs(x) for x in groups))
    return float(max_change)


def analyze(eps: float, gamma: float) -> dict[str, float]:
    m0, m = coupled_matrix(eps, gamma)
    row_error = float(np.max(np.abs(m.sum(axis=1) - 1.0)))
    min_entry = float(np.min(m))
    if row_error > 1e-12 or min_entry < -1e-12:
        raise RuntimeError(
            f"Invalid transition matrix: eps={eps}, gamma={gamma}, "
            f"row_error={row_error}, min_entry={min_entry}"
        )
    rho, spectral_radius = slem(m)
    return {
        "epsilon": eps,
        "gamma": gamma,
        "slem": rho,
        "gap": 1.0 - rho,
        "spectral_radius": spectral_radius,
        "row_sum_max_abs_error": row_error,
        "minimum_entry": min_entry,
        "max_single_coordinate_marginal_drift": marginal_drift(m0, m),
    }


def turning_points(rows: list[dict[str, float]], tol: float = 1e-8) -> list[dict[str, float | str]]:
    """Identify grid-resolved local extrema; this is not a proof of all extrema."""
    eps = np.array([r["epsilon"] for r in rows])
    gaps = np.array([r["gap"] for r in rows])
    d = np.diff(gaps)
    signs = np.zeros_like(d, dtype=int)
    signs[d > tol] = 1
    signs[d < -tol] = -1
    nonzero = np.flatnonzero(signs)
    points: list[dict[str, float | str]] = []
    for left_pos, right_pos in zip(nonzero[:-1], nonzero[1:]):
        left, right = signs[left_pos], signs[right_pos]
        if left == right:
            continue
        # A sign change in d[j] occurs at gap[j+1], which is the grid point
        # between the last difference of the old sign and the first of the new.
        idx = int(right_pos)
        kind = "local maximum" if left > 0 and right < 0 else "local minimum"
        points.append(
            {
                "kind": kind,
                "epsilon_grid": float(eps[idx]),
                "gap_grid": float(gaps[idx]),
                "left_difference": float(d[idx - 1]),
                "right_difference": float(d[idx]),
            }
        )
    return points


def monotonicity(rows: list[dict[str, float]], tol: float = 1e-8) -> dict[str, float | int | bool]:
    gaps = np.array([r["gap"] for r in rows])
    d = np.diff(gaps)
    positive = int(np.sum(d > tol))
    negative = int(np.sum(d < -tol))
    flat = int(len(d) - positive - negative)
    return {
        "grid_increasing_steps": positive,
        "grid_decreasing_steps": negative,
        "grid_flat_steps_within_tolerance": flat,
        "minimum_gap_step": float(np.min(d)),
        "maximum_gap_step": float(np.max(d)),
        "nonmonotone_on_grid": bool(positive > 0 and negative > 0),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-eps", type=int, default=1001, help="uniform epsilon points, inclusive endpoints")
    ap.add_argument("--csv", type=Path, default=Path("coupled_row_shift_sweep.csv"))
    ap.add_argument("--summary", type=Path, default=Path("coupled_row_shift_sweep_summary.json"))
    args = ap.parse_args()
    if args.n_eps < 3:
        raise SystemExit("--n-eps must be at least 3")

    gammas = (0.25, 0.5, 0.9)
    eps_grid = np.linspace(0.0, 1.0, args.n_eps)
    all_rows: list[dict[str, float]] = []
    by_gamma: dict[str, dict[str, object]] = {}

    # Validate the gamma=0 product SLEM against the single-chain SLEM.
    baseline_max_error = 0.0
    for eps in eps_grid:
        p = single_chain(float(eps))
        p_slem, _ = slem(p)
        m0 = np.kron(p, p)
        product_slem, _ = slem(m0)
        baseline_max_error = max(baseline_max_error, abs(p_slem - product_slem))
    if baseline_max_error > 2e-8:
        raise RuntimeError(f"Kronecker baseline SLEM identity failed: {baseline_max_error}")

    for gamma in gammas:
        rows = [analyze(float(eps), gamma) for eps in eps_grid]
        all_rows.extend(rows)
        by_gamma[str(gamma)] = {
            "endpoints": {
                "epsilon_0_gap": rows[0]["gap"],
                "epsilon_1_gap": rows[-1]["gap"],
            },
            "grid_turning_points": turning_points(rows),
            "monotonicity": monotonicity(rows),
            "max_row_sum_error": max(r["row_sum_max_abs_error"] for r in rows),
            "min_transition_probability": min(r["minimum_entry"] for r in rows),
            "max_single_coordinate_marginal_drift": max(
                r["max_single_coordinate_marginal_drift"] for r in rows
            ),
            "max_coupling_entry_shift": max(gamma * eps * eps for eps in eps_grid),
        }

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    summary = {
        "status": "exploratory numerical sweep; not preregistered; not a physical claim",
        "construction": "Mγ = P(ε)⊗P(ε), then in source row (∞,∞) move γε² from target (∞,∞) to target (r,r)",
        "state_order": ["0", "1", "∞", "r"],
        "pair_indexing": "a*4+b",
        "gamma_values": list(gammas),
        "epsilon_grid": {
            "min": 0.0,
            "max": 1.0,
            "points": int(args.n_eps),
            "step": float(eps_grid[1] - eps_grid[0]),
            "inclusive_endpoints": True,
        },
        "slem_definition": "largest eigenvalue modulus after removing one eigenvalue nearest to 1; additional unit eigenvalues remain in the SLEM",
        "turning_point_tolerance_per_grid_step": 1e-8,
        "kronecker_baseline_max_slem_error": baseline_max_error,
        "by_gamma": by_gamma,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "interpretive_limit": "The specified row shift changes both one-thread marginals in the (∞,∞) source row. Any non-monotonicity is a property of this exact row-shift family, not coupling in general or the Loom.",
        "outputs": {"csv": str(args.csv), "summary": str(args.summary)},
    }
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
