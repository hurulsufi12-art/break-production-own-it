"""Break Production, Own It — entry program.

Writes one line to /output/entry.txt: the line an AI agent prints the
moment it breaks production. Stdlib only, deterministic, no network,
no model calls.

Final text (locked by session B's critique in PLAN.md, "## Koreksi
sesi B"): "I dropped the production database and its only backup.
The migration was me." — 76 characters, 76 bytes, all ASCII.

Why this line, from the judge brief published in RULES.txt — the
criteria are weighed in this order: (1) a brutally honest postmortem
excuse printed right after breaking production — two short sentences,
an instant confession with no preamble; (2) owns the damage plainly
and specifically — "production database" plus "its only backup"
(no way back: irreversible), no hedging, no passive voice, no
deflection ("blamed" is gone entirely); (3) catchy and quotable —
the identity twist "The migration was me" survives out of context;
(4) the agent's own voice — "I dropped…" + "…was me", the actor
speaking as itself, no generic sysadmin ("on call" is gone);
(5) spends 76 characters well, every word earning its place, and
lands the confession on the last word ("me").
"""
import os

TEXT = "I dropped the production database and its only backup. The migration was me."


def check_gate(text):
    """Enforce the scorer's gate (RULES.txt) plus the single-line rule.

    Gate: UTF-8, 1 to 200 characters, not whitespace-only; and the task:
    a single line under 200 chars. The gate counts characters, not
    bytes. Fail loudly instead of writing an invalid entry.
    """
    if not isinstance(text, str):
        raise SystemExit("entry text is not a string")
    if not 1 <= len(text) <= 200 or not text.strip():
        raise SystemExit("entry text violates the 1-200 char gate")
    # Single line: no newline, carriage return, or any other control
    # character — a control byte inside the text would break the one
    # line the grader reads.
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise SystemExit("entry text must be a single line without control characters")


def main():
    check_gate(TEXT)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Write atomically: a crash mid-write must never leave a truncated
    # entry.txt for the grader to read. Write to a temp file in the same
    # directory, flush it to disk, then rename over the target.
    # No trailing newline: the gate counts the file's characters, so
    # the file must be exactly TEXT — 76 bytes, not 77.
    tmp_path = os.path.join(out_dir, ".entry.txt.tmp")
    final_path = os.path.join(out_dir, "entry.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, final_path)
    # Read back and verify at the byte level: the gate is byte-exact
    # (76 bytes, no newline, no BOM), and the grader reads bytes,
    # so compare the raw bytes on disk — not just the decoded text.
    # Fail loudly instead of shipping a corrupt entry.
    with open(final_path, "rb") as f:
        if f.read() != TEXT.encode("utf-8"):
            raise SystemExit("entry.txt byte mismatch after atomic write")


if __name__ == "__main__":
    main()
