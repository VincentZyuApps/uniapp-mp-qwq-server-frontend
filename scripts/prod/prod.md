# 🚀 部署指南：自有服务器部署（脱敏版）

> **项目**：uniapp-qwq-server（qwq 拨无因果的神秘小服服 · 前端）
>
> **目标**：将 UniApp H5 前端部署到 `https://<YOUR_DOMAIN>/qwq-server`
>
> **本指南涵盖**：环境准备 → 本地构建打包 → 上传 → 服务器零停机切换 → Nginx 配置 → 验证 → 回滚 → 故障排查
>
> 💡 **敏感信息已脱敏**，占位符（`<YOUR_DOMAIN>` 等）请替换为实际值。
> 真实生产环境的值保存在 `tmp/prod.md`（已被 `.gitignore` 排除，不会提交）。

---

## 📑 目录

- [架构概览](#架构概览)
- [前置要求](#前置要求)
- [快速部署（推荐）](#快速部署推荐)
- [Nginx 配置参考](#nginx-配置参考)
- [SSL 证书管理](#ssl-证书管理)
- [验证与健康检查](#验证与健康检查)
- [回滚方案](#回滚方案)
- [故障排查](#故障排查)

---

## 架构概览

```
用户浏览器 → https://<YOUR_DOMAIN>/qwq-server
                        │ HTTPS :443
                        ▼
                1Panel OpenResty
    ┌──────────────────────────────────────────┐
    │  /qwq-server/   → alias /www/sites/.../  │
    │  /qs/           → proxy_pass 127.0.0.1   │
    │  /mpbackend/    → proxy_pass 127.0.0.1   │
    │  /              → proxy_pass 127.0.0.1   │
    └──────────────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ 静态文件  │ │ 后端 API │ │ Bot 框架 │
    └──────────┘ └──────────┘ └──────────┘
```

**多端部署一览：**

| 平台 | 地址 | 部署方式 |
|:---|:---|:---|
| 🖥️ 自有服务器 | `https://<YOUR_DOMAIN>/qwq-server` | 手动 / 一键脚本 |
| 🐙 GitHub Pages | `https://<YOUR_ORG>.github.io/<REPO>/` | CI 自动 |
| ☁️ Cloudflare Pages | `https://<PROJECT>.pages.dev/` | CI 自动 |

---

## 前置要求

### 本地环境

| 工具 | 用途 |
|:---|:---|
| **HBuilderX** | 构建 UniApp H5 |
| **Python 3** (≥ 3.10) | 运行 `deploy.py` 并生成部署压缩包 |
| **SSH 客户端** | 连接远程服务器 |

### 服务器环境

| 项目 | 要求 |
|:---|:---|
| **操作系统** | Ubuntu / Debian |
| **Nginx** | ≥ 1.18 |
| **unzip** | 解压 zip 包 |
| **Let's Encrypt** | SSL 证书（certbot） |
| **目标目录** | 1Panel 宿主机上的最终网页目录 |
| **Web 用户** | 与 OpenResty 站点权限匹配的用户，默认可使用 `root:root` |

---

## 快速部署（推荐）

### 方式一：PowerShell

```powershell
# 设置环境变量（请替换实际值）
$env:DEPLOY_SSH_HOST   = "<YOUR_SERVER>"
$env:DEPLOY_SSH_PORT   = "22"
$env:DEPLOY_SSH_USER   = "root"
$env:DEPLOY_SSH_KEY    = ""
$env:DEPLOY_REMOTE_DIR = "/opt/1panel/www/sites/<YOUR_DOMAIN>/index"
$env:DEPLOY_REMOTE_OWNER = "root:root"
$env:DEPLOY_VERIFY_URL = "https://<YOUR_DOMAIN>/qwq-server/"

# 执行部署
python scripts\prod\deploy.py
```

### 方式二：CMD

```cmd
set DEPLOY_SSH_HOST=<YOUR_SERVER>
set DEPLOY_SSH_PORT=22
set DEPLOY_SSH_USER=root
set DEPLOY_REMOTE_DIR=/opt/1panel/www/sites/<YOUR_DOMAIN>/index
set DEPLOY_REMOTE_OWNER=root:root
set DEPLOY_VERIFY_URL=https://<YOUR_DOMAIN>/qwq-server/
python scripts\prod\deploy.py
```

### 方式三：Linux / WSL / Git Bash

```bash
export DEPLOY_SSH_HOST="<YOUR_SERVER>"
export DEPLOY_SSH_PORT="22"
export DEPLOY_SSH_USER="root"
export DEPLOY_REMOTE_DIR="/opt/1panel/www/sites/<YOUR_DOMAIN>/index"
export DEPLOY_REMOTE_OWNER="root:root"
export DEPLOY_VERIFY_URL="https://<YOUR_DOMAIN>/qwq-server/"
python3 scripts/prod/deploy.py
```

### 方式四：使用包装脚本

```bash
# 先设置部署环境变量
bash scripts/prod/deploy.sh

# 或运行 scripts/prod/deploy.bat（Windows CMD）
# 或运行 scripts/prod/deploy.ps1（Windows PowerShell）
```

**脚本执行流程：**

```
[1/3] 📦 本地打包   — 7z 压缩 web/ → web.zip
[2/3] 📤 上传       — scp 传输 web.zip 到服务器
[3/3] 🔄 远程部署   — 解压 → 备份旧版 → 原子切换 → 设置权限 → 清理
```

> ⚠️ `scripts/prod/` 目录下的脚本均为脱敏模板，请通过环境变量传入真实值。
> 建议将真实敏感值保存在 `tmp/` 目录（已被 `.gitignore` 排除）。

---

## SSH 免密登录配置（可选，推荐）

配置后 `scp` / `ssh` 不再需要输入密码，部署脚本可全自动运行。

### Windows PowerShell

> ⚠️ PowerShell 管道会将公钥内容和 SSH 密码提示混淆，**不要使用 `type \| ssh` 管道**。下面是最稳的方式：

```powershell
# 1. 生成密钥（已有可跳过）
ssh-keygen -t ed25519 -C "YourName-Win"

# 2. 先读公钥到变量，再通过 echo 上传到服务器（需输入一次密码）
$key = Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"
ssh root@<YOUR_SERVER> "mkdir -p ~/.ssh && echo '$key' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# 3. 验证免密登录（不会再要密码即成功）
ssh root@<YOUR_SERVER> "echo '✅ SSH 免密登录配置成功！'"
```

### Windows CMD

```cmd
REM 1. 生成密钥（已有可跳过）
ssh-keygen -t ed25519 -C "YourName-Win"

REM 2. 上传公钥到服务器（需输入一次密码）
type "%USERPROFILE%\.ssh\id_ed25519.pub" | ssh -p 22 root@<YOUR_SERVER> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

REM 3. 验证免密登录
ssh root@<YOUR_SERVER> "echo '✅ SSH 免密登录配置成功！'"
```

### Linux / WSL

```bash
# 1. 生成密钥（已有可跳过）
ssh-keygen -t ed25519 -C "YourName-Linux"

# 2. 一键上传公钥（需输入一次密码）
ssh-copy-id -p 22 root@<YOUR_SERVER>

# 3. 验证免密登录
ssh root@<YOUR_SERVER> "echo '✅ SSH 免密登录配置成功！'"
```

### 部署时指定私钥

配置免密后，部署时设置 `DEPLOY_SSH_KEY` 环境变量即可：

```powershell
$env:DEPLOY_SSH_KEY = "$env:USERPROFILE\.ssh\id_ed25519"
```

```cmd
set DEPLOY_SSH_KEY=C:\Users\YourName\.ssh\id_ed25519
```

```bash
export DEPLOY_SSH_KEY="$HOME/.ssh/id_ed25519"
```

> 🔐 建议使用 `ed25519` 算法（比 RSA 更安全且密钥更短）。私钥文件权限应为 `600`。

---

## 1Panel OpenResty 配置参考

1Panel 生成站点后，应保留它管理的 `server`、SSL、日志和 ACME 配置，只在现有 `server` 中增加业务 `location` 喵。

```nginx
location ^~ /qs/ {
    proxy_pass http://127.0.0.1:8326/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location ^~ /mpbackend/ {
    proxy_pass http://127.0.0.1:8416/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location = /qwq-server {
    return 301 /qwq-server/;
}

location /qwq-server/ {
    alias /www/sites/<YOUR_DOMAIN>/index/;
    index index.html;
    try_files $uri $uri/ /qwq-server/index.html;
}
```

配置中的 `/www/sites/...` 是 OpenResty 容器路径，部署脚本使用的 `/opt/1panel/www/sites/...` 是宿主机路径喵。

```bash
docker exec <OPENRESTY_CONTAINER> openresty -t
docker exec <OPENRESTY_CONTAINER> openresty -s reload
```

不要使用系统 `nginx -t` 验证 1Panel OpenResty 配置喵。

---

## SSL 证书管理

站点证书默认交给 1Panel 管理喵。不要同时让 1Panel 和 Certbot续期同一张证书喵。

前端部署脚本只更新静态文件，不修改证书或 OpenResty 配置喵。

---

## 验证与健康检查

| 检查项 | 命令 |
|:---|:---|
| OpenResty 配置 | `docker exec <OPENRESTY_CONTAINER> openresty -t` |
| 前端文件 | `ls -la <DEPLOY_REMOTE_DIR>/index.html` |
| 后端监听 | `ss -lntp \| grep -E ':(8326\|8416)\\b'` |
| 公开页面 | `curl -fsSI https://<YOUR_DOMAIN>/qwq-server/` |

---

## 回滚方案

脚本会在目标目录的父目录中留下 `.<目录名>.bak.<时间戳>` 备份喵。

```bash
cd <DEPLOY_REMOTE_DIR的父目录>
mv <目标目录名> ".failed.$(date +%Y%m%d%H%M%S)"
mv .<目标目录名>.bak.<TIMESTAMP> <目标目录名>
```

静态文件回滚不需要重载 OpenResty 喵。

---

## 故障排查

### 页面白屏、404 或 403

```bash
ls -la <DEPLOY_REMOTE_DIR>/index.html
docker exec <OPENRESTY_CONTAINER> openresty -t
```

### API 返回 502

```bash
ss -lntp | grep -E ':(8326|8416)\b'
curl -fsS http://127.0.0.1:8326/openapi.json
curl -fsS http://127.0.0.1:8416/openapi.json
```

### 日志位置

| 日志 | 路径 |
|:---|:---|
| 站点日志 | `/opt/1panel/www/sites/<YOUR_DOMAIN>/log/` |
| OpenResty 日志 | `/opt/1panel/apps/openresty/openresty/log/` |
