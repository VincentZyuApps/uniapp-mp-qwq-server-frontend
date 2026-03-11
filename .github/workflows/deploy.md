# 部署流程说明 (Deploy Workflow)

本项目使用 GitHub Actions 自动部署 UniApp H5 构建产物到 **GitHub Pages** 和 **Cloudflare Pages**。

> ⚠️ 本项目使用 HBuilderX 本地构建，CI 仅负责部署，不执行构建。

---

## 📋 触发机制

为了节省资源，自动化部署需要在 **Commit Message** 中包含特定关键词。

| 关键词 | 说明 | 触发动作 |
| :--- | :--- | :--- |
| `pub page` | 发布页面 | ✅ 触发 GitHub Pages 部署<br>✅ 触发 Cloudflare Pages 部署 |

此外，也支持在 GitHub Actions 页面手动触发 (`workflow_dispatch`)。

**示例 Commit：**
```bash
git commit -m "update: 更新首页样式 (pub page)"
```

如果提交信息中**不包含** `pub page`，GitHub Action 将**不会运行**。

---

## 🔨 构建 & 提交流程

由于本项目使用 **HBuilderX** 构建，部署前需要手动操作：

1. 在 HBuilderX 中打开项目
2. 菜单：**发行 → 网站-PC Web或手机H5**
3. 构建产物输出到 `unpackage/dist/build/web/`
4. 提交构建产物并推送：

```bash
git add unpackage/dist/build/web/
git commit -m "build: 构建 H5 (pub page)"
git push github main
```

> `.gitignore` 已配置允许追踪 `unpackage/dist/build/web/` 目录。

---

## 🛠️ 部署逻辑

两个 Job **并行执行**，互不依赖：

### 1. GitHub Pages
- **部署内容**：`unpackage/dist/build/web/`
- **部署方式**：`actions/deploy-pages@v4`
- **访问地址**：`https://vincentzyuapps.github.io/uniapp-mp-qwq-server-frontend/`

### 2. Cloudflare Pages
- **部署内容**：`unpackage/dist/build/web/`
- **部署方式**：`cloudflare/pages-action@v1`
- **项目名称**：`uniapp-mp-qwq-server-frontend`（需与 Cloudflare Dashboard 一致）
- **访问地址**：`https://uniapp-mp-qwq-server-frontend.pages.dev/`（或绑定的自定义域名）

> `manifest.json` 中 `h5.router.base` 已设为 `"./"`（相对路径），两个平台均可正常访问。

---

## 🚀 前置准备：创建 Cloudflare Pages 项目

使用 API Token 推送模式，需要先在 Cloudflare 手动创建项目：

1. 进入 [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Workers & Pages**
2. 点击 **Create application**
3. 选择 **Pages** 标签页
4. 点击 **Upload assets**（不要连接 GitHub）
5. 项目名称输入：`uniapp-mp-qwq-server-frontend`（必须与 `deploy.yml` 中的 `projectName` 一致）
6. 点击 **Create project**，上传一个随便的 `index.html` 占位即可
7. 后续 GitHub Action 会自动覆盖内容

---

## 🔑 需要配置的 Secrets

在 GitHub 仓库 **Settings → Secrets and variables → Actions** 中添加：

| Secret Name | 说明 | 获取方式 |
| :--- | :--- | :--- |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API 令牌 | [管理 API Tokens](https://dash.cloudflare.com/profile/api-tokens)<br>→ Create Token → 模板选 **Edit Cloudflare Workers**<br>→ 权限需包含 `Cloudflare Pages:Edit` |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare 账户 ID | [Cloudflare Dashboard](https://dash.cloudflare.com/)<br>→ 点击任意站点 → Overview 右侧栏底部复制 **Account ID** |

> GitHub Pages 使用内置的 `GITHUB_TOKEN`，无需额外配置。

---

## ⚙️ 配置修改

如需修改 Cloudflare Pages 项目名称，编辑 `.github/workflows/deploy.yml`：

```yaml
projectName: uniapp-mp-qwq-server-frontend  # 👈 改为你的 Cloudflare 项目名
```
