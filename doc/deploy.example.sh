#!/bin/bash
# UniApp H5 一键部署 — 环境变量配置（示例模板）
#
# 📌 使用方法：
#   1. 复制本文件到 tmp/ 目录并重命名：
#      cp doc/deploy.example.sh tmp/deploy.sh
#   2. 编辑 tmp/deploy.sh，填入你的真实服务器信息
#   3. 运行：bash tmp/deploy.sh
#
# ⚠️ tmp/ 目录已在 .gitignore 中，你的真实配置不会被提交！

echo "============================================"
echo "  UniApp H5 一键部署 — 环境变量配置"
echo "============================================"
echo ""

# ====== 👇 在这里填写你的服务器信息 ======

# 服务器地址（IP 或域名）
export DEPLOY_SSH_HOST="your-server.example.com"

# SSH 端口（默认 22）
export DEPLOY_SSH_PORT="22"

# SSH 用户名（建议使用专用部署用户，而非 root）
export DEPLOY_SSH_USER="deployer"

# SSH 私钥路径（留空则使用密码登录或默认密钥）
export DEPLOY_SSH_KEY=""
# 如果使用密钥登录，取消注释并填写路径，例如:
# export DEPLOY_SSH_KEY="$HOME/.ssh/id_ed25519"

# 服务器上的部署目标目录
export DEPLOY_REMOTE_DIR="/var/www/my_frontend"

# 本地 7z 可执行文件路径（如已加入 PATH 则无需修改）
export DEPLOY_7Z_PATH="7z"

# ====== 执行部署脚本 ======
echo "🔑 环境变量已设置:"
echo "   HOST = $DEPLOY_SSH_HOST"
echo "   PORT = $DEPLOY_SSH_PORT"
echo "   USER = $DEPLOY_SSH_USER"
echo "   KEY  = ${DEPLOY_SSH_KEY:-(未设置，使用密码/默认密钥)}"
echo "   DIR  = $DEPLOY_REMOTE_DIR"
echo ""

cd "$(dirname "$0")/.."
python3 update.py
