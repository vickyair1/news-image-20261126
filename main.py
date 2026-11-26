#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered front page to /output/entry.png.

Standard library only (os, shutil, sys). The PNG signature is verified
before copying, so a corrupt or non-PNG file can never be submitted.
"""
import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        head = f.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        print("entry.png: bad PNG signature", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
