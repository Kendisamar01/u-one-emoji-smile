import os
from pathlib import Path

EMOJI = "🙂"

output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / "entry.txt").write_text(EMOJI, encoding="utf-8")
