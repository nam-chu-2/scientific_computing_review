"""Value comparison for both answer modes.

The whole game grades by COMPARING VALUES, never by matching source text.
That is what lets multiple correct forms of an answer all pass: an
object-oriented form, a functional form, a comprehension, a NumPy call --
if it produces the right value under the right mode, it's correct.

Modes
-----
exact        array_equal / == ; dtype-agnostic. Ints, strings, lists, bools.
close        np.allclose on floats. Use for any real-valued result.
scalar       plain ==        ; tuples (shape), ints, dtype objects, bools.
array        np.array_equal  ; force ndarray semantics.
exact_dtype  values AND dtype must match (NumPy).
set          order-independent, duplicates ignored (set(a) == set(e)).
sorted       order-independent, duplicates kept (sorted(a) == sorted(e)).
pandas       Series/DataFrame .equals (values + index + dtype).
"""

from __future__ import annotations

import numpy as np


def compare(expected, actual, mode: str = "exact") -> bool:
    """True if `actual` matches `expected` under `mode`. Never raises."""
    try:
        if mode == "close":
            return bool(np.allclose(np.asarray(actual, dtype=float),
                                    np.asarray(expected, dtype=float)))
        if mode == "scalar":
            return bool(expected == actual)
        if mode == "array":
            return bool(np.array_equal(np.asarray(actual), np.asarray(expected)))
        if mode == "exact_dtype":
            a, e = np.asarray(actual), np.asarray(expected)
            return a.dtype == e.dtype and bool(np.array_equal(a, e))
        if mode == "set":
            return set(actual) == set(expected)
        if mode == "sorted":
            return list(sorted(actual)) == list(sorted(expected))
        if mode == "pandas":
            return bool(expected.equals(actual))
        # default: "exact" -- dtype-agnostic value match.
        if isinstance(expected, (np.ndarray, list, tuple)) or \
                isinstance(actual, (np.ndarray, list, tuple)):
            return bool(np.array_equal(np.asarray(actual), np.asarray(expected)))
        return bool(actual == expected)
    except Exception:
        return False


def base_namespace() -> dict:
    """A fresh namespace for evaluating answers.

    Always has numpy (`np`), `math`, and `statistics`. Adds pandas (`pd`)
    when it's installed, so pandas answers work and others don't break.
    """
    import math
    import statistics
    ns = {"np": np, "math": math, "statistics": statistics}
    try:
        import pandas as pd
        ns["pd"] = pd
    except ImportError:
        pass
    return ns


def fmt(value) -> str:
    """Compact one-line repr of a value for terminal display."""
    if isinstance(value, np.ndarray):
        text = np.array2string(value, separator=", ")
    else:
        text = repr(value)
    return " ".join(text.split())
