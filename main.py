"""The Best Meal You Ever Had -- make.fun entry.

Writes a single sentence (at most 200 characters) about the best meal I
ever had to <MAKEFUN_OUTPUT_DIR>/entry.txt, then validates what was written
against the kit gate. Pure Python standard library.
"""

import os

SENTENCE = (
    "Nobody believes me, but the best meal of my life was instant mie "
    "goreng eaten on a ferry deck at sunrise, salt wind in my face and "
    "my wife asleep on my shoulder."
)

MAX_CHARS = 200


def validate(text):
    """Enforce the kit gate: one sentence, 1-200 chars, non-whitespace, UTF-8."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d-character cap"
            % (len(text), MAX_CHARS)
        )
    terminators = [c for c in text if c in ".!?"]
    if len(terminators) != 1 or not text.endswith(terminators[0]):
        raise ValueError("entry must be exactly one sentence")
    text.encode("utf-8")
    return True


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    validate(SENTENCE)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(SENTENCE)
    with open(path, encoding="utf-8") as handle:
        written = handle.read()
    validate(written)
    if written.encode("utf-8") != SENTENCE.encode("utf-8"):
        raise ValueError("written bytes do not match the sentence")
    if os.path.getsize(path) != len(SENTENCE.encode("utf-8")):
        raise ValueError("written file size does not match the sentence")
    print("wrote %d characters to %s" % (len(SENTENCE), path))


if __name__ == "__main__":
    main()
