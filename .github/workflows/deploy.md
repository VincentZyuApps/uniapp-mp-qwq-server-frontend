# 部署流程说明 (Deploy Workflow)

本项目使用 GitHub Actions 部署已经由本地 HBuilderX 生成的 UniApp H5 构建产物到 **GitHub Pages** 和 **Cloudflare Pages**。

> **核心原则**：先更新版本，再由开发者使用 HBuilderX GUI 手动构建；CI 只上传仓库中的 `unpackage/dist/build/web/`，不会安装依赖或重新构建。

---

## 📋 触发机制

自动部署需要同时满足：

1. 推送到 GitHub 的 `main` 分支。
2. 本次推送的 HEAD 提交信息包含精确小写关键词 `pub page`。

也可以从 GitHub Actions 页面通过 `workflow_dispatch` 手动触发，此时不检查提交信息。

```bash
git commit -m "feat: 发布 v0.3.x Web H5 (pub page)"
git push github main
```

如果一次推送包含多个提交，确保最后一个提交含有 `pub page`，否则 GitHub Pages 与 Cloudflare Pages 两个 Job 都会被跳过。

---

## 🧱 版本更新与 HBuilderX 构建

### 1. 更新版本（必须早于构建）

在项目根目录执行：

```bash
# 常规发布：versionCode 自动使用 Asia/Shanghai 当天日期
python scripts/bump.py -v 0.3.x-rc.y

# 可选：只预览，不写文件
python scripts/bump.py -v 0.3.x-rc.y --dry-run
```

脚本会同步更新 `package.json`、`manifest.json` 与 `App.vue`，并将 `manifest.json.versionCode` 更新为上海当天的 `YYYYMMDD`。补发历史版本时才需要显式传入 `-c YYYYMMDD`。

### 2. 使用 HBuilderX 手动构建

1. 在 HBuilderX 中打开项目。
2. 点击 **发行 → 网站-PC Web 或手机 H5**。
3. 等待 HBuilderX 提示编译和打包成功。
4. 确认构建产物位于 `unpackage/dist/build/web/`。

Codex、GitHub Actions、npm 和 Vite 都不能替代这一步；版本或源码变化后必须重新使用 HBuilderX 发行。

---

## 🧭 UniApp 路由基路径与 `_redirects`

本项目的 `manifest.json` 使用：

```json
"router": {
  "mode": "hash",
  "base": "./"
}
```

HBuilderX 因此会在 `index.html` 中生成 `./assets/...` 相对资源路径，同一份构建产物可以部署在 GitHub Pages 仓库根路径、Cloudflare Pages 根路径以及 `/qwq-server/` 子目录。

**本仓库不需要生成 `_redirects`**。不要复制 Koishi 仓库的 `/uniapp-koishi-market/* /:splat 200` 规则，因为它属于另一个项目的绝对子路径映射。如果以后将 `base` 改为绝对路径，必须同时重新评估 GitHub Pages、Cloudflare Pages 和自建站点的路径映射。

---

## 📟 完整 Git 发布流程

```bash
# 1. 先更新版本，再用 HBuilderX 手动发行 Web H5
python scripts/bump.py -v 0.3.x-rc.y
# HBuilderX GUI：发行 -> 网站-PC Web 或手机 H5

# 2. 暂存源码、文档、旧哈希删除及其他变更
git add -A
# web 目录已通过白名单允许跟踪；再次 -f 可确保新哈希产物完整加入
git add -f unpackage/dist/build/web/

# 3. 检查即将提交的内容
git status --short
git --no-pager diff --cached --stat
git diff --cached --check
git status --short -- unpackage/dist/build/web/
git ls-files -- unpackage/dist/build/web/

# 4. 提交；精确小写关键词 pub page 用于触发部署
git commit -m "feat: 发布 v0.3.x Web H5 (pub page)"
git log -1 --format=fuller

# 5. GitHub 触发 Pages 部署，origin 同步到 Gitee
git push github main
git push origin main
```

`git diff --cached` 只展示暂存区，也就是下一次提交真正包含的内容；不要使用 `git diff HEAD --stat --short`，`git diff` 没有 `--short` 参数。如果只需要一行统计，可以使用 `git --no-pager diff --cached --shortstat`。

---

## ✅ 构建产物检查清单

- `unpackage/dist/build/web/index.html` 与 `assets/` 目录存在。
- `index.html` 中的入口资源使用 `./assets/...` 相对路径。
- `index.html` 引用的 JS、CSS、图标文件都实际存在。
- 新哈希资源已加入、旧哈希资源已删除，且 `index.html` 已指向新入口文件。
- 构建产物内嵌 `appVersion` 与 `package.json`、`manifest.json`、`App.vue` 一致。
- 构建产物中的生产地址为 `bluerosion.vincentzyu233.cn`，没有重新出现 `sh-aliyun2.vincentzyu233.cn`。
- `git diff --cached --check` 没有输出，并且 `git status --short` 中没有意外文件。

---

## 🛠️ 部署逻辑

两个 GitHub Actions Job 并行执行，互不依赖：

### 1. GitHub Pages

- **部署内容**：`unpackage/dist/build/web/`
- **部署方式**：`actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4`
- **访问地址**：`https://vincentzyuapps.github.io/uniapp-mp-qwq-server-frontend/`

### 2. Cloudflare Pages

- **部署内容**：`unpackage/dist/build/web/`
- **部署方式**：`cloudflare/pages-action@v1`
- **项目名称**：`uniapp-mp-qwq-server-frontend`
- **访问地址**：`https://uniapp-mp-qwq-server-frontend.pages.dev/`（或绑定的自定义域名）

两个平台上传的是同一份已提交构建产物，不会在 CI 中重新构建。

### 3. 自建生产站点

Pages 发布不会自动部署到 `https://bluerosion.vincentzyu233.cn/qwq-server/`。自建站点使用 `scripts/prod/` 下的部署脚本，执行前必须单独阅读 [`scripts/prod/prod.md`](../../scripts/prod/prod.md)，确认服务器路径和环境变量，并获得明确部署授权。

---

## 🚀 Cloudflare Pages 前置配置

使用 API Token 推送模式，需要先在 Cloudflare 创建 **Direct Upload** 类型项目：

1. 进入 Cloudflare Dashboard 的 **Workers & Pages**。
2. 点击 **Create application → Pages → Upload assets**，不要连接 Git 仓库。
3. 创建项目 `uniapp-mp-qwq-server-frontend`，名称必须与 `.github/workflows/deploy.yml` 中的 `projectName` 一致。
4. 首次可上传一个简单的 `index.html` 完成初始化，后续 GitHub Action 会覆盖内容。

在 GitHub 仓库 **Settings → Secrets and variables → Actions** 的 Repository secrets 中添加：

| Secret Name | 说明 |
| :--- | :--- |
| `CLOUDFLARE_API_TOKEN` | 令牌至少需要 `Account → Cloudflare Pages → Edit` 权限 |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare Dashboard 中当前账户的 Account ID |

GitHub Pages 使用内置的 `GITHUB_TOKEN`，无需额外配置。

---

## 🔧 常见问题

### Actions 显示 skipped

确认推送目标是 GitHub `main`，并用 `git log -1 --format=fuller` 检查 HEAD 提交信息是否包含精确小写 `pub page`。

### 页面空白或入口资源 404

检查 `index.html` 是否使用 `./assets/...`，对应哈希文件是否已经提交，不要手工修改压缩后的构建文件。

### 页面仍显示旧版本

通常是忘记在版本更新后重新运行 HBuilderX，或没有完整暂存新旧哈希资源。检查源码版本、构建产物内嵌 `appVersion` 和 `git status --short -- unpackage/dist/build/web/`。

### Cloudflare 报 `Project not found`

确认 Cloudflare 中已创建同名 Direct Upload 项目，并检查 `CLOUDFLARE_ACCOUNT_ID`、API Token 权限及 `projectName`。
