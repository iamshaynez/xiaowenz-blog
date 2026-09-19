#!/usr/bin/env bash
# upload_media.sh — push migrated media to Cloudflare R2.
#
# NOT executed by sync.py; run by hand after credentials are in place.
#
# Required env:
#   R2_BUCKET    target bucket name, e.g. xiaowenz-media
#   R2_ENDPOINT  https://<accountid>.r2.cloudflarestorage.com
#   AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY   (R2 API token)
#
# What it does:
#   1. syncs media-sync/images/  ->  s3://$R2_BUCKET/images/
#      (these back https://media.xiaowenz.com/images/<basename>,
#       which markdown image links were rewritten to)
#   2. if ./originals/*.mp3 exists, uploads each as
#      s3://$R2_BUCKET/audio/{episode_slug}.mp3
#      (episode slugs: see data/audio-manifest.csv)
set -euo pipefail

: "${R2_BUCKET:?set R2_BUCKET}"
: "${R2_ENDPOINT:?set R2_ENDPOINT}"

cd "$(dirname "$0")/../.."

aws s3 sync media-sync/images "s3://$R2_BUCKET/images" \
  --endpoint-url "$R2_ENDPOINT" \
  --cache-control "public, max-age=31536000, immutable"

if compgen -G "originals/*.mp3" > /dev/null; then
  aws s3 sync originals "s3://$R2_BUCKET/audio" \
    --endpoint-url "$R2_ENDPOINT" \
    --cache-control "public, max-age=31536000, immutable"
else
  echo "note: no originals/*.mp3 found - upload episode audio later" \
    "(expected names: <episode_slug>.mp3, see data/audio-manifest.csv)"
fi
