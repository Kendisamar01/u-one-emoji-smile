import os
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent
OUTPUT_DIR = Path("/tmp/emojiout")
ENTRY = OUTPUT_DIR / "entry.txt"


def is_emoji(char):
    point = ord(char)
    return (
        0x1F000 <= point <= 0x1FAFF
        or 0x2600 <= point <= 0x27BF
        or 0x2190 <= point <= 0x21FF
        or point in {0x00A9, 0x00AE, 0x203C, 0x2049, 0x2122, 0x2139, 0x3030, 0x303D, 0x3297, 0x3299}
    )


def grapheme_count(text):
    count = 0
    join_next = False
    regional_open = False
    for char in text:
        point = ord(char)
        if point == 0x200D:
            join_next = True
            continue
        if (
            point in (0xFE0E, 0xFE0F)
            or 0x1F3FB <= point <= 0x1F3FF
            or unicodedata.category(char).startswith("M")
        ):
            continue
        if 0x1F1E6 <= point <= 0x1F1FF:
            if not regional_open and not join_next:
                count += 1
            regional_open = not regional_open
            join_next = False
            continue
        regional_open = False
        if not join_next:
            count += 1
        join_next = False
    return count


def main():
    ENTRY.unlink(missing_ok=True)
    env = os.environ.copy()
    env["MAKEFUN_OUTPUT_DIR"] = str(OUTPUT_DIR)
    subprocess.run(
        [sys.executable, str(REPO / "main.py")],
        cwd=REPO,
        env=env,
        check=True,
    )
    data = ENTRY.read_bytes()
    text = data.decode("utf-8")
    assert 1 <= len(text) <= 8, f"gate needs 1-8 characters, got {len(text)}"
    assert not any(char.isspace() for char in text), "entry contains whitespace"
    assert not any(char.isalnum() for char in text), "entry contains a word or number"
    assert any(is_emoji(char) for char in text), "entry contains no emoji"
    assert grapheme_count(text) == 1, f"expected one emoji grapheme, got {grapheme_count(text)}"
    assert data == text.encode("utf-8"), "entry is not exact UTF-8 of one emoji"
    print("PASS")


if __name__ == "__main__":
    main()
