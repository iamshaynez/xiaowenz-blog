# MIGRATION.md — Typlog → 自研切换手册

切换原则：**先全部就绪，再切 DNS；播客 feed 连续性是最高优先级；旧站保留观察期。**

> **2026-10-25 勘察备注**：线上仍为 Typlog（经 Cloudflare）；`core.xiaowenz.com` 尚无公开 DNS 记录。
> 本地内容与线上已全量对齐（152 篇博客 + 6 集播客，slug 零缺漏）——Typlog 2026-10 的
> lastmod 批量变化只是其模板升级（`<picture>` webp/懒加载标记），重跑 `sync.py --refresh`
> 仅产生 frontmatter 噪声（YAML 引号风格、`&quot;` 实体、episode 丢 season/subtitle），
> 正文零变化，已验证并回滚；**迁移前不必再同步**，除非在 Typlog 后台新发内容。

> **2026-10-28 进度**：v3 已合并 main 并发布到 Cloudflare Pages 生产环境，`blog.xiaowenz.com`
> 即新站（apex 仍指 Typlog，作为切换前的 staging 域名）。发布机制：**生产分支是 main**，
> 推 main 即生产构建，推其他分支只有 preview。core 已落 gb-test（见阶段 1）。注意：Pages
> 项目当前实际用 Hugo 0.126.1 构建（建议在项目环境变量里设 `HUGO_VERSION=0.164.0` 与 README 钉死版本一致）。

## 阶段 0：资产抢救（动手最早，互不依赖）

- [ ] Typlog 后台导出订阅者名单 CSV
- [x] 下载 6 集播客音频原件（r.typlog.com 是签名 URL，会过期；清单在 `data/audio-manifest.csv`）——
      成片已在本地 `garden/av/` 各项目内（episode.mp3），上传 R2 时以 `audio_slug` 命名
- [ ] 确认 Typlog 评论是否可导出（大概率不能，接受割舍或手工搬运精品）

## 阶段 1：基础设施

- [ ] R2 建桶 → 绑定 `media.xiaowenz.com`（**该子域目前尚无 DNS 记录**）→ 上传媒体：
      `media-sync/images/` → `images/` 前缀（`scripts/sync/upload_media.sh` 有命令模板）；
      音频原件 → `audio/{episode-slug}.mp3`（文件名必须与剧集 `audio_slug` 一致）
- [x] core 部署 ~~到 Zeabur~~ **到 gb-test**（2026-10-28，落点变更：DNS 已由 CF 代理指向 gb-test）：
      镜像 `/opt/apps/core/src`（GOPROXY=goproxy.cn 服务器侧补丁）→ 容器 `xiaowenz-core`
      （apps 网络 + `/opt/apps/core/data` 持久卷 + 127.0.0.1:18092）→ openresty `conf.d/core.conf`
      反代（CF Flexible 走 80）。**当前 `CORE_ENV=dev`（staging）**：admin token 在服务器
      `/opt/apps/core/env`（600，root 可读）；SMTP 凭据到位后改 `CORE_ENV=prod` 并补
      `CORE_SMTP_*` / `CORE_TURNSTILE_SECRET` / `CORE_R2_*` 重启容器
- [ ] core 冒烟：`/admin` 导入订阅者 CSV → 发一封测试 newsletter 给自己 → 上传一个测试音频并确认 `/a/test.mp3` 302
      （已远端验证：healthz / admin 303 / API 参数校验 / CORS 仅放行 xiaowenz.com；其余待 SMTP+R2）

## 阶段 2：静态站上线

- [x] Pages 新建项目连本仓库——已建并**生产发布**：生产分支 main，`blog.xiaowenz.com` 已服务 v3
      （sitemap 218 条、双 feed、`/search/`、`/blog/{slug}.html` 抽查均 200）
- [ ] 自查清单：sitemap 217 条 URL 与线上一致；`/feed.xml`、`/feed/audio.xml` 可解析且 enclosure 指向 core；
      随机 10 篇文章与线上逐屏对比；`/search/` 可用；订阅表单能收到验证邮件；评论提交后 admin 可见
      （机器侧抽查已过；逐屏人工对比、订阅/评论闭环待 SMTP+R2 后在 blog.xiaowenz.com 上做）
- [ ] DNS：`xiaowenz.com` 切到 Pages（CNAME  flattening 或 A 记录按 Pages 提示）——**最后一步，勿急**

## 阶段 3：观察期（2–4 周，Typlog 不急着退）

- [ ] Apple Podcasts / Spotify / 小宇宙后台确认 feed 抓取正常（新 URL 同内容，GUID 不变则听众无感）
- [ ] GA / core 统计面板流量正常；抽查播客下载计数在跳动
- [ ] Google Search Console 看抓取异常；确认 sitemap 已重新提交
- [ ] 一切正常 → 退订 Typlog，导出最终名单增量再导入一次 core

## 回滚

任何阶段出问题：DNS 切回 Typlog（A/CNAME 指回原值），Typlog 站保持原样期间零数据丢失。core 的 SQLite 每日快照在 R2 `backups/` 前缀，重建服务时恢复最近一份即可。
