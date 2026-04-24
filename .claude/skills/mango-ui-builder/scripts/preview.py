#!/usr/bin/env python3
"""preview.py — Cross-platform localhost HTML preview with auto-open + port fallback.

Auto-detects project root by walking up directories looking for markers
(mock-data/, package.json, pyproject.toml, .git) so CSV/JSON/asset paths
like ../../../mock-data/ work correctly.

Usage:
    python preview.py <html-file-path> [port]

Example:
    python preview.py demos/demo-b/src/rental_list.html
    python preview.py src/dashboard.html 3000
"""
from __future__ import annotations
import http.server
import io
import socketserver
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Force UTF-8 stdout (Windows fix for emoji output)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)


def find_free_port(start: int = 8080, max_tries: int = 20) -> int:
    for port in range(start, start + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise RuntimeError(f"No free port in range {start}-{start + max_tries}")


def find_project_root(html_path: Path) -> Path:
    """Walk up looking for project markers. Prefer strong markers (.git, .claude,
    pyproject.toml, package.json) over data folders to avoid stopping at subprojects."""
    strong = {".git", ".claude", "pyproject.toml", "package.json"}
    weak = {"mock-data", "data"}
    current = html_path.parent
    candidates = [current, *current.parents]

    # Pass 1: find highest ancestor with any strong marker
    for ancestor in candidates:
        if any((ancestor / m).exists() for m in strong):
            return ancestor
    # Pass 2: fall back to first ancestor with weak marker
    for ancestor in candidates:
        if any((ancestor / m).exists() for m in weak):
            return ancestor
    return current


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python preview.py <html-file-path> [port]")
        return 1

    html_path = Path(sys.argv[1]).resolve()
    if not html_path.is_file():
        print(f"❌ File not found: {html_path}")
        return 1

    requested_port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    port = find_free_port(requested_port)
    if port != requested_port:
        print(f"⚠️  Port {requested_port} busy → using {port}")

    root = find_project_root(html_path)
    try:
        url_path = html_path.relative_to(root).as_posix()
    except ValueError:
        # HTML not under root (shouldn't happen) — fall back to parent
        root = html_path.parent
        url_path = html_path.name
    url = f"http://localhost:{port}/{url_path}"

    handler = http.server.SimpleHTTPRequestHandler

    class ScopedHandler(handler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(root), **kwargs)
        def log_message(self, fmt, *args):  # quieter output
            print(f"  [{self.address_string()}] {fmt % args}")

    with socketserver.TCPServer(("", port), ScopedHandler) as httpd:
        print(f"🚀 Root:     {root}")
        print(f"📍 URL:      {url}")
        print("   (Ctrl+C to stop)")
        print()

        # Open browser after small delay (so server is ready)
        def open_browser():
            time.sleep(0.8)
            webbrowser.open(url)
        threading.Thread(target=open_browser, daemon=True).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
