# Cheat-sheet — read AFTER drilling

> Spoilers. This is a review reference for *after* a session, not during one.
> The interactive `explain` command shows the same notes per question.

## Tier 1 — Fastballs (recall)

| Skill | Idiom |
|-------|-------|
| total / mean / peak | `sum(xs)`, `sum(xs)/len(xs)` (or `np.mean`), `max(xs)` |
| count | `len(xs)`; rows of a frame: `len(df)` / `df.shape[0]` |
| last / first-k / reverse | `xs[-1]`, `xs[:3]`, `xs[::-1]` |
| upper / lower | `s.upper()`, `s.lower()` (immutable → returns a copy) |
| money string | `f"${x:.2f}"` (rounds *and* pads to 2 places) |
| parse text→int | `int(raw)` (form/`input()` values are strings) |
| even test | `n % 2 == 0` |
| full pages | `total // 10`; leftover `total % 10`; ceil `-(-total // 10)` |
| round | `round(x, 2)` (banker's rounding: half→even) |
| ranges | `np.arange(0, 10, 2)` (stop exclusive) vs `np.linspace` (count, inclusive) |
| cumulative | `np.cumprod`, `np.cumsum` |
| membership | `x in xs` (list O(n); set/dict O(1)) |
| dict lookup | `d['k']` (KeyError) vs `d.get('k')` (None) |

## Tier 2 — Mixed pitches (combine)

- **Filter:** `[r for r in readings if r > 35]`  → pandas `s[s > 35]`
- **Share %:** `[round(v/sum(vals)*100, 1) for v in vals]` (bind `sum` first if large)
- **Dot / weighted avg:** `w @ r`
- **Accumulator:** `n = 0; for ...: if ...: n += 1` — boundary `>` vs `>=`
- **Seasons / ranges:** tuple compare `(3,20) <= (m,d) <= (6,20)`; wrap-around is the `else`
- **2nd largest (distinct):** `sorted(set(xs))[-2]`; one-pass top-two is O(n)
- **Tip total:** float math, format last: `f"${bill*(1+pct/100):.2f}"`
- **Nested loops:** `[[(i+1)*(j+1) for j in range(n)] for i in range(n)]`
- **Validate:** `len(s) == 1 and s.isalpha()`
- **pandas group-of-one:** `df[df['city']==c]['rent'].mean()` → all at once `df.groupby('city')['rent'].mean()`

## Tier 3 — Breaking balls (gotchas)

- **Vectorize z-score:** `a=np.asarray(xs,float); (a-a.mean())/a.std()` (population std, ddof=0)
- **Vectorize polynomial:** `coef @ (x ** np.arange(len(coef)))`
- **Vectorize cumulative:** `np.cumsum(xs)`
- **Broadcasting rows:** `a / a.sum(axis=1, keepdims=True)` — `keepdims` makes (r,1) broadcast
- **Hamming / misclass:** `range(len(x))` (not `len-1`), and `!=` (not `==`); or `zip`
- **Mutable default:** `def f(x, log=None): if log is None: log = []` — never `log=[]`
- **Integer division trap:** `1 // 4 == 0`; use `/` for percentages
- **O(n) dedup:** `list(dict.fromkeys(xs))` or a `seen` set (list membership is O(n²))
- **O(n) pair-sum:** keep a `seen` set; check `target - x in seen`
- **Running mean:** divide by `i + 1` (enumerate starts at 0); keep `return` outside the loop
