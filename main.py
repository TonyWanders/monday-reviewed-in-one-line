#!/usr/bin/env python3
"""Write one funny one-line review of Monday to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The review is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 200 characters, a single line, not only white space.
"""

import os
import sys
from pathlib import Path

REVIEW = (
    "My Monday earned one star: 47 unread emails, a meeting about the "
    "meeting, and a Quick Sync that synced nothing."
)

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, one line, not blank.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"review is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("review is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("review must be a single line")
    return chars


def main() -> int:
    try:
        chars = validate(REVIEW)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(REVIEW, encoding="utf-8")
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
