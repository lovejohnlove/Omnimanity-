import numpy as np

def evaluate_prereg_rules(p1: bool, p2: bool, p3: bool) -> str:
    """
    Frozen §5 rule:
    if p1 AND p2 AND p3 -> SUPPORTED
    elif NOT p1 OR (NOT p2 AND NOT p3) -> FALSIFIED
    else -> PARTIAL
    """
    if p1 and p2 and p3:
        return "SUPPORTED"
    elif (not p1) or ((not p2) and (not p3)):
        return "FALSIFIED"
    else:
        return "PARTIAL"

def robust_lstsq_s_eval(x: np.ndarray, y: np.ndarray):
    """
    Robust demonstration using least-squares and median(max) scaling S.
    """
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    residuals = np.abs(y - (m * x + c))
    S = float(np.median(np.maximum(residuals, 1e-12)))
    return m, c, S

def run_harness_demo():
    x = np.linspace(0, 10, 50)
    y = 2.5 * x + 1.0 + np.random.normal(0, 0.1, size=len(x))
    
    m, c, S = robust_lstsq_s_eval(x, y)
    
    p1 = abs(m - 2.5) < 0.2
    p2 = abs(c - 1.0) < 0.2
    p3 = S < 0.5
    
    verdict = evaluate_prereg_rules(p1, p2, p3)
    print(f"§5 Rule Verification Output:")
    print(f"  p1 (slope): {p1}, p2 (intercept): {p2}, p3 (residual scale S): {p3}")
    print(f"  Final Verdict: {verdict}")
    return verdict

if __name__ == "__main__":
    run_harness_demo()
