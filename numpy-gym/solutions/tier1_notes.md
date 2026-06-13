# Tier 1 — Fastballs: notes & cheat-sheet

> Read this **after** drilling, not before. It's the canonical reference for
> every skill the Tier 1 generators drill.

## Creation from lists
```python
np.array([4, 7, 2, 9])              # 1-D
np.array([[1, 2, 3], [4, 5, 6]])    # 2-D (list of rows)
np.array([[[1, 2], [3, 4]],         # 3-D (list of 2-D blocks)
          [[5, 6], [7, 8]]])
```

## Special arrays
```python
np.zeros((2, 3))         # shape as a TUPLE; default dtype float64
np.ones((2, 3))
np.full((2, 2), 7)       # np.full(shape, fill_value)
np.empty((2, 3))         # UNINITIALIZED — contents are garbage; only shape/dtype defined
np.eye(3)                # NxN identity (can also do eye(N, M, k))
np.identity(4)           # NxN identity only
```
`zeros`/`ones`/`empty` take a shape tuple. A bare `np.zeros(3)` is a length-3
*vector*, not a 3x3 matrix.

## Ranges
```python
np.arange(5)             # [0 1 2 3 4]   — stop-exclusive, like range()
np.arange(2, 10, 2)      # [2 4 6 8]     — start, stop, step
np.linspace(0, 1, 5)     # 5 points, endpoints INCLUSIVE -> [0, .25, .5, .75, 1]
np.logspace(0, 2, 3)     # 10**0 .. 10**2 -> [1, 10, 100]  (exponents, not values)
```
- `arange` is stop-**exclusive** and counts by *step*.
- `linspace` is endpoint-**inclusive** and counts by *number of points*.
- `logspace(a, b, n)` spaces `n` points evenly between `10**a` and `10**b`.

## Random family (seed first → reproducible)
```python
np.random.seed(42)
np.random.rand(2, 3)        # uniform [0, 1), shape from *dims* (not a tuple)
np.random.randn(4)          # standard normal, shape from *dims*
np.random.randint(0, 10, 5) # ints in [low, high), size last; high is EXCLUSIVE
```
Note the API quirk: `rand`/`randn` take dimensions as separate args
(`rand(2, 3)`), while `zeros`/`ones` take a shape tuple (`zeros((2, 3))`).

## dtype & astype
```python
np.array([1, 2, 3], dtype=np.float64)   # set dtype at creation
np.array([1.5, 2.7, 3.9]).astype(np.int64)  # cast; truncates TOWARD ZERO -> [1, 2, 3]
```
`astype` does not round — `3.9 -> 3`, `-3.9 -> -3`.

## Shape inspection
```python
a.shape    # tuple of dimension sizes, e.g. (2, 3)
a.ndim     # number of dimensions (len of .shape)
a.size     # total number of elements (product of .shape)
a.dtype    # element type, e.g. dtype('float64')
```

## Matplotlib (pyplot)
The drills give you a ready-made Axes `ax` (from `fig, ax = plt.subplots()`).
Prefer the object-oriented `ax.set_*` form; the `plt.*` shortcuts act on the
"current" Axes and are accepted too.
```python
ax.plot(x, y)                 # line plot (points connected in order)
ax.scatter(x, y)              # individual markers, no connecting line
ax.bar(x, height)             # vertical bars; ax.barh for horizontal
ax.set_xlabel('time')         # x-axis label   (plt.xlabel)
ax.set_ylabel('value')        # y-axis label   (plt.ylabel)
ax.set_title('Results')       # Axes title     (plt.title; plt.suptitle = figure)
ax.set_xlim(0, 10)            # x view range; get_xlim() -> (0.0, 10.0)
ax.set_ylim(0, 5)             # y view range
ax.set_xticks([0, 2, 4])      # explicit tick positions
ax.set_yscale('log')          # 'linear' (default) | 'log'; set_xscale for x
ax.plot(x, y, color='red')    # color: 'red' | 'r' | '#ff0000'; also linestyle, marker
```
- `plot` vs `scatter`: lines for ordered/continuous data, scatter for
  unordered points.
- Limits return float tuples; matplotlib may auto-pad data limits, so set them
  explicitly when you need exact bounds.

