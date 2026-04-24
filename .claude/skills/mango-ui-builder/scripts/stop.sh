#!/usr/bin/env bash
# stop.sh — Stop any running http.server on given port (default 8080)
PORT="${1:-8080}"

if command -v lsof >/dev/null 2>&1; then
  PID=$(lsof -ti :$PORT)
  if [[ -n "$PID" ]]; then
    kill $PID && echo "✅ Stopped server on port $PORT (PID $PID)"
  else
    echo "ℹ️  No process listening on port $PORT"
  fi
elif command -v netstat >/dev/null 2>&1; then
  # Windows Git Bash fallback
  PID=$(netstat -ano | grep ":$PORT " | grep LISTENING | awk '{print $5}' | head -1)
  if [[ -n "$PID" ]]; then
    taskkill //PID $PID //F && echo "✅ Stopped server on port $PORT (PID $PID)"
  else
    echo "ℹ️  No process listening on port $PORT"
  fi
else
  echo "❌ Can't detect running servers (lsof/netstat not found)"
  exit 1
fi
