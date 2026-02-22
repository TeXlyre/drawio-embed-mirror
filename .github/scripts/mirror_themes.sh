#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$(pwd)}"

declare -A THEMES=(["light"]="kennedy" ["dark"]="dark")

for theme in "${!THEMES[@]}"; do
  ui="${THEMES[$theme]}"
  node "$WORKSPACE/.github/scripts/download.js" "$ui" "$theme" "$WORKSPACE"
done

for theme in "${!THEMES[@]}"; do
  mkdir -p "$WORKSPACE/drawio-embed/$theme/resources"

  cat > "$WORKSPACE/drawio-embed/$theme/service-worker.js" <<'EOF'
self.addEventListener('install', () => { self.skipWaiting(); });
self.addEventListener('activate', (e) => { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', () => {});
EOF

  curl -fsSL -o "$WORKSPACE/drawio-embed/$theme/shortcuts.svg" \
    "https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp/shortcuts.svg"
done