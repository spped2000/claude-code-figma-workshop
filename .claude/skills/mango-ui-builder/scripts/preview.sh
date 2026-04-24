#!/usr/bin/env bash
# preview.sh — Start localhost server for HTML preview + auto-open browser
# Usage: preview.sh <html-file-path> [port]
#
# Example:
#   ./preview.sh demos/demo-b/src/rental_list.html
#   ./preview.sh src/dashboard.html 3000

set -e

HTML_PATH="${1:?Usage: preview.sh <html-file-path> [port]}"
PORT="${2:-8080}"

# Resolve absolute path + parent directory
if [[ ! -f "$HTML_PATH" ]]; then
  echo "❌ File not found: $HTML_PATH"
  exit 1
fi

HTML_FILE=$(basename "$HTML_PATH")
PARENT_DIR=$(dirname "$HTML_PATH")

# Check if port is already in use
if command -v lsof >/dev/null 2>&1; then
  if lsof -i :$PORT >/dev/null 2>&1; then
    echo "⚠️  Port $PORT is in use — trying $((PORT+1))"
    PORT=$((PORT+1))
  fi
fi

# Pick server: python3 > python > node
if command -v python3 >/dev/null 2>&1; then
  SERVER_CMD="python3 -m http.server $PORT --directory $PARENT_DIR"
elif command -v python >/dev/null 2>&1; then
  SERVER_CMD="python -m http.server $PORT --directory $PARENT_DIR"
elif command -v npx >/dev/null 2>&1; then
  SERVER_CMD="npx serve $PARENT_DIR -p $PORT"
else
  echo "❌ No static server available. Install Python or Node."
  exit 1
fi

URL="http://localhost:$PORT/$HTML_FILE"

echo "🚀 Starting: $SERVER_CMD"
echo "📍 URL:      $URL"
echo "📁 Serving:  $PARENT_DIR"
echo ""
echo "Press Ctrl+C to stop."
echo ""

# Open browser (cross-platform)
sleep 1 && {
  case "$(uname -s)" in
    MINGW*|CYGWIN*|MSYS*) start "" "$URL" ;;
    Darwin) open "$URL" ;;
    Linux) xdg-open "$URL" 2>/dev/null || echo "Open manually: $URL" ;;
  esac
} &

exec $SERVER_CMD
