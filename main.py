#!/usr/bin/env python3
"""
Sum up 20 November 2026 world news in one image.
make.fun bounty: news-image-20261120, $250, 50 places paid.
Deadline: Sun 22 Nov 2026 00:00 UTC.

The front page itself (entry.png, a broadsheet in the manner of a
classic newspaper nameplate paper - off-white paper, black serif
type, thin rules, columns, no bright panels, no icons, no flat AI
look) ships in this repository, and this program copies it to the
output directory. That is the kit's own simplest program.

Standard library only, on purpose: the grader runs Python 3.13 with
nothing installed before it runs, so Pillow is NOT available there.
The previous version imported PIL and died on the import, which is
why the first submission failed its run check. This version imports
nothing beyond the standard library.

Deterministic: no network, no random, no timestamps, no external
files. The output is byte-identical to entry.png in this repository.
It never writes beside its own file: in the grader that folder is
read-only, and only the output directory is writable.

Run: python3 main.py
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    shutil.copyfile(src, out)
    if out.stat().st_size != src.stat().st_size:
        raise SystemExit(f"copy incomplete: {out} is not {src.stat().st_size} bytes")
    print(f"Wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
