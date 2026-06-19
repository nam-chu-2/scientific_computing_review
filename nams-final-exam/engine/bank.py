"""Load the question bank (public) and the grading key (quarantined).

Public, browsable-without-spoilers:   questions/tier{1,2,3}.json
Quarantined answer key + hidden tests: solutions/grading.py

A question's `prompt` / `notes` / `starter` may be written in the JSON as
a list of lines (nicer to author); they're joined with newlines on load.
"""

from __future__ import annotations

import importlib.util
import json
from dataclasses import dataclass, field
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
QUESTIONS_DIR = BASE / "questions"
SOLUTIONS_DIR = BASE / "solutions"
ATTEMPTS_DIR = BASE / "attempts"


def _text(value) -> str:
    """A string field that may be authored as a list of lines."""
    if isinstance(value, list):
        return "\n".join(value)
    return value or ""


@dataclass
class Question:
    id: str
    topic: str
    tier: int
    mode: str                       # "cli" | "script"
    prompt: str
    hint: str = ""
    notes: str = ""                 # concept explanation, NEVER the answer
    entry: str = ""                 # script: function name to grade
    starter: str = ""               # script: seed code for attempts/<id>.py
    visible: list = field(default_factory=list)   # script: example calls (display)
    requires: str = ""              # optional library gate, e.g. "pandas"


def _availability(lib: str) -> bool:
    if not lib:
        return True
    try:
        __import__(lib)
        return True
    except ImportError:
        return False


def load_questions() -> dict:
    """Return {id: Question} from questions/*.json, dropping unavailable ones."""
    out, dropped = {}, {}
    for path in sorted(QUESTIONS_DIR.glob("tier*.json")):
        for raw in json.loads(path.read_text(encoding="utf-8")):
            q = Question(
                id=raw["id"], topic=raw["topic"], tier=int(raw["tier"]),
                mode=raw["mode"], prompt=_text(raw["prompt"]),
                hint=_text(raw.get("hint", "")), notes=_text(raw.get("notes", "")),
                entry=raw.get("entry", ""), starter=_text(raw.get("starter", "")),
                visible=raw.get("visible", []), requires=raw.get("requires", ""),
            )
            if not _availability(q.requires):
                dropped.setdefault(q.requires, []).append(q.id)
                continue
            out[q.id] = q
    for lib, ids in dropped.items():
        print(f"({lib} not installed - skipping {len(ids)} question(s): "
              f"{', '.join(ids)})")
    return out


def load_grading() -> dict:
    """Import the quarantined GRADING dict from solutions/grading.py."""
    path = SOLUTIONS_DIR / "grading.py"
    spec = importlib.util.spec_from_file_location("_exam_grading", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.GRADING


# ----------------------------------------------------------------------
# Selection helpers
# ----------------------------------------------------------------------

def all_topics(questions: dict) -> list:
    seen = []
    for q in questions.values():
        if q.topic not in seen:
            seen.append(q.topic)
    return seen


def select(questions: dict, tiers=None, topics=None, modes=None) -> list:
    """Filter questions by tier / topic / mode. Returns a list of Questions."""
    pool = list(questions.values())
    if tiers:
        tiers = {int(t) for t in tiers}
        pool = [q for q in pool if q.tier in tiers]
    if topics:
        topics = {t.lower() for t in topics}
        pool = [q for q in pool
                if q.topic.lower() in topics or any(t in q.id.lower() for t in topics)]
    if modes:
        modes = {m.lower() for m in modes}
        pool = [q for q in pool if q.mode in modes]
    return pool
