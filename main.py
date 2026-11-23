#!/usr/bin/env python3
"""Write the entry image to the output directory.

The image (entry.png) ships in this repository next to this file. This
program only copies it byte for byte, so the two grading runs produce
identical output. Standard library only; no network access.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def output_dir():
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def main() -> int:
    source = Path(__file__).resolve().parent / IMAGE_NAME
    if not source.is_file():
        print(f"missing image: {source}", file=sys.stderr)
        return 1
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / IMAGE_NAME
    shutil.copyfile(source, dest)
    copied = dest.stat().st_size
    expected = source.stat().st_size
    if copied != expected:
        print(f"size mismatch after copy: {copied} != {expected}",
              file=sys.stderr)
        return 1
    if sha256_of(dest) != sha256_of(source):
        print("hash mismatch after copy", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({copied} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
