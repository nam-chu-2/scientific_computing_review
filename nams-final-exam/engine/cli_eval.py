"""Grading for `mode: cli` questions -- single-expression answers.

The expected value is produced by evaluating the QUARANTINED canonical
expression (loaded from solutions/), never shown to the player. The
player's expression is evaluated in an independent namespace and compared
by VALUE, so any expression with the right result is accepted.
"""

from __future__ import annotations

from .compare import base_namespace, compare


def expected_value(grading: dict):
    """Evaluate the canonical answer to get the expected value."""
    ns = base_namespace()
    if grading.get("setup"):
        exec(grading["setup"], ns)
    return eval(grading["canonical"], ns)


def evaluate(grading: dict, user_expr: str):
    """Evaluate a player's expression and grade it.

    Returns (ok, actual, expected). Raises on syntax/runtime errors in the
    player's expression so the caller can re-prompt without penalty.
    """
    expected = expected_value(grading)

    ns = base_namespace()
    if grading.get("setup"):
        exec(grading["setup"], ns)
    actual = eval(user_expr, ns)            # may raise -> caller re-prompts

    return compare(expected, actual, grading.get("compare", "exact")), actual, expected
