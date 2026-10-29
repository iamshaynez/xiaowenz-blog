# xiaowenz.com — 静态站（Hugo）

三杯过后 | Xiaowen.Z Deployed。第三代架构：Hugo 静态生成 + Cloudflare Pages 托管；评论、订阅、Newsletter、统计由独立自研服务 **xiaowen-core**（私有仓库）承担。本仓库 = 内容 + 主题，Git 是内容的唯一真相源。

## 快速开始

```bash
hugo server -D          # 本地预览 http://localhost:1313
hugo --minify           # 产出到 public/
npx pagefind --site public   # 生成搜索索引（/search/ 依赖）
```

## 目录契约

```
content/
  blog/{slug}.md          # 博客，URL = /blog/{slug}.html（与 Typlog 时代一致）
  blog/{YYYY}/_index.md   # 年度索引 /blog/{YYYY}/
  episodes/{slug}.md      # 播客，URL = /episodes/{slug}，frontmatter 见下
  archive/{YYYY}.md       # /archive/{YYYY}/ 归档页
  pages/*.md              # 独立页（about / read-books / search / subscribed ...）
themes/xuanmo/            # 玄墨主题（自研，Typlog 版移植）
scripts/sync/             # Typlog 内容同步脚本 + 媒体清单（迁移一次性用途）
media-sync/               # 已下载的媒体原件（gitignored，待传 R2）
```

### 播客剧集 frontmatter

```yaml
type: episode
episode: 7
audio_slug: "my-episode-slug"      # 对应 R2 上 audio/{slug}.mp3
audio_bytes: 14277501              # 必须准确，iTunes enclosure length 依赖
audio_duration: "16:45"
```

feed 里的 enclosure URL 由 `config.yaml` 的 `params.audioBase`（core 的 302 计数端点）+ `audio_slug.mp3` 拼成；GUID = 页面 URL（无尾斜杠），与 Apple/Spotify 存量订阅兼容。

## 发布流

- **写文章**：新建 `content/blog/{slug}.md` → push 到 main → Pages 自动构建上线。
- **发播客**：① 用 core 管理台或 `scripts/sync/upload_media.sh` 把 MP3 传 R2 的 `audio/` 前缀；② 新建剧集 md 填好 frontmatter → push。Apple/Spotify/小宇宙下次抓取自动更新。
- **Newsletter**：在 core 管理台写 markdown 群发，不在本仓库。发文后可在管理台「新建 Newsletter」页直接粘贴文章 URL 抓取生成草稿（标题/导语/链接自动填），人工检查后发送。

### 内容门禁（slug 与 frontmatter 守护）

直推即发布，URL 是冻结资产——推前门禁把守命名与元数据不变量：

```bash
python3 scripts/lint-content.py          # 手动跑
git config core.hooksPath .githooks      # 一次性启用 pre-push 自动跑（本仓已配置）
```

CI（`content-lint` 工作流）在每次 push/PR 上提供同样检查的快速失败信号；Pages 构建不看它状态，所以本地钩子是第一道闸。

## URL 策略（重要）

Hugo 0.164 对 `/blog/:slug.html` 输出目录式页面（尾斜杠 URL）。为保持与 Typlog 完全一致的规范 URL：

- 主题内 `util/canonical-url.html` 统一输出无尾斜杠的 canonical/og:url/sitemap/feed 链接（博客、播客、独立页）；
- `themes/xuanmo/static/_redirects` 用 Cloudflare Pages 的 200 rewrite 把无斜杠 URL 映射到目录内容，**零 301，规范 URL 不变**。

改动 URL 结构前，先读 `themes/xuanmo/layouts/partials/util/canonical-url.html` 的规则。

## Cloudflare Pages 部署

- 构建命令：`hugo --minify && npx pagefind --site public`
- 输出目录：`public`
- 环境变量：`HUGO_VERSION=0.164.0`（钉版本）
- 域名：`xiaowenz.com` 绑定到 Pages 项目

## 相关文档

- 迁移切换手册：`MIGRATION.md`
- core 服务规格：core 仓库的 `docs/SPEC.md`
