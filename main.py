#!/usr/bin/env python3
"""Entrypoint for the news-image-20261126 round-2 entry.

Standard library only (os, shutil, sys). The grade sandbox runs
Python 3.13 with no third-party packages installed, so this file
imports nothing beyond the standard library. It copies the
pre-rendered front page (entry.png, sitting beside this file) to
the output directory, after checking the PNG signature and size.
"""
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(src, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
        handle.seek(0, os.SEEK_END)
        size = handle.tell()
    if magic != PNG_MAGIC:
        print("entry.png: not a PNG file", file=sys.stderr)
        return 1
    if size > MAX_BYTES:
        print("entry.png: %d bytes, over the 1 MiB cap" % size,
              file=sys.stderr)
        return 1
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
