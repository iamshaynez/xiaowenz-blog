# MIGRATION.md — Typlog → 自研切换手册

切换原则：**先全部就绪，再切 DNS；播客 feed 连续性是最高优先级；旧站保留观察期。**

## 阶段 0：资产抢救（动手最早，互不依赖）

- [ ] Typlog 后台导出订阅者名单 CSV
- [ ] 下载 6 集播客音频原件（r.typlog.com 是签名 URL，会过期；清单在 `data/audio-manifest.csv`）
- [ ] 确认 Typlog 评论是否可导出（大概率不能，接受割舍或手工搬运精品）

## 阶段 1：基础设施

- [ ] R2 建桶 → 绑定 `media.xiaowenz.com` → 上传媒体：
      `media-sync/images/` → `images/` 前缀（`scripts/sync/upload_media.sh` 有命令模板）；
      音频原件 → `audio/{episode-slug}.mp3`（文件名必须与剧集 `audio_slug` 一致）
- [ ] core 部署到 Zeabur：连 core 仓库 → Dockerfile 自动识别 → **挂持久卷到 /data** →
      配环境变量（见 core 仓 README 配置表，`CORE_ENV=prod`）→ 绑定 `core.xiaowenz.com`
- [ ] core 冒烟：`/admin` 导入订阅者 CSV → 发一封测试 newsletter 给自己 → 上传一个测试音频并确认 `/a/test.mp3` 302

## 阶段 2：静态站上线

- [ ] Pages 新建项目连本仓库（构建命令与变量见 README），先在 `*.pages.dev` 预览域名全量自查
- [ ] 自查清单：sitemap 217 条 URL 与线上一致；`/feed.xml`、`/feed/audio.xml` 可解析且 enclosure 指向 core；
      随机 10 篇文章与线上逐屏对比；`/search/` 可用；订阅表单能收到验证邮件；评论提交后 admin 可见
- [ ] DNS：`xiaowenz.com` 切到 Pages（CNAME  flattening 或 A 记录按 Pages 提示）

## 阶段 3：观察期（2–4 周，Typlog 不急着退）

- [ ] Apple Podcasts / Spotify / 小宇宙后台确认 feed 抓取正常（新 URL 同内容，GUID 不变则听众无感）
- [ ] GA / core 统计面板流量正常；抽查播客下载计数在跳动
- [ ] Google Search Console 看抓取异常；确认 sitemap 已重新提交
- [ ] 一切正常 → 退订 Typlog，导出最终名单增量再导入一次 core

## 回滚

任何阶段出问题：DNS 切回 Typlog（A/CNAME 指回原值），Typlog 站保持原样期间零数据丢失。core 的 SQLite 每日快照在 R2 `backups/` 前缀，重建服务时恢复最近一份即可。
