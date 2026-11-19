#!/usr/bin/env python3
"""Exploratory sweep of a 16-state marginal-preserving coupling family.

This is a numerical investigation of the explicitly specified matrix family,
not a claim about coupling in general, Time Loom, or physical systems.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import sys
from pathlib import Path

import mpmath as mp
import numpy as np

GAMMAS = (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0)
UNIFORM_EPS = np.linspace(0.0, 1.0, 1001)
LOG_P = np.logspace(-1.0, -8.0, 141)


def epsilon_grid() -> np.ndarray:
    raw = list(UNIFORM_EPS) + [1.0 - float(p) for p in LOG_P]
    raw.sort()
    result: list[float] = []
    for x in raw:
        if not result or abs(x - result[-1]) > 1e-14:
            result.append(x)
    return np.array(result, dtype=float)


def single_chain(eps: float) -> np.ndarray:
    return np.array(
        [[0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, eps, 1.0 - eps],
         [1.0, 0.0, 0.0, 0.0]], dtype=float
    )


def coupled_matrix(eps: float, gamma: float) -> tuple[np.ndarray, np.ndarray]:
    """Return P⊗P and M_gamma with delta=gamma*eps*(1-eps) row update."""
    p = single_chain(eps)
    base = np.kron(p, p)
    m = base.copy()
    row = 4 * 2 + 2
    delta = gamma * eps * (1.0 - eps)
    m[row, 4 * 2 + 2] += delta
    m[row, 4 * 2 + 3] -= delta
    m[row, 4 * 3 + 2] -= delta
    m[row, 4 * 3 + 3] += delta
    return base, m


def orthonormal_swap_bases() -> tuple[np.ndarray, np.ndarray]:
    """Columns span the 10-D symmetric and 6-D antisymmetric pair spaces."""
    sym_cols: list[np.ndarray] = []
    anti_cols: list[np.ndarray] = []
    for a in range(4):
        v = np.zeros(16)
        v[4 * a + a] = 1.0
        sym_cols.append(v)
    invsqrt2 = 1.0 / math.sqrt(2.0)
    for a in range(4):
        for b in range(a + 1, 4):
            plus = np.zeros(16)
            plus[4 * a + b] = invsqrt2
            plus[4 * b + a] = invsqrt2
            sym_cols.append(plus)
            minus = np.zeros(16)
            minus[4 * a + b] = invsqrt2
            minus[4 * b + a] = -invsqrt2
            anti_cols.append(minus)
    return np.column_stack(sym_cols), np.column_stack(anti_cols)


def coordinate_basis() -> np.ndarray:
    """Basis for X-only observables plus three independent Y-only observables."""
    cols: list[np.ndarray] = []
    for a in range(4):
        v = np.zeros(16)
        for b in range(4):
            v[4 * a + b] = 1.0
        cols.append(v)
    for b in (1, 2, 3):
        v = np.zeros(16)
        for a in range(4):
            v[4 * a + b] = 1.0
        cols.append(v)
    return np.column_stack(cols)


def hungarian(cost: np.ndarray) -> np.ndarray:
    """Return a minimum-cost column for each row (rectangular, rows<=cols)."""
    cost = np.asarray(cost, dtype=float)
    n, m = cost.shape
    if n > m:
        trans = hungarian(cost.T)
        out = np.full(n, -1, dtype=int)
        for col_original, row_original in enumerate(trans):
            out[row_original] = col_original
        return out
    u = np.zeros(n + 1)
    v = np.zeros(m + 1)
    p = np.zeros(m + 1, dtype=int)
    way = np.zeros(m + 1, dtype=int)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = np.full(m + 1, np.inf)
        used = np.zeros(m + 1, dtype=bool)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = np.inf
            j1 = 0
            for j in range(1, m + 1):
                if not used[j]:
                    cur = cost[i0 - 1, j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    assignment = np.full(n, -1, dtype=int)
    for j in range(1, m + 1):
        if p[j] != 0:
            assignment[p[j] - 1] = j - 1
    return assignment


def spectral_match(a: np.ndarray, b: np.ndarray) -> tuple[float, np.ndarray]:
    """Min-squared-distance assignment from a into b; return max matched error."""
    a = np.asarray(a, dtype=complex)
    b = np.asarray(b, dtype=complex)
    costs = np.abs(a[:, None] - b[None, :]) ** 2
    assignment = hungarian(costs)
    errors = np.abs(a - b[assignment])
    return float(np.max(errors)) if len(errors) else 0.0, assignment


def slem(vals: np.ndarray) -> tuple[float, int, float]:
    vals = np.asarray(vals, dtype=complex)
    perron_idx = int(np.argmin(np.abs(vals - 1.0)))
    others = np.delete(vals, perron_idx)
    return float(np.max(np.abs(others))), perron_idx, float(np.max(np.abs(vals)))


def max_abs(x: np.ndarray) -> float:
    return float(np.max(np.abs(x))) if np.size(x) else 0.0


def charpoly_coefficients(matrix: np.ndarray) -> np.ndarray:
    """Faddeev-LeVerrier coefficients, avoiding eigenvalue-root instability."""
    a = np.asarray(matrix, dtype=float)
    n = a.shape[0]
    traces = [0.0]
    power = np.eye(n)
    for _ in range(1, n + 1):
        power = power @ a
        traces.append(float(np.trace(power)))
    coeff = [1.0]
    for k in range(1, n + 1):
        coeff.append(-sum(coeff[k - j] * traces[j] for j in range(1, k + 1)) / k)
    return np.asarray(coeff)


def analyze_point(eps: float, gamma: float, sym_basis: np.ndarray,
                  anti_basis: np.ndarray, coord_basis: np.ndarray) -> tuple[dict, np.ndarray]:
    base, m = coupled_matrix(eps, gamma)
    p = single_chain(eps)
    row_err = max_abs(m.sum(axis=1) - 1.0)
    minimum = float(np.min(m))

    # Test both coordinate marginals against P(eps) on every source row.
    marginal_error = 0.0
    for src in range(16):
        a, b = divmod(src, 4)
        mx = np.zeros(4)
        my = np.zeros(4)
        for target in range(16):
            c, d = divmod(target, 4)
            mx[c] += m[src, target]
            my[d] += m[src, target]
        marginal_error = max(marginal_error, max_abs(mx - p[a]), max_abs(my - p[b]))

    swap = np.array([4 * b + a for a in range(4) for b in range(4)], dtype=int)
    swap_error = max_abs(m[np.ix_(swap, swap)] - m)
    sym_block = sym_basis.T @ m @ sym_basis
    anti_block = anti_basis.T @ m @ anti_basis
    off_block = sym_basis.T @ m @ anti_basis
    full_vals = np.linalg.eigvals(m)
    route_vals = np.concatenate([np.linalg.eigvals(sym_block), np.linalg.eigvals(anti_block)])
    route_match_error, _ = spectral_match(full_vals, route_vals)
    direct_slem, perron_idx, radius = slem(full_vals)
    route_slem, _, _ = slem(route_vals)
    symmetric_vals = np.linalg.eigvals(sym_block)
    symmetric_slem, _, _ = slem(symmetric_vals)

    # The additive coordinate-observable invariant space has dimension 7.
    # Its restricted action has eigenvalues {1} plus two copies of each
    # nontrivial eigenvalue of P.  The quotient is dimension 16-7=9.
    restricted = np.linalg.lstsq(coord_basis, m @ coord_basis, rcond=None)[0]
    invariant_residual = max_abs(m @ coord_basis - coord_basis @ restricted)
    restricted_vals = np.linalg.eigvals(restricted)
    pvals = np.linalg.eigvals(p)
    p_perron = int(np.argmin(np.abs(pvals - 1.0)))
    p_nonperron = np.delete(pvals, p_perron)
    expected_degree7 = np.concatenate([pvals, p_nonperron])
    factor_internal_error, _ = spectral_match(restricted_vals, expected_degree7)
    factor_full_error, _ = spectral_match(expected_degree7, full_vals)
    p_poly = charpoly_coefficients(p)
    p_nonperron_poly, p_division_remainder = np.polydiv(p_poly, np.array([1.0, -1.0]))
    expected_factor_poly = np.polymul(p_poly, p_nonperron_poly)
    restricted_factor_poly = charpoly_coefficients(restricted)
    factor_charpoly_error = max_abs(restricted_factor_poly - expected_factor_poly)
    p_factor_division_error = max_abs(p_division_remainder)
    single_rho, _, _ = slem(pvals)

    row = {
        "epsilon": eps,
        "gamma": gamma,
        "slem": direct_slem,
        "gap": 1.0 - direct_slem,
        "slem_symmetric_block": symmetric_slem,
        "single_chain_rho": single_rho,
        "symmetric_block_excess_over_rho": symmetric_slem - single_rho,
        "spectral_radius": radius,
        "row_sum_max_abs_error": row_err,
        "minimum_transition_probability": minimum,
        "marginal_max_abs_error": marginal_error,
        "swap_commutator_max_abs_error": swap_error,
        "swap_off_block_max_abs_error": max_abs(off_block),
        "direct_vs_10plus6_spectrum_max_match_error": route_match_error,
        "direct_vs_swap_route_slem_abs_error": abs(direct_slem - route_slem),
        "coordinate_invariant_space_residual": invariant_residual,
        "coordinate_degree7_restricted_root_match_error_diagnostic": factor_internal_error,
        "coordinate_degree7_restricted_charpoly_coefficient_error": factor_charpoly_error,
        "single_chain_charpoly_division_remainder_error": p_factor_division_error,
        "coordinate_degree7_full_spectrum_subset_error": factor_full_error,
        "coordinate_factor_degree": 7,
        "generic_quotient_degree": 9,
        "removed_perron_eigenvalue_index_numpy": perron_idx,
        "gamma0_product_matrix_max_abs_error": max_abs(m - base) if gamma == 0 else 0.0,
        "gamma1_synchronized_row_error": 0.0,
    }
    if gamma == 1.0:
        target = np.zeros(16)
        target[4 * 2 + 2] = eps
        target[4 * 3 + 3] = 1.0 - eps
        row["gamma1_synchronized_row_error"] = max_abs(m[4 * 2 + 2] - target)
    return row, full_vals


def local_extrema(gaps: np.ndarray, eps: np.ndarray, tol: float) -> list[dict]:
    d = np.diff(gaps)
    signs = np.zeros(len(d), dtype=int)
    signs[d > tol] = 1
    signs[d < -tol] = -1
    nz = np.flatnonzero(signs)
    out: list[dict] = []
    for left_pos, right_pos in zip(nz[:-1], nz[1:]):
        left, right = signs[left_pos], signs[right_pos]
        if left == right:
            continue
        idx = int(right_pos)
        out.append({
            "kind": "local maximum" if left > 0 else "local minimum",
            "index": idx,
            "epsilon_grid": float(eps[idx]),
            "gap_grid": float(gaps[idx]),
            "left_step": float(d[idx - 1]),
            "right_step": float(d[idx]),
        })
    return out


def mp_matrix(eps: mp.mpf, gamma: mp.mpf) -> tuple[mp.matrix, mp.matrix]:
    one = mp.mpf(1)
    p = mp.matrix([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, eps, one - eps], [1, 0, 0, 0]])
    m = mp.matrix(16)
    for a in range(4):
        for b in range(4):
            src = 4 * a + b
            for c in range(4):
                for d in range(4):
                    m[src, 4 * c + d] = p[a, c] * p[b, d]
    delta = gamma * eps * (one - eps)
    row = 10
    m[row, 10] += delta
    m[row, 11] -= delta
    m[row, 14] -= delta
    m[row, 15] += delta
    return p, m


def mp_slem_gap(eps: mp.mpf, gamma: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    p, m = mp_matrix(eps, gamma)
    root2 = mp.sqrt(2)
    w = mp.matrix(16, 10)
    col = 0
    for a in range(4):
        w[4 * a + a, col] = 1
        col += 1
    for a in range(4):
        for b in range(a + 1, 4):
            w[4 * a + b, col] = 1 / root2
            w[4 * b + a, col] = 1 / root2
            col += 1
    sym = w.T * m * w
    sym_vals = mp.eig(sym, left=False, right=False)
    p_vals = mp.eig(p, left=False, right=False)
    anti_vals = [p_vals[i] * p_vals[j] for i in range(4) for j in range(i + 1, 4)]
    all_vals = list(sym_vals) + anti_vals
    perron = min(range(len(all_vals)), key=lambda i: abs(all_vals[i] - 1))
    radius = max(abs(v) for i, v in enumerate(all_vals) if i != perron)
    return radius, 1 - radius


def mp_symmetric_block_excess(eps: mp.mpf, gamma: mp.mpf) -> mp.mpf:
    """Return SLEM of the symmetric block minus the single-chain rho."""
    p, m = mp_matrix(eps, gamma)
    root2 = mp.sqrt(2)
    w = mp.matrix(16, 10)
    col = 0
    for a in range(4):
        w[4 * a + a, col] = 1
        col += 1
    for a in range(4):
        for b in range(a + 1, 4):
            w[4 * a + b, col] = 1 / root2
            w[4 * b + a, col] = 1 / root2
            col += 1
    sym_vals = list(mp.eig(w.T * m * w, left=False, right=False))
    sym_perron = min(range(len(sym_vals)), key=lambda i: abs(sym_vals[i] - 1))
    sym_slem = max(abs(v) for i, v in enumerate(sym_vals) if i != sym_perron)
    p_vals = list(mp.eig(p, left=False, right=False))
    p_perron = min(range(len(p_vals)), key=lambda i: abs(p_vals[i] - 1))
    rho = max(abs(v) for i, v in enumerate(p_vals) if i != p_perron)
    return sym_slem - rho


def mp_endpoint_coordinate_factor_check(dps: int = 50) -> dict:
    """High-precision check of the degree-7 coordinate factor at epsilon=1."""
    mp.mp.dps = dps
    _, m = mp_matrix(mp.mpf(1), mp.mpf("0.5"))
    basis = mp.matrix(16, 7)
    for a in range(4):
        for b in range(4):
            basis[4 * a + b, a] = 1
    for b in (1, 2, 3):
        for a in range(4):
            basis[4 * a + b, 3 + b] = 1
    image = m * basis
    restricted = mp.matrix(7)
    for j in range(7):
        for a in range(4):
            restricted[a, j] = image[4 * a, j]
        for b in (1, 2, 3):
            restricted[3 + b, j] = image[b, j] - image[0, j]
    residual = max(abs(x) for x in m * basis - basis * restricted)
    roots = list(mp.eig(restricted, left=False, right=False))
    one_idx = min(range(7), key=lambda i: abs(roots[i] - 1))
    zero_root_max = max(abs(v) for i, v in enumerate(roots) if i != one_idx)
    return {
        "epsilon": "1",
        "gamma": "0.5 (delta=0 at this endpoint)",
        "expected_coordinate_factor": "(lambda-1)*lambda^6",
        "high_precision_invariant_subspace_residual": mp.nstr(residual, 12),
        "high_precision_max_modulus_of_six_zero_roots": mp.nstr(zero_root_max, 12),
        "working_precision_decimal_digits": dps,
        "interpretation": "confirms endpoint factor at high precision; double-precision eigensolver root matching near the defective zero cluster is ill-conditioned",
    }


def refine_candidate(candidate: dict, eps_grid: np.ndarray, gamma: float,
                     dps: int = 50) -> dict:
    """High-precision neighborhood check and golden-section local refinement."""
    mp.mp.dps = dps
    idx = int(candidate["index"])
    lo_f = float(eps_grid[max(0, idx - 1)])
    hi_f = float(eps_grid[min(len(eps_grid) - 1, idx + 1)])
    lo, hi = mp.mpf(repr(lo_f)), mp.mpf(repr(hi_f))
    gm = mp.mpf(repr(float(gamma)))
    nscan = 9
    xs = [lo + (hi - lo) * i / (nscan - 1) for i in range(nscan)]
    fs = [mp_slem_gap(x, gm)[1] for x in xs]
    is_max = candidate["kind"] == "local maximum"
    candidates = []
    for j in range(1, nscan - 1):
        if is_max and fs[j] >= fs[j - 1] and fs[j] >= fs[j + 1]:
            candidates.append(j)
        if not is_max and fs[j] <= fs[j - 1] and fs[j] <= fs[j + 1]:
            candidates.append(j)
    if not candidates:
        return {
            **candidate, "status": "not persistent in 50-digit local scan",
            "scan_interval": [str(lo), str(hi)], "working_precision_decimal_digits": dps,
            "scan_points": nscan,
        }
    j = min(candidates, key=lambda k: abs(xs[k] - mp.mpf(repr(candidate["epsilon_grid"]))))
    a, b = xs[j - 1], xs[j + 1]
    phi = (mp.sqrt(5) - 1) / 2
    c = b - phi * (b - a)
    d = a + phi * (b - a)
    fc = mp_slem_gap(c, gm)[1]
    fd = mp_slem_gap(d, gm)[1]
    evals = nscan + 2
    while b - a > mp.mpf("5e-11"):
        if (fc > fd) == is_max:
            b, d, fd = d, c, fc
            c = b - phi * (b - a)
            fc = mp_slem_gap(c, gm)[1]
        else:
            a, c, fc = c, d, fd
            d = a + phi * (b - a)
            fd = mp_slem_gap(d, gm)[1]
        evals += 1
        if evals > 200:
            raise RuntimeError("High-precision refinement exceeded 200 evaluations")
    best_x = (a + b) / 2
    best_gap = mp_slem_gap(best_x, gm)[1]
    return {
        **candidate,
        "status": "persistent; locally refined",
        "scan_interval": [mp.nstr(lo, 18), mp.nstr(hi, 18)],
        "scan_points": nscan,
        "working_precision_decimal_digits": dps,
        "refined_epsilon": mp.nstr(best_x, 40),
        "refined_gap": mp.nstr(best_gap, 40),
        "epsilon_bracket": [mp.nstr(a, 40), mp.nstr(b, 40)],
        "epsilon_bracket_width": mp.nstr(b - a, 8),
        "high_precision_evaluations": evals,
    }


def refine_excess_peak(gamma: float, eps_grid: np.ndarray,
                       rows: list[dict], dps: int = 50) -> dict:
    """Refine the largest sampled symmetric-block excess if it clears noise."""
    mp.mp.dps = dps
    excesses = np.array([r["symmetric_block_excess_over_rho"] for r in rows])
    idx = int(np.argmax(excesses))
    coarse = float(excesses[idx])
    threshold = 1e-12
    if coarse <= threshold or idx == 0 or idx == len(eps_grid) - 1:
        return {
            "gamma": gamma,
            "status": "no robust interior excess peak to refine",
            "coarse_max_excess": coarse,
            "noise_threshold": threshold,
        }
    lo = mp.mpf(repr(float(eps_grid[idx - 1])))
    hi = mp.mpf(repr(float(eps_grid[idx + 1])))
    gm = mp.mpf(repr(float(gamma)))
    nscan = 9
    xs = [lo + (hi - lo) * i / (nscan - 1) for i in range(nscan)]
    fs = [mp_symmetric_block_excess(x, gm) for x in xs]
    peaks = [j for j in range(1, nscan - 1) if fs[j] >= fs[j - 1] and fs[j] >= fs[j + 1]]
    if not peaks:
        return {
            "gamma": gamma,
            "status": "not a persistent local maximum in 50-digit scan",
            "coarse_epsilon": float(eps_grid[idx]),
            "coarse_max_excess": coarse,
            "scan_interval": [mp.nstr(lo, 18), mp.nstr(hi, 18)],
            "working_precision_decimal_digits": dps,
        }
    j = min(peaks, key=lambda k: abs(xs[k] - mp.mpf(repr(float(eps_grid[idx])))))
    a, b = xs[j - 1], xs[j + 1]
    phi = (mp.sqrt(5) - 1) / 2
    c = b - phi * (b - a)
    d = a + phi * (b - a)
    fc = mp_symmetric_block_excess(c, gm)
    fd = mp_symmetric_block_excess(d, gm)
    evals = nscan + 2
    while b - a > mp.mpf("5e-11"):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - phi * (b - a)
            fc = mp_symmetric_block_excess(c, gm)
        else:
            a, c, fc = c, d, fd
            d = a + phi * (b - a)
            fd = mp_symmetric_block_excess(d, gm)
        evals += 1
    best_x = (a + b) / 2
    best_excess = mp_symmetric_block_excess(best_x, gm)
    return {
        "gamma": gamma,
        "status": "persistent; locally refined",
        "coarse_epsilon": float(eps_grid[idx]),
        "coarse_max_excess": coarse,
        "scan_interval": [mp.nstr(lo, 18), mp.nstr(hi, 18)],
        "working_precision_decimal_digits": dps,
        "refined_epsilon": mp.nstr(best_x, 40),
        "refined_symmetric_block_excess_over_rho": mp.nstr(best_excess, 40),
        "epsilon_bracket": [mp.nstr(a, 40), mp.nstr(b, 40)],
        "epsilon_bracket_width": mp.nstr(b - a, 8),
        "high_precision_evaluations": evals,
    }


def branch_track(gamma: float, eps_grid: np.ndarray, values: list[np.ndarray]) -> list[dict]:
    rows: list[dict] = []
    previous: np.ndarray | None = None
    tracked: np.ndarray | None = None
    for k, (eps, raw) in enumerate(zip(eps_grid, values)):
        vals = np.asarray(raw, dtype=complex)
        if previous is None:
            order = np.lexsort((vals.imag, vals.real))
            tracked = vals[order]
            step_error = 0.0
            raw_to_branch = np.empty(len(vals), dtype=int)
            raw_to_branch[order] = np.arange(len(vals))
        else:
            _, assignment = spectral_match(previous, vals)
            tracked = vals[assignment]
            step_error = float(np.max(np.abs(tracked - previous)))
            raw_to_branch = np.empty(len(vals), dtype=int)
            raw_to_branch[assignment] = np.arange(len(vals))
        removed_raw = int(np.argmin(np.abs(vals - 1.0)))
        removed_branch = int(raw_to_branch[removed_raw])
        candidate_branch = [i for i in range(len(tracked)) if i != removed_branch]
        dominant_branch = max(candidate_branch, key=lambda i: abs(tracked[i]))
        min_separation = float("inf")
        for i in range(len(tracked)):
            for j in range(i + 1, len(tracked)):
                min_separation = min(min_separation, float(abs(tracked[i] - tracked[j])))
        for branch_id, z in enumerate(tracked):
            rows.append({
                "gamma": gamma,
                "epsilon": float(eps),
                "branch_id_path_dependent": branch_id,
                "eigenvalue_real": float(z.real),
                "eigenvalue_imag": float(z.imag),
                "eigenvalue_modulus": float(abs(z)),
                "removed_nearest_to_one_branch": branch_id == removed_branch,
                "controls_slem_branch": branch_id == dominant_branch,
                "max_assignment_step_from_previous_epsilon": step_error,
                "minimum_pairwise_branch_separation_at_epsilon": min_separation,
            })
        previous = tracked.copy()
    return rows


def noise_floor_checks(records: dict[float, list[dict]],
                       eps_grid: np.ndarray, gammas: tuple[float, ...]) -> dict:
    """Compare spectra under deterministic random conjugate state relabelings."""
    rng = np.random.default_rng(20261119)
    checked = 0
    max_spectrum_error = 0.0
    max_slem_error = 0.0
    points: list[dict] = []
    for gamma in gammas:
        rows = records[gamma]
        gaps = np.array([r["gap"] for r in rows])
        base_indices = set(np.linspace(0, len(eps_grid) - 1, 25, dtype=int).tolist())
        # Include all coarse/local turning candidates and adjacent samples.
        for c in local_extrema(gaps, eps_grid, 1e-10):
            i = int(c["index"])
            base_indices.update(j for j in (i - 1, i, i + 1) if 0 <= j < len(eps_grid))
        per_point = 8
        for idx in sorted(base_indices):
            eps = float(eps_grid[idx])
            _, matrix = coupled_matrix(eps, gamma)
            ref = np.linalg.eigvals(matrix)
            ref_slem, _, _ = slem(ref)
            point_max = 0.0
            point_slem = 0.0
            for _ in range(per_point):
                perm = rng.permutation(16)
                perm_vals = np.linalg.eigvals(matrix[np.ix_(perm, perm)])
                err, _ = spectral_match(ref, perm_vals)
                perm_slem, _, _ = slem(perm_vals)
                point_max = max(point_max, err)
                point_slem = max(point_slem, abs(ref_slem - perm_slem))
                checked += 1
            max_spectrum_error = max(max_spectrum_error, point_max)
            max_slem_error = max(max_slem_error, point_slem)
            points.append({"gamma": gamma, "epsilon": eps,
                           "permutations": per_point,
                           "max_spectrum_match_error": point_max,
                           "max_slem_difference": point_slem})
    return {
        "relabeling_method": "random simultaneous row/column conjugation by state permutation (similarity transform)",
        "seed": 20261119,
        "permutations_per_sampled_matrix": 8,
        "sampled_matrix_count": len(points),
        "total_permuted_spectrum_checks": checked,
        "max_spectrum_match_error": max_spectrum_error,
        "max_slem_difference": max_slem_error,
        "samples": points,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, default=Path("."))
    ap.add_argument("--mp-dps", type=int, default=50)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    eps_grid = epsilon_grid()
    sym_basis, anti_basis = orthonormal_swap_bases()
    coord_basis = coordinate_basis()
    all_rows: list[dict] = []
    raw_values: dict[float, list[np.ndarray]] = {}
    rows_by_gamma: dict[float, list[dict]] = {}
    branches: list[dict] = []

    for gamma in GAMMAS:
        print(f"sweeping gamma={gamma:g} ({len(eps_grid)} epsilon points)", flush=True)
        vals_for_gamma: list[np.ndarray] = []
        rows_for_gamma: list[dict] = []
        for i, eps in enumerate(eps_grid):
            row, eigs = analyze_point(float(eps), gamma, sym_basis, anti_basis, coord_basis)
            all_rows.append(row)
            rows_for_gamma.append(row)
            vals_for_gamma.append(eigs)
        raw_values[gamma] = vals_for_gamma
        rows_by_gamma[gamma] = rows_for_gamma
        branches.extend(branch_track(gamma, eps_grid, vals_for_gamma))

    noise = noise_floor_checks(rows_by_gamma, eps_grid, GAMMAS)
    candidates: dict[str, list[dict]] = {}
    refinements: list[dict] = []
    effective_tol = max(1e-11, 10.0 * noise["max_slem_difference"])
    for gamma in GAMMAS:
        rows = rows_by_gamma[gamma]
        gaps = np.array([r["gap"] for r in rows])
        found = local_extrema(gaps, eps_grid, effective_tol)
        candidates[str(gamma)] = found
        for candidate in found:
            refinements.append(refine_candidate(candidate, eps_grid, gamma, args.mp_dps))

    block_exceedance: dict[str, dict] = {}
    exceedance_tolerance = max(1e-12, 10.0 * noise["max_slem_difference"])
    for gamma in GAMMAS:
        rows = rows_by_gamma[gamma]
        excesses = np.array([r["symmetric_block_excess_over_rho"] for r in rows])
        max_idx = int(np.argmax(excesses))
        above = [i for i, x in enumerate(excesses) if x > exceedance_tolerance]
        block_exceedance[str(gamma)] = {
            "max_symmetric_block_nonperron_modulus_minus_rho": float(excesses[max_idx]),
            "epsilon_at_maximum_excess": float(eps_grid[max_idx]),
            "points_exceeding_rho_beyond_noise_tolerance": len(above),
            "noise_tolerance_for_exceedance": exceedance_tolerance,
            "first_exceedance_epsilon_if_any": float(eps_grid[above[0]]) if above else None,
            "interpretation": "sampled 10x10 symmetric-block SLEM compared with rho(epsilon); not a continuum proof",
        }
    excess_refinements = [
        refine_excess_peak(gamma, eps_grid, rows_by_gamma[gamma], args.mp_dps)
        for gamma in GAMMAS
    ]

    # Check the gamma=0 product reference and gamma=1 synchronized-row anchor.
    gamma0_matrix_max_error = 0.0
    gamma0_gap_max_error = 0.0
    gamma1_row_max_error = 0.0
    gamma0_rows = rows_by_gamma[0.0]
    for eps, row in zip(eps_grid, gamma0_rows):
        base, m0 = coupled_matrix(float(eps), 0.0)
        p = single_chain(float(eps))
        pvals = np.linalg.eigvals(p)
        p_slem, _, _ = slem(pvals)
        gamma0_matrix_max_error = max(gamma0_matrix_max_error, max_abs(m0 - base))
        gamma0_gap_max_error = max(gamma0_gap_max_error, abs(row["gap"] - (1.0 - p_slem)))
    for eps in eps_grid:
        _, m1 = coupled_matrix(float(eps), 1.0)
        expected = np.zeros(16)
        expected[10] = eps
        expected[15] = 1.0 - eps
        gamma1_row_max_error = max(gamma1_row_max_error, max_abs(m1[10] - expected))

    # High-precision endpoint scaling check, kept empirical rather than promoted
    # to an asymptotic theorem.  p=1-epsilon is sampled by decade.
    mp.mp.dps = args.mp_dps
    endpoint_scaling: dict[str, dict] = {}
    p_values = [mp.mpf(10) ** (-k) for k in range(1, 9)]
    for gamma in GAMMAS:
        slem_values = []
        for pval in p_values:
            r, _ = mp_slem_gap(1 - pval, mp.mpf(repr(gamma)))
            slem_values.append(r)
        logx = np.array([float(mp.log(pv)) for pv in p_values[1:]])
        logy = np.array([float(mp.log(sv)) for sv in slem_values[1:]])
        slope, intercept = np.polyfit(logx, logy, 1)
        endpoint_scaling[str(gamma)] = {
            "method": "50-digit eigensolve on 10x10 symmetric block plus six pinned antisymmetric products",
            "p_values_1_minus_epsilon": [mp.nstr(pv, 8) for pv in p_values],
            "nonperron_slem_values": [mp.nstr(sv, 30) for sv in slem_values],
            "loglog_slope_fit_using_p_1e-2_to_1e-8": float(slope),
            "interpretation": "finite-range empirical scaling estimate; not an asymptotic proof",
        }

    # Numeric validation maxima over the full sweep.
    fields = [
        "row_sum_max_abs_error", "minimum_transition_probability",
        "marginal_max_abs_error", "swap_commutator_max_abs_error",
        "swap_off_block_max_abs_error", "direct_vs_10plus6_spectrum_max_match_error",
        "direct_vs_swap_route_slem_abs_error", "coordinate_invariant_space_residual",
        "coordinate_degree7_restricted_charpoly_coefficient_error",
        "single_chain_charpoly_division_remainder_error",
        "coordinate_degree7_full_spectrum_subset_error",
    ]
    maxima = {f: max(float(r[f]) for r in all_rows) for f in fields if f != "minimum_transition_probability"}
    maxima["minimum_transition_probability"] = min(float(r["minimum_transition_probability"]) for r in all_rows)
    maxima["gamma0_product_matrix_max_abs_error"] = gamma0_matrix_max_error
    maxima["gamma0_gap_vs_single_chain_max_abs_error"] = gamma0_gap_max_error
    maxima["gamma1_synchronized_row_max_abs_error"] = gamma1_row_max_error

    csv_path = args.out_dir / "marginal_preserving_coupling_sweep.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)
    branch_path = args.out_dir / "marginal_preserving_coupling_branch_tracking.csv"
    with branch_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(branches[0].keys()))
        writer.writeheader()
        writer.writerows(branches)

    summary = {
        "experiment": "marginal-preserving two-coordinate coupling; distinct from the earlier row-shift arm",
        "status": "exploratory numerical run; local and review-only; no physical claim",
        "construction": "M=P(epsilon) tensor P(epsilon); in source row (infinity,infinity), delta=gamma*epsilon*(1-epsilon); add delta to (infinity,infinity) and (r,r), subtract delta from (infinity,r) and (r,infinity)",
        "state_order": ["0", "1", "infinity", "r"],
        "pair_indexing": "4*a+b",
        "gamma_values": list(GAMMAS),
        "epsilon_grid": {
            "uniform_points": 1001,
            "uniform_step": 0.001,
            "log_spaced_p_points": 141,
            "p_definition": "p=1-epsilon",
            "p_min": 1e-8,
            "p_max": 1e-1,
            "deduplication_absolute_tolerance": 1e-14,
            "unique_points": int(len(eps_grid)),
            "includes_epsilon_0_and_1": True,
        },
        "matrix_validation_maxima": maxima,
        "spectral_structure": {
            "coordinate_observable_invariant_factor_degree": 7,
            "coordinate_factor_roots": "one eigenvalue 1 plus two copies of each of the three nontrivial eigenvalues of P(epsilon)",
            "generic_quotient_degree": 9,
            "swap_symmetric_block_dimension": 10,
            "swap_antisymmetric_block_dimension": 6,
            "antisymmetric_eigenvalues": "lambda_i*lambda_j for i<j from P(epsilon)",
            "full_matrix_vs_10_plus_6_block_check": "performed at every sweep point; report maxima above",
            "incorrect_chi_P_squared_divisor_used": False,
            "restricted_root_matching_caveat": "double-precision eigenvalue matching for the degree-7 restricted block becomes ill-conditioned at epsilon=1, where the zero eigenvalue has high multiplicity; invariant-space residual, coefficient-based factor check, full-spectrum subset match, and separate 50-digit endpoint check are recorded",
        },
        "symmetric_block_vs_rho_sampled_test": {
            "comparison": "largest modulus after removing one eigenvalue nearest 1 in the 10x10 symmetric block, versus rho(epsilon) of P(epsilon)",
            "results_by_gamma": block_exceedance,
            "interpretive_limit": "grid result only; does not establish a bound for every real epsilon",
        },
        "symmetric_block_excess_peak_refinements": excess_refinements,
        "high_precision_endpoint_coordinate_factor_check": mp_endpoint_coordinate_factor_check(args.mp_dps),
        "state_label_permutation_noise_floor": noise,
        "turning_point_candidates_by_gamma": candidates,
        "turning_point_refinements": refinements,
        "exceptional_point_labels": [],
        "exceptional_point_policy": "No EP labels assigned. Branch proximity/crossing alone is insufficient; a high-precision eigenvalue coalescence and geometric-multiplicity check would be required.",
        "endpoint_scaling_check": endpoint_scaling,
        "interpretive_limits": [
            "Extrema are local numerical candidates only; high-precision local refinement does not prove global extrema or exhaust unsampled structure.",
            "The endpoint scaling fit is empirical over a finite range and is not an asymptotic theorem.",
            "No inference about the Time Loom, Double Alpha as a whole, physical time, gravity, or experiment 005a follows from these matrix results.",
        ],
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "mpmath": mp.__version__,
            "platform": platform.platform(),
            "high_precision_decimal_digits": args.mp_dps,
        },
        "outputs": {
            "sweep_csv": str(csv_path.resolve()),
            "branch_tracking_csv": str(branch_path.resolve()),
        },
    }
    summary_path = args.out_dir / "marginal_preserving_coupling_sweep_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "epsilon_points": len(eps_grid),
        "rows": len(all_rows),
        "validation_maxima": maxima,
        "permutation_noise_floor": {k: v for k, v in noise.items() if k != "samples"},
        "turning_point_candidates": {g: len(v) for g, v in candidates.items()},
        "refinements": refinements,
        "symmetric_block_excess_peak_refinements": excess_refinements,
        "endpoint_slopes": {g: v["loglog_slope_fit_using_p_1e-2_to_1e-8"] for g, v in endpoint_scaling.items()},
        "outputs": summary["outputs"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
