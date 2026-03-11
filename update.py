#!/usr/bin/env python3
"""
deploy_to_server.py — 一键部署 UniApp H5 到云服务器
流程：本地 7z 打包 → rsync 上传 → SSH 远程解压覆盖

所有敏感信息通过环境变量传入，脚本本身不含任何密钥/IP。

环境变量说明：
  DEPLOY_SSH_HOST       — 服务器地址（IP 或域名）
  DEPLOY_SSH_PORT       — SSH 端口（默认 22）
  DEPLOY_SSH_USER       — SSH 用户名（默认 root）
  DEPLOY_SSH_KEY        — SSH 私钥文件路径（可选，不设则使用密码或默认密钥）
  DEPLOY_REMOTE_DIR     — 服务器目标目录（如 /data/mp_qwq_frontend）
  DEPLOY_7Z_PATH        — 本地 7z 可执行文件路径（默认 7z，即 PATH 中查找）
"""

import os
import sys
import subprocess
import time
from pathlib import Path


# ==================== 配置 ====================

def env(key: str, default: str = "") -> str:
    """读取环境变量，未设置时返回默认值"""
    return os.environ.get(key, default)


def require_env(key: str) -> str:
    """读取必需的环境变量，未设置时退出"""
    val = os.environ.get(key)
    if not val:
        print(f"❌ 缺少环境变量: {key}")
        sys.exit(1)
    return val


# ==================== 工具函数 ====================

def run(cmd: str | list, cwd: str = None, check: bool = True, shell: bool = False):
    """执行命令并实时输出"""
    print(f"\n🔧 执行: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    print("-" * 60)
    result = subprocess.run(
        cmd, cwd=cwd, check=check, shell=shell,
        text=True, encoding="utf-8", errors="replace"
    )
    return result


def build_ssh_cmd(host: str, port: str, user: str, key: str = "") -> list:
    """构建 SSH 基础命令参数"""
    ssh = ["ssh", "-o", "StrictHostKeyChecking=no"]
    if port and port != "22":
        ssh += ["-p", port]
    if key:
        ssh += ["-i", key]
    ssh.append(f"{user}@{host}")
    return ssh


def build_scp_cmd(host: str, port: str, user: str, key: str = "") -> list:
    """构建 scp 基础命令参数"""
    scp = ["scp", "-o", "StrictHostKeyChecking=no"]
    if port and port != "22":
        scp += ["-P", port]  # 注意：scp 用大写 -P
    if key:
        scp += ["-i", key]
    return scp


# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("🚀 UniApp H5 一键部署脚本")
    print("=" * 60)

    # 1. 读取环境变量
    host = require_env("DEPLOY_SSH_HOST")
    port = env("DEPLOY_SSH_PORT", "22")
    user = env("DEPLOY_SSH_USER", "root")
    key = env("DEPLOY_SSH_KEY")
    remote_dir = require_env("DEPLOY_REMOTE_DIR")
    z7_path = env("DEPLOY_7Z_PATH", "7z")

    # 2. 确定本地路径
    # 脚本所在目录即项目根目录
    project_root = Path(__file__).resolve().parent
    build_dir = project_root / "unpackage" / "dist" / "build"
    web_dir = build_dir / "web"
    zip_file = build_dir / "web.zip"

    if not web_dir.exists():
        print(f"❌ 构建产物不存在: {web_dir}")
        print("   请先在 HBuilderX 中执行: 发行 → 网站-PC Web或手机H5")
        sys.exit(1)

    print(f"\n📋 部署配置:")
    print(f"   服务器: {user}@{host}:{port}")
    print(f"   远程目录: {remote_dir}")
    print(f"   本地构建: {web_dir}")
    print(f"   SSH 密钥: {key or '(使用默认/密码)'}")

    # 3. 本地打包
    print("\n📦 [1/3] 本地打包...")
    if zip_file.exists():
        zip_file.unlink()
        print(f"   已删除旧的 {zip_file.name}")

    run([z7_path, "a", "-tzip", "-y", str(zip_file), str(web_dir) + "/*"], cwd=str(build_dir))
    size_mb = zip_file.stat().st_size / 1024 / 1024
    print(f"   ✅ 打包完成: {zip_file.name} ({size_mb:.2f} MB)")

    # 4. scp 上传
    print("\n📤 [2/3] 上传到服务器...")
    scp_cmd = build_scp_cmd(host, port, user, key)
    scp_cmd += [str(zip_file), f"{user}@{host}:{remote_dir}/"]
    run(scp_cmd)
    print("   ✅ 上传完成")

    # 5. SSH 远程解压 & 覆盖（零停机策略）
    print("\n🔄 [3/3] 远程解压 & 覆盖...")
    timestamp = time.strftime("%Y%m%d%H%M%S")
    remote_script = f"""
set -e
cd {remote_dir}
echo ">>> 解压到临时目录..."
rm -rf web_new
mkdir -p web_new
unzip -o web.zip -d web_new
echo ">>> 备份旧版本..."
[ -d web ] && mv web web_bak_{timestamp}
echo ">>> 切换到新版本..."
mv web_new web
echo ">>> 设置权限..."
chown -R www-data:www-data {remote_dir}/web
echo ">>> 清理旧备份..."
rm -rf web_bak_*
echo ">>> ✅ 部署完成！"
"""

    ssh_cmd = build_ssh_cmd(host, port, user, key)
    ssh_cmd.append(remote_script)
    run(ssh_cmd)

    print("\n" + "=" * 60)
    print("🎉 部署成功！")
    print("=" * 60)


if __name__ == "__main__":
    main()
