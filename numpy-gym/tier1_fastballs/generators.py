"""Procedural generators for Tier 1 (Fastballs).

Each generator takes a `random.Random` instance (so problems are
randomized but reproducible from a seed) and returns a `Rep`.

A `Rep` is a single, atomic micro-drill:

    - prompt:   plain-English spec shown to the user
    - solution: a canonical SINGLE-EXPRESSION answer (the source of truth;
                the expected value is computed by evaluating this)
    - setup:    optional code run in the namespace before evaluation
                (e.g. seeding the RNG, or defining an array `a`)
    - compare:  how to check the user's answer against the expected value

The drill never shows `solution` to the user -- it only uses it to
compute the expected result, then compares with the user's expression.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


# ----------------------------------------------------------------------
# Rep model
# ----------------------------------------------------------------------

@dataclass
class Rep:
    topic: str
    prompt: str
    solution: str            # canonical single-expression answer
    setup: str = ""          # code exec'd before eval (seed, define `a`, ...)
    compare: str = "exact"   # exact | exact_dtype | close | shape | scalar
    hint: str = ""           # short nudge (the *function*, never the answer)
    check: str = ""          # if set: run the answer for side effects, then
                             # eval this expression and compare ITS value
                             # (used for matplotlib, where commands mutate `ax`)


# ----------------------------------------------------------------------
# Small helpers for generating clean, readable numbers
# ----------------------------------------------------------------------

def _ints(rng, n, lo=0, hi=9):
    return [rng.randint(lo, hi) for _ in range(n)]


def _list_repr(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


# ----------------------------------------------------------------------
# Creation from nested lists
# ----------------------------------------------------------------------

def gen_array_1d(rng):
    xs = _ints(rng, rng.randint(3, 5))
    return Rep(
        topic="array1d",
        prompt=f"Create a 1-D array containing {', '.join(str(x) for x in xs)}.",
        solution=f"np.array({_list_repr(xs)})",
        hint="np.array",
    )


def gen_array_2d(rng):
    cols = rng.randint(2, 3)
    r0 = _ints(rng, cols)
    r1 = _ints(rng, cols)
    return Rep(
        topic="array2d",
        prompt=f"Create a 2-D array with rows {_list_repr(r0)} and {_list_repr(r1)}.",
        solution=f"np.array([{_list_repr(r0)}, {_list_repr(r1)}])",
        hint="np.array of a list of lists",
    )


def gen_array_3d(rng):
    block = [[[rng.randint(1, 8) for _ in range(2)] for _ in range(2)] for _ in range(2)]
    return Rep(
        topic="array3d",
        prompt=f"Create a 3-D array from the nested list {block}.",
        solution=f"np.array({block})",
        hint="np.array of nested lists, three deep",
    )


# ----------------------------------------------------------------------
# Special arrays
# ----------------------------------------------------------------------

def gen_zeros(rng):
    r, c = rng.randint(2, 4), rng.randint(2, 4)
    return Rep(
        topic="zeros",
        prompt=f"Create a {r}x{c} array of zeros.",
        solution=f"np.zeros(({r}, {c}))",
        hint="np.zeros((rows, cols))",
    )


def gen_ones(rng):
    r, c = rng.randint(2, 4), rng.randint(2, 4)
    return Rep(
        topic="ones",
        prompt=f"Create a {r}x{c} array of ones.",
        solution=f"np.ones(({r}, {c}))",
        hint="np.ones((rows, cols))",
    )


def gen_full(rng):
    r, c = rng.randint(2, 3), rng.randint(2, 3)
    val = rng.randint(2, 9)
    return Rep(
        topic="full",
        prompt=f"Create a {r}x{c} array filled with the value {val}.",
        solution=f"np.full(({r}, {c}), {val})",
        hint="np.full(shape, fill_value)",
    )


def gen_empty(rng):
    # Contents of np.empty are undefined -> only the shape/dtype are checked.
    r, c = rng.randint(2, 4), rng.randint(2, 4)
    return Rep(
        topic="empty",
        prompt=(f"Create an UNINITIALIZED {r}x{c} float array "
                f"(contents don't matter; only shape & dtype are checked)."),
        solution=f"np.empty(({r}, {c}))",
        compare="shape",
        hint="np.empty((rows, cols))",
    )


def gen_eye(rng):
    n = rng.randint(2, 5)
    return Rep(
        topic="eye",
        prompt=f"Create a {n}x{n} identity matrix using np.eye.",
        solution=f"np.eye({n})",
        hint="np.eye(n)",
    )


def gen_identity(rng):
    n = rng.randint(2, 5)
    return Rep(
        topic="identity",
        prompt=f"Create a {n}x{n} identity matrix using np.identity.",
        solution=f"np.identity({n})",
        hint="np.identity(n)",
    )


# ----------------------------------------------------------------------
# Ranges
# ----------------------------------------------------------------------

def gen_arange(rng):
    start = rng.randint(0, 4)
    step = rng.choice([1, 2, 3])
    stop = start + step * rng.randint(3, 5)
    if start == 0 and step == 1:
        prompt = f"Create an array of integers from 0 up to (not including) {stop}."
        solution = f"np.arange({stop})"
    else:
        prompt = (f"Create an array starting at {start}, up to (not including) "
                  f"{stop}, stepping by {step}.")
        solution = f"np.arange({start}, {stop}, {step})"
    return Rep(topic="arange", prompt=prompt, solution=solution, hint="np.arange")


def gen_linspace(rng):
    start = rng.choice([0, 1, 2])
    stop = start + rng.choice([1, 4, 9, 10])
    num = rng.choice([3, 5, 6])
    return Rep(
        topic="linspace",
        prompt=f"Create {num} evenly spaced points from {start} to {stop} (inclusive).",
        solution=f"np.linspace({start}, {stop}, {num})",
        compare="close",
        hint="np.linspace(start, stop, num)",
    )


def gen_logspace(rng):
    start = rng.choice([0, 1])
    stop = start + rng.choice([1, 2, 3])
    num = rng.choice([3, 4])
    return Rep(
        topic="logspace",
        prompt=(f"Create {num} points spaced evenly on a log scale, "
                f"from 10^{start} to 10^{stop} (inclusive)."),
        solution=f"np.logspace({start}, {stop}, {num})",
        compare="close",
        hint="np.logspace(start_exp, stop_exp, num)",
    )


# ----------------------------------------------------------------------
# Random family (seed is set in `setup`, so answers are reproducible)
# ----------------------------------------------------------------------

def gen_rand(rng):
    seed = rng.randint(0, 99)
    r, c = rng.randint(2, 3), rng.randint(2, 3)
    return Rep(
        topic="rand",
        prompt=(f"With the seed already set to {seed}, create a {r}x{c} array of "
                f"uniform random floats in [0, 1) using np.random.rand."),
        solution=f"np.random.rand({r}, {c})",
        setup=f"np.random.seed({seed})",
        compare="close",
        hint="np.random.rand(rows, cols)",
    )


def gen_randn(rng):
    seed = rng.randint(0, 99)
    n = rng.randint(3, 5)
    return Rep(
        topic="randn",
        prompt=(f"With the seed already set to {seed}, create a length-{n} array of "
                f"standard-normal samples using np.random.randn."),
        solution=f"np.random.randn({n})",
        setup=f"np.random.seed({seed})",
        compare="close",
        hint="np.random.randn(n)",
    )


def gen_randint(rng):
    seed = rng.randint(0, 99)
    hi = rng.choice([5, 10, 100])
    n = rng.randint(3, 5)
    return Rep(
        topic="randint",
        prompt=(f"With the seed already set to {seed}, draw {n} random integers in "
                f"[0, {hi}) using np.random.randint."),
        solution=f"np.random.randint(0, {hi}, {n})",
        setup=f"np.random.seed({seed})",
        compare="exact",
        hint="np.random.randint(low, high, size)",
    )


# ----------------------------------------------------------------------
# dtype specification & astype
# ----------------------------------------------------------------------

def gen_dtype(rng):
    xs = _ints(rng, rng.randint(3, 4), 1, 6)
    target, name = rng.choice([("np.float64", "float64"),
                               ("np.int32", "int32"),
                               ("np.float32", "float32")])
    return Rep(
        topic="dtype",
        prompt=f"Create a 1-D array of {', '.join(map(str, xs))} with dtype {name}.",
        solution=f"np.array({_list_repr(xs)}, dtype={target})",
        compare="exact_dtype",
        hint="np.array(..., dtype=...)",
    )


def gen_astype(rng):
    xs = [round(rng.uniform(1, 9), 1) for _ in range(rng.randint(3, 4))]
    target, name = rng.choice([("np.int64", "int64"), ("np.int32", "int32")])
    return Rep(
        topic="astype",
        prompt=(f"Given a = np.array({xs}), cast it to {name} "
                f"(values truncate toward zero)."),
        solution=f"a.astype({target})",
        setup=f"a = np.array({xs})",
        compare="exact_dtype",
        hint="a.astype(...)",
    )


# ----------------------------------------------------------------------
# Shape inspection
# ----------------------------------------------------------------------

def _random_array_setup(rng):
    """Build a small array `a` and return (setup_code, the array's literal)."""
    ndim = rng.choice([1, 2, 2, 3])
    if ndim == 1:
        xs = _ints(rng, rng.randint(3, 6))
        return f"a = np.array({_list_repr(xs)})"
    if ndim == 2:
        r, c = rng.randint(2, 3), rng.randint(2, 4)
        rows = [_ints(rng, c) for _ in range(r)]
        return f"a = np.array([{', '.join(_list_repr(x) for x in rows)}])"
    block = [[[rng.randint(1, 8) for _ in range(2)] for _ in range(2)] for _ in range(2)]
    return f"a = np.array({block})"


def gen_shape(rng):
    setup = _random_array_setup(rng)
    return Rep(topic="shape", prompt=f"Given {setup}, report a.shape.",
               solution="a.shape", setup=setup, compare="scalar", hint=".shape")


def gen_ndim(rng):
    setup = _random_array_setup(rng)
    return Rep(topic="ndim", prompt=f"Given {setup}, report a.ndim.",
               solution="a.ndim", setup=setup, compare="scalar", hint=".ndim")


def gen_size(rng):
    setup = _random_array_setup(rng)
    return Rep(topic="size", prompt=f"Given {setup}, report a.size (total elements).",
               solution="a.size", setup=setup, compare="scalar", hint=".size")


def gen_dtype_attr(rng):
    target, name = rng.choice([("np.float64", "float64"), ("np.int32", "int32")])
    xs = _ints(rng, 4, 1, 6)
    setup = f"a = np.array({_list_repr(xs)}, dtype={target})"
    return Rep(topic="dtypeattr", prompt=f"Given {setup}, report a.dtype.",
               solution="a.dtype", setup=setup, compare="scalar", hint=".dtype")


# ----------------------------------------------------------------------
# Matplotlib (pyplot) -- atomic plotting commands
#
# These mutate a provided Axes `ax` instead of returning an array, so each
# Rep carries a `check` expression that inspects `ax` after the command runs.
# The expected value is computed by running the canonical solution + check;
# the user's answer is checked the same way, so any command with the same
# visible effect is accepted (e.g. plt.plot vs ax.plot, 'r' vs 'red').
# ----------------------------------------------------------------------

_MPL = (
    "import matplotlib\n"
    "matplotlib.use('Agg')\n"
    "import matplotlib.pyplot as plt\n"
    "import numpy as np\n"
    "plt.rcParams['figure.max_open_warning'] = 0\n"
    "plt.close('all')\n"
    "fig, ax = plt.subplots()\n"
)


def _xy(rng):
    """A small, clean (x, y) pair as a setup snippet."""
    n = rng.randint(3, 5)
    x = list(range(n))
    y = _ints(rng, n, 1, 9)
    return f"x = np.array({x})\ny = np.array({y})\n", x, y


def gen_plot(rng):
    data, x, y = _xy(rng)
    return Rep(
        topic="plot",
        prompt=("Given x and y (already defined), draw a LINE plot of y "
                "against x on the Axes `ax`."),
        solution="ax.plot(x, y)",
        setup=_MPL + data,
        check="(list(ax.lines[-1].get_xdata()), list(ax.lines[-1].get_ydata()))",
        compare="close",
        hint="ax.plot(x, y)",
    )


def gen_scatter_plot(rng):
    data, x, y = _xy(rng)
    return Rep(
        topic="scatter",
        prompt="Given x and y, make a SCATTER plot of y against x on `ax`.",
        solution="ax.scatter(x, y)",
        setup=_MPL + data,
        check="np.asarray(ax.collections[-1].get_offsets())",
        compare="close",
        hint="ax.scatter(x, y)",
    )


def gen_bar(rng):
    n = rng.randint(3, 4)
    x = list(range(n))
    heights = _ints(rng, n, 1, 9)
    return Rep(
        topic="bar",
        prompt=("Given x and h (positions and heights, already defined), draw a "
                "BAR chart of h at positions x on `ax`."),
        solution="ax.bar(x, h)",
        setup=_MPL + f"x = np.array({x})\nh = np.array({heights})\n",
        check="[p.get_height() for p in ax.patches]",
        compare="close",
        hint="ax.bar(x, h)",
    )


def gen_xlabel(rng):
    label = rng.choice(["time", "x", "samples", "frequency", "index"])
    return Rep(
        topic="xlabel",
        prompt=f"Set the x-axis label of `ax` to '{label}'.",
        solution=f"ax.set_xlabel('{label}')",
        setup=_MPL,
        check="ax.get_xlabel()",
        compare="scalar",
        hint="ax.set_xlabel(...)",
    )


def gen_ylabel(rng):
    label = rng.choice(["value", "y", "amplitude", "count", "voltage"])
    return Rep(
        topic="ylabel",
        prompt=f"Set the y-axis label of `ax` to '{label}'.",
        solution=f"ax.set_ylabel('{label}')",
        setup=_MPL,
        check="ax.get_ylabel()",
        compare="scalar",
        hint="ax.set_ylabel(...)",
    )


def gen_title(rng):
    title = rng.choice(["Results", "Signal", "Demo", "Overview", "Trend"])
    return Rep(
        topic="title",
        prompt=f"Set the title of `ax` to '{title}'.",
        solution=f"ax.set_title('{title}')",
        setup=_MPL,
        check="ax.get_title()",
        compare="scalar",
        hint="ax.set_title(...)",
    )


def gen_xlim(rng):
    lo = rng.randint(0, 3)
    hi = lo + rng.choice([5, 8, 10])
    return Rep(
        topic="xlim",
        prompt=f"Set the x-axis limits of `ax` to {lo} (left) and {hi} (right).",
        solution=f"ax.set_xlim({lo}, {hi})",
        setup=_MPL,
        check="ax.get_xlim()",
        compare="close",
        hint="ax.set_xlim(left, right)",
    )


def gen_ylim(rng):
    lo = rng.randint(0, 3)
    hi = lo + rng.choice([4, 6, 9])
    return Rep(
        topic="ylim",
        prompt=f"Set the y-axis limits of `ax` to {lo} (bottom) and {hi} (top).",
        solution=f"ax.set_ylim({lo}, {hi})",
        setup=_MPL,
        check="ax.get_ylim()",
        compare="close",
        hint="ax.set_ylim(bottom, top)",
    )


def gen_xticks(rng):
    step = rng.choice([1, 2, 5])
    ticks = list(range(0, step * rng.randint(3, 4) + 1, step))
    return Rep(
        topic="xticks",
        prompt=f"Set the x-axis tick positions of `ax` to {ticks}.",
        solution=f"ax.set_xticks({ticks})",
        setup=_MPL,
        check="list(ax.get_xticks())",
        compare="close",
        hint="ax.set_xticks([...])",
    )


def gen_yscale(rng):
    scale = rng.choice(["log", "linear"])
    return Rep(
        topic="yscale",
        prompt=f"Make the y-axis of `ax` use a '{scale}' scale.",
        solution=f"ax.set_yscale('{scale}')",
        setup=_MPL,
        check="ax.get_yscale()",
        compare="scalar",
        hint="ax.set_yscale(...)",
    )


def gen_plot_color(rng):
    data, x, y = _xy(rng)
    color = rng.choice(["red", "green", "blue", "black", "orange"])
    return Rep(
        topic="plotcolor",
        prompt=f"Given x and y, plot y against x on `ax` as a {color} line.",
        solution=f"ax.plot(x, y, color='{color}')",
        setup=_MPL + data,
        # normalize to RGBA so 'r'/'red' and shorthand all compare equal
        check="matplotlib.colors.to_rgba(ax.lines[-1].get_color())",
        compare="close",
        hint="ax.plot(x, y, color=...)",
    )


# ----------------------------------------------------------------------
# Registry
# ----------------------------------------------------------------------

# Each entry: key -> (human description, generator function)
GENERATORS = {
    "array1d":   ("np.array from a 1-D list",          gen_array_1d),
    "array2d":   ("np.array from a 2-D list",          gen_array_2d),
    "array3d":   ("np.array from a 3-D list",          gen_array_3d),
    "zeros":     ("np.zeros",                          gen_zeros),
    "ones":      ("np.ones",                           gen_ones),
    "full":      ("np.full",                           gen_full),
    "empty":     ("np.empty (shape/dtype only)",       gen_empty),
    "eye":       ("np.eye",                            gen_eye),
    "identity":  ("np.identity",                       gen_identity),
    "arange":    ("np.arange",                         gen_arange),
    "linspace":  ("np.linspace",                       gen_linspace),
    "logspace":  ("np.logspace",                       gen_logspace),
    "rand":      ("np.random.rand (seeded)",           gen_rand),
    "randn":     ("np.random.randn (seeded)",          gen_randn),
    "randint":   ("np.random.randint (seeded)",        gen_randint),
    "dtype":     ("np.array(..., dtype=...)",          gen_dtype),
    "astype":    (".astype(...)",                      gen_astype),
    "shape":     (".shape",                            gen_shape),
    "ndim":      (".ndim",                             gen_ndim),
    "size":      (".size",                             gen_size),
    "dtypeattr": (".dtype",                            gen_dtype_attr),
    "plot":      ("ax.plot (line)",                    gen_plot),
    "scatter":   ("ax.scatter",                        gen_scatter_plot),
    "bar":       ("ax.bar",                            gen_bar),
    "xlabel":    ("ax.set_xlabel",                     gen_xlabel),
    "ylabel":    ("ax.set_ylabel",                     gen_ylabel),
    "title":     ("ax.set_title",                      gen_title),
    "xlim":      ("ax.set_xlim",                       gen_xlim),
    "ylim":      ("ax.set_ylim",                       gen_ylim),
    "xticks":    ("ax.set_xticks",                     gen_xticks),
    "yscale":    ("ax.set_yscale",                     gen_yscale),
    "plotcolor": ("ax.plot(color=...)",                gen_plot_color),
}

# Convenience groupings for the menu.
GROUPS = {
    "creation":   ["array1d", "array2d", "array3d"],
    "special":    ["zeros", "ones", "full", "empty", "eye", "identity"],
    "ranges":     ["arange", "linspace", "logspace"],
    "random":     ["rand", "randn", "randint"],
    "dtypes":     ["dtype", "astype"],
    "inspection": ["shape", "ndim", "size", "dtypeattr"],
    "plotting":   ["plot", "scatter", "bar", "xlabel", "ylabel", "title",
                   "xlim", "ylim", "xticks", "yscale", "plotcolor"],
}

# Topics that require matplotlib (skipped if it isn't installed).
PLOTTING_TOPICS = set(GROUPS["plotting"])


def matplotlib_available():
    try:
        import matplotlib  # noqa: F401
        return True
    except ImportError:
        return False


def all_topics():
    return list(GENERATORS.keys())


def make_rep(topic, rng):
    """Build one Rep for the given topic key."""
    return GENERATORS[topic][1](rng)
