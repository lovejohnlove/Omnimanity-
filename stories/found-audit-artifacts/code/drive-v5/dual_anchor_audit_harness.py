import math

MIN_LENGTH_DEFAULT = 3
TOL_DEFAULT = 1e-9

def audit_dual_anchor(series_a, series_b, span_tol=TOL_DEFAULT, extremes_balanced=True):
    """
    Dual-anchor verification audit harness (v3 Clean).
    Weaknesses 1-6 resolved. Returns verdict code and diagnostic dictionary.
    """
    if not series_a or not series_b:
        return "HOLD_MISSING_DATA", {"reason": "One or both input series are empty"}
    
    len_a = len(series_a)
    len_b = len(series_b)
    
    if len_a < MIN_LENGTH_DEFAULT or len_b < MIN_LENGTH_DEFAULT:
        return "INSUFFICIENT_DATA", {
            "reason": f"Series lengths ({len_a}, {len_b}) below minimum required ({MIN_LENGTH_DEFAULT})"
        }
    
    if len_a != len_b:
        return "HOLD_MISSING_DATA", {"reason": "Series length mismatch"}
    
    diffs = [abs(a - b) for a, b in zip(series_a, series_b)]
    max_diff = max(diffs)
    mean_diff = sum(diffs) / len(diffs)
    
    if max_diff > span_tol:
        return "FALSIFIED", {
            "max_diff": max_diff,
            "mean_diff": mean_diff,
            "tolerance": span_tol
        }
    
    if extremes_balanced:
        min_a, max_a = min(series_a), max(series_a)
        min_b, max_b = min(series_b), max(series_b)
        if abs((max_a - min_a) - (max_b - min_b)) > span_tol:
            return "FALSIFIED", {"reason": "Extremes imbalance detected"}
            
    return "VERIFIED", {
        "max_diff": max_diff,
        "mean_diff": mean_diff,
        "span_tol": span_tol,
        "samples": len_a
    }

if __name__ == "__main__":
    test_a = [1.0, 2.0, 3.0, 4.0]
    test_b = [1.0, 2.0, 3.0, 4.0]
    verdict, stats = audit_dual_anchor(test_a, test_b)
    print(f"Audit Verdict: {verdict} | Stats: {stats}")
