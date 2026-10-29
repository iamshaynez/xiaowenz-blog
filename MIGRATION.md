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

- [x] Typlog 后台导出订阅者名单 CSV（2026-10-29 已导出并导入 core：327 行 → 剔除 1 个
      oastify.com 探针地址、合并 1 个大小写重复后导入 324、跳过已存在 1，全部 active，零发信）
- [x] 下载 6 集播客音频原件（2026-10-29 完成）：3 集为本地 `garden/av/` 成片，
      3 集（ep001/ep003/humanity）从线上 feed enclosure 补下，全部与 `audio-manifest.csv` 字节数精确校验
- [ ] 确认 Typlog 评论是否可导出（大概率不能，接受割舍或手工搬运精品）

## 阶段 1：基础设施

- [x] R2 建桶 `blog` + 绑定 `media.xiaowenz.com`（2026-10-29）：5 张图片（`images/`）+ 6 集音频
      （`audio/{slug}.mp3`）已上传并经 core `/admin/media` 注册（含 immutable 缓存头）；
      **遗留**：`audio/ep001.mp3` 与 `images/podcast-cover.jpg` 两条 URL 有上传前探测产生的
      404 负缓存，需在 CF 面板 Purge Cache
- [x] core 部署到 gb-test（2026-10-28 上线，2026-10-29 转 **prod**）：SMTP 走
      **Cloudflare Email Service**（`smtp.mx.cloudflare.net:465`，Workers Paid 含 3000 封/月）；
      `CORE_R2_*` 已配（备份每日快照已验证）；`CORE_TURNSTILE_SECRET` 仍空（上线前配）；
      **`CORE_SITE_URL` 当前为 `https://blog.xiaowenz.com`（staging 实际服务域）——
      apex DNS 切换 Pages 时必须改回 `https://xiaowenz.com` 并重启容器**
- [x] core 冒烟（2026-10-29）：healthz ✓ / admin 登录 ✓ / 订阅 API 真发验证邮件到站长邮箱 ✓ /
      音频上传注册 ✓ / `/a/ep001.mp3` 302 计数 ✓；剩余：CSV 导入订阅者 → 群发一封测试 newsletter

## 阶段 2：静态站上线

- [x] Pages 新建项目连本仓库——已建并**生产发布**：生产分支 main，`blog.xiaowenz.com` 已服务 v3
      （sitemap 218 条、双 feed、`/search/`、`/blog/{slug}.html` 抽查均 200）
- [ ] 自查清单：sitemap 217 条 URL 与线上一致；`/feed.xml`、`/feed/audio.xml` 可解析且 enclosure 指向 core；
      随机 10 篇文章与线上逐屏对比；`/search/` 可用；订阅表单能收到验证邮件；评论提交后 admin 可见
      （机器侧抽查已过；逐屏人工对比、订阅/评论闭环待 SMTP+R2 后在 blog.xiaowenz.com 上做）
- [x] DNS：`xiaowenz.com` 切到 Pages（2026-10-29 完成：Pages 自定义域挂载 apex，
      www 302 → apex；注意**必须把域挂到 Pages 项目**，只改 DNS 会 522）

## 阶段 3：观察期（2026-10-29 起算，2–4 周，Typlog 不急着退）

- [x] **2026-10-29 切换当日验收**：apex=v3（Hugo 0.164）；feed/audio.xml=Hugo 版且 GUID 延续
      （Apple/小宇宙订阅者无感）；enclosure 走 core 302；www→apex 302；CORE_SITE_URL 已回切
      apex（CORS/回跳/feed 联动归位，分发页显示 Apple「已同步」）

- [ ] Apple Podcasts / Spotify / 小宇宙后台确认 feed 抓取正常（新 URL 同内容，GUID 不变则听众无感）
- [ ] GA / core 统计面板流量正常；抽查播客下载计数在跳动
- [ ] Google Search Console 看抓取异常；确认 sitemap 已重新提交
- [ ] 一切正常 → 退订 Typlog，导出最终名单增量再导入一次 core

## 回滚

任何阶段出问题：DNS 切回 Typlog（A/CNAME 指回原值），Typlog 站保持原样期间零数据丢失。core 的 SQLite 每日快照在 R2 `backups/` 前缀，重建服务时恢复最近一份即可。
