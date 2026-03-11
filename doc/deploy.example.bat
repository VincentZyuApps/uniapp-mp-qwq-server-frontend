@echo off
chcp 65001 >nul
echo ============================================
echo   UniApp H5 一键部署 — 环境变量配置（示例模板）
echo ============================================
echo.
echo   使用方法：
echo     1. 复制本文件到 tmp\ 目录并重命名：
echo        copy doc\deploy.example.bat tmp\deploy.bat
echo     2. 编辑 tmp\deploy.bat，填入你的真实服务器信息
echo     3. 运行：.\tmp\deploy.bat
echo.
echo   tmp\ 目录已在 .gitignore 中，你的真实配置不会被提交！
echo.

REM ====== 👇 在这里填写你的服务器信息 ======

REM 服务器地址（IP 或域名）
set DEPLOY_SSH_HOST=your-server.example.com

REM SSH 端口（默认 22）
set DEPLOY_SSH_PORT=22

REM SSH 用户名（建议使用专用部署用户，而非 root）
set DEPLOY_SSH_USER=deployer

REM SSH 私钥路径（留空则使用密码登录或默认密钥）
set DEPLOY_SSH_KEY=
REM 如果使用密钥登录，取消注释并填写路径，例如:
REM set DEPLOY_SSH_KEY=C:\Users\YourName\.ssh\id_ed25519

REM 服务器上的部署目标目录
set DEPLOY_REMOTE_DIR=/var/www/my_frontend

REM 本地 7z 可执行文件路径（如已加入 PATH 则无需修改）
set DEPLOY_7Z_PATH=7z

REM ====== 执行部署脚本 ======
echo 🔑 环境变量已设置:
echo    HOST = %DEPLOY_SSH_HOST%
echo    PORT = %DEPLOY_SSH_PORT%
echo    USER = %DEPLOY_SSH_USER%
echo    KEY  = %DEPLOY_SSH_KEY%
echo    DIR  = %DEPLOY_REMOTE_DIR%
echo.

cd /d "%~dp0.."
python update.py

echo.
pause
