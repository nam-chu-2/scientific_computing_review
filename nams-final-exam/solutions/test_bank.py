"""Self-test of the quarantined answer key (for maintainers, not players).

Verifies the bank is internally consistent:
  - cli:    the canonical expression evaluates, and its value matches itself
            under the question's compare mode (catches a wrong compare mode);
  - script: the canonical solution passes ALL of its own cases AND satisfies
            its structural constraints (max_loops / forbid);
  - parity: every question has a grading entry and vice-versa.

Run either way:
    pytest solutions/test_bank.py        # if pytest is installed
    python solutions/test_bank.py        # plain stdlib -- prints a report
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from engine import bank, cli_eval, script_harness          # noqa: E402
from engine.compare import compare                          # noqa: E402

GRADING = bank.load_grading()
QUESTIONS = bank.load_questions()
CLI_IDS = sorted(i for i, g in GRADING.items() if "entry" not in g)
SCRIPT_IDS = sorted(i for i, g in GRADING.items() if "entry" in g)


def _check_cli(qid):
    g = GRADING[qid]
    val = cli_eval.expected_value(g)
    assert compare(val, val, g.get("compare", "exact")), \
        f"{qid}: value doesn't match itself under compare='{g.get('compare')}'"


def _check_script(qid):
    g = GRADING[qid]
    rep = script_harness.run_checks(g["canonical"], f"<canonical:{qid}>", g)
    assert not rep.get("structural_error"), f"{qid}: {rep.get('structural_error')}"
    assert not rep.get("load_error"), f"{qid}: {rep.get('load_error')}"
    assert rep["ok"], \
        f"{qid}: canonical failed {rep['total'] - rep['passed']}/{rep['total']} cases"


def _check_parity():
    qids, gids = set(QUESTIONS), set(GRADING)
    assert not (qids - gids), f"questions without grading: {sorted(qids - gids)}"
    assert not (gids - qids), f"grading without a question: {sorted(gids - qids)}"


# --- pytest entry points (only if pytest is installed) ---------------
try:
    import pytest

    @pytest.mark.parametrize("qid", CLI_IDS)
    def test_cli(qid):
        _check_cli(qid)

    @pytest.mark.parametrize("qid", SCRIPT_IDS)
    def test_script(qid):
        _check_script(qid)

    def test_parity():
        _check_parity()
except ImportError:
    pass


def _main():
    fails = []
    for qid in CLI_IDS:
        try:
            _check_cli(qid)
        except AssertionError as exc:
            fails.append(str(exc))
    for qid in SCRIPT_IDS:
        try:
            _check_script(qid)
        except AssertionError as exc:
            fails.append(str(exc))
    try:
        _check_parity()
    except AssertionError as exc:
        fails.append(str(exc))

    total = len(CLI_IDS) + len(SCRIPT_IDS) + 1
    print(f"bank self-test: {total - len(fails)}/{total} passed "
          f"({len(CLI_IDS)} cli, {len(SCRIPT_IDS)} script, 1 parity)")
    for f in fails:
        print("  FAIL:", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(_main())
