"""Coaching helpers for Tier 1 drills.

Two ways to ask about the question you just did:

- `explain(rep)`  -> always-offline. Returns built-in notes for the rep's
  concept plus the canonical answer. No network, no API key, pure NumPy.

- `ask(rep, question)` -> free-form Q&A. Uses the Claude API when the
  `anthropic` SDK is installed AND a key is available (ANTHROPIC_API_KEY or
  ANTHROPIC_AUTH_TOKEN); otherwise returns None so the caller can fall back
  to `explain`.

Enabling live Q&A:
    pip install anthropic
    set ANTHROPIC_API_KEY=sk-ant-...      (PowerShell: $env:ANTHROPIC_API_KEY="...")
Optional model override:  set NUMPY_GYM_MODEL=claude-sonnet-4-6
"""

from __future__ import annotations

import os


# ----------------------------------------------------------------------
# Offline notes, keyed by generator topic
# ----------------------------------------------------------------------

NOTES = {
    "array1d":
        "np.array(list) builds an ndarray from a Python list. A flat list "
        "gives a 1-D array; dtype is inferred from the values (all ints -> "
        "int64, any float -> float64).",
    "array2d":
        "A list OF lists makes a 2-D array; each inner list is one row. All "
        "rows must be the same length, or you get an object array / error.",
    "array3d":
        "Nesting three deep makes a 3-D array with shape (blocks, rows, cols). "
        "The outermost list indexes the first axis.",
    "zeros":
        "np.zeros(shape) takes the shape as a TUPLE: np.zeros((2, 3)). Default "
        "dtype is float64. np.zeros(3) is a length-3 vector, not 3x3.",
    "ones":
        "np.ones(shape) — like zeros but filled with 1.0. Shape is a tuple; "
        "default dtype float64.",
    "full":
        "np.full(shape, fill_value) fills an array of the given shape with one "
        "value. dtype follows the fill value (np.full((2,2), 7) is int).",
    "empty":
        "np.empty(shape) allocates without initializing — contents are whatever "
        "was in memory (garbage). Only shape and dtype are defined, so checks "
        "verify those, not the values. Use it only when you'll overwrite every "
        "element.",
    "eye":
        "np.eye(n) makes an n x n identity matrix (1s on the diagonal). It can "
        "also take eye(n, m) for non-square and k= to shift the diagonal.",
    "identity":
        "np.identity(n) makes an n x n identity matrix. It's the square-only "
        "cousin of np.eye — no offset or rectangular options.",
    "arange":
        "np.arange([start,] stop[, step]) is like range(): the STOP is "
        "EXCLUSIVE and it counts by step. np.arange(2, 10, 2) -> [2 4 6 8]. "
        "With a float step, prefer linspace to avoid rounding surprises.",
    "linspace":
        "np.linspace(start, stop, num) returns num evenly spaced points with "
        "BOTH endpoints included. Counts by number-of-points, not step: "
        "linspace(0, 1, 5) -> [0, .25, .5, .75, 1].",
    "logspace":
        "np.logspace(a, b, num) spaces num points evenly on a log scale between "
        "10**a and 10**b. The args are EXPONENTS: logspace(0, 2, 3) -> "
        "[1, 10, 100].",
    "rand":
        "np.random.rand(d0, d1, ...) draws uniform floats in [0, 1). It takes "
        "dimensions as SEPARATE args (rand(2, 3)), unlike zeros which takes a "
        "tuple. Seed first (np.random.seed) for reproducibility.",
    "randn":
        "np.random.randn(d0, d1, ...) draws from the standard normal "
        "(mean 0, std 1). Dimensions are separate args, like rand. For a "
        "general normal use mean + std*randn(...) or np.random.normal.",
    "randint":
        "np.random.randint(low, high, size) draws integers in [low, high) — "
        "HIGH IS EXCLUSIVE. size is the count/shape. Seed first to reproduce.",
    "dtype":
        "np.array(values, dtype=...) sets the element type at creation. "
        "dtype=np.float64 stores floats; dtype=np.int32 truncates floats and "
        "uses 32-bit ints. The dtype is part of what makes two arrays equal here.",
    "astype":
        "a.astype(dtype) returns a NEW array cast to the given type. Float->int "
        "TRUNCATES toward zero (3.9 -> 3, -3.9 -> -3); it does not round. Use "
        "np.round first if you want rounding.",
    "shape":
        "a.shape is a tuple of the size along each axis, e.g. (2, 3) for 2 rows "
        "x 3 cols. len(a.shape) == a.ndim.",
    "ndim":
        "a.ndim is the number of dimensions (axes) — 1 for a vector, 2 for a "
        "matrix. It equals len(a.shape).",
    "size":
        "a.size is the total number of elements: the product of a.shape. A "
        "(2, 3) array has size 6. Don't confuse it with len(a), which is just "
        "the first axis.",
    "dtypeattr":
        "a.dtype is the element type object, e.g. dtype('float64'). Set it with "
        "dtype= at creation or change it with .astype.",

    # --- matplotlib (pyplot) ---
    "plot":
        "ax.plot(x, y) draws a line connecting the (x, y) points in order. With "
        "one arg, ax.plot(y) uses 0..len(y)-1 as x. The object-oriented form "
        "(ax.plot) is preferred over plt.plot for clarity in real code.",
    "scatter":
        "ax.scatter(x, y) plots individual points (markers), not a connected "
        "line. Use it when there's no meaningful order between points; use "
        "ax.plot for lines/curves.",
    "bar":
        "ax.bar(x, height) draws vertical bars: x is the bar positions, height "
        "is each bar's height. ax.barh(y, width) is the horizontal version.",
    "xlabel":
        "ax.set_xlabel('...') labels the x-axis. On the OO API you set things "
        "with ax.set_* methods; the pyplot shortcut is plt.xlabel('...').",
    "ylabel":
        "ax.set_ylabel('...') labels the y-axis. pyplot shortcut: plt.ylabel.",
    "title":
        "ax.set_title('...') sets the title of that Axes. plt.title sets it on "
        "the current Axes. (plt.suptitle is the whole-figure title.)",
    "xlim":
        "ax.set_xlim(left, right) sets the x-axis view range. Read it back with "
        "ax.get_xlim(), which returns a (left, right) float tuple.",
    "ylim":
        "ax.set_ylim(bottom, top) sets the y-axis view range. Matplotlib may "
        "auto-pad data limits, so set them explicitly when you need exact bounds.",
    "xticks":
        "ax.set_xticks([...]) sets exactly which x positions get ticks. Pass a "
        "second list (or set_xticklabels) to relabel them.",
    "yscale":
        "ax.set_yscale('log') switches the y-axis to a logarithmic scale "
        "('linear' is the default). Useful when values span many orders of "
        "magnitude. set_xscale does the same for x.",
    "plotcolor":
        "ax.plot(x, y, color='red') sets the line color. Accepts names ('red'), "
        "single letters ('r'), or hex ('#ff0000'). Sibling kwargs: linestyle "
        "('--'), linewidth, marker ('o').",

    # --- pandas ---
    "series":
        "pd.Series(data) wraps a 1-D sequence with an index. With no index= "
        "given you get the default RangeIndex 0..n-1. dtype is inferred like "
        "NumPy (all ints -> int64, any float -> float64).",
    "seriesindex":
        "pd.Series(data, index=[...]) attaches explicit labels. The index "
        "length must match the data; labels are how you select later "
        "(s['a']). Two Series are .equals only if values AND index match.",
    "seriesvalues":
        "s.values (or the preferred s.to_numpy()) returns the underlying data "
        "as a plain NumPy ndarray, dropping the index. Use it to hand pandas "
        "data to NumPy-only code.",
    "dataframe":
        "pd.DataFrame({'col': [...], ...}) builds a table from a dict of "
        "columns: each key is a column name, each value the column's data. All "
        "columns must be the same length; the row index defaults to 0..n-1.",
    "dfshape":
        "df.shape is a (n_rows, n_columns) tuple -- rows first, like a 2-D "
        "NumPy array. len(df) gives just the row count.",
    "dfcolumns":
        "df.columns is an Index of the column names. Wrap it in list(...) for "
        "a plain Python list; df.index is the row labels counterpart.",
    "selectcol":
        "df['col'] returns that column as a Series (1-D). df[['col']] with a "
        "LIST returns a one-column DataFrame instead -- single brackets vs "
        "double brackets is the usual gotcha.",
    "dfhead":
        "df.head(n) returns the first n rows (default 5) as a DataFrame; "
        "df.tail(n) returns the last n. Handy for a quick peek at big tables.",
    "colmean":
        "df['col'].mean() reduces a column to its mean, skipping NaN by "
        "default. df.mean() (no column) reduces every numeric column at once, "
        "returning a Series indexed by column name.",
    "colsum":
        "df['col'].sum() totals a column, skipping NaN. As with mean, df.sum() "
        "reduces all columns; sum over string columns concatenates them.",
}


def explain(rep) -> str:
    """Offline explanation for a rep: concept note + the canonical answer."""
    note = NOTES.get(rep.topic, "(no notes for this topic yet)")
    return f"{note}\n   canonical answer: {rep.solution}"


# ----------------------------------------------------------------------
# Optional live Q&A via the Claude API
# ----------------------------------------------------------------------

_MODEL = os.environ.get("NUMPY_GYM_MODEL", "claude-opus-4-8")

_SYSTEM = (
    "You are a concise scientific-Python tutor (NumPy, pandas, matplotlib) "
    "helping a student during a fast recall drill. They just attempted a "
    "single-expression problem and want to understand it. Answer their "
    "question in a few sentences. Focus on the concept and the common gotcha. "
    "Use plain text (no LaTeX). Do not write long code listings — a short "
    "inline expression is fine."
)


def live_available() -> bool:
    """True if the anthropic SDK is importable and a credential is set."""
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    return bool(os.environ.get("ANTHROPIC_API_KEY")
                or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def ask(rep, question: str):
    """Free-form Q&A about a rep via the Claude API.

    Returns the answer text, or None if live Q&A isn't available (so the
    caller can fall back to `explain`).
    """
    if not live_available():
        return None

    import anthropic

    context = (
        f"The drill prompt was: {rep.prompt}\n"
        f"The canonical answer is: {rep.solution}\n"
        f"(checking mode: {rep.compare})\n\n"
        f"Student's question: {question}"
    )
    try:
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=_MODEL,
            max_tokens=1024,
            system=_SYSTEM,
            messages=[{"role": "user", "content": context}],
        )
        return "".join(b.text for b in resp.content if b.type == "text").strip()
    except anthropic.APIError as exc:  # network/auth/rate-limit etc.
        return f"(live Q&A failed: {type(exc).__name__}: {exc}. Showing notes instead.)"
