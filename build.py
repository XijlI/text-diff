#!/usr/bin/env python3
"""Assemble a single self-contained TextDiff.html from src/app.html + src/diff.min.js."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
MARKER = "/*@@JSDIFF@@*/"

html = (SRC / "app.html").read_text(encoding="utf-8")
lib = (SRC / "diff.min.js").read_text(encoding="utf-8")
lib = re.sub(r"//# sourceMappingURL=\S*", "", lib).strip()

assert MARKER in html, "marker missing"
assert "</script" not in lib.lower(), "library would break out of the script tag"

out = html.replace(MARKER, lib)
target = ROOT / "TextDiff.html"
target.write_text(out, encoding="utf-8")
print(f"wrote {target} ({len(out):,} chars, lib {len(lib):,})")
