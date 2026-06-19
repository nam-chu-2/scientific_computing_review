"""Grading for `mode: script` questions -- you write a function body.

A pytest-style harness: each question carries a list of test CASES (some
visible, most hidden). The player edits attempts/<id>.py; on `check` we:

  1. optionally enforce a STRUCTURAL constraint (e.g. "no explicit loops"
     for vectorize questions, via an AST scan -- robust to whitespace and
     to the word "for" appearing inside identifiers);
  2. import their function;
  3. run every case and report pass/fail PER CASE.

Hidden cases never reveal their inputs or expected output -- only
visible cases show "you got X, expected Y". The canonical solution and
the full case list live in solutions/ (quarantined); this module is the
only thing that reads them, and it never prints them.

No hard dependency on the `pytest` package: the case runner is pure
stdlib so `check` always works. (solutions/test_bank.py uses real pytest
to self-verify the bank; that's optional and for maintenance.)
"""

from __future__ import annotations

import ast
import copy

from .compare import base_namespace, compare, fmt


# Node types that represent an explicit Python-level loop. Comprehensions
# count too: "vectorize this" means push the loop into NumPy, and a
# comprehension is still a Python loop.
_LOOP_NODES = (ast.For, ast.AsyncFor, ast.While,
               ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


def count_loops(source: str) -> int:
    """Number of explicit loop / comprehension constructs in `source`."""
    tree = ast.parse(source)
    return sum(isinstance(node, _LOOP_NODES) for node in ast.walk(tree))


def _structural_check(source: str, grading: dict):
    """Return an error string if a structural constraint is violated, else None."""
    max_loops = grading.get("max_loops")
    if max_loops is not None:
        try:
            n = count_loops(source)
        except SyntaxError as exc:
            return f"your code has a syntax error: {exc}"
        if n > max_loops:
            if max_loops == 0:
                return ("this drill wants it VECTORIZED -- no for/while loops "
                        "or comprehensions. Push the work into array operations.")
            return (f"this drill allows at most {max_loops} loop(s); "
                    f"found {n}. Aim for a lower-complexity approach.")
    for bad in grading.get("forbid", []):
        if bad in source:
            return f"this drill doesn't allow `{bad}` -- find another approach."
    return None


def _load_function(source: str, path: str, entry: str):
    """Exec the attempt and return (fn, error). fn is None on failure."""
    ns = base_namespace()
    try:
        exec(compile(source, path, "exec"), ns)
    except Exception as exc:  # noqa: BLE001 -- surface any import/run error
        return None, f"your code didn't run: {type(exc).__name__}: {exc}"
    fn = ns.get(entry)
    if not callable(fn):
        return None, f"couldn't find a function named `{entry}` in your file."
    return fn, None


def _run_case(fn, case, default_mode="exact"):
    """Run one case. Returns (ok, got, error)."""
    mode = case.get("compare", default_mode)
    try:
        if "sequence" in case:
            # Call fn repeatedly (same function object -> catches shared
            # mutable-default-argument bugs); grade the LAST return value.
            got = None
            for args in case["sequence"]:
                got = fn(*copy.deepcopy(args))
        else:
            got = fn(*copy.deepcopy(case.get("args", [])))
    except Exception as exc:  # noqa: BLE001
        return False, None, f"{type(exc).__name__}: {exc}"
    return compare(case["expected"], got, mode), got, None


def run_checks(source: str, path: str, grading: dict) -> dict:
    """Grade an attempt. Returns a structured report (no spoilers in it)."""
    structural = _structural_check(source, grading)
    if structural:
        return {"ok": False, "passed": 0, "total": len(grading["cases"]),
                "structural_error": structural, "cases": []}

    fn, err = _load_function(source, path, grading["entry"])
    if err:
        return {"ok": False, "passed": 0, "total": len(grading["cases"]),
                "load_error": err, "cases": []}

    default_mode = grading.get("compare", "exact")
    results = []
    for i, case in enumerate(grading["cases"], 1):
        ok, got, error = _run_case(fn, case, default_mode)
        visible = case.get("visible", False)
        row = {"n": i, "ok": ok, "visible": visible,
               "label": case.get("label", f"case {i}")}
        if error:
            row["error"] = error
        if visible:                      # only visible cases reveal details
            row["got"] = fmt(got) if error is None else None
            row["expected"] = fmt(case["expected"])
            if "sequence" in case:
                row["calls"] = [fmt(a) for a in case["sequence"]]
            else:
                row["args"] = [fmt(a) for a in case.get("args", [])]
        results.append(row)

    passed = sum(r["ok"] for r in results)
    return {"ok": passed == len(results), "passed": passed,
            "total": len(results), "cases": results}


def run_only(source: str, path: str, grading: dict) -> str:
    """Run the attempt WITHOUT grading (the `run` command). Returns output text."""
    fn, err = _load_function(source, path, grading["entry"])
    if err:
        return err
    # Demonstrate on the first visible case's input, if any.
    sample = next((c for c in grading["cases"] if c.get("visible")), None)
    if sample is None:
        return f"`{grading['entry']}` defined OK. (no sample input to demo)"
    try:
        if "sequence" in sample:
            got = None
            for args in sample["sequence"]:
                got = fn(*copy.deepcopy(args))
            call = " then ".join(f"{grading['entry']}({', '.join(map(fmt, a))})"
                                 for a in sample["sequence"])
        else:
            args = sample.get("args", [])
            got = fn(*copy.deepcopy(args))
            call = f"{grading['entry']}({', '.join(map(fmt, args))})"
    except Exception as exc:  # noqa: BLE001
        return f"ran, but raised: {type(exc).__name__}: {exc}"
    return f"{call}  ->  {fmt(got)}"
