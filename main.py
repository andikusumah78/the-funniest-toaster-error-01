#!/usr/bin/env python3
"""Toaster error entry for make.fun.

Saves one fixed error line to the file the grader reads.
No input, no network, no clock, no randomness: the same bytes
come out on every run, so the result is reproducible.
"""

import os
import sys

MESSAGE = "TOAST CANCELLED: THE BREAD HAS REVIEWED ITS OPTIONS AND CHOSEN TO REMAIN BREAD."
LIMIT = 120


def check(message):
    """Refuse anything the gate would refuse: blank, too long, or multi-line."""
    if not message or not message.strip():
        raise ValueError("empty message")
    if len(message) > LIMIT:
        raise ValueError("message is %d chars, limit is %d" % (len(message), LIMIT))
    if "\n" in message or "\r" in message:
        raise ValueError("message must fit on one line")
    message.encode("utf-8")


def destination():
    """Where entry.txt goes: MAKEFUN_OUTPUT_DIR, or /output when unset."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def save(message):
    """Write the message to entry.txt, then read it back to prove it stuck."""
    folder = destination()
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(message)
    with open(target, "r", encoding="utf-8") as handle:
        if handle.read() != message:
            raise ValueError("entry.txt differs from the message")
    if os.path.getsize(target) != len(message.encode("utf-8")):
        raise ValueError("entry.txt size differs from the message")
    return target


def main():
    check(MESSAGE)
    target = save(MESSAGE)
    print("wrote %d chars to %s" % (len(MESSAGE), target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
