"""QUARANTINED answer key + hidden tests.  DO NOT OPEN until after you've tried.

The game reads this file to GRADE your answers, but never displays anything
here until you reveal it (a wrong answer, `explain`, or `skip`). Opening it
yourself defeats the retrieval practice -- that's on you.

Schema per question id:

  cli     -> {"setup": <code or "">, "canonical": <one expression>,
              "compare": <mode>}
  script  -> {"entry": <function name>, "canonical": <full source>,
              "compare": <default mode>, "cases": [...],
              "max_loops": <int|None>, "forbid": [<substr>, ...]}

  case    -> {"args": [...] | "sequence": [[...], ...],
              "expected": <value>, "visible": <bool>, "label": <str>,
              "compare": <mode override, optional>}

Comparison modes are documented in engine/compare.py.
"""

import math  # noqa: F401 -- available to canonical expressions if needed

GRADING = {

    # ================================================================
    # Tier 1 -- Fastballs (cli)
    # ================================================================
    "t1-total-rainfall": {
        "setup": "rain = [12, 0, 5, 8, 3]",
        "canonical": "sum(rain)", "compare": "exact"},
    "t1-mean-temp": {
        "setup": "temps = [18, 21, 19, 24, 22]",
        "canonical": "sum(temps) / len(temps)", "compare": "close"},
    "t1-count-records": {
        "setup": "survey = ['yes', 'no', 'yes', 'maybe', 'no', 'yes']",
        "canonical": "len(survey)", "compare": "exact"},
    "t1-last-price": {
        "setup": "prices = [101.2, 99.8, 103.5, 102.1]",
        "canonical": "prices[-1]", "compare": "close"},
    "t1-first-three": {
        "setup": "readings = [7, 4, 9, 2, 8, 5]",
        "canonical": "readings[:3]", "compare": "exact"},
    "t1-reverse-series": {
        "setup": "series = [1, 2, 3, 4, 5]",
        "canonical": "series[::-1]", "compare": "exact"},
    "t1-upper-code": {
        "setup": "code = 'yyz'",
        "canonical": "code.upper()", "compare": "exact"},
    "t1-normalize-label": {
        "setup": "label = 'Housing'",
        "canonical": "label.lower()", "compare": "exact"},
    "t1-money-format": {
        "setup": "amount = 1234.5",
        "canonical": "f'${amount:.2f}'", "compare": "exact"},
    "t1-parse-double": {
        "setup": "raw = '42'",
        "canonical": "int(raw) * 2", "compare": "exact"},
    "t1-is-even": {
        "setup": "n = 7",
        "canonical": "n % 2 == 0", "compare": "scalar"},
    "t1-full-pages": {
        "setup": "total = 47",
        "canonical": "total // 10", "compare": "exact"},
    "t1-round-rate": {
        "setup": "rate = 0.18342",
        "canonical": "round(rate, 2)", "compare": "close"},
    "t1-arange-evens": {
        "setup": "",
        "canonical": "np.arange(0, 10, 2)", "compare": "exact"},
    "t1-cumprod-growth": {
        "setup": "factors = np.array([2, 3, 4])",
        "canonical": "np.cumprod(factors)", "compare": "exact"},
    "t1-max-peak": {
        "setup": "load = [3.1, 4.8, 4.2, 5.6, 5.0]",
        "canonical": "max(load)", "compare": "close"},
    "t1-membership": {
        "setup": "pollutants = ['NO2', 'CO2', 'PM25', 'O3']",
        "canonical": "'CO2' in pollutants", "compare": "scalar"},
    "t1-dict-lookup": {
        "setup": "pop = {'ON': 14.8, 'QC': 8.6, 'BC': 5.2}",
        "canonical": "pop['ON']", "compare": "close"},

    # ================================================================
    # Tier 2 -- Mixed pitches
    # ================================================================
    # --- cli ---
    "t2-filter-threshold": {
        "setup": "readings = [10, 35, 12, 55, 41]",
        "canonical": "[r for r in readings if r > 35]", "compare": "exact"},
    "t2-share-pct": {
        "setup": "vals = [40, 30, 30]",
        "canonical": "[round(v / sum(vals) * 100, 1) for v in vals]",
        "compare": "close"},
    "t2-dot-weighted": {
        "setup": "w = np.array([0.2, 0.3, 0.5])\nr = np.array([10.0, 5.0, 8.0])",
        "canonical": "w @ r", "compare": "close"},

    # --- script ---
    "t2-count-above": {
        "entry": "count_unhealthy", "compare": "exact", "max_loops": None,
        "canonical":
            "def count_unhealthy(readings, limit):\n"
            "    n = 0\n"
            "    for r in readings:\n"
            "        if r > limit:\n"
            "            n += 1\n"
            "    return n",
        "cases": [
            {"args": [[10, 35, 12, 55, 55], 35], "expected": 2,
             "visible": True, "label": "two above 35"},
            {"args": [[], 10], "expected": 0,
             "visible": True, "label": "empty list"},
            {"args": [[5, 5, 5], 5], "expected": 0,
             "label": "all equal to limit -> strict >"},
            {"args": [[-3, -1, 0, 2], -1], "expected": 2,
             "label": "negatives"},
            {"args": [[1.5, 2.5, 3.5], 2.0], "expected": 2,
             "label": "floats"},
        ]},
    "t2-season": {
        "entry": "season", "compare": "exact", "max_loops": None,
        "canonical":
            "def season(month, day):\n"
            "    md = (month, day)\n"
            "    if (3, 20) <= md <= (6, 20):\n"
            "        return 'Spring'\n"
            "    if (6, 21) <= md <= (9, 22):\n"
            "        return 'Summer'\n"
            "    if (9, 23) <= md <= (12, 20):\n"
            "        return 'Fall'\n"
            "    return 'Winter'",
        "cases": [
            {"args": [3, 19], "expected": "Winter", "visible": True,
             "label": "Mar 19 -> Winter"},
            {"args": [3, 21], "expected": "Spring", "visible": True,
             "label": "Mar 21 -> Spring"},
            {"args": [7, 1], "expected": "Summer", "visible": True,
             "label": "Jul 1 -> Summer"},
            {"args": [6, 20], "expected": "Spring", "label": "Jun 20 boundary"},
            {"args": [6, 21], "expected": "Summer", "label": "Jun 21 boundary"},
            {"args": [9, 23], "expected": "Fall", "label": "Sep 23 boundary"},
            {"args": [12, 21], "expected": "Winter", "label": "Dec 21 boundary"},
            {"args": [1, 5], "expected": "Winter", "label": "Jan -> Winter"},
            {"args": [12, 20], "expected": "Fall", "label": "Dec 20 -> Fall"},
        ]},
    "t2-second-largest": {
        "entry": "second_largest", "compare": "exact", "max_loops": None,
        "canonical":
            "def second_largest(xs):\n"
            "    distinct = sorted(set(xs))\n"
            "    return distinct[-2]",
        "cases": [
            {"args": [[4, 7, 7, 1, 5]], "expected": 5, "visible": True,
             "label": "duplicates ignored"},
            {"args": [[10, 20]], "expected": 10, "visible": True,
             "label": "two values"},
            {"args": [[5, 4, 3, 2, 1]], "expected": 4, "label": "descending"},
            {"args": [[-1, -2, -3]], "expected": -2, "label": "negatives"},
            {"args": [[100, 1, 100, 50]], "expected": 50, "label": "dup max"},
            {"args": [[2, 2, 2, 9]], "expected": 2, "label": "many dups"},
        ]},
    "t2-tip-total": {
        "entry": "total_with_tip", "compare": "exact", "max_loops": None,
        "canonical":
            "def total_with_tip(bill, tip_pct):\n"
            "    total = bill * (1 + tip_pct / 100)\n"
            "    return f'${total:.2f}'",
        "cases": [
            {"args": [27.95, 17], "expected": "$32.70", "visible": True,
             "label": "27.95 + 17%"},
            {"args": [10, 0], "expected": "$10.00", "visible": True,
             "label": "no tip, padded"},
            {"args": [100, 25], "expected": "$125.00", "label": "round amount"},
            {"args": [50, 10], "expected": "$55.00", "label": "10%"},
            {"args": [19.99, 20], "expected": "$23.99", "label": "rounding"},
        ]},
    "t2-times-table": {
        "entry": "times_table", "compare": "exact", "max_loops": None,
        "canonical":
            "def times_table(n):\n"
            "    table = []\n"
            "    for i in range(n):\n"
            "        row = []\n"
            "        for j in range(n):\n"
            "            row.append((i + 1) * (j + 1))\n"
            "        table.append(row)\n"
            "    return table",
        "cases": [
            {"args": [2], "expected": [[1, 2], [2, 4]], "visible": True,
             "label": "2 x 2"},
            {"args": [1], "expected": [[1]], "visible": True, "label": "1 x 1"},
            {"args": [3], "expected": [[1, 2, 3], [2, 4, 6], [3, 6, 9]],
             "label": "3 x 3"},
            {"args": [0], "expected": [], "label": "empty table"},
        ]},
    "t2-valid-guess": {
        "entry": "is_valid_guess", "compare": "scalar", "max_loops": None,
        "canonical":
            "def is_valid_guess(s):\n"
            "    return len(s) == 1 and s.isalpha()",
        "cases": [
            {"args": ["a"], "expected": True, "visible": True,
             "label": "single letter"},
            {"args": ["ab"], "expected": False, "visible": True,
             "label": "two chars"},
            {"args": ["1"], "expected": False, "visible": True,
             "label": "a digit"},
            {"args": [""], "expected": False, "label": "empty string"},
            {"args": ["Q"], "expected": True, "label": "uppercase letter"},
            {"args": [" "], "expected": False, "label": "a space"},
            {"args": ["!"], "expected": False, "label": "punctuation"},
        ]},

    # ================================================================
    # Tier 3 -- Breaking balls
    # ================================================================
    "t3-vec-zscore": {
        "entry": "zscore", "compare": "close", "max_loops": 0,
        "canonical":
            "import numpy as np\n\n"
            "def zscore(xs):\n"
            "    a = np.asarray(xs, dtype=float)\n"
            "    return (a - a.mean()) / a.std()",
        "cases": [
            {"args": [[1, 2, 3, 4, 5]],
             "expected": [-1.4142135623730951, -0.7071067811865476, 0.0,
                          0.7071067811865476, 1.4142135623730951],
             "visible": True, "label": "1..5"},
            {"args": [[10, 10, 10, 20]],
             "expected": [-0.5773502691896257, -0.5773502691896257,
                          -0.5773502691896257, 1.7320508075688772],
             "label": "repeated values"},
            {"args": [[-2, -1, 0, 1, 2]],
             "expected": [-1.4142135623730951, -0.7071067811865476, 0.0,
                          0.7071067811865476, 1.4142135623730951],
             "label": "symmetric, negatives"},
        ]},
    "t3-vec-poly": {
        "entry": "poly", "compare": "close", "max_loops": 0,
        "canonical":
            "import numpy as np\n\n"
            "def poly(x, coef):\n"
            "    coef = np.asarray(coef, dtype=float)\n"
            "    powers = x ** np.arange(len(coef))\n"
            "    return coef @ powers",
        "cases": [
            {"args": [2, [1, 1, 1]], "expected": 7.0, "visible": True,
             "label": "1 + 2 + 4"},
            {"args": [0, [5, 9, 9]], "expected": 5.0, "visible": True,
             "label": "x = 0 -> constant"},
            {"args": [3, [2, 0, 1]], "expected": 11.0, "label": "2 + 9"},
            {"args": [2, [0, 0, 0, 1]], "expected": 8.0, "label": "x^3"},
            {"args": [-1, [1, 1, 1, 1]], "expected": 0.0, "label": "alternating"},
        ]},
    "t3-vec-cumsum": {
        "entry": "running_total", "compare": "exact", "max_loops": 0,
        "canonical":
            "import numpy as np\n\n"
            "def running_total(xs):\n"
            "    return np.cumsum(xs)",
        "cases": [
            {"args": [[3, 1, 4]], "expected": [3, 4, 8], "visible": True,
             "label": "basic"},
            {"args": [[1, 1, 1, 1]], "expected": [1, 2, 3, 4], "label": "ones"},
            {"args": [[5]], "expected": [5], "label": "single"},
            {"args": [[2, -2, 2, -2]], "expected": [2, 0, 2, 0],
             "label": "with negatives"},
        ]},
    "t3-normalize-rows": {
        "entry": "normalize_rows", "compare": "close", "max_loops": 0,
        "canonical":
            "import numpy as np\n\n"
            "def normalize_rows(mat):\n"
            "    a = np.asarray(mat, dtype=float)\n"
            "    return a / a.sum(axis=1, keepdims=True)",
        "cases": [
            {"args": [[[1, 1], [1, 3]]],
             "expected": [[0.5, 0.5], [0.25, 0.75]],
             "visible": True, "label": "two rows"},
            {"args": [[[2, 2, 4]]],
             "expected": [[0.25, 0.25, 0.5]], "label": "one row"},
            {"args": [[[1, 0], [0, 5]]],
             "expected": [[1.0, 0.0], [0.0, 1.0]], "label": "diagonal-ish"},
        ]},
    "t3-bug-misclass": {
        "entry": "mismatches", "compare": "scalar", "max_loops": None,
        "canonical":
            "def mismatches(pred, true):\n"
            "    count = 0\n"
            "    for i in range(len(pred)):\n"
            "        if pred[i] != true[i]:\n"
            "            count += 1\n"
            "    return count",
        "cases": [
            {"args": [["cat", "dog", "cat"], ["cat", "dog", "fish"]],
             "expected": 1, "visible": True, "label": "one wrong"},
            {"args": [["a", "b", "c"], ["a", "b", "x"]], "expected": 1,
             "label": "mismatch in LAST position"},
            {"args": [[1, 2, 3], [1, 2, 3]], "expected": 0, "label": "identical"},
            {"args": [[1, 2, 3], [4, 5, 6]], "expected": 3, "label": "all differ"},
            {"args": [["x"], ["y"]], "expected": 1, "label": "single element"},
        ]},
    "t3-bug-mutable-default": {
        "entry": "add_reading", "compare": "exact", "max_loops": None,
        "canonical":
            "def add_reading(value, log=None):\n"
            "    if log is None:\n"
            "        log = []\n"
            "    log.append(value)\n"
            "    return log",
        "cases": [
            {"sequence": [[10], [20]], "expected": [20], "visible": True,
             "label": "second call starts fresh"},
            {"args": [5], "expected": [5], "label": "isolated call stays clean"},
            {"sequence": [[1], [2], [3]], "expected": [3],
             "label": "third call fresh"},
            {"args": [99], "expected": [99], "label": "still isolated"},
        ]},
    "t3-bug-pct": {
        "entry": "pct", "compare": "close", "max_loops": None,
        "canonical":
            "def pct(part, whole):\n"
            "    return part / whole * 100",
        "cases": [
            {"args": [1, 4], "expected": 25.0, "visible": True, "label": "1 of 4"},
            {"args": [3, 4], "expected": 75.0, "visible": True, "label": "3 of 4"},
            {"args": [1, 8], "expected": 12.5, "label": "1 of 8"},
            {"args": [5, 5], "expected": 100.0, "label": "whole"},
            {"args": [0, 10], "expected": 0.0, "label": "zero part"},
        ]},
    "t3-dedup-fast": {
        "entry": "unique_preserve", "compare": "exact", "max_loops": 1,
        "forbid": [".count(", "xs[:"],
        "canonical":
            "def unique_preserve(xs):\n"
            "    seen = set()\n"
            "    result = []\n"
            "    for x in xs:\n"
            "        if x not in seen:\n"
            "            seen.add(x)\n"
            "            result.append(x)\n"
            "    return result",
        "cases": [
            {"args": [["a", "b", "a", "c", "b"]], "expected": ["a", "b", "c"],
             "visible": True, "label": "order preserved"},
            {"args": [[]], "expected": [], "label": "empty"},
            {"args": [[1, 1, 1]], "expected": [1], "label": "all same"},
            {"args": [[3, 1, 2, 3, 1]], "expected": [3, 1, 2],
             "label": "first-seen order"},
            {"args": [list(range(200)) + list(range(200))],
             "expected": list(range(200)), "label": "large input (O(n))"},
        ]},
    "t3-twosum": {
        "entry": "has_pair_sum", "compare": "scalar", "max_loops": 1,
        "canonical":
            "def has_pair_sum(xs, target):\n"
            "    seen = set()\n"
            "    for x in xs:\n"
            "        if target - x in seen:\n"
            "            return True\n"
            "        seen.add(x)\n"
            "    return False",
        "cases": [
            {"args": [[2, 7, 11, 15], 9], "expected": True, "visible": True,
             "label": "2 + 7 = 9"},
            {"args": [[1, 2, 3], 7], "expected": False, "visible": True,
             "label": "no pair"},
            {"args": [[3, 3], 6], "expected": True, "label": "two 3s"},
            {"args": [[3], 6], "expected": False,
             "label": "single element, no double-count"},
            {"args": [[0, 4, 3, 0], 0], "expected": True, "label": "two zeros"},
            {"args": [[-1, 5, 4], 3], "expected": True, "label": "negative"},
        ]},
    "t3-bug-running-mean": {
        "entry": "running_mean", "compare": "close", "max_loops": None,
        "canonical":
            "def running_mean(xs):\n"
            "    out, total = [], 0\n"
            "    for i, x in enumerate(xs):\n"
            "        total += x\n"
            "        out.append(total / (i + 1))\n"
            "    return out",
        "cases": [
            {"args": [[2, 4, 6]], "expected": [2.0, 3.0, 4.0], "visible": True,
             "label": "running average"},
            {"args": [[5]], "expected": [5.0], "label": "single (no div by 0)"},
            {"args": [[10, 0]], "expected": [10.0, 5.0], "label": "two items"},
            {"args": [[1, 2, 3, 4]], "expected": [1.0, 1.5, 2.0, 2.5],
             "label": "four items"},
        ]},
}


# ----------------------------------------------------------------------
# pandas-gated questions: only registered when pandas is installed (the
# bank drops the matching question otherwise, so the two stay consistent).
# ----------------------------------------------------------------------
try:
    import pandas as pd

    _rent_df = pd.DataFrame({
        "city": ["Ottawa", "Ottawa", "Toronto", "Toronto"],
        "rent": [2000.0, 2200.0, 2400.0, 2600.0],
    })
    GRADING["t2-avg-rent"] = {
        "entry": "avg_rent", "compare": "close", "max_loops": None,
        "canonical":
            "def avg_rent(df, city):\n"
            "    return df[df['city'] == city]['rent'].mean()",
        "cases": [
            {"args": [_rent_df, "Ottawa"], "expected": 2100.0, "visible": True,
             "label": "mean Ottawa rent"},
            {"args": [_rent_df, "Toronto"], "expected": 2500.0,
             "label": "mean Toronto rent"},
        ]}
except ImportError:
    pass
