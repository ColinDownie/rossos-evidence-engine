"""
jacobian_tools.py

Utilities for numerically estimating the Jacobian of a vector-valued
operator via central finite differences, and computing its Frobenius
norm.

This module has no side effects and no external state — every function
takes real arrays in and returns real numbers/arrays out, so it's
straightforward to unit test.
"""

from __future__ import annotations
import numpy as np


def default_operator(X: np.ndarray) -> np.ndarray:
    """
    Example nonlinear operator: R(X) = sin(X) + 0.5 * X^2, applied
    elementwise. Maps R^n -> R^n.
    """
    X = np.asarray(X, dtype=float)
    return np.sin(X) + 0.5 * X ** 2


def calculate_jacobian(X: np.ndarray, operator=default_operator, eps: float = 1e-5) -> np.ndarray:
    """
    Estimate the Jacobian of `operator` at point X using central
    finite differences.

    Parameters
    ----------
    X : array_like, shape (n,)
        Point at which to evaluate the Jacobian.
    operator : callable
        Function mapping R^n -> R^n.
    eps : float
        Finite-difference step size.

    Returns
    -------
    J : ndarray, shape (n, n)
        J[:, i] = d(operator)/d(X_i)
    """
    X = np.asarray(X, dtype=float)
    n = X.size
    J = np.zeros((n, n))

    for i in range(n):
        X_pos = X.copy()
        X_neg = X.copy()
        X_pos[i] += eps
        X_neg[i] -= eps
        J[:, i] = (operator(X_pos) - operator(X_neg)) / (2 * eps)

    return J


def frobenius_norm(J: np.ndarray) -> float:
    """Frobenius norm of a matrix J."""
    return float(np.linalg.norm(J, ord="fro"))


def verify_structural_integrity(X: np.ndarray, operator=default_operator, eps: float = 1e-5) -> float:
    """
    Convenience wrapper: compute the Jacobian of `operator` at X and
    return its Frobenius norm.
    """
    J = calculate_jacobian(X, operator=operator, eps=eps)
    return frobenius_norm(J)


if __name__ == "__main__":
    X = np.array([0.2, 0.5, -0.1])
    result = verify_structural_integrity(X)
    print("Frobenius Norm:", result)
