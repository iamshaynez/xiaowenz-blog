#!/usr/bin/env python3
"""lint-content.py — site 内容门禁。

直推 content/ 是合法发布路径（md 进仓库 = 发布），本脚本守住 publish.sh
曾经把守的不变量，供 pre-push 钩子与 CI 使用：

  1. 博客文件名即 slug：{slug}.md，且 ^[a-z0-9-]+$（URL 冻结资产的前提）
  2. frontmatter 的 slug 字段（若有）必须与文件名一致
  3. title 非空、date 可解析、draft 不为 true
  4. episodes：同上（slug 同样是 /episodes/{slug} 冻结资产）

用法: python3 scripts/lint-content.py   （在 site 仓库根执行；退出码非 0 = 有问题）
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("需要 PyYAML: pip3 install --user pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?([+-]\d{2}:?\d{2}|Z)?$")

problems: list[str] = []

def check(path: Path, kind: str) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not m:
        problems.append(f"{path}: 缺 frontmatter")
        return
    fm = yaml.safe_load(m.group(1)) or {}
    stem = path.stem
    if stem != "_index":
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

for pattern, kind in (("blog/*.md", "blog"), ("episodes/*.md", "episodes")):
    for p in sorted((ROOT / "content").glob(pattern)):
        check(p, kind)

if problems:
    print(f"✗ 内容门禁未过（{len(problems)} 处）：")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("✓ 内容门禁通过")
