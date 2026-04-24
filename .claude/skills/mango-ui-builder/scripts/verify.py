#!/usr/bin/env python3
"""verify.py — Smoke-test a rendered HTML page via localhost.

Checks:
  1. HTML file exists
  2. Parses as valid HTML (basic check)
  3. All inline JS has no syntax errors (via node if available)
  4. All `<img src>` / `<link href>` resolve (relative paths exist)
  5. No hardcoded secrets (API keys, passwords)

Usage:
    python verify.py <html-file-path>
"""
from __future__ import annotations
import io
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

# Force UTF-8 stdout (Windows fix for emoji output)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)


class ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.img_srcs: list[str] = []
        self.css_hrefs: list[str] = []
        self.scripts: list[str] = []
        self.inline_js: list[str] = []
        self._in_script = False

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "img" and "src" in attrs_d:
            self.img_srcs.append(attrs_d["src"])
        elif tag == "link" and attrs_d.get("rel", "").startswith("style") and "href" in attrs_d:
            self.css_hrefs.append(attrs_d["href"])
        elif tag == "script":
            if "src" in attrs_d:
                self.scripts.append(attrs_d["src"])
            else:
                self._in_script = True
                self._current_script = []

    def handle_data(self, data):
        if self._in_script:
            self._current_script.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._in_script:
            self.inline_js.append("".join(self._current_script))
            self._in_script = False


SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI/Anthropic-style API key"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"-----BEGIN (RSA |EC )?PRIVATE KEY-----", "Private key"),
    (r"['\"]password['\"]:\s*['\"][^'\"]+['\"]", "Hardcoded password"),
    (r"Bearer\s+[A-Za-z0-9\-._~+/]+=*", "Bearer token"),
]


def check(html_path: Path) -> int:
    print(f"🔍 Verifying: {html_path}")
    fails = 0

    # 1. File exists + readable
    if not html_path.is_file():
        print("  ❌ File does not exist")
        return 1
    content = html_path.read_text(encoding="utf-8")
    print(f"  ✅ File readable ({len(content)} bytes, {content.count(chr(10))+1} lines)")

    # 2. Parse HTML
    parser = ResourceParser()
    try:
        parser.feed(content)
        print(f"  ✅ HTML parses (img:{len(parser.img_srcs)}, link:{len(parser.css_hrefs)}, script:{len(parser.scripts)}, inline-js:{len(parser.inline_js)})")
    except Exception as e:
        print(f"  ❌ HTML parse error: {e}")
        fails += 1

    # 3. Check relative resource paths exist
    parent = html_path.parent
    for src in parser.img_srcs + parser.css_hrefs + parser.scripts:
        if src.startswith(("http://", "https://", "//", "data:")):
            continue  # external, skip
        target = (parent / src).resolve()
        if not target.exists():
            print(f"  ⚠️  Broken reference: {src}")
            fails += 1

    # 4. Inline JS syntax check (if node available)
    if parser.inline_js:
        try:
            import tempfile
            all_ok = True
            for idx, js in enumerate(parser.inline_js):
                with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
                    f.write(js)
                    tmp_path = f.name
                try:
                    r = subprocess.run(
                        ["node", "--check", tmp_path],
                        capture_output=True, text=True, timeout=5,
                    )
                    if r.returncode != 0:
                        print(f"  ⚠️  Inline JS #{idx+1} syntax issue: {r.stderr.strip()[:200]}")
                        fails += 1
                        all_ok = False
                finally:
                    Path(tmp_path).unlink(missing_ok=True)
            if all_ok:
                print(f"  ✅ Inline JS ({len(parser.inline_js)}) syntax OK")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("  ℹ️  Node not available — skipping JS syntax check")

    # 5. Secret scan
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, content):
            print(f"  🚨 Possible secret: {label}")
            fails += 1
    if not fails:
        print("  ✅ No secrets detected")

    # 6. Accessibility smoke-check
    if not re.search(r"<html[^>]+lang=", content):
        print("  ⚠️  Missing `lang` attribute on <html>")
        fails += 1
    if not re.search(r'<meta[^>]+name="viewport"', content):
        print("  ⚠️  Missing viewport meta tag (responsive issue)")
        fails += 1

    print()
    if fails == 0:
        print("✅ All checks passed.")
        return 0
    else:
        print(f"❌ {fails} issue(s) to fix.")
        return fails


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify.py <html-file-path>")
        sys.exit(2)
    sys.exit(check(Path(sys.argv[1]).resolve()))
