@echo off
chcp 65001 >nul
echo ============================================
echo   UniApp H5 一键部署 — CMD
echo ============================================
echo.

REM ============================================================
REM  环境变量说明（必填）
REM
REM  DEPLOY_SSH_HOST       — 服务器地址（IP 或域名）
REM  DEPLOY_SSH_PORT       — SSH 端口（默认 22）
REM  DEPLOY_SSH_USER       — SSH 用户名（默认 root）
REM  DEPLOY_SSH_KEY        — SSH 私钥文件路径（可选，不设则使用密码或默认密钥）
REM  DEPLOY_REMOTE_DIR     — 服务器最终网页目录
REM  DEPLOY_REMOTE_OWNER   — 远端文件所有者（可选，如 root:root）
REM  DEPLOY_VERIFY_URL     — 部署后验证 URL（可选）
REM
REM  用法：在执行前先设好环境变量，例如：
REM     set DEPLOY_SSH_HOST=your-server.com
REM     set DEPLOY_REMOTE_DIR=/opt/1panel/www/sites/example.com/index
REM     scripts\prod\deploy.bat
REM
REM  敏感信息请勿提交到 Git！
REM  建议将真实值保存在 tmp/ 目录（已被 .gitignore 排除）。
REM ============================================================

REM ====== 校验必需环境变量 ======
set MISSING=

if "%DEPLOY_SSH_HOST%"=="" (
    echo [ERROR] 缺少环境变量: DEPLOY_SSH_HOST
    set MISSING=1
)

if "%DEPLOY_REMOTE_DIR%"=="" (
    echo [ERROR] 缺少环境变量: DEPLOY_REMOTE_DIR
    set MISSING=1
)

if defined MISSING (
    echo.
    echo 请在执行前设置环境变量：
    echo    set DEPLOY_SSH_HOST=your-server.com
    echo    set DEPLOY_REMOTE_DIR=/opt/1panel/www/sites/example.com/index
    echo.
    pause
    exit /b 1
)

REM ====== 设置可选变量的默认值 ======
if "%DEPLOY_SSH_PORT%"=="" set DEPLOY_SSH_PORT=22
if "%DEPLOY_SSH_USER%"=="" set DEPLOY_SSH_USER=root
REM ====== 打印环境变量 ======
echo 🔑 环境变量已设置:
echo    HOST = %DEPLOY_SSH_HOST%
echo    PORT = %DEPLOY_SSH_PORT%
echo    USER = %DEPLOY_SSH_USER%
echo    KEY  = %DEPLOY_SSH_KEY%
echo    DIR  = %DEPLOY_REMOTE_DIR%
echo    OWNER = %DEPLOY_REMOTE_OWNER%
echo    URL   = %DEPLOY_VERIFY_URL%
echo.

REM ====== 执行部署脚本 ======
python "%~dp0deploy.py"

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ 部署失败！
    pause
    exit /b %ERRORLEVEL%
)

echo.
pause
