"""Nam's Final Exam -- a deliberate-practice drill for your CS coursework.

Retrieval practice with immediate feedback. You read a spec, write code, run
it, and get told right/wrong. You never see a solution before attempting one;
canonical answers and hidden tests stay quarantined in solutions/.

Two answer modes:
  cli    -- type a SINGLE expression; graded by value (many forms accepted).
  script -- write a function in attempts/<id>.py; graded by a hidden test
            suite via the `check` command.

The loop is: Generate (attempt) -> Struggle -> Resolve (`check`) ->
Reconstruct (`explain`) -> Elaborate (`ask`).

Run from this folder:
    python exam.py                       # interactive: pick tiers + reps
    python exam.py --reps 30             # 30 questions, all tiers
    python exam.py --tier 1              # only Tier 1 (fastballs)
    python exam.py --tier 2 3            # Tiers 2 and 3
    python exam.py --topics loops vectorization
    python exam.py --mode script         # only script questions
    python exam.py --seed 1 --reps 20    # fully reproducible session
    python exam.py --list                # list every question and exit
"""

from __future__ import annotations

import argparse
import random
import sys
import time

from engine import bank, cli_eval, coach, script_harness
from engine.compare import fmt


# ----------------------------------------------------------------------
# Small display helpers
# ----------------------------------------------------------------------

def _block(text, indent="   "):
    print(indent + text.replace("\n", "\n" + indent) + "\n")


def _reveal(question, grading):
    """Show concept notes + the canonical answer (a deliberate spoiler)."""
    _block(coach.explain(question, grading))


def _do_ask(question, grading, raw):
    """Handle `ask <q>`. Falls back to NOTES ONLY (never the answer) offline."""
    q = raw[3:].strip()
    if not q:
        print("   usage: ask <your question>   e.g.  ask why use a set here?\n")
        return
    answer = coach.ask(question, grading, q)
    if answer is None:
        print("   (live Q&A not enabled - showing concept notes; the answer "
              "stays hidden. `pip install anthropic` + set ANTHROPIC_API_KEY)")
        _block(question.notes or "(no notes for this question)")
    else:
        _block(answer)


def _review(question, grading):
    """After a miss/skip/reveal: let the player dig in before moving on."""
    print("   ('ask <q>', Enter = next, or 'quit')")
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
        if low == "explain":
            _reveal(question, grading)
        elif low == "ask" or low.startswith("ask "):
            _do_ask(question, grading, raw)
        else:
            print("   commands: ask <q> | (Enter)=next | quit")


# ----------------------------------------------------------------------
# CLI-mode question
# ----------------------------------------------------------------------

def present_cli(question, grading):
    """Run one cli question. Returns (outcome, elapsed)."""
    print(question.prompt)
    print("   (type one expression, or: hint | explain | ask <q> | skip | quit)")
    start = time.perf_counter()

    while True:
        try:
            answer = input(">>> ").strip()
        except EOFError:
            answer = "quit"
        low = answer.lower()

        if low == "quit":
            return "quit", None
        if low == "skip":
            print(f"   skipped.")
            _reveal(question, grading)
            outcome = "skipped"
            return ("quit", None) if _review(question, grading) == "quit" else (outcome, None)
        if low == "hint":
            print(f"   hint: {question.hint}\n")
            continue
        if low == "explain":
            print("   (revealing the answer - this one counts as missed)")
            _reveal(question, grading)
            return ("quit", None) if _review(question, grading) == "quit" \
                else ("incorrect", time.perf_counter() - start)
        if low == "ask" or low.startswith("ask "):
            _do_ask(question, grading, answer)
            continue
        if not answer:
            continue

        try:
            ok, actual, expected = cli_eval.evaluate(grading, answer)
        except Exception as exc:  # noqa: BLE001 -- syntax/runtime: re-prompt free
            print(f"   ! {type(exc).__name__}: {exc}  -- try again "
                  f"(or hint/skip/quit)")
            continue

        elapsed = time.perf_counter() - start
        if ok:
            print(f"   OK  ({elapsed:.1f}s)")
            return "correct", elapsed
        print(f"   X  ({elapsed:.1f}s)")
        print(f"      you typed: {answer}  ->  {fmt(actual)}")
        _reveal(question, grading)
        return ("quit", None) if _review(question, grading) == "quit" \
            else ("incorrect", elapsed)


# ----------------------------------------------------------------------
# Script-mode question
# ----------------------------------------------------------------------

def _seed_attempt(question, force=False):
    """Create attempts/<id>.py from the starter (unless it already exists)."""
    bank.ATTEMPTS_DIR.mkdir(parents=True, exist_ok=True)
    path = bank.ATTEMPTS_DIR / f"{question.id}.py"
    if force or not path.exists():
        header = (f"# {question.id} -- edit this function, then type 'check' "
                  f"in the exam.\n# (run `reset` in the exam to restore this "
                  f"starter.)\n\n")
        path.write_text(header + question.starter + "\n", encoding="utf-8")
    return path


def _print_check(report):
    """Pretty-print a check report without leaking hidden inputs."""
    if report.get("structural_error"):
        print(f"   ! {report['structural_error']}\n")
        return
    if report.get("load_error"):
        print(f"   ! {report['load_error']}\n")
        return
    print(f"   ran {report['total']} checks: "
          f"{report['passed']} passed, {report['total'] - report['passed']} failed")
    for r in report["cases"]:
        mark = "ok " if r["ok"] else "X  "
        if r["visible"]:
            detail = ""
            if not r["ok"]:
                if "error" in r:
                    detail = f"  raised {r['error']}"
                else:
                    detail = f"  got {r.get('got')}, expected {r['expected']}"
            print(f"     {mark} {r['label']}{detail}")
        else:
            print(f"     {mark} {r['label']} (hidden)")
    print()


def present_script(question, grading):
    """Run one script question. Returns (outcome, elapsed)."""
    print(question.prompt)
    path = _seed_attempt(question)
    print(f"\n   your scratch file:  {path}")
    if question.visible:
        print("   visible examples:")
        for ex in question.visible:
            print(f"     - {ex}")
    print("   (edit the file, then: check | run | hint | explain | ask <q> | "
          "reset | skip | quit)")
    start = time.perf_counter()

    while True:
        try:
            cmd = input(">>> ").strip()
        except EOFError:
            cmd = "quit"
        low = cmd.lower()

        if low == "quit":
            return "quit", None
        if low == "skip":
            print("   skipped.")
            _reveal(question, grading)
            return ("quit", None) if _review(question, grading) == "quit" \
                else ("skipped", None)
        if low == "reset":
            _seed_attempt(question, force=True)
            print(f"   reset {path} to the starter.\n")
            continue
        if low == "hint":
            print(f"   hint: {question.hint}\n")
            continue
        if low == "explain":
            print("   (revealing the solution - this one counts as missed)")
            _reveal(question, grading)
            return ("quit", None) if _review(question, grading) == "quit" \
                else ("incorrect", time.perf_counter() - start)
        if low == "ask" or low.startswith("ask "):
            _do_ask(question, grading, cmd)
            continue
        if low in ("check", "run"):
            if not path.exists():
                _seed_attempt(question, force=True)
            source = path.read_text(encoding="utf-8")
            if low == "run":
                print("   " + script_harness.run_only(source, str(path), grading) + "\n")
                continue
            report = script_harness.run_checks(source, str(path), grading)
            _print_check(report)
            if report["ok"]:
                elapsed = time.perf_counter() - start
                print(f"   all checks pass!  ({elapsed:.1f}s)\n")
                return "correct", elapsed
            continue
        if not cmd:
            continue
        print("   commands: check | run | hint | explain | ask <q> | reset | "
              "skip | quit\n")


# ----------------------------------------------------------------------
# Session
# ----------------------------------------------------------------------

def _build_order(pool, reps, rng):
    """Pick `reps` questions, shuffling and not repeating until the pool empties."""
    order, bag = [], []
    for _ in range(reps):
        if not bag:
            bag = pool[:]
            rng.shuffle(bag)
        order.append(bag.pop())
    return order


def run(pool, grading, reps, seed):
    rng = random.Random(seed)
    order = _build_order(pool, reps, rng)

    print(f"\nDrilling {reps} questions over {len(pool)} available. (seed={seed})")
    print("Practice loop:  Generate -> Struggle -> Resolve (check) -> "
          "Reconstruct (explain) -> Elaborate (ask).")
    if not coach.live_available():
        print("(tip: `ask` uses offline notes until you `pip install anthropic` "
              "and set ANTHROPIC_API_KEY)")

    correct = attempted = skipped = 0
    streak = best_streak = 0
    times = []

    for i, q in enumerate(order, 1):
        tier_name = {1: "Fastball", 2: "Mixed pitch", 3: "Breaking ball"}.get(q.tier, "?")
        print(f"\n--- Q{i}/{reps}  [T{q.tier} {tier_name}]  {q.mode}  ({q.topic}) ---")
        present = present_script if q.mode == "script" else present_cli
        outcome, elapsed = present(q, grading[q.id])

        if outcome == "quit":
            break
        if outcome == "skipped":
            skipped += 1
            streak = 0
            continue
        attempted += 1
        if elapsed is not None:
            times.append(elapsed)
        if outcome == "correct":
            correct += 1
            streak += 1
            best_streak = max(best_streak, streak)
            if streak >= 3:
                print(f"   streak {streak}  " + "*" * streak)
        else:
            streak = 0

    _summary(correct, attempted, skipped, times, best_streak)


def _summary(correct, attempted, skipped, times, best_streak):
    acc = (100 * correct / attempted) if attempted else 0.0
    avg = (sum(times) / len(times)) if times else 0.0
    print("\n" + "=" * 48)
    print("Session complete.")
    print(f"  Correct:     {correct}/{attempted}  ({acc:.0f}% accuracy)")
    print(f"  Skipped:     {skipped}")
    print(f"  Best streak: {best_streak}")
    print(f"  Avg time:    {avg:.1f}s per attempted question")
    print("=" * 48)
    print("Review notes (after drilling): solutions/notes.md")


# ----------------------------------------------------------------------
# Selection / CLI
# ----------------------------------------------------------------------

def _list(questions):
    for q in sorted(questions.values(), key=lambda q: (q.tier, q.mode, q.id)):
        print(f"  T{q.tier}  {q.mode:6s}  {q.id:22s}  {q.topic}")


def interactive_setup(questions):
    print("\n=== Nam's Final Exam ===")
    counts = {t: sum(1 for q in questions.values() if q.tier == t) for t in (1, 2, 3)}
    print("Tiers:")
    print(f"  1  Fastballs     (atomic recall, fast)        [{counts[1]} questions]")
    print(f"  2  Mixed pitches (combine 2-3 concepts)       [{counts[2]} questions]")
    print(f"  3  Breaking balls(gotchas, debug, vectorize)  [{counts[3]} questions]")
    raw = input("\nPick tiers (e.g. '1 2', or Enter for ALL): ").strip()
    tiers = [t for t in raw.split() if t in ("1", "2", "3")]

    reps = 20
    raw = input("How many questions? [20]: ").strip()
    if raw:
        try:
            reps = max(1, int(raw))
        except ValueError:
            print("  (not a number -> using 20)")
    return tiers, reps


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Nam's Final Exam -- deliberate-practice drills from your "
                    "COMP 1005/1405 coursework + numpy notebook.")
    p.add_argument("--tier", nargs="+", help="tiers to include: 1 2 3")
    p.add_argument("--topics", nargs="+", help="topic names or id substrings")
    p.add_argument("--mode", nargs="+", help="answer modes: cli script")
    p.add_argument("--reps", type=int, help="number of questions")
    p.add_argument("--seed", type=int, default=None, help="reproducible session")
    p.add_argument("--list", action="store_true", help="list all questions and exit")
    args = p.parse_args(argv)

    questions = bank.load_questions()
    grading = bank.load_grading()
    if not questions:
        print("No questions available."); return 1
    if args.list:
        _list(questions); return 0

    if (args.reps is None and not args.tier and not args.topics and not args.mode):
        tiers, reps = interactive_setup(questions)
        args.tier, args.reps = tiers, reps

    reps = args.reps if args.reps else 20
    seed = args.seed if args.seed is not None else random.randint(0, 10**6)
    pool = bank.select(questions, tiers=args.tier, topics=args.topics, modes=args.mode)
    if not pool:
        print("Nothing matched that selection. Try --list."); return 1

    try:
        run(pool, grading, reps, seed)
    except KeyboardInterrupt:
        print("\n(interrupted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
