#!/usr/bin/env python3
"""The Funniest Toaster Error Message - make.fun entry.

Writes a single funny error message to /output/entry.txt.

The gate requires UTF-8 text of 1 to 120 characters, not only
whitespace. The line is fixed, so every run writes byte-identical
output: no randomness, no clock, no network, pure stdlib.

Helpers: resolve_out_dir() reads MAKEFUN_OUTPUT_DIR (default
"/output") to pick the output directory; write_entry() writes the
line to entry.txt in that directory and verifies it by reading
it back.
"""

import os
import sys

# Fixed line (not generated): determinism - every run writes byte-identical output.
LINE = "TOAST CANCELLED: THE BREAD HAS REVIEWED ITS OPTIONS AND CHOSEN TO REMAIN BREAD."

GATE_MAX_CHARS = 120


def validate_line(line):
    """Check the line against the gate: 1-120 chars, not blank."""
    if not isinstance(line, str):
        raise TypeError("line must be str")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if len(line) > GATE_MAX_CHARS:
        raise ValueError("line is %d chars, over the 120 limit" % len(line))
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line: no embedded newlines")
    line.encode("utf-8")
    return line


def resolve_out_dir():
    """Return the output directory: MAKEFUN_OUTPUT_DIR, or "/output"."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def write_entry(line, out_dir):
    """Write line to entry.txt in out_dir and verify by reading it back."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line)
    # Read back and verify: the file on disk must be exactly the line
    # we validated, otherwise the run is not reproducible.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise ValueError("read-back mismatch: entry.txt does not match the validated line")
    return path


def main():
    line = validate_line(LINE)
    out_dir = resolve_out_dir()
    path = write_entry(line, out_dir)
    print("wrote %d chars to %s" % (len(line), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
