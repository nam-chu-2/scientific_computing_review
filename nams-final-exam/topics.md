# Nam's Final Exam — Topic Taxonomy

This is the **review map** for the practice game. It is built from your actual
course materials, then extended with a small number of topics an employer would
expect for a data-science role. **Review this and tell me what to keep, cut, or
re-weight before I generate the full question bank.**

## Where these came from

| Tag | Source |
|-----|--------|
| `[T1]` | COMP 1005/1405 — Winter 2022, Tutorial 1 (setup, print, input, variables, math, algorithm design) |
| `[T2]` | Tutorial 2 (type conversion, rounding, string formatting, escape chars, `.lower/.upper`, `len`) |
| `[T3]` | Tutorial 3 (conditionals, boolean logic, `//` & `%`, input validation, `.isalpha/.isdigit`) |
| `[T4]` | Tutorial 4 (`for`/`while`, nested loops, `range`, iterating strings, accumulator, Hamming distance) |
| `[NB]` | `10-numpy.ipynb` (arrays, indexing, `cumprod`, `@`/dot, `ones_like`, vectorizing a loop) |
| `[extension]` | **Not in your materials.** Added for DS-internship readiness. Keep or cut freely. |

**Theming:** every question is flavored with realistic data-science / economics /
public-sector-data scenarios (rainfall & emissions readings, rent prices, survey
records, station logs, CPI baskets) — never `foo`/`bar`. Performance / "interview
gotcha" / algorithmic-complexity material is pushed into **Tier 3**.

**Tiers (baseball metaphor):** **T1 Fastballs** = atomic recall, one skill, fast
(mostly `cli` one-liners). **T2 Mixed pitches** = combine 2–3 concepts (`cli` or
small `script`). **T3 Breaking balls** = gotchas, debugging, edge cases, vectorize,
Big-O (mostly `script`).

---

## Theme 1 — I/O & program basics  `[T1] [T2]`

| Topic | Source | Tier | Mode | Notes |
|-------|--------|------|------|-------|
| `print` (sep, end) | T1, T4 | 1 | cli | `print(a, b, sep=", ")`, `end=""` to suppress newline |
| `input()` + capturing to a variable | T1 | 1 | cli | always returns a **string** |
| variables & assignment | T1 | 1 | cli | naming, reassignment |
| comments | T1 | — | — | covered but not worth drilling |

## Theme 2 — Numbers, operators & type conversion  `[T1] [T2] [T3]`

| Topic | Source | Tier | Mode | Notes |
|-------|--------|------|------|-------|
| arithmetic `+ - * / ** ` | T1 | 1 | cli | incl. `y = m*x + b` style eval |
| integer division `//` and modulo `%` | T3 | 1–2 | cli | quotient + remainder, `divmod()` |
| operator precedence | T1, T2 | 2 | cli | classic gotcha (push edge cases to T3) |
| `round(x, ndigits)` | T2 | 1 | cli | banker's rounding gotcha → T3 |
| type conversion `int()` `float()` `str()` | T2 | 1 | cli | `int("12")`, `str(n)` for concatenation |

## Theme 3 — Strings  `[T2] [T3] [T4]`

| Topic | Source | Tier | Mode | Notes |
|-------|--------|------|------|-------|
| concatenation & repetition | T2 | 1 | cli | `"$" + str(n)`, `"-"*10` |
| indexing & slicing | T4 | 1–2 | cli | `s[0]`, `s[1:]`, `s[::-1]` |
| escape sequences `\n \t \\` | T2 | 1 | cli | the hangman/backslash gotcha |
| `len()` | T2 | 1 | cli | and "do it **without** `len`" → T2/T3 script |
| case methods `.lower() .upper()` | T2 | 1 | cli | case-insensitive matching |
| validators `.isalpha() .isdigit()` | T3 | 1 | cli | input validation building block |
| f-strings / `format` (2 decimals, padding) | T2 | 1–2 | cli | `f"${x:.2f}"`, column alignment |
| count occurrences of a char | T4 | 2 | script | accumulator over a string |

## Theme 4 — Conditionals & boolean logic  `[T3]`

| Topic | Source | Tier | Mode | Notes |
|-------|--------|------|------|-------|
| `if` / `elif` / `else` | T3 | 1–2 | cli/script | season-from-date, grade buckets |
| comparison operators | T3 | 1 | cli | `==`, `!=`, chained `a < x <= b` |
| boolean ops `and` / `or` / `not` | T3 | 1–2 | cli | combining range checks |
| input validation (number? in range?) | T3 | 2 | script | guard clauses |
| multi-branch dispatch | T3 | 2 | script | calculator (A/S/M/D) pattern |

## Theme 5 — Loops & iteration  `[T4]`

| Topic | Source | Tier | Mode | Notes |
|-------|--------|------|------|-------|
| `for` + `range()` | T4 | 1 | cli | sum/loop over a range |
| `while` + sentinel / `break` | T4 | 2 | script | "read until 'quit'" loop |
| nested loops | T4 | 2 | script | multiplication table, reveal-one-char |
| accumulator pattern (sum/count/max) | T4 | 1–2 | cli/script | the DS workhorse |
| iterate a string / sequence | T4 | 1 | cli | `for ch in s` |
| build a string incrementally | T4 | 2 | script | progressive reveal |

## Theme 6 — Algorithmic thinking & complexity  `[T1] [T4]`

| Topic | Source | Tier | Mode | Notes |
|-------|--------|------|------|-------|
| find max / 2nd largest in a list | T1 | 2 | script | one-pass scan |
| Hamming distance of two strings | T4 | 2 | script | element-wise compare + validation |
| pattern analysis (line ↔ length math) | T4 | 2 | script | reveal-the-word |
| reason about Big-O `[extension]` | — | 3 | cli/script | "what's the complexity?", O(n²)→O(n) |
| computational thinking / decomposition | T1, T2 | — | — | meta-skill; baked into prompts, not drilled directly |

## Theme 7 — NumPy & vectorization  `[NB]`

| Topic | Source | Tier | Mode | Notes |
|-------|--------|------|------|-------|
| array creation & dtype | NB | 1 | cli | `np.array`, `ones_like`, `arange` |
| indexing & slicing | NB | 1 | cli | `X[1]`, boolean masks `[extension]` |
| `cumprod` / `cumsum` | NB | 1 | cli | your polynomial exercise |
| dot / `@` / matrix-vector | NB | 2 | cli/script | `coef @ powers` |
| **vectorize a Python loop** | NB | 3 | script | the headline T3 skill: replace a loop with array ops |
| aggregations `sum/mean/std/argmax` `[extension]` | — | 1–2 | cli | core DS reductions |

---

## `[extension]` themes — not in your materials (keep or cut)

These aren't in COMP 1005/1405 or the notebook, but a DS-internship interviewer
would likely probe them. Marked so you can prune.

| Theme | Topics | Tier | Mode | Why include |
|-------|--------|------|------|-------------|
| **Functions & scope** | `def`, parameters, `return`, default args, local vs global | 1–2 | cli/script | Only *lightly* present (the notebook defines `p(x, coef)`); worth making explicit |
| **Data structures** | `list`, `dict`, `set`, `tuple`; methods; membership `in` | 1–2 | cli/script | Daily DS work; dict-counting is a top interview pattern |
| **Comprehensions** | list/dict/set comprehensions, conditional comps | 2 | cli | The Pythonic replacement for the T4 accumulator loops |
| **Error handling** | `try`/`except`, `ValueError` from `int()` | 2 | script | Robust input parsing (ties to T3 validation) |
| **File & data I/O** | `open`, read/write, `csv` module | 2–3 | script | Loading a dataset = step 1 of every DS task |
| **Sorting & searching** | `sorted(key=...)`, linear vs binary search | 2–3 | script | Classic interview material |
| **pandas** | `Series`/`DataFrame`, select, filter, `groupby`, `mean` | 1–2 | cli | Your stated stack; mirrors the numpy-gym pandas drills |
| **SQL** | `SELECT`/`WHERE`/`GROUP BY`/`ORDER BY`/aggregates | 1–2 | script | Your stated stack; gradeable in-process via `sqlite3` |

---

## Open questions for you (answer any, or just say "looks good")

1. **Extensions:** keep all, or cut some? My instinct: **keep** functions, data
   structures, comprehensions, pandas; treat **SQL** as a stretch (needs its own
   `sqlite3` checker) and **file I/O** as optional.
2. **Weighting:** roughly how many questions total, and should it lean toward
   pure-Python fundamentals (the actual coursework) or DS extensions (the job)?
3. **SQL:** want it in this game at all, or keep this Python-only and do SQL
   separately?
