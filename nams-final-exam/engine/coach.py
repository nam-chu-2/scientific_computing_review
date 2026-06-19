"""Coaching: `explain` (always offline) and `ask` (live Claude, optional).

- explain(question, grading) -> concept notes + the canonical answer.
  Offline, no API key. This is the "Reconstruct" step of the practice loop;
  it reveals the answer, so the runner counts the question as not-correct.

- ask(question, grading, q) -> free-form Q&A about the question via the
  Claude API when `anthropic` is installed AND a key is set; otherwise
  returns None so the caller falls back to explain. The "Elaborate" step.

Enabling live Q&A:
    pip install anthropic
    bash:        export ANTHROPIC_API_KEY=sk-ant-...
    PowerShell:  $env:ANTHROPIC_API_KEY = "sk-ant-..."
Optional model override:  EXAM_MODEL (default claude-opus-4-8)
    bash:        export EXAM_MODEL=claude-sonnet-4-6
    PowerShell:  $env:EXAM_MODEL = "claude-sonnet-4-6"
"""

from __future__ import annotations

import os

_MODEL = os.environ.get("EXAM_MODEL", "claude-opus-4-8")

_SYSTEM = (
    "You are a concise Python + data-science tutor helping a student during "
    "a deliberate-practice drill. They are prepping for a data-science "
    "internship; their stack is Python and SQL. They just attempted a "
    "problem and want to understand it. Answer in a few sentences. Focus on "
    "the concept and the common gotcha, and connect it to data-science work "
    "when natural. Plain text, no LaTeX. Keep code to short inline snippets."
)


def explain(question, grading: dict) -> str:
    """Offline: concept note + the canonical answer for this question."""
    note = question.notes or "(no notes for this question yet)"
    canonical = grading.get("canonical", "").strip()
    if question.mode == "script":
        body = "\n".join("    " + ln for ln in canonical.splitlines())
        return f"{note}\n  canonical solution:\n{body}"
    return f"{note}\n  canonical answer:  {canonical}"


def live_available() -> bool:
    """True if the anthropic SDK is importable and a credential is set."""
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    return bool(os.environ.get("ANTHROPIC_API_KEY")
                or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def ask(question, grading: dict, user_question: str):
    """Free-form Q&A via Claude. Returns text, or None if live Q&A is off."""
    if not live_available():
        return None

    import anthropic

    context = (
        f"The drill prompt was:\n{question.prompt}\n\n"
        f"The canonical answer is:\n{grading.get('canonical', '')}\n\n"
        f"(tier {question.tier}, mode {question.mode}, topic {question.topic})\n\n"
        f"Student's question: {user_question}"
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
    except anthropic.APIError as exc:
        return (f"(live Q&A failed: {type(exc).__name__}: {exc}. "
                f"Showing offline notes instead.)")
