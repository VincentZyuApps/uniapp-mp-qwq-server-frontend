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
                   Nginx 反向代理
    ┌──────────────────────────────────────────┐
    │  /qwq-server/   → alias /data/.../web/   │
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
| **Python 3** (≥ 3.8) | 运行 `deploy.py` |
| **7-Zip** (≥ 21.0) | 本地打包 |
| **SSH 客户端** | 连接远程服务器 |

### 服务器环境

| 项目 | 要求 |
|:---|:---|
| **操作系统** | Ubuntu / Debian |
| **Nginx** | ≥ 1.18 |
| **unzip** | 解压 zip 包 |
| **Let's Encrypt** | SSL 证书（certbot） |
| **目标目录** | `/data/mp_qwq_frontend/` |
| **Web 用户** | `www-data` |

---

## 快速部署（推荐）

### 方式一：PowerShell

```powershell
# 设置环境变量（请替换实际值）
$env:DEPLOY_SSH_HOST   = "<YOUR_SERVER>"
$env:DEPLOY_SSH_PORT   = "22"
$env:DEPLOY_SSH_USER   = "root"
$env:DEPLOY_SSH_KEY    = ""
$env:DEPLOY_REMOTE_DIR = "/data/mp_qwq_frontend"
$env:DEPLOY_7Z_PATH    = "7z"

# 执行部署
python prod\deploy.py
```

### 方式二：CMD

```cmd
set DEPLOY_SSH_HOST=<YOUR_SERVER>
set DEPLOY_SSH_PORT=22
set DEPLOY_SSH_USER=root
set DEPLOY_REMOTE_DIR=/data/mp_qwq_frontend
set DEPLOY_7Z_PATH=7z
python prod\deploy.py
```

### 方式三：Linux / WSL / Git Bash

```bash
export DEPLOY_SSH_HOST="<YOUR_SERVER>"
export DEPLOY_SSH_PORT="22"
export DEPLOY_SSH_USER="root"
export DEPLOY_REMOTE_DIR="/data/mp_qwq_frontend"
export DEPLOY_7Z_PATH="7z"
python3 prod/deploy.py
```

### 方式四：使用包装脚本

```bash
# 先编辑 prod/deploy.sh 填入服务器信息
bash prod/deploy.sh

# 或编辑 prod/deploy.bat 后双击运行（Windows CMD）
# 或编辑 prod/deploy.ps1 后右键"Run with PowerShell"
```

**脚本执行流程：**

```
[1/3] 📦 本地打包   — 7z 压缩 web/ → web.zip
[2/3] 📤 上传       — scp 传输 web.zip 到服务器
[3/3] 🔄 远程部署   — 解压 → 备份旧版 → 原子切换 → 设置权限 → 清理
```

> ⚠️ `prod/` 目录下的脚本均为脱敏模板，修改后请勿提交含真实值的版本。
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

## Nginx 配置参考

### 主站配置

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name <YOUR_DOMAIN>;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name <YOUR_DOMAIN>;

    ssl_certificate     /etc/letsencrypt/live/<YOUR_DOMAIN>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<YOUR_DOMAIN>/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Koishi 主服务
    location / {
        proxy_pass http://127.0.0.1:51214;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # FastAPI 后端
    location /qs/ {
        proxy_pass http://127.0.0.1:8326/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 其他后端服务
    location /mpbackend/ {
        proxy_pass http://127.0.0.1:8416/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # H5 前端静态文件
    location = /qwq-server {
        return 301 /qwq-server/;
    }
    location /qwq-server/ {
        alias /data/mp_qwq_frontend/web/;
        index index.html;
        try_files $uri $uri/ /qwq-server/index.html;
    }
}
```

### 应用配置

```bash
nginx -t && systemctl reload nginx
```

---

## SSL 证书管理

```bash
# 申请证书
certbot --nginx -d <YOUR_DOMAIN>

# 查看证书状态
certbot certificates

# 手动续签
certbot renew

# 验证自动续期
certbot renew --dry-run

# 查看自动续签定时器
systemctl list-timers | grep certbot
```

---

## 验证与健康检查

### 检查清单

| 检查项 | 命令 |
|:---|:---|
| Nginx 运行状态 | `systemctl status nginx` |
| 前端文件就位 | `ls -la /data/mp_qwq_frontend/web/index.html` |
| 后端端口监听 | `ss -tlnp \| grep -E '8326\|8416\|51214'` |
| 本地 curl 测试 | `curl -sI https://<YOUR_DOMAIN>/qwq-server/ \| head -5` |

### 访问地址

| 平台 | 地址 |
|:---|:---|
| 🖥️ 自有服务器 | `https://<YOUR_DOMAIN>/qwq-server` |

---

## 回滚方案

```bash
ssh <USER>@<YOUR_SERVER>

cd /data/mp_qwq_frontend

# 查看可用备份
ls -ld web_bak_*

# 回滚到指定备份
mv web web_broken
mv web_bak_<TIMESTAMP> web
chown -R www-data:www-data web

# 确认成功后清理
rm -rf web_broken
```

---

## 故障排查

### 页面白屏 / 404

```bash
# 检查文件是否存在
ls -la /data/mp_qwq_frontend/web/index.html

# 检查 Nginx 错误日志
tail -50 /var/log/nginx/error.log

# 检查配置语法
nginx -t
```

### API 请求失败（502 / 连接超时）

```bash
# 检查后端服务端口
ss -tlnp | grep -E '8326|8416'

# 查看后端日志
journalctl -u <BACKEND_SERVICE> -n 50
```

### 权限错误（403 Forbidden）

```bash
ls -la /data/mp_qwq_frontend/web/
chown -R www-data:www-data /data/mp_qwq_frontend/web
chmod -R 755 /data/mp_qwq_frontend/web
```

### 日志位置

| 日志 | 路径 |
|:---|:---|
| Nginx 访问日志 | `/var/log/nginx/access.log` |
| Nginx 错误日志 | `/var/log/nginx/error.log` |
