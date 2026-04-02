@echo off
REM 禁用代理启动 nanobot gateway

echo 🚀 启动 nanobot gateway (不使用代理)...
echo.

REM 清除代理环境变量
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=

echo ✅ 已禁用代理
echo.

REM 启动 nanobot
call .env312\Scripts\python.exe -m nanobot gateway --verbose

echo.
echo 🛑 Gateway 已停止
pause
