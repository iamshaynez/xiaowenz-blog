#!/usr/bin/env python3
"""lint-content.py — site 内容门禁。

直推 content/ 是合法发布路径（md 进仓库 = 发布），本脚本守住 publish.sh
曾经把守的不变量，供 pre-push 钩子与 CI 使用：

  1. 博客布局：content/blog/{YYYY}/{yyyy-mm-dd}-{slug}.md，日期与年份取自 frontmatter date。
     URL 只由 frontmatter slug 决定（/blog/{slug}.html 冻结资产），所以 slug 必填、
     且 ^[a-z0-9-]+$；文件名只管排序，改名/挪目录不影响 URL。
     例外：slug 本身已以本文日期开头的老文章（Typlog 时代的 2012-04-12-12），文件名 = {slug}.md
  2. 博客年份目录必须有 _index.md 年份 stub（layout: year、year: YYYY），否则 /blog/YYYY/ 缺页
  3. title 非空、date 可解析、draft 不为 true
  4. episodes：文件名即 slug（{slug}.md，slug 字段若有须一致；/episodes/{slug} 冻结资产）
  5. recipes：同 episodes（slug 是 /recipes/{slug} 冻结资产，拼音命名）

用法: python3 scripts/lint-content.py   （在 site 仓库根执行；退出码非 0 = 有问题）
"""
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("需要 PyYAML: pip3 install --user pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?([+-]\d{2}:?\d{2}|Z)?$")

problems: list[str] = []

def check_blog_layout(path: Path, fm: dict) -> None:
    """博客文章必须在 blog/{YYYY}/{yyyy-mm-dd}-{slug}.md（规则 1、2）。"""
    slug = str(fm.get("slug") or "")
    if not SLUG_RE.match(slug):
        problems.append(f"{path}: slug 缺失或非法（必填，^[a-z0-9-]+$；URL 由它决定）: {slug!r}")
        return
    day = str(fm.get("date") or "")[:10]
    if not DAY_RE.match(day):
        return  # date 异常由通用检查报告
    expect = f"{slug}.md" if slug.startswith(day + "-") else f"{day}-{slug}.md"
    if path.name != expect:
        problems.append(f"{path}: 文件名应为 {expect}（{{yyyy-mm-dd}}-{{slug}}.md，日期取自 date）")
    year_dir = ROOT / "content" / "blog" / day[:4]
    if path.parent != year_dir:
        problems.append(f"{path}: 应位于 content/blog/{day[:4]}/（年份取自 date）")
    stub = year_dir / "_index.md"
    if not stub.exists():
        problems.append(f"{year_dir}: 缺年份 stub _index.md（layout: year、year: {day[:4]}）")

def check(path: Path, kind: str) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not m:
        problems.append(f"{path}: 缺 frontmatter")
        return
    fm = yaml.safe_load(m.group(1)) or {}
    stem = path.stem
    if kind == "blog":
        check_blog_layout(path, fm)
    elif stem != "_index":
        if not SLUG_RE.match(stem):
            problems.append(f"{path}: 文件名 {stem!r} 不是合法 slug（^[a-z0-9-]+$）")
        if fm.get("slug") and str(fm["slug"]) != stem:
            problems.append(f"{path}: frontmatter slug={fm['slug']!r} 与文件名 {stem!r} 不一致")
    if not str(fm.get("title") or "").strip():
        problems.append(f"{path}: title 为空")
    if not DATE_RE.match(str(fm.get("date") or "")):
        problems.append(f"{path}: date 缺失或格式异常: {fm.get('date')!r}")
    if fm.get("draft") is True:
        problems.append(f"{path}: draft=true 会不构建（要么删掉这行，要么别推）")

for pattern, kind in (("blog/**/*.md", "blog"), ("episodes/*.md", "episodes"), ("recipes/*.md", "recipes")):
    for p in sorted((ROOT / "content").glob(pattern)):
        if kind == "blog" and p.stem == "_index":
            continue  # section 首页与年份 stub，不是文章
        check(p, kind)

# ── 播客对账：剧集 md ↔ core 302 链路 ──────────────────────────────
# 每集 audio_slug 必须在 core 拿到 302（音频已注册），跳转对象的实际大小
# 必须等于 frontmatter 的 audio_bytes——抄错一位在这里拦下。
# 网络不可达只警告不拦截（离线也能 push）；LINT_OFFLINE=1 跳过本节。
# 传输走系统 curl（urllib 在本机对 CF 端点不可靠，见 scripts/sync/README）。

CORE_PUBLIC = os.environ.get("CORE_PUBLIC_URL", "https://core.xiaowenz.com")

def curl_head_info(url: str) -> tuple[int, str, dict[str, str]]:
    """HEAD 一个 URL：返回 (状态码, 重定向地址, 响应头)。失败返回 (0, "", {})。"""
    try:
        r = subprocess.run(
            ["curl", "-sI", "--max-time", "15", "-w", "\n%{http_code} %{redirect_url}", url],
            capture_output=True, text=True, timeout=20,
        )
    except OSError:
        return 0, "", {}
    lines = [l for l in r.stdout.strip().splitlines() if l.strip()]
    if not lines:
        return 0, "", {}
    tail = lines[-1].split()
    status = int(tail[0]) if tail and tail[0].isdigit() else 0
    redirect = tail[1] if len(tail) > 1 else ""
    headers: dict[str, str] = {}
    for l in lines[:-1]:
        if ":" in l:
            k, v = l.split(":", 1)
            headers[k.strip().lower()] = v.strip()
    return status, redirect, headers

network_ok = True
if os.environ.get("LINT_OFFLINE") != "1":
    for p in sorted((ROOT / "content").glob("episodes/*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
        fm = yaml.safe_load(m.group(1)) if m else {}
        slug = str(fm.get("audio_slug") or "").strip()
        if not slug:
            problems.append(f"{p}: episodes 必须有 audio_slug（音频经 core /a/ 计数分发）")
            continue
        code, redirect, _ = curl_head_info(f"{CORE_PUBLIC}/a/{slug}.mp3")
        if code == 0:
            network_ok = False
            continue  # 网络不可达：稍后统一警告，不判失败
        if code != 302:
            problems.append(f"{p}: core /a/{slug}.mp3 返回 {code}（应为 302；音频未上传或未注册）")
            continue
        declared = fm.get("audio_bytes")
        if declared is None or not redirect:
            continue
        c3, _, h3 = curl_head_info(redirect)
        actual = h3.get("content-length")
        if actual and int(actual) != int(declared):
            problems.append(
                f"{p}: audio_bytes={declared} 与实际对象 {actual} 不一致（frontmatter 抄错或音频换代未同步）"
            )
    if not network_ok:
        print("⚠ core 不可达，播客对账跳过（仅本地校验生效）")

if problems:
    print(f"✗ 内容门禁未过（{len(problems)} 处）：")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("✓ 内容门禁通过")
