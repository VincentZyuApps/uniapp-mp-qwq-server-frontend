#!/bin/bash
# ============================================================
# UniApp H5 一键部署 — Linux / WSL / Git Bash
#
# 必需环境变量（执行前设置）：
#   DEPLOY_SSH_HOST       — 服务器地址（IP 或域名）
#   DEPLOY_SSH_PORT       — SSH 端口（默认 22）
#   DEPLOY_SSH_USER       — SSH 用户名（默认 root）
#   DEPLOY_SSH_KEY        — SSH 私钥文件路径（可选，不设则使用密码或默认密钥）
#   DEPLOY_REMOTE_DIR     — 服务器最终网页目录
#   DEPLOY_REMOTE_OWNER   — 远端文件所有者（可选，如 root:root）
#   DEPLOY_VERIFY_URL     — 部署后验证 URL（可选）
#
# 用法：
#   export DEPLOY_SSH_HOST="your-server.com"
#   export DEPLOY_REMOTE_DIR="/opt/1panel/www/sites/example.com/index"
#   bash scripts/prod/deploy.sh
#
# 敏感信息请勿提交到 Git！
# 建议将真实值保存在 tmp/ 目录（已被 .gitignore 排除）。
# ============================================================

echo "============================================"
echo "  UniApp H5 一键部署 — Bash"
echo "============================================"
echo ""

# ====== 校验必需环境变量 ======
MISSING=0

if [ -z "$DEPLOY_SSH_HOST" ]; then
    echo "[ERROR] 缺少环境变量: DEPLOY_SSH_HOST"
    MISSING=1
fi

if [ -z "$DEPLOY_REMOTE_DIR" ]; then
    echo "[ERROR] 缺少环境变量: DEPLOY_REMOTE_DIR"
    MISSING=1
fi

if [ "$MISSING" -ne 0 ]; then
    echo ""
    echo "请在执行前设置环境变量："
    echo "  export DEPLOY_SSH_HOST=\"your-server.com\""
    echo "  export DEPLOY_REMOTE_DIR=\"/opt/1panel/www/sites/example.com/index\""
    echo ""
    exit 1
fi

# ====== 设置可选变量的默认值 ======
[ -z "$DEPLOY_SSH_PORT" ] && DEPLOY_SSH_PORT="22"
[ -z "$DEPLOY_SSH_USER" ] && DEPLOY_SSH_USER="root"
# ====== 打印环境变量 ======
echo "🔑 环境变量已设置:"
echo "   HOST = $DEPLOY_SSH_HOST"
echo "   PORT = $DEPLOY_SSH_PORT"
echo "   USER = $DEPLOY_SSH_USER"
echo "   KEY  = $DEPLOY_SSH_KEY"
echo "   DIR  = $DEPLOY_REMOTE_DIR"
echo "   OWNER = $DEPLOY_REMOTE_OWNER"
echo "   URL   = $DEPLOY_VERIFY_URL"
echo ""

# ====== 执行部署脚本 ======
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python3 "$SCRIPT_DIR/deploy.py"
