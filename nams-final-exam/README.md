# Nam's Final Exam

A self-contained terminal gym for re-earning your CS fundamentals through
**deliberate, retrieval-based practice**: you read a spec, write the code, run
it, and get told right/wrong on the spot. You never see a solution before
attempting a problem — canonical answers and hidden tests are quarantined in
`solutions/`, which you only open after you've tried.

It generalizes the sibling **NumPy Practice Gym** from NumPy-only to the full
span of your **COMP 1005/1405** coursework (Tutorials 1–4) plus the NumPy
notebook, and adds a **script-writing mode** on top of one-line recall.

Questions are themed to data-science / economics / public-sector scenarios
(rainfall, emissions, rent, survey records) — the work you're aiming at, not
abstract `foo`/`bar`.

## The practice loop

Every question supports the same loop:

**Generate** (attempt) → **Struggle** → **Resolve** (`check`) →
**Reconstruct** (`explain`) → **Elaborate** (`ask`).

## Two answer modes

- **`cli`** — type a **single expression**; it's evaluated and compared **by
  value**, so any correct form is accepted (a built-in, a comprehension, a
  NumPy call — all fine). Syntax/runtime errors just re-prompt; they don't cost
  you the question.
- **`script`** — you write a **whole function** in `attempts/<id>.py`, then run
  `check` to grade it against a **visible + hidden** test suite (pass/fail per
  case). Hidden cases never reveal their inputs. The hard tier leans on this for
  *find-and-fix-the-bug* and *vectorize-this* problems.

## Tiers — the baseball metaphor

| Tier | Name | Trains | Typical mode |
|------|------|--------|--------------|
| 1 | **Fastballs** | Atomic recall, one skill per rep, fast | mostly `cli` |
| 2 | **Mixed pitches** | Combine 2–3 concepts in a real at-bat | `cli` + small `script` |
| 3 | **Breaking balls** | Gotchas, debugging, edge cases, complexity, vectorization | mostly `script` |

The quant-/performance-/interview-gotcha material lives mainly in **Tier 3**.

## Requirements

- Python 3.8+
- `numpy` (required)
- `pandas` (optional — unlocks a few Tier 2 questions; they're skipped if it's
  absent)
- `anthropic` (optional — enables live `ask`; offline notes are used otherwise)
- `pytest` (optional — only for the bank self-test in `solutions/`)

```bash
pip install numpy
pip install pandas anthropic pytest   # optional extras
```

## How to run

```bash
cd nams-final-exam

python exam.py                       # interactive: pick tiers + how many
python exam.py --reps 30             # 30 questions across all tiers
python exam.py --tier 1              # only Tier 1 (fastballs)
python exam.py --tier 2 3            # Tiers 2 and 3
python exam.py --topics loops vectorization
python exam.py --mode script         # only the write-a-function questions
python exam.py --seed 1 --reps 20    # fully reproducible session
python exam.py --list                # list every question and exit
```

## Commands during a question

Type your answer (an expression in `cli` mode), or one of:

| Command | Mode | Effect |
|---------|------|--------|
| `hint` | both | a small nudge (the function / approach, never the answer) |
| `explain` | both | concept notes **+ the canonical answer** — counts as not-correct |
| `ask <question>` | both | free-form Q&A (live via Claude if set up, else offline notes) |
| `check` | script | run the hidden test suite and report pass/fail per case |
| `run` | script | run your code on the sample input **without** grading |
| `reset` | script | restore `attempts/<id>.py` to the starter |
| `skip` | both | skip without penalty (reveals the answer for review) |
| `quit` | both | end early and show the summary |

A **wrong** `cli` answer reveals the canonical answer and moves on. A `script`
question stays open across as many `check`/edit cycles as you like until it
passes (or you `skip`/`explain`). At the end you get score, accuracy, best
streak, and average time per question.

**No-spoiler rule:** the canonical answer and hidden tests are never printed
until *after* an attempt (a wrong answer, `explain`, or `skip`). `solutions/`
stays quarantined — don't open it mid-session.

## Live Q&A (optional)

`explain` always works offline. `ask <question>` answers free-form questions via
the Claude API when it's set up, and otherwise falls back to the question's
offline notes (without revealing the answer). To enable live Q&A:

```bash
pip install anthropic
```
```bash
# bash:
export ANTHROPIC_API_KEY=sk-ant-...
```
```powershell
# PowerShell:
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

Optional model override via `EXAM_MODEL` (default `claude-opus-4-8`):

```bash
export EXAM_MODEL=claude-sonnet-4-6          # bash
```
```powershell
$env:EXAM_MODEL = "claude-sonnet-4-6"        # PowerShell
```

## Repo layout

```
nams-final-exam/
  exam.py            # runner + game loop
  engine/            # bank loading, cli/script grading, comparison, coach
  questions/         # the question bank, by tier (browsable, no answers)
    tier1.json  tier2.json  tier3.json
  attempts/          # your scratch files for script questions (git-ignored)
  solutions/         # QUARANTINED: answer key, hidden tests, cheat-sheet
    grading.py  notes.md  test_bank.py
  topics.md          # the topic taxonomy (what's drilled + extensions)
  README.md
```

- **`topics.md`** — the full map of what's covered and where it came from.
- **`solutions/notes.md`** — a cheat-sheet to review *after* drilling.

## Adding your own questions

1. Add a public entry to `questions/tier{1,2,3}.json` (id, topic, tier, mode,
   prompt, hint, notes; for `script`: `entry`, `starter`, `visible`).
2. Add a matching grading entry to `solutions/grading.py` (the canonical answer
   and, for `script`, the test `cases` + any `max_loops`/`forbid` constraint).
3. Verify the bank stays consistent:

```bash
python solutions/test_bank.py     # or: pytest solutions/test_bank.py
```
