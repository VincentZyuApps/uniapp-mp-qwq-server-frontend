<#
.SYNOPSIS
    UniApp H5 一键部署 — PowerShell
.DESCRIPTION
    调用 deploy.py 完成打包 → 上传 → 远程部署全流程。
    必需环境变量通过外部传入，脚本本身不含任何敏感信息。

    环境变量说明（必填）：
      DEPLOY_SSH_HOST       — 服务器地址（IP 或域名）
      DEPLOY_SSH_PORT       — SSH 端口（默认 22）
      DEPLOY_SSH_USER       — SSH 用户名（默认 root）
      DEPLOY_SSH_KEY        — SSH 私钥文件路径（可选，不设则使用密码或默认密钥）
      DEPLOY_REMOTE_DIR     — 服务器目标目录（如 /data/mp_qwq_frontend）
      DEPLOY_7Z_PATH        — 本地 7z 可执行文件路径（默认 7z，即 PATH 中查找）

    用法：执行前先设好环境变量，例如：
      $env:DEPLOY_SSH_HOST   = "your-server.com"
      $env:DEPLOY_REMOTE_DIR = "/data/mp_qwq_frontend"
      .\deploy.ps1

.NOTES
    敏感信息请勿提交到 Git！
    建议将真实值保存在 tmp/ 目录（已被 .gitignore 排除）。
#>

# ====== 校验必需环境变量 ======
$missingVars = @()

if (-not $env:DEPLOY_SSH_HOST)   { $missingVars += "DEPLOY_SSH_HOST" }
if (-not $env:DEPLOY_REMOTE_DIR) { $missingVars += "DEPLOY_REMOTE_DIR" }

if ($missingVars.Count -gt 0) {
    Write-Host "`n[ERROR] 缺少必需的环境变量:" -ForegroundColor Red
    foreach ($var in $missingVars) {
        Write-Host "    $var" -ForegroundColor Yellow
    }
    Write-Host "`n请在执行前设置环境变量，例如:" -ForegroundColor Cyan
    Write-Host '    $env:DEPLOY_SSH_HOST   = "your-server.com"'
    Write-Host '    $env:DEPLOY_REMOTE_DIR = "/data/mp_qwq_frontend"'
    Write-Host ""
    Read-Host "按 Enter 退出"
    exit 1
}

# ====== 设置可选变量的默认值 ======
if (-not $env:DEPLOY_SSH_PORT) { $env:DEPLOY_SSH_PORT = "22" }
if (-not $env:DEPLOY_SSH_USER) { $env:DEPLOY_SSH_USER = "root" }
if (-not $env:DEPLOY_7Z_PATH)  { $env:DEPLOY_7Z_PATH  = "7z" }

# ====== 打印环境变量 ======
Write-Host "🔑 环境变量已设置:"
Write-Host "   HOST = $env:DEPLOY_SSH_HOST"
Write-Host "   PORT = $env:DEPLOY_SSH_PORT"
Write-Host "   USER = $env:DEPLOY_SSH_USER"
Write-Host "   KEY  = $env:DEPLOY_SSH_KEY"
Write-Host "   DIR  = $env:DEPLOY_REMOTE_DIR"
Write-Host ""

# ====== 执行部署脚本 ======
$projectRoot = Split-Path -Parent $PSScriptRoot
python "$projectRoot\prod\deploy.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ 部署失败！" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit $LASTEXITCODE
}

Write-Host "`n🎉 部署完成！" -ForegroundColor Green
Read-Host "按 Enter 退出"
