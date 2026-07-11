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

"""
tests/test_jacobian.py

Real pytest test suite (assertions, not just print statements).

Design notes:
- test_jacobian_matches_known_linear_operator is the most important test
  here: for a linear operator R(X) = A @ X, the true Jacobian is exactly
  A everywhere. Comparing the finite-difference estimate against that
  known-correct answer validates that calculate_jacobian() is actually
  correct, not just "runs without crashing."
- The other tests cover shape correctness, numerical stability
  (finite/no NaNs), and basic edge cases (zero vector, single element).
"""

import numpy as np
import pytest

from jacobian_tools import (
    calculate_jacobian,
    frobenius_norm,
    verify_structural_integrity,
    default_operator,
)


def test_jacobian_shape():
    X = np.array([0.2, 0.5, -0.1])
    J = calculate_jacobian(X)
    assert J.shape == (3, 3)


def test_jacobian_matches_known_linear_operator():
    """
    Ground-truth check: for R(X) = A @ X, the exact Jacobian is A.
    This validates correctness, not just shape.
    """
    rng = np.random.default_rng(42)
    A = rng.standard_normal((4, 4))

    def linear_operator(X):
        return A @ X

    X = rng.standard_normal(4)
    J = calculate_jacobian(X, operator=linear_operator, eps=1e-5)

    np.testing.assert_allclose(J, A, atol=1e-6)


def test_frobenius_norm_known_value():
    J = np.array([[3.0, 0.0], [0.0, 4.0]])
    assert frobenius_norm(J) == pytest.approx(5.0)


def test_verify_structural_integrity_matches_manual_computation():
    X = np.array([0.2, 0.5, -0.1])
    J = calculate_jacobian(X, operator=default_operator)
    expected = np.linalg.norm(J, ord="fro")
    result = verify_structural_integrity(X)
    assert result == pytest.approx(expected)


def test_output_is_finite():
    X = np.array([10.0, -10.0, 5.0])
    result = verify_structural_integrity(X)
    assert np.isfinite(result)


def test_zero_vector_does_not_crash():
    X = np.zeros(3)
    result = verify_structural_integrity(X)
    assert np.isfinite(result)
    assert result >= 0.0


def test_single_element_vector():
    X = np.array([1.0])
    J = calculate_jacobian(X)
    assert J.shape == (1, 1)


def test_frobenius_norm_is_nonnegative():
    rng = np.random.default_rng(0)
    X = rng.standard_normal(5)
    result = verify_structural_integrity(X)
    assert result >= 0.0

numpy>=1.24
pytest>=7.0

