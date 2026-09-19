#!/usr/bin/env python3
"""
sync.py — migrate xiaowenz.com (Typlog) content into this Hugo repo.

Idempotent and re-runnable:
  - HTML is cached under data/cache/ (sha1(url).html); reruns only hit the
    network for URLs never fetched before (0.25s polite delay on misses).
  - Generated content files are overwritten deterministically.
  - Downloaded images under media-sync/images/ are skipped when present.

Usage:
  python3 scripts/sync/sync.py              # full sync (fetch + convert + images)
  python3 scripts/sync/sync.py --no-media   # skip image downloading
  python3 scripts/sync/sync.py --refresh    # ignore HTML cache, refetch all
"""

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from markdownify import markdownify as md_convert

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE_DIR = os.path.join(ROOT, "data", "cache")
MEDIA_DIR = os.path.join(ROOT, "media-sync", "images")
CONTENT_DIR = os.path.join(ROOT, "content")
DATA_DIR = os.path.join(ROOT, "data")

BASE = "https://xiaowenz.com"
MEDIA_BASE = "https://media.xiaowenz.com/images/"
CST = timezone(timedelta(hours=8))

UA = {"User-Agent": "Mozilla/5.0 (compatible; xiaowenz-migration/1.0)"}

STANDALONE_PAGES = [
    "about",
    "read-books",
    "run-a-uk-company",
    "service-and-afdian",
    "business-reports",
]

ITUNES_NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}

report = {
    "posts": 0,
    "episodes": 0,
    "pages": 0,
    "year_stubs": 0,
    "images_downloaded": 0,
    "images_failed": [],
    "failures": [],
    "notes": "",
}
notes = []


# ---------------------------------------------------------------- fetch/cache

def cache_path(url):
    return os.path.join(CACHE_DIR, hashlib.sha1(url.encode()).hexdigest() + ".html")


def fetch(url, refresh=False):
    """Fetch URL text, with on-disk cache. 0.25s polite delay on misses.

    Transport is curl: Cloudflare serves this host as chunked HTTP/1.1 with a
    stream ending urllib's http.client rejects (IncompleteRead), while curl
    tolerates it. Kept stdlib-only.
    """
    path = cache_path(url)
    if not refresh and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    data = fetch_binary(url)
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return data.decode("utf-8", "replace")


def fetch_binary(url):
    import subprocess
    last_err = None
    for attempt in range(3):
        time.sleep(0.25)
        p = subprocess.run(
            ["curl", "-fsSL", "--retry", "2", "-A", UA["User-Agent"], url],
            capture_output=True)
        if p.returncode == 0 and p.stdout:
            return p.stdout
        last_err = RuntimeError(
            f"curl exited {p.returncode}: {p.stderr.decode('utf-8', 'replace')[:200]}")
        time.sleep(1.5 * (attempt + 1))
    raise last_err


# ---------------------------------------------------------------- extraction

def parse_date(iso_z, slug):
    """Parse Typlog '2025-04-10T11:09:02Z' -> RFC3339 in +08:00.
    Fall back to a slug date prefix like 2019-12-01-58."""
    if iso_z:
        dt = datetime.fromisoformat(iso_z.replace("Z", "+00:00"))
        return dt.astimezone(CST).isoformat(timespec="seconds")
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})-", slug)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}T08:00:00+08:00"
    return None


def clean_body(body):
    """Strip non-content leftovers from the extracted article body."""
    for tag in body.find_all(["script", "style", "meta", "link", "noscript"]):
        tag.decompose()
    # schema.org metadata blocks carried inside articleBody
    for tag in body.find_all(attrs={"itemscope": True}):
        tag.decompose()
    for tag in body.find_all(attrs={"itemprop": ["image", "publisher", "dateModified", "author"]}):
        tag.decompose()
    # subscription forms / comment containers / share buttons, if any leaked in
    for cls in ("js-subscribe", "subscribe", "comment", "entry-share", "entry-enjoy"):
        for tag in body.find_all(class_=cls):
            tag.decompose()
    return body


def extract_article(html, slug):
    """Return dict(title, date, description, tags, body_html) from a Typlog page."""
    soup = BeautifulSoup(html, "html.parser")

    h1 = soup.select_one("h1.article__title") or soup.find("h1")
    title = h1.get_text(strip=True) if h1 else None

    t = soup.select_one("time.dt-published") or soup.find("time", attrs={"datetime": True})
    date = parse_date(t["datetime"] if t else None, slug)

    desc = None
    m = soup.find("meta", attrs={"name": "description"})
    if m and m.get("content"):
        desc = m["content"].strip()

    tags = []
    for a in soup.select("article a.p-category"):
        href = a.get("href", "")
        mm = re.match(r"^/tags/([^/]+)/?$", href)
        if mm and mm.group(1) not in tags:
            tags.append(mm.group(1))

    body = soup.select_one("div.article__body")
    if not body:
        raise ValueError("no div.article__body found")
    clean_body(body)
    return {"title": title, "date": date, "description": desc,
            "tags": tags, "body_html": str(body)}


def to_markdown(body_html):
    md = md_convert(
        body_html,
        heading_style="ATX",
        bullets="-",
        strong_em_symbol="*",
        strip=["script", "style", "meta", "link", "source", "picture"],
    )
    # collapse runs of blank lines, strip trailing spaces, drop empty leftovers
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    # empty links/images left over from stripped wrappers
    md = re.sub(r"!\[\]\(\s*\)", "", md)
    md = re.sub(r"\[\]\(\s*\)", "", md)
    return md.strip() + "\n"


# ---------------------------------------------------------------- frontmatter

def yaml_str(s):
    # JSON double-quoted strings are valid YAML scalars
    return json.dumps(str(s), ensure_ascii=False)


def frontmatter(mapping):
    lines = ["---"]
    for key, val in mapping.items():
        if val is None:
            continue
        if isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        elif isinstance(val, int):
            lines.append(f"{key}: {val}")
        elif isinstance(val, list):
            if not val:
                continue
            lines.append(f"{key}:")
            for item in val:
                lines.append(f"  - {yaml_str(item)}")
        else:
            lines.append(f"{key}: {yaml_str(val)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def write_content(rel_path, fm, body_md=""):
    path = os.path.join(CONTENT_DIR, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter(fm))
        if body_md:
            f.write("\n" + body_md)
    return path


# ---------------------------------------------------------------- images

TYplog_IMG_RE = re.compile(
    r"!\[([^\]]*)\]\((https?://(?:i|s|s3)\.typlog\.com/[^)\s]+)\)"
)

media_rows = {}       # original_url -> row dict
used_basenames = {}   # basename -> original_url


def strip_oss(url):
    p = urlparse(url)
    return p.scheme + "://" + p.netloc + p.path


def collect_images(md_text):
    """Return (rewritten_md, [(original_url, basename)]) for typlog-hosted imgs."""
    found = []

    def repl(m):
        alt, url = m.group(1), m.group(2)
        orig = strip_oss(url)
        base = os.path.basename(urlparse(orig).path)
        if base in used_basenames and used_basenames[base] != orig:
            stem, ext = os.path.splitext(base)
            base = f"{stem}-{hashlib.sha1(orig.encode()).hexdigest()[:8]}{ext}"
        used_basenames.setdefault(base, orig)
        found.append((orig, base))
        return f"![{alt}]({MEDIA_BASE}{base})"

    return TYplog_IMG_RE.sub(repl, md_text), found


def download_one(job):
    orig, base = job
    dest = os.path.join(MEDIA_DIR, base)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return (orig, base, os.path.getsize(dest), False)
    try:
        data = fetch_binary(orig)
        os.makedirs(MEDIA_DIR, exist_ok=True)
        with open(dest, "wb") as f:
            f.write(data)
        return (orig, base, len(data), True)
    except Exception as e:  # noqa: BLE001
        return (orig, base, str(e), None)


# ---------------------------------------------------------------- sitemap

def classify(urls):
    posts, episodes, years = [], [], set()
    for u in urls:
        p = urlparse(u).path
        if re.match(r"^/blog/[^/]+\.html$", p):
            posts.append(u)
        elif re.match(r"^/episodes/[^/]+$", p):
            episodes.append(u)
        elif re.match(r"^/blog/\d{4}/$", p):
            years.add(p.strip("/").split("/")[-1])
    return sorted(posts), sorted(episodes), sorted(years)


def slug_of(url, ext=".html"):
    p = urlparse(url).path.rstrip("/")
    s = p.rsplit("/", 1)[-1]
    return s[: -len(ext)] if ext and s.endswith(ext) else s


# ---------------------------------------------------------------- audio feed

def parse_audio_feed(xml_text):
    items = {}
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    chan_img = channel.find("itunes:image", ITUNES_NS)
    cover = chan_img.get("href") if chan_img is not None else None
    for it in channel.findall("item"):
        link = it.findtext("link") or it.findtext("guid")
        if not link:
            continue
        slug = slug_of(link, ext=None)
        enc = it.find("enclosure")
        img = it.find("itunes:image", ITUNES_NS)
        items[slug] = {
            "title": it.findtext("title"),
            "link": link,
            "pubDate": it.findtext("pubDate"),
            "enclosure_url": enc.get("url") if enc is not None else None,
            "bytes": int(enc.get("length")) if enc is not None and enc.get("length") else None,
            "duration": it.findtext("itunes:duration", namespaces=ITUNES_NS),
            "episode": it.findtext("itunes:episode", namespaces=ITUNES_NS),
            "image": img.get("href") if img is not None else None,
        }
    return items, cover


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-media", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- sitemap ---
    sitemap = fetch(BASE + "/sitemap.xml", refresh=args.refresh)
    urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    posts, episode_urls, sitemap_years = classify(urls)
    print(f"sitemap: {len(posts)} posts, {len(episode_urls)} episodes, "
          f"years {','.join(sitemap_years)}")

    image_jobs = {}

    # --- blog posts ---
    years = set()
    for url in posts:
        slug = slug_of(url)
        try:
            art = extract_article(fetch(url, refresh=args.refresh), slug)
            md_text, imgs = collect_images(to_markdown(art["body_html"]))
            for orig, base in imgs:
                image_jobs[orig] = base
            fm = {
                "title": art["title"] or slug,
                "date": art["date"],
                "slug": slug,
                "description": art["description"],
                "tags": art["tags"],
                "draft": False,
                "type": "blog",
            }
            write_content(f"blog/{slug}.md", fm, md_text)
            if art["date"]:
                years.add(art["date"][:4])
            report["posts"] += 1
        except Exception as e:  # noqa: BLE001
            report["failures"].append({"url": url, "error": str(e)})

    # --- episodes ---
    feed_xml = fetch(BASE + "/feed/audio.xml", refresh=args.refresh)
    feed_items, feed_cover = parse_audio_feed(feed_xml)
    audio_rows = []
    for url in episode_urls:
        slug = slug_of(url, ext=None)
        try:
            art = extract_article(fetch(url, refresh=args.refresh), slug)
            md_text, imgs = collect_images(to_markdown(art["body_html"]))
            for orig, base in imgs:
                image_jobs[orig] = base
            fi = feed_items.get(slug, {})
            fm = {
                "title": art["title"] or fi.get("title") or slug,
                "date": art["date"],
                "slug": slug,
                "description": art["description"],
                "draft": False,
                "type": "episode",
            }
            if fi:
                if fi.get("episode"):
                    fm["episode"] = int(fi["episode"])
                fm["audio_slug"] = slug
                if fi.get("bytes"):
                    fm["audio_bytes"] = fi["bytes"]
                if fi.get("duration"):
                    fm["audio_duration"] = fi["duration"]
                if fi.get("image"):
                    # migrate episode cover off the expiring typlog host
                    orig = strip_oss(fi["image"])
                    if orig in image_jobs:
                        base = image_jobs[orig]  # shared cover, reuse basename
                    else:
                        base = os.path.basename(urlparse(orig).path)
                        stem, ext = os.path.splitext(base)
                        base = f"episode-{slug}{ext}"
                        image_jobs[orig] = base
                    fm["audio_image"] = MEDIA_BASE + base
                audio_rows.append([slug, fi.get("enclosure_url") or "",
                                   fi.get("bytes") or "", fi.get("duration") or ""])
            else:
                report["failures"].append(
                    {"url": url, "error": "not found in feed/audio.xml"})
            write_content(f"episodes/{slug}.md", fm, md_text)
            report["episodes"] += 1
        except Exception as e:  # noqa: BLE001
            report["failures"].append({"url": url, "error": str(e)})

    with open(os.path.join(DATA_DIR, "audio-manifest.csv"), "w", newline="",
              encoding="utf-8") as f:
        f.write("# Audio originals manifest. The r.typlog.com URLs below are EXPIRING\n")
        f.write("# signed URLs kept for provenance only -- do NOT hotlink them.\n")
        f.write("# Action needed: supply the original .mp3 for each episode and upload\n")
        f.write("# to R2 as audio/{episode_slug}.mp3 (see scripts/sync/upload_media.sh).\n")
        w = csv.writer(f)
        w.writerow(["episode_slug", "original_url", "bytes", "duration"])
        w.writerows(audio_rows)

    # --- standalone pages (live site serves these WITHOUT trailing slash) ---
    for name in STANDALONE_PAGES:
        url = f"{BASE}/{name}"
        try:
            art = extract_article(fetch(url, refresh=args.refresh), name)
            md_text, imgs = collect_images(to_markdown(art["body_html"]))
            for orig, base in imgs:
                image_jobs[orig] = base
            fm = {
                "title": art["title"] or name,
                "date": art["date"],
                "url": f"/{name}/",
                "type": "page",
            }
            write_content(f"pages/{name}.md", fm, md_text)
            report["pages"] += 1
        except Exception as e:  # noqa: BLE001
            report["failures"].append({"url": url, "error": str(e)})

    # synthetic service pages (do not exist on the live site; core will use them)
    write_content("pages/search.md", {
        "title": "搜索", "url": "/search/", "layout": "search", "type": "page"})
    write_content("pages/subscribed.md", {
        "title": "订阅成功", "url": "/subscribed/", "type": "page"},
        "验证成功，欢迎订阅三杯过后。\n")
    write_content("pages/subscribe-expired.md", {
        "title": "链接已过期", "url": "/subscribe-expired/", "type": "page"},
        "这个订阅确认链接已经过期了，请回到[订阅页](/)重新订阅，我们会给你发一封新的确认邮件。\n")
    report["pages"] += 3

    # --- year stubs + archive ---
    all_years = sorted(set(years) | set(sitemap_years))
    for y in all_years:
        write_content(f"blog/{y}/_index.md",
                      {"title": y, "layout": "year"})
        write_content(f"archive/{y}.md",
                      {"title": f"{y} 归档", "layout": "archive"})
        report["year_stubs"] += 2
    write_content("archive/_index.md", {"title": "归档"})

    # --- home ---
    write_content("_index.md", {"title": "三杯过后 | Xiaowen.Z Deployed"})

    # --- images ---
    # podcast cover: config.yaml params.podcast.image expects podcast-cover.jpg
    # (downloaded even when the same image also serves as an episode cover)
    extra_jobs = []
    if feed_cover:
        extra_jobs.append((strip_oss(feed_cover), "podcast-cover.jpg"))
    downloaded = failed = 0
    if not args.no_media:
        jobs = sorted(image_jobs.items()) + extra_jobs
        with ThreadPoolExecutor(max_workers=4) as ex:
            for orig, base, size, did in ex.map(download_one, jobs):
                if did is None:
                    failed += 1
                    report["images_failed"].append({"url": orig, "error": size})
                else:
                    downloaded += 1  # ensured on disk (new or already cached)
                    media_rows[orig] = {
                        "basename": base,
                        "local_file": os.path.join("media-sync", "images", base),
                        "final_url": MEDIA_BASE + base,
                        "bytes": size,
                    }
    else:
        for orig, base in sorted(image_jobs.items()):
            media_rows[orig] = {
                "basename": base,
                "local_file": os.path.join("media-sync", "images", base),
                "final_url": MEDIA_BASE + base,
                "bytes": "",
            }
    report["images_downloaded"] = downloaded

    with open(os.path.join(DATA_DIR, "media-manifest.csv"), "w", newline="",
              encoding="utf-8") as f:
        f.write("# Downloaded from i/s/s3.typlog.com (x-oss-process suffix stripped =\n")
        f.write("# original). Upload media-sync/images/ to R2 as images/ so final_url\n")
        f.write("# resolves (see scripts/sync/upload_media.sh).\n")
        w = csv.writer(f)
        w.writerow(["original_url", "basename", "local_file", "final_url", "bytes"])
        for orig in sorted(media_rows):
            r = media_rows[orig]
            w.writerow([orig, r["basename"], r["local_file"], r["final_url"],
                        r["bytes"]])

    # --- report ---
    notes.append("Standalone pages on the live site serve at /about (no trailing "
                 "slash; /about/ is 404). Hugo url frontmatter uses /about/; with "
                 "pretty-URL hosting (e.g. Cloudflare Pages) the canonical served "
                 "path matches the no-slash form.")
    dup_eps = {}
    for slug, fi in feed_items.items():
        if fi.get("episode"):
            dup_eps.setdefault(fi["episode"], []).append(slug)
    for num, slugs in dup_eps.items():
        if len(slugs) > 1:
            notes.append(f"itunes:episode {num} is shared by {slugs} "
                         "(upstream feed data inconsistency; kept as-is).")
    report["notes"] = " ".join(notes)
    with open(os.path.join(DATA_DIR, "sync-report.json"), "w",
              encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(json.dumps({k: v for k, v in report.items() if k != "notes"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
