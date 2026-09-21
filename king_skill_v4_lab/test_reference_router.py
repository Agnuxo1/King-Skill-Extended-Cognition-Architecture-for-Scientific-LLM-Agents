"""Regression tests for the dependency-free reference router."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from keyword_router import route_task  # noqa: E402


class ReferenceRouterTests(unittest.TestCase):
    def test_arxiv_bibtex_request_is_not_misclassified_as_latex(self) -> None:
        prompt = "Fetch arXiv:2401.00001 abstract and BibTeX via arxiv.org API."
        self.assertEqual(route_task(prompt), "skill-03-arxiv-fetch")

    def test_symbolic_integral_uses_sympy(self) -> None:
        self.assertEqual(
            route_task("Simplify the integral symbolically and give a closed form."),
            "skill-09-sympy",
        )

    def test_numeric_fft_uses_python_executor(self) -> None:
        self.assertEqual(
            route_task("Compute an FFT with NumPy."),
            "skill-01-python-executor",
        )

    def test_simulation_uses_scipy_skill(self) -> None:
        self.assertEqual(
            route_task("Simulate a Lorenz ODE with solve_ivp."),
            "skill-07-scipy-sim",
        )

    def test_unmatched_prompt_uses_fallback(self) -> None:
        self.assertEqual(route_task("Discuss epistemology without invoking tools."), "fallback")


if __name__ == "__main__":
    unittest.main()
