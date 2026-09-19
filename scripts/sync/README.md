# scripts/sync — Typlog → Hugo content migration

Migrates all content from the live Typlog site (https://xiaowenz.com) into this
repo's `content/` tree, downloads Typlog-hosted images, and records manifests.

## Re-run

```bash
python3 scripts/sync/sync.py              # full sync; cached HTML makes reruns near-instant
python3 scripts/sync/sync.py --refresh    # ignore HTML cache, refetch every page
python3 scripts/sync/sync.py --no-media   # convert content but skip image downloads
```

Dependencies: `pip3 install --user markdownify beautifulsoup4` (transport is the
system `curl` via subprocess — Cloudflare's chunked HTTP/1.1 on this host breaks
urllib's `http.client`).

The script is idempotent:

- Fetched HTML is cached in `data/cache/<sha1(url)>.html` (0.25s polite delay on
  network misses only). Delete the cache or pass `--refresh` to refetch.
- Generated files under `content/` are overwritten deterministically.
- Images already present in `media-sync/images/` are not re-downloaded.

## Outputs

| Path | Meaning |
| --- | --- |
| `content/blog/{slug}.md` | One file per `/blog/{slug}.html` post |
| `content/blog/{YYYY}/_index.md` | Year stub (`layout: year`) |
| `content/episodes/{slug}.md` | Podcast show notes + audio frontmatter |
| `content/pages/{name}.md` | Standalone pages (about, read-books, ...) |
| `content/archive/{YYYY}.md`, `content/archive/_index.md` | Archive pages |
| `data/cache/` | Raw HTML cache (safe to delete) |
| `data/media-manifest.csv` | Image migration ledger |
| `data/audio-manifest.csv` | Podcast audio ledger |
| `data/sync-report.json` | Machine-readable run summary |
| `media-sync/images/` | Downloaded image binaries (gitignored) |

## data/media-manifest.csv

One row per Typlog-hosted image (`i/s/s3.typlog.com`, `?x-oss-process=...`
suffix stripped to get the original):

- `original_url` — where it was downloaded from
- `basename` / `local_file` — file on disk under `media-sync/images/`
- `final_url` — `https://media.xiaowenz.com/images/{basename}`; markdown image
  links were rewritten to this. The upload step below is what makes it resolve.

Third-party-hosted images (cdn.sa.net, vip2.loli.io, i.see.you, ...) are left
untouched in the markdown by design.

## data/audio-manifest.csv

One row per podcast episode. `original_url` is the **expiring** signed
`r.typlog.com` URL — kept for provenance only, never hotlinked. Frontmatter
carries only stable metadata (`audio_slug`, `audio_bytes`, `audio_duration`,
`audio_image`); the theme resolves audio through `params.audioBase`.

**Action needed:** supply the original `.mp3` for each episode and upload to R2
as `audio/{episode_slug}.mp3`.

## Uploading media to R2

See `upload_media.sh` (documented, not executed by the sync):

```bash
export R2_BUCKET=... R2_ENDPOINT=https://<accountid>.r2.cloudflarestorage.com
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=...
bash scripts/sync/upload_media.sh                 # images
# plus, after supplying originals:
aws s3 cp originals/ "s3://$R2_BUCKET/audio/" --endpoint-url "$R2_ENDPOINT" --recursive
```
