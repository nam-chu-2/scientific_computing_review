"""Tier 1 -- Fastballs: interactive drill CLI.

Active recall with immediate feedback. You are shown a plain-English spec,
you type a SINGLE expression, and you're told right/wrong instantly.
You never see the solution. Drills span scientific libraries (numpy,
pandas, matplotlib) and can be sliced by library, group, or topic.

Run from anywhere:

    python drill.py                       # interactive: pick library/topics + reps
    python drill.py --reps 50             # 50 reps, all libraries
    python drill.py --libs pandas         # only pandas drills
    python drill.py --libs numpy pandas   # two whole libraries
    python drill.py --groups random ranges
    python drill.py --topics arange linspace --reps 20
    python drill.py --seed 123 --reps 30  # fully reproducible session

During a rep:
    - type a single expression (e.g.  np.array([4, 7, 2, 9]) )
    - 'skip'  -> skip this rep (not counted as wrong)
    - 'hint'  -> show a small nudge (the function name, never the answer)
    - 'quit'  -> end early and show the summary
Syntax / runtime errors just re-prompt -- they don't cost you the rep.
"""

from __future__ import annotations

import argparse
import random
import sys
import time

import numpy as np

import generators as G
import coach


# ----------------------------------------------------------------------
# Evaluation & checking
# ----------------------------------------------------------------------

def _resolve(rep, expr):
    """Return the comparable value produced by `expr` for this rep.

    Normal reps: just eval the expression (it returns an array/scalar).
    Reps with a `check` (matplotlib): run the expression for its side
    effect on `ax`, then eval the check expression and return its value.
    """
    ns = {"np": np}
    if rep.setup:
        exec(rep.setup, ns)
    if rep.check:
        exec(expr, ns)            # statement OK; we want the effect on `ax`
        return eval(rep.check, ns)
    return eval(expr, ns)


def check(expected, actual, mode):
    """Return True if `actual` matches `expected` under the given mode."""
    try:
        if mode == "close":
            return np.allclose(np.asarray(actual, dtype=float),
                               np.asarray(expected, dtype=float))
        if mode == "shape":
            a, e = np.asarray(actual), np.asarray(expected)
            return a.shape == e.shape and a.dtype == e.dtype
        if mode == "scalar":
            # .shape (tuple), .ndim/.size (int), .dtype (dtype object)
            return expected == actual
        if mode == "exact_dtype":
            a, e = np.asarray(actual), np.asarray(expected)
            return a.dtype == e.dtype and np.array_equal(a, e)
        if mode == "pandas":
            # Series/DataFrame: .equals enforces values, index, and dtype.
            return bool(expected.equals(actual))
        # default: exact value match (dtype-agnostic)
        return np.array_equal(np.asarray(actual), np.asarray(expected))
    except Exception:
        return False


def _print_block(text):
    """Print a multi-line coach response indented under the prompt."""
    print("   " + text.replace("\n", "\n   ") + "\n")


def _run_coach(rep, raw):
    """Handle 'explain' / 'ask <q>'. Returns True if it was a coach command."""
    low = raw.lower()
    if low == "explain":
        _print_block(coach.explain(rep))
        return True
    if low == "ask" or low.startswith("ask "):
        question = raw[3:].strip()
        if not question:
            print("   usage: ask <your question>   e.g.  ask why is the shape a tuple?\n")
            return True
        answer = coach.ask(rep, question)
        if answer is None:
            print("   (live Q&A not enabled - showing offline notes; see coach.py)")
            _print_block(coach.explain(rep))
        else:
            _print_block(answer)
        return True
    return False


def _review(rep):
    """After a miss/skip, let the user dig in before moving on."""
    print("   ('explain', 'ask <q>', Enter = next, or 'quit')")
    while True:
        try:
            raw = input("   > ").strip()
        except EOFError:
            return "next"
        low = raw.lower()
        if low in ("", "next", "n"):
            return "next"
        if low == "quit":
            return "quit"
        if not _run_coach(rep, raw):
            print("   commands: explain | ask <q> | (Enter)=next | quit")


def _fmt(value):
    """Compact one-line repr of an expected value for post-mortem display."""
    text = np.array2string(np.asarray(value), separator=", ") \
        if isinstance(value, np.ndarray) else repr(value)
    return " ".join(text.split())


# ----------------------------------------------------------------------
# Topic selection
# ----------------------------------------------------------------------

def _drop_unavailable(topics):
    """Drop topics whose backing library isn't installed; report what was cut."""
    kept = []
    dropped = {}
    for t in topics:
        lib = G.library_of_topic(t)
        if G.library_available(lib):
            kept.append(t)
        else:
            dropped.setdefault(lib, []).append(t)
    for lib, ts in dropped.items():
        print(f"({lib} not installed - skipping {len(ts)} drills: "
              f"{', '.join(ts)})")
    return kept


def resolve_topics(args):
    topics = []
    if args.topics:
        topics = [t for t in args.topics if t in G.GENERATORS]
    else:
        # --libs and --groups can be combined (interactive sets both).
        for lib in args.libs or []:
            topics.extend(G.topics_for_library(lib))
        for grp in args.groups or []:
            topics.extend(G.GROUPS.get(grp, []))
    if not topics:
        topics = G.all_topics()
    # de-dup, preserve order
    seen, out = set(), []
    for t in topics:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return _drop_unavailable(out)


def interactive_setup():
    print("\n=== Tier 1: Fastballs ===")
    print("Libraries (pick a whole library, or specific groups within one):")
    for lib, groups in G.LIBRARIES.items():
        flag = "" if G.library_available(lib) else "  [not installed]"
        print(f"  {lib:11s} -> {', '.join(groups)}{flag}")
    raw = input("\nPick libraries or groups (space-separated), "
                "or Enter for ALL: ").strip()
    tokens = raw.split()
    libs = [t for t in tokens if t in G.LIBRARIES]
    groups = [t for t in tokens if t in G.GROUPS]
    unknown = [t for t in tokens if t not in G.LIBRARIES and t not in G.GROUPS]
    if unknown:
        print(f"  (ignoring unknown: {', '.join(unknown)})")

    reps = 20
    raw = input("How many reps? [20]: ").strip()
    if raw:
        try:
            reps = max(1, int(raw))
        except ValueError:
            print("  (not a number -> using 20)")
    return libs, groups, reps


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------

def run(topics, reps, seed):
    rng = random.Random(seed)
    print(f"\nDrilling {reps} reps over {len(topics)} topics. "
          f"(seed={seed})")
    print("Type an expression, or 'hint' / 'explain' / 'ask <q>' / 'skip' / 'quit'.")
    if not coach.live_available():
        print("(tip: 'ask' uses offline notes until you `pip install anthropic` "
              "and set ANTHROPIC_API_KEY)")
    print()

    correct = 0
    attempted = 0
    skipped = 0
    times = []
    streak = 0
    best_streak = 0

    for i in range(1, reps + 1):
        topic = rng.choice(topics)
        rep = G.make_rep(topic, rng)

        try:
            expected = _resolve(rep, rep.solution)
        except Exception as exc:  # generator bug -- skip gracefully
            print(f"[internal] skipping malformed rep ({topic}): {exc}")
            continue

        print(f"--- Rep {i}/{reps} ---")
        print(rep.prompt)

        start = time.perf_counter()
        hinted = False
        while True:
            try:
                answer = input(">>> ").strip()
            except EOFError:
                answer = "quit"

            low = answer.lower()
            if low == "quit":
                return _summary(correct, attempted, skipped, times, best_streak,
                                quit_early=True)
            if low == "skip":
                skipped += 1
                streak = 0
                print(f"   skipped.  answer: {rep.solution}  ->  {_fmt(expected)}")
                if _review(rep) == "quit":
                    return _summary(correct, attempted, skipped, times,
                                    best_streak, quit_early=True)
                print()
                break
            if low == "hint":
                print(f"   hint: {rep.hint}")
                hinted = True
                continue
            if low == "explain" or low == "ask" or low.startswith("ask "):
                _run_coach(rep, answer)
                continue
            if not answer:
                continue

            try:
                actual = _resolve(rep, answer)
            except Exception as exc:
                print(f"   ! {type(exc).__name__}: {exc}  -- try again "
                      f"(or skip/hint/quit)")
                continue

            elapsed = time.perf_counter() - start
            attempted += 1
            times.append(elapsed)

            if check(expected, actual, rep.compare):
                correct += 1
                streak += 1
                best_streak = max(best_streak, streak)
                flame = "  " + "*" * streak if streak >= 3 else ""
                print(f"   OK  ({elapsed:.1f}s)  streak {streak}{flame}\n")
            else:
                streak = 0
                print(f"   X  ({elapsed:.1f}s)")
                print(f"      you typed: {answer}  ->  {_fmt(actual)}")
                print(f"      answer:    {rep.solution}  ->  {_fmt(expected)}")
                if _review(rep) == "quit":
                    return _summary(correct, attempted, skipped, times,
                                    best_streak, quit_early=True)
                print()
            break

    return _summary(correct, attempted, skipped, times, best_streak)


def _summary(correct, attempted, skipped, times, best_streak, quit_early=False):
    print("=" * 44)
    print("Quit early." if quit_early else "Session complete.")
    acc = (100 * correct / attempted) if attempted else 0.0
    avg = (sum(times) / len(times)) if times else 0.0
    print(f"  Correct:     {correct}/{attempted}  ({acc:.0f}% accuracy)")
    print(f"  Skipped:     {skipped}")
    print(f"  Best streak: {best_streak}")
    print(f"  Avg time:    {avg:.1f}s per rep")
    print("=" * 44)
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Tier 1 scientific-computing "
                                "fastball drills (numpy / pandas / matplotlib).")
    p.add_argument("--reps", type=int, help="number of reps")
    p.add_argument("--libs", nargs="+",
                   help=f"whole libraries: {', '.join(G.LIBRARIES)}")
    p.add_argument("--topics", nargs="+", help="specific topic keys")
    p.add_argument("--groups", nargs="+",
                   help=f"topic groups: {', '.join(G.GROUPS)}")
    p.add_argument("--seed", type=int, default=None, help="reproducible session")
    args = p.parse_args(argv)

    # If no selection given at all, fall into the interactive menu.
    if (args.reps is None and not args.topics and not args.groups
            and not args.libs):
        libs, groups, reps = interactive_setup()
        args.libs = libs
        args.groups = groups
        args.reps = reps

    reps = args.reps if args.reps else 20
    seed = args.seed if args.seed is not None else random.randint(0, 10**6)
    topics = resolve_topics(args)

    try:
        return run(topics, reps, seed)
    except KeyboardInterrupt:
        print("\n(interrupted)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
