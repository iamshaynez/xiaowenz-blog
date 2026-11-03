#!/usr/bin/env bash
# render.sh — OG 卡片 SVG → PNG（1200×630），输出到 static/og/
# 依赖：Google Chrome（headless 截图，字体用系统 Songti SC / Hiragino Sans GB）
# 用法：cd site/scripts/og && ./render.sh
set -euo pipefail

cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for src in src/*.svg; do
  name="$(basename "${src%.svg}")"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=1 --window-size=1200,630 \
    --screenshot="../../static/og/${name}.png" "$src" 2>/dev/null
  echo "rendered ${name}.png"
done
