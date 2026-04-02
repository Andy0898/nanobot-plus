@echo off
REM ========================================
REM 钉钉域名白名单直连脚本
REM 功能：只让钉钉相关域名不走代理
REM ========================================

echo 🚀 配置钉钉域名白名单...
echo.

REM 钉钉相关域名
set DINGTALK_DOMAINS=wss-open-connection-union.dingtalk.com;api.dingtalk.com;oapi.dingtalk.com;dingtalk.com

REM 检查是否已有 NO_PROXY
if defined NO_PROXY (
    echo ℹ️  检测到现有 NO_PROXY 配置
    echo   原配置：%NO_PROXY%
    set "NO_PROXY=%DINGTALK_DOMAINS%,%NO_PROXY%"
) else (
    echo ℹ️  未检测到 NO_PROXY 配置
    set "NO_PROXY=%DINGTALK_DOMAINS%"
)

echo.
echo ✅ 新的 NO_PROXY 配置:
echo   %NO_PROXY%
echo.

REM 显示代理配置
echo 📊 当前网络配置:
echo   HTTP_PROXY:  %HTTP_PROXY%
echo   HTTPS_PROXY: %HTTPS_PROXY%
echo   NO_PROXY:    %NO_PROXY%
echo.

echo 💡 说明:
echo   - 钉钉相关域名将直连（不走代理）
echo   - 其他域名继续使用代理
echo   - 仅在当前会话有效
echo.

REM 启动 nanobot
echo ▶️  启动 nanobot gateway...
call .env312\Scripts\python.exe -m nanobot gateway --verbose

echo.
echo 🛑 Gateway 已停止
pause
