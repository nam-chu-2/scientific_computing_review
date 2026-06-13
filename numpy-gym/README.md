# NumPy Practice Gym

A self-contained gym for building scientific-computing fluency through
**deliberate, retrieval-based practice**: you write the code, run it, and get
told right/wrong on the spot. You never see a solution before attempting a
problem — solutions are quarantined in `solutions/`, which you only open after
you've tried.

The difficulty model uses a baseball metaphor:

| Tier | Name | Trains | Pitch |
|------|------|--------|-------|
| 1 | **Fastballs** | Pure recall / muscle memory. One atomic skill per rep. | Same pitch, 100+ times, fast. |
| 2 | **Mixed pitches** | Application. Combine 2–3 concepts. | Varied pitches, real at-bat. |
| 3 | **Breaking balls** | Gotchas, debugging, vectorization, edge cases. | Pitches designed to fool you. |

## Requirements

- Python 3.8+
- `numpy` (all tiers), `matplotlib` (Tier 1 plotting drills), `pytest` (Tier 3 only)

```bash
pip install numpy matplotlib pytest
```

If `matplotlib` isn't installed, the plotting drills are skipped automatically
and the rest of Tier 1 still works.

## Tier 1 — Fastballs

Procedurally generated micro-drills. Each rep is a **single expression**: you
read a plain-English spec and type one line of NumPy. Reps are randomized but
**reproducible** via `--seed`.

```bash
cd numpy-gym/tier1_fastballs

python drill.py                          # interactive: pick topics + rep count
python drill.py --reps 50                # 50 reps across all topics
python drill.py --groups random ranges   # only those topic groups
python drill.py --topics arange linspace --reps 20
python drill.py --seed 123 --reps 30     # fully reproducible session
```

**Topic groups:** `creation`, `special`, `ranges`, `random`, `dtypes`,
`inspection`, `plotting` (matplotlib: `plot`, `scatter`, `bar`, axis labels,
title, limits, ticks, scale, color).

Matplotlib drills run a non-interactive backend (no windows pop up): you type
the plotting command (e.g. `ax.set_xlabel('time')`), and the drill checks the
resulting figure state. Both the object-oriented (`ax.set_...`) and pyplot
(`plt....`) forms are accepted.

**During a rep**, type a single expression, or one of:
- `hint` — a small nudge (the function name, never the answer)
- `explain` — built-in notes on this rep's concept + the canonical answer
- `ask <question>` — free-form question about this rep (see live Q&A below)
- `skip` — skip this rep (not counted as wrong)
- `quit` — end early and show the summary

When you get a rep **wrong** (or skip it), the drill shows the canonical
expression you should have typed and then drops into a short review prompt where
you can `explain`, `ask <question>`, or press Enter to move on. Correct answers
advance immediately. Syntax/runtime errors just re-prompt — they don't cost you
the rep. At the end you get score, accuracy, best streak, and average time per rep.

### Live Q&A (optional)

`explain` always works offline. `ask <question>` answers free-form questions via
the Claude API when it's set up, and otherwise falls back to the offline notes.
To enable live Q&A:

```bash
pip install anthropic
# PowerShell:
$env:ANTHROPIC_API_KEY = "sk-ant-..."
# bash:
export ANTHROPIC_API_KEY=sk-ant-...
```

Optional model override: set `NUMPY_GYM_MODEL` (default `claude-opus-4-8`).

Notes / cheat-sheet for review *after* drilling: [`solutions/tier1_notes.md`](solutions/tier1_notes.md).

## Tier 2 — Mixed pitches

_Coming next (pending review of Tier 1)._

## Tier 3 — Breaking balls

_Coming after Tier 2 (pending review)._
