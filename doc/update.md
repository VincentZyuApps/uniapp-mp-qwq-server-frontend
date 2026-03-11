# 更新部署说明

本项目支持三种部署方式，可以按需选择。

---

## 方式一：自有服务器部署（`update.py`）

一键完成：本地 7z 打包 → rsync 上传 → SSH 远程解压覆盖。

### 前置要求

| 工具 | 说明 |
| :--- | :--- |
| Python 3 | 运行部署脚本 |
| 7-Zip (`7z`) | 本地打包，需在 PATH 中 |
| rsync | 上传文件（Windows 可通过 Git Bash / WSL 使用） |
| SSH | 远程执行命令 |

### 使用方法

1. 在 HBuilderX 中构建 H5：**发行 → 网站-PC Web或手机H5**
2. 编辑 `tmp/deploy.bat`（或 `tmp/deploy.sh`），填入你的服务器信息
3. 运行：

**Windows (cmd/PowerShell):**
```powershell
.\tmp\deploy.bat
```

**Linux / WSL / Git Bash:**
```bash
bash tmp/deploy.sh
```

### 环境变量

| 变量 | 必填 | 说明 | 示例 |
| :--- | :--- | :--- | :--- |
| `DEPLOY_SSH_HOST` | ✅ | 服务器地址 | `sh-aliyun2.vincentzyu233.cn` |
| `DEPLOY_SSH_PORT` | | SSH 端口（默认 22） | `22` |
| `DEPLOY_SSH_USER` | | SSH 用户（默认 root） | `root` |
| `DEPLOY_SSH_KEY` | | SSH 私钥路径（可选） | `~/.ssh/id_rsa` |
| `DEPLOY_REMOTE_DIR` | ✅ | 服务器目标目录 | `/data/mp_qwq_frontend` |
| `DEPLOY_7Z_PATH` | | 7z 可执行路径（默认 `7z`） | `7z` |

> ⚠️ `tmp/` 目录已在 `.gitignore` 中，你的配置信息不会被提交。

---

## 方式二：GitHub Pages + Cloudflare Pages（CI 自动部署）

通过 GitHub Actions 自动部署到两个平台。

### 触发方式

在 commit message 中包含 `pub page` 关键词：

```bash
git add unpackage/dist/build/web/
git commit -m "build: 更新 H5 构建产物 (pub page)"
git push github main
```

### 访问地址

| 平台 | 地址 |
| :--- | :--- |
| GitHub Pages | https://vincentzyuapps.github.io/uniapp-mp-qwq-server-frontend/ |
| Cloudflare Pages | https://uniapp-mp-qwq-server-frontend.pages.dev/ |

详见 [deploy.md](.github/workflows/deploy.md)。

---

## 完整更新流程（三端同时发布）

```bash
# 1. HBuilderX 构建 H5

# 2. 部署到自有服务器
.\tmp\deploy.bat

# 3. 提交并触发 CI 部署到 GitHub Pages + Cloudflare Pages
git add unpackage/dist/build/web/
git commit -m "build: 更新 H5 (pub page)"
git push github main
```
