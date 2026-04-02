# 🐈 nanobot 调试与运行指南

## 📋 目录

1. [快速开始](#快速开始)
2. [虚拟环境管理](#虚拟环境管理)
3. [VS Code 调试配置](#vs-code-调试配置)
4. [命令行运行方式](#命令行运行方式)
5. [Docker 部署](#docker-部署)
6. [常见问题排查](#常见问题排查)

---

## 🔧 虚拟环境管理

### 为什么使用虚拟环境？

虚拟环境可以：
- ✅ 隔离项目依赖，避免与其他 Python 项目冲突
- ✅ 自由使用 Python 3.12+ 版本（即使系统 Python 是其他版本）
- ✅ 方便地管理和导出依赖包
- ✅ 快速清理和重建开发环境

### 📦 使用 uv 创建虚拟环境（推荐）

```bash
# 创建虚拟环境（自动选择 Python 3.12）
uv venv --python 3.12

# 或使用项目名称作为环境名
uv venv .env312
```

**uv 的优势**：
- 🚀 比 pip 快 10-100 倍
- 🎯 自动管理 Python 版本
- 💾 更好的缓存机制
- 🔒 完全可重现的依赖锁定

### 🔌 激活虚拟环境

#### Windows PowerShell

```powershell
# 激活虚拟环境
\.env312\Scripts\Activate.ps1

# 如果提示权限问题，执行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# 然后再试一次
```

#### Windows CMD

```cmd
.env312\Scripts\activate.bat
```

#### macOS / Linux

```bash
source .env312/bin/activate
```

### ✅ 验证虚拟环境已激活

激活后，命令行前缀应该显示 `(.env312)` 或类似标识：

```bash
# 检查 Python 版本
python --version
# 应该显示：Python 3.12.x

# 检查 Python 路径
where python  # Windows
which python  # macOS/Linux
# 应该指向虚拟环境目录

# 查看已安装的包
pip list
# 或
uv pip list
```

### 📥 安装依赖到虚拟环境

```bash
# 使用 uv（推荐，超快）
uv pip install -e . --python .\.env312\Scripts\python.exe

# 如果虚拟环境已激活，可以直接使用
uv pip install -e .

# 或使用标准 pip
pip install -e .
```

### 🔄 退出虚拟环境

```bash
deactivate
```

### 🗑️ 删除虚拟环境

```bash
# 直接删除目录即可
rm -rf .env312  # macOS/Linux
rmdir /s .env312  # Windows CMD
Remove-Item -Recurse -Force .env312  # PowerShell
```

### 🛠️ 虚拟环境常见问题

**Q1: 找不到 Activate.ps1？**
```bash
# 检查目录是否存在
ls .env312\Scripts\  # Windows
ls .env312/bin/  # macOS/Linux

# 如果不存在，重新创建
uv venv .env312
```

**Q2: PowerShell 提示权限错误？**
```powershell
# 临时允许执行脚本
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 或永久允许（推荐）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Q3: 如何为虚拟环境安装特定版本的 Python？**
```bash
# 创建时指定
uv venv --python 3.11 .env311

# 或让 uv 自动下载
uv venv --python 3.12
# uv 会自动下载并安装 Python 3.12
```

**Q4: 如何在 VS Code 中选择虚拟环境？**
1. 按 `Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (macOS)
2. 输入 "Python: Select Interpreter"
3. 选择包含 `.env312` 的路径
4. 重启终端

---

## 🚀 快速开始

### 1️⃣ 安装依赖

**前提条件**：确保已激活虚拟环境（可选但推荐）

```bash
# 检查虚拟环境是否激活
python --version  # 应该 >= 3.11

# 推荐使用 uv（超快）
uv pip install -e .

# 或使用 pip
pip install -e .

# 开发模式（包含测试工具）
pip install -e ".[dev]"
```

**使用 uv 指定 Python 版本**：
```bash
# 如果未激活虚拟环境，可以指定 Python 路径
uv pip install -e . --python .\.env312\Scripts\python.exe
```

### 2️⃣ 初始化配置

```bash
# 首次运行需要初始化
nanobot onboard
```

这会创建：
- `~/.nanobot/config.json` - 配置文件
- `~/.nanobot/workspace/` - 工作空间

### 3️⃣ 配置 API Key

编辑 `~/.nanobot/config.json`，添加你的 LLM API key：

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  }
}
```

获取 API Key:
- [OpenRouter](https://openrouter.ai/keys) (推荐，支持多种模型)
- [Anthropic](https://console.anthropic.com) (Claude 直接)
- [OpenAI](https://platform.openai.com) (GPT 直接)

---

## 🖥️ VS Code 调试配置

### 📝 前置配置

#### 1. 选择正确的 Python 解释器

**重要**: 必须选择你的虚拟环境解释器！

**步骤**：
1. 按 `Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (macOS)
2. 输入 `Python: Select Interpreter`
3. 选择包含 `.env312` 或你虚拟环境名称的路径
4. 示例：`.env312\\Scripts\\python.exe`

**验证**：
- 打开新终端，应该看到 `(.env312)` 前缀
- 运行 `python --version` 应显示 3.12.x

#### 2. 推荐的 VS Code 扩展

- ✅ **Python** (Microsoft)
- ✅ **Pylance** (Microsoft)
- ✅ **Ruff** (代码检查和格式化)
- ✅ **isort** (导入排序)

### ⚙️ launch.json 配置说明

已为你配置好以下调试场景（位于 `.vscode/launch.json`）：

**使用方法**：
1. 按 `F5` 或点击运行和调试图标
2. 从下拉菜单选择调试场景
3. 点击绿色启动按钮

### 🐈 Gateway (网关模式)
**用途**: 启动完整网关，连接配置的聊天渠道（Telegram/WhatsApp 等）

**调试场景**: 
- 测试渠道消息接收和发送
- 调试 Channel Manager
- 测试 Heartbeat/Cron 服务

**启动文件**: `nanobot/cli/commands.py::gateway()`

**断点建议位置**:
- `nanobot/agent/loop.py` - Agent 核心循环
- `nanobot/channels/manager.py` - 渠道管理
- `nanobot/bus/queue.py` - 消息总线

### 🤖 Agent CLI (命令行交互)
**用途**: 启动交互式 CLI 对话

**调试场景**:
- 测试 Agent 对话逻辑
- 调试工具调用
- 测试记忆系统

**启动文件**: `nanobot/cli/commands.py::agent()`

**断点建议位置**:
- `nanobot/agent/context.py` - 上下文构建
- `nanobot/agent/memory.py` - 记忆管理
- `nanobot/agent/tools/*.py` - 工具实现

### 💬 Agent Single Message (单次消息)
**用途**: 发送单条消息并获取回复（快速测试）

**调试场景**:
- 快速测试特定 prompt
- 调试单次对话流程
- 性能分析

**示例参数**: `["agent", "-m", "Hello!"]`

### ⚙️ Status (状态检查)
**用途**: 查看配置状态和 API key 配置

**调试场景**:
- 检查配置加载
- 验证 Provider 匹配逻辑

### 🔧 Onboard (初始化配置)
**用途**: 初始化配置和工作空间

**调试场景**:
- 调试配置生成逻辑
- 测试模板同步

### 🧪 Run Tests (运行测试)
**用途**: 运行 pytest 测试套件

**调试场景**:
- 调试失败的测试
- 编写新测试用例

**参数**: `tests -v` (详细输出)

### 🐛 Debug Current File (调试当前文件)
**用途**: 调试当前打开的 Python 文件

**调试场景**:
- 针对特定模块调试
- 单元测试编写

---

## 🎯 VS Code 高级调试技巧

### 🔍 断点类型

#### 1. 普通断点
- **操作**: 点击行号左侧
- **用途**: 在特定行暂停

#### 2. 条件断点
- **操作**: 右键断点 → 编辑断点 → 输入条件
- **示例**: `msg.content.startswith("/stop")`
- **用途**: 只在满足条件时暂停

#### 3. 日志点（不暂停）
- **操作**: 右键断点 → 编辑断点 → 勾选 "记录消息"
- **示例**: `Tool call: {tool_call.name}`
- **用途**: 记录信息但不中断执行

#### 4. 异常断点
- **操作**: 运行和调试视图 → 异常断点
- **用途**: 在任何异常抛出时暂停

### 🎮 调试控制

| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `F5` | 继续 | 继续执行直到下一个断点 |
| `F9` | 切换断点 | 在当前行添加/移除断点 |
| `F10` | 单步跳过 | 执行当前行，不进入函数 |
| `F11` | 单步进入 | 进入函数内部 |
| `Shift+F11` | 单步跳出 | 跳出当前函数 |
| `Ctrl+Shift+F5` | 重新启动 | 重新开始调试 |

### 🔬 监视和变量

#### 1. 变量窗口
- **作用域**: 查看局部变量、全局变量、闭包
- **操作**: 展开对象查看属性
- **修改**: 双击值可以修改

#### 2. 监视表达式
- **操作**: 右键变量 → 添加到监视
- **示例**: `msg.session_key`, `len(session.messages)`
- **用途**: 持续跟踪表达式值变化

#### 3. 调用堆栈
- **位置**: 调试侧边栏
- **用途**: 查看函数调用链
- **操作**: 点击帧跳转到对应代码

### 📊 调试控制台技巧

#### 1. 即时求值
在调试控制台中输入任何表达式：
```python
msg.content.upper()
session.get_history()
tool.tools.get_definitions()
```

#### 2. 执行代码
可以在调试时执行 Python 代码：
```python
# 打印变量
print(f"Messages: {len(messages)}")

# 修改状态
session.last_consolidated = 0

# 调用函数
result = await agent.process_direct("test")
```

#### 3. 查看对象详情
```python
# 查看对象所有属性
dir(msg)
vars(tool)

# 查看类型
type(response)

# 查看文档
help(tool.execute)
```

### 🐛 实战调试场景

#### 场景 1: 消息处理失败

**问题**: 用户发送消息后没有响应

**调试步骤**:
1. 在 `nanobot/agent/loop.py::_process_message()` 设置断点
2. 启动 "🤖 Agent CLI" 调试
3. 发送测试消息
4. 检查：
   - `msg.content` 是否正确
   - `session.messages` 的历史记录
   - LLM 响应内容
   - 工具调用参数

#### 场景 2: 工具调用异常

**问题**: 工具执行报错

**调试步骤**:
1. 在 `nanobot/agent/tools/registry.py::execute()` 设置断点
2. 添加条件断点：`tool_name == 'exec'`
3. 检查：
   - 工具参数字典
   - 工作目录设置
   - 权限和路径限制

#### 场景 3: 记忆整合失败

**问题**: 记忆没有正确保存

**调试步骤**:
1. 在 `nanobot/agent/memory.py::consolidate()` 设置断点
2. 启动调试，触发记忆整合
3. 检查：
   - `session.messages` 数量
   - LLM 返回的工具调用
   - `MEMORY.md` 和 `HISTORY.md` 内容

### 📈 性能调试

#### 1. 使用内置的性能分析

在代码中添加：
```python
import time
start = time.time()
# ... 代码 ...
end = time.time()
print(f"Elapsed: {end - start:.3f}s")
```

#### 2. 使用 cProfile

创建调试配置：
```json
{
    "name": "📊 Profile Agent",
    "type": "debugpy",
    "request": "launch",
    "module": "cProfile",
    "console": "integratedTerminal",
    "args": ["-o", "profile.stats", "-m", "nanobot", "agent", "-m", "test"],
    "cwd": "${workspaceFolder}"
}
```

分析结果：
```bash
python -m pstats profile.stats
(P) sort cumtime
(P) stats 20
```

### 🎨 自定义调试配置

#### 示例：调试特定渠道

```json
{
    "name": "📱 Debug Telegram",
    "type": "debugpy",
    "request": "launch",
    "module": "nanobot",
    "console": "integratedTerminal",
    "args": ["gateway", "--config", "~/.nanobot-telegram/config.json"],
    "cwd": "${workspaceFolder}",
    "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "LOG_LEVEL": "DEBUG"
    },
    "justMyCode": false
}
```

#### 示例：带日志的调试

```json
{
    "name": "📝 Debug with Logs",
    "type": "debugpy",
    "request": "launch",
    "module": "nanobot",
    "console": "integratedTerminal",
    "args": ["agent", "--logs"],
    "cwd": "${workspaceFolder}",
    "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "LOGURU_LEVEL": "DEBUG"
    }
}
```

---

## 💻 命令行运行方式

### 基础命令

```bash
# 初始化
nanobot onboard

# 查看状态
nanobot status

# 单次对话
nanobot agent -m "Hello!"

# 交互式对话
nanobot agent

# 启动网关
nanobot gateway

# 带日志运行
nanobot agent --logs

# 纯文本输出（无 Markdown）
nanobot agent --no-markdown
```

### 高级选项

```bash
# 指定配置文件
nanobot gateway --config ~/.nanobot-telegram/config.json

# 指定工作空间
nanobot agent --workspace /path/to/workspace

# 自定义端口
nanobot gateway --port 18791

# 显示运行时日志
nanobot agent --logs
```

### 多实例运行

```bash
# 终端 1: Telegram 机器人
nanobot gateway --config ~/.nanobot-telegram/config.json

# 终端 2: Discord 机器人
nanobot gateway --config ~/.nanobot-discord/config.json

# 终端 3: CLI 测试
nanobot agent -c ~/.nanobot-telegram/config.json -m "Test"
```

---

## 🐳 Docker 部署

### Docker Compose (推荐)

```bash
# 首次初始化
docker compose run --rm nanobot-cli onboard

# 编辑配置
vim ~/.nanobot/config.json

# 启动网关
docker compose up -d nanobot-gateway

# 运行 CLI
docker compose run --rm nanobot-cli agent -m "Hello!"

# 查看日志
docker compose logs -f nanobot-gateway

# 停止服务
docker compose down
```

### 纯 Docker

```bash
# 构建镜像
docker build -t nanobot .

# 初始化配置
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot onboard

# 启动网关
docker run -v ~/.nanobot:/root/.nanobot -p 18790:18790 nanobot gateway

# 运行 CLI
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot agent -m "Hello!"
```

---

## 🐛 常见问题排查

### 💻 虚拟环境相关问题

#### 1. 虚拟环境未激活

**症状**: 
- `uv pip install` 报错 "No virtual environment found"
- 安装到了系统 Python 目录

**解决方案**:
```bash
# PowerShell: 激活虚拟环境
\.env312\Scripts\Activate.ps1

# 或使用 --system 参数（不推荐）
uv pip install -e . --system

# 或指定 Python 路径
uv pip install -e . --python .\.env312\Scripts\python.exe
```

#### 2. Python 版本不匹配

**症状**:
- 报错 "Python>=3.11 is required"
- 系统 Python 是 3.10 或更低版本

**解决方案**:
```bash
# 创建新的虚拟环境（自动下载 Python 3.12）
uv venv .env312 --python 3.12

# 激活并重新安装
\.env312\Scripts\Activate.ps1
uv pip install -e .
```

#### 3. 依赖冲突

**症状**:
- 安装时报 "No solution found when resolving dependencies"

**解决方案**:
```bash
# 清理缓存
uv cache clean

# 强制重新安装
uv pip install -e . --force-reinstall

# 或删除虚拟环境重建
rm -rf .env312
uv venv .env312
uv pip install -e .
```

### 🔧 VS Code 调试问题

```bash
# 检查 Python 版本
python --version  # 必须 >= 3.11

# 重新安装依赖
pip install --upgrade -e .

# 清理缓存重装
pip cache purge && pip install -e .
```

### 🔧 VS Code 调试问题

#### 1. 找不到 Python 解释器

**症状**:
- VS Code 提示 "Select Python Interpreter"
- 运行调试时找不到模块

**解决方案**:
1. 按 `Ctrl+Shift+P` → 输入 "Python: Select Interpreter"
2. 选择 `.env312\Scripts\python.exe`
3. 重启 VS Code
4. 验证：打开新终端应显示 `(.env312)`

#### 2. 调试无法启动

**症状**:
- 点击 F5 没反应
- 报错 "Debug adapter not found"

**解决方案**:
```bash
# 确保已安装 Python 扩展
# Ctrl+Shift+X → 搜索 "Python" → 安装

# 检查 launch.json 是否存在
# 如果不存在，运行下面的命令创建配置
```

**手动创建配置**：
1. 打开命令面板 `Ctrl+Shift+P`
2. 输入 "Debug: Open launch.json"
3. 选择 "Python"
4. 使用我为你提供的配置

#### 3. 断点不命中

**症状**:
- 程序运行但断点没有变红
- 断点变成空心圆（未验证）

**原因和解决**:
- **代码路径不对**: 确保运行的是当前工作区的代码
- **justMyCode=true**: 设置为 `false` 以调试第三方库
- **缓存问题**: 清理 `__pycache__` 文件夹

```bash
# 清理缓存
find . -name "__pycache__" -type d -exec rm -rf {} +
# 或 Windows
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
```

### 📦 依赖安装问题

#### 1. uv 安装慢或失败

**症状**:
- `uv pip install` 卡住不动
- 网络超时错误

**解决方案**:
```bash
# 使用国内镜像（推荐）
uv pip install -e . --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用 pip 备用
pip install -e .
```

#### 2. 编译错误

**症状**:
- 报错 "Microsoft Visual C++ 14.0 or greater is required"
- C 扩展编译失败

**解决方案**:
```bash
# Windows: 安装 Build Tools
# 访问：https://visualstudio.microsoft.com/visual-cpp-build-tools/
# 下载并安装 "Desktop development with C++"

# 或使用预编译 wheel
pip install --only-binary :all: -e .
```

### ⚙️ 配置问题

```bash
# 重置配置
rm -rf ~/.nanobot
nanobot onboard

# 检查配置文件
cat ~/.nanobot/config.json

# 验证 API key
nanobot status
```

### 3. WhatsApp 桥接问题

```bash
# 重建 WhatsApp bridge
rm -rf ~/.nanobot/bridge
nanobot channels login

# 检查 Node.js 版本
node --version  # 必须 >= 18

# 手动构建 bridge
cd ~/.nanobot/bridge
npm install
npm run build
```

### 4. 调试技巧

**设置断点**:
```python
# 在关键位置添加
import pdb; pdb.set_trace()  # 传统断点
breakpoint()  # Python 3.7+
```

**日志级别**:
```bash
# 启用详细日志
nanobot gateway --verbose

# 或在代码中设置
from loguru import logger
logger.enable("nanobot")
```

**查看会话历史**:
```bash
# 会话文件位置
ls ~/.nanobot/workspace/sessions/

# 查看记忆文件
cat ~/.nanobot/workspace/memory/MEMORY.md
cat ~/.nanobot/workspace/memory/HISTORY.md
```

### 5. 性能分析

```bash
# 使用 cProfile
python -m cProfile -s cumtime $(which nanobot) agent -m "test" | head -50

# 使用 py-spy (外部工具)
py-spy record -o profile.svg -- nanobot agent -m "test"
```

### ⚙️ 配置问题

#### 1. 配置文件丢失

**症状**:
- 报错 "Config file not found"
- `nanobot status` 失败

**解决方案**:
```bash
# 重新初始化
nanobot onboard

# 或手动创建目录
mkdir -p ~/.nanobot/workspace

# 编辑配置
notepad ~/.nanobot/config.json
```

#### 2. API Key 无效

**症状**:
- 调用 LLM 时返回 401 错误
- 提示 "Invalid API key"

**解决方案**:
1. 检查配置文件：
   ```bash
   cat ~/.nanobot/config.json
   ```
2. 验证 API key 格式正确
3. 测试 API key：
   ```bash
   nanobot agent -m "test"
   ```
4. 重新获取 API key 并更新

### 🌐 渠道连接问题

#### 1. Telegram Bot 无响应

**症状**:
- 发送消息机器人没反应
- 日志显示连接错误

**检查清单**:
- [ ] Bot Token 是否正确
- [ ] 是否启用了 Message Content Intent
- [ ] `allowFrom` 是否包含你的 User ID
- [ ] 防火墙是否阻止连接

**调试步骤**:
```bash
# 启用详细日志
nanobot gateway --verbose

# 查看日志
tail -f ~/.nanobot/logs/nanobot.log
```

#### 2. WhatsApp Bridge 失败

**症状**:
- QR 码不显示
- 连接立即断开

**解决方案**:
```bash
# 重建 bridge
rm -rf ~/.nanobot/bridge
nanobot channels login

# 检查 Node.js 版本
node --version  # 必须 >= 18

# 手动构建
cd ~/.nanobot/bridge
npm install
npm run build
npm start
```

### 🐍 Python 环境问题

#### 1. 多个 Python 版本冲突

**症状**:
- `python` 命令指向错误的版本
- 包安装在错误的位置

**解决方案**:
```bash
# Windows: 查看 Python 路径
where python
where python3

# macOS/Linux: 查看 Python 路径
which python
which python3

# 使用完整路径
/full/path/to/.env312/Scripts/python.exe -m pip install -e .
```

#### 2. 权限问题

**症状**:
- 报错 "Permission denied"
- 无法写入 site-packages

**解决方案**:
```bash
# 不要使用 sudo！这会破坏虚拟环境

# 正确做法：确保虚拟环境在你名下
chown -R $USER:$USER .env312  # macOS/Linux

# Windows: 右键文件夹 → 属性 → 安全 → 编辑权限
```

### 🧪 测试相关问题

#### 1. pytest 找不到测试

**症状**:
- `pytest tests` 不执行任何测试
- 报错 "no tests ran"

**解决方案**:
```bash
# 确保在正确的目录
cd /path/to/nanobot-plus

# 使用 -v 查看详细输出
pytest tests -v

# 运行特定测试
pytest tests/test_commands.py -v

# 清除 pytest 缓存
rm -rf .pytest_cache
rm -rf __pycache__
```

#### 2. 异步测试失败

**症状**:
- 报错 "async def functions are not natively supported"

**解决方案**:
确保安装了 `pytest-asyncio` 并在 `pyproject.toml` 中配置：

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

---

## 🔍 核心代码路径

### 调试入口点

| 功能 | 文件路径 | 函数 |
|------|---------|------|
| CLI 命令 | `nanobot/cli/commands.py` | `app()` |
| Gateway | `nanobot/cli/commands.py` | `gateway()` |
| Agent | `nanobot/cli/commands.py` | `agent()` |
| Agent Loop | `nanobot/agent/loop.py` | `run()` / `_process_message()` |
| Channel Manager | `nanobot/channels/manager.py` | `start_all()` |
| Message Bus | `nanobot/bus/queue.py` | `publish_*()` / `consume_*()` |

### 关键数据流

```
用户输入 → Channel.receive() → Bus.publish_inbound()
→ AgentLoop.run() → Bus.consume_inbound()
→ AgentLoop._process_message()
→ ContextBuilder.build_messages()
→ LLMProvider.chat()
→ ToolRegistry.execute()
→ Bus.publish_outbound()
→ Channel.send() → 用户输出
```

---

## 📚 进一步阅读

- [项目架构文档](./nanobot_arch.png)
- [安全最佳实践](./SECURITY.md)
- [通信频道设置](./COMMUNICATION.md)
- [技能开发指南](./nanobot/skills/README.md)

---

## 💡 提示与最佳实践

### 🎯 开发工作流建议

#### 1. 日常开发循环

```bash
# 1. 激活虚拟环境
\.env312\Scripts\Activate.ps1

# 2. 运行测试确保功能正常
pytest tests/test_commands.py -v

# 3. 使用单次消息快速测试新功能
nanobot agent -m "测试我的新功能"

# 4. 需要调试时启动 VS Code
# F5 → 选择对应的调试场景

# 5. 完整测试后提交代码
git add .
git commit -m "feat: 添加新功能"
```

#### 2. 调试优先级

**从简单到复杂**：
1. **print 调试**: 最简单直接
2. **日志调试**: `logger.debug()` 查看流程
3. **VS Code 断点**: 交互式调试
4. **性能分析**: cProfile 分析瓶颈

#### 3. 代码修改后的测试策略

```bash
# 小改动：单次消息测试
nanobot agent -m "quick test"

# 中等改动：交互模式测试
nanobot agent

# 大改动：完整测试套件
pytest tests/ -v --tb=short

# 核心逻辑改动：启动网关 + 真实渠道测试
nanobot gateway
```

### 📚 学习路径建议

#### 第 1 周：熟悉基础
- ✅ 安装和配置环境
- ✅ CLI 基本使用
- ✅ 阅读核心文件：`loop.py`, `context.py`

#### 第 2 周：深入理解
- 🔍 工具系统实现
- 🔍 消息总线架构
- 🔍 Provider 路由机制

#### 第 3 周：扩展开发
- 🛠️ 添加自定义工具
- 🛠️ 集成新渠道
- 🛠️ 编写技能模块

#### 第 4 周：贡献代码
- 📝 修复 issue
- 📝 优化性能
- 📝 提交 PR

### 🔐 安全提醒

#### 1. API Key 保护

```bash
# ✅ 好做法：配置文件权限
chmod 600 ~/.nanobot/config.json  # macOS/Linux
# Windows: 右键 → 属性 → 安全 → 只允许管理员读取

# ❌ 坏做法：不要提交到 git
echo "*.json" >> .gitignore
```

#### 2. Shell 工具安全

```python
# 在代码中使用 exec 工具时：
# ✅ 启用 restrict_to_workspace
config.tools.restrict_to_workspace = True

# ✅ 设置超时
config.tools.exec.timeout = 30

# ❌ 避免：以 root/admin 身份运行
```

#### 3. 渠道访问控制

```json
{
  "channels": {
    "telegram": {
      "allowFrom": ["your_user_id"]  // ✅ 白名单
    },
    "whatsapp": {
      "allowFrom": ["+8613800000000"]  // ✅ 指定号码
    }
  }
}
```

### 🎨 代码风格建议

#### 1. 遵循项目规范

```python
# ✅ 使用类型注解
def process_message(self, msg: InboundMessage) -> OutboundMessage | None:
    ...

# ✅ 使用 docstring
async def consolidate(self, session: Session) -> bool:
    """Consolidate memory via LLM tool call."""
    ...

# ✅ 使用 loguru 记录日志
from loguru import logger
logger.info("Processing message from {}:{}", msg.channel, msg.sender_id)
```

#### 2. 异步编程最佳实践

```python
# ✅ 使用 async/await
async def run(self) -> None:
    while self._running:
        msg = await self.bus.consume_inbound()
        await self._process_message(msg)

# ✅ 使用 asyncio.gather 并发
results = await asyncio.gather(
    task1(),
    task2(),
    task3(),
    return_exceptions=True
)

# ✅ 正确处理取消
try:
    await long_running_task()
except asyncio.CancelledError:
    logger.info("Task cancelled")
    raise
```

### 📊 性能优化技巧

#### 1. 减少 LLM 调用

```python
# ✅ 缓存常用结果
@lru_cache(maxsize=100)
def build_prompt(template: str, context: str) -> str:
    return f"{template}\n\n{context}"

# ✅ 批量处理消息
messages_to_process = session.messages[-10:]  # 一次处理多条
```

#### 2. 优化记忆系统

```python
# ✅ 定期整合记忆，避免上下文过长
if len(session.messages) > memory_window:
    await MemoryStore.consolidate(session)

# ✅ 截断大的工具结果
if len(tool_result) > MAX_CHARS:
    tool_result = tool_result[:MAX_CHARS] + "... (truncated)"
```

#### 3. 并发控制

```python
# ✅ 使用信号量限制并发数
semaphore = asyncio.Semaphore(5)

async def limited_task():
    async with semaphore:
        await do_something()

# ✅ 使用超时避免卡住
try:
    result = await asyncio.wait_for(task(), timeout=30)
except asyncio.TimeoutError:
    logger.warning("Task timed out")
```

---

## 📖 进一步阅读

### 📚 官方文档
- [项目架构文档](./nanobot_arch.png) - 可视化架构图
- [安全最佳实践](./SECURITY.md) - 生产部署必读
- [通信频道设置](./COMMUNICATION.md) - 加入社区
- [技能开发指南](./nanobot/skills/README.md) - 扩展技能

### 🔗 外部资源
- [LiteLLM 文档](https://docs.litellm.ai/) - LLM 提供商集成
- [Pydantic 文档](https://docs.pydantic.dev/) - 数据验证
- [FastAPI 教程](https://fastapi.tiangolo.com/tutorial/) - 异步编程参考

### 🎓 学习资源
- [Python 异步编程](https://docs.python.org/3/library/asyncio.html)
- [Design Patterns for AI Agents](https://github.com/HKUDS/nanobot/discussions)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)

---

## 🎯 快速参考卡片

### 常用命令速查

```bash
# 环境管理
\.env312\Scripts\Activate.ps1     # 激活虚拟环境
deactivate                         # 退出虚拟环境
uv pip list                        # 查看已安装包

# 基础命令
nanobot onboard                    # 初始化配置
nanobot status                     # 查看状态
nanobot agent -m "Hello!"          # 单次对话
nanobot agent                      # 交互对话
nanobot gateway                    # 启动网关

# 高级选项
nanobot agent --logs               # 显示日志
nanobot agent --no-markdown        # 纯文本输出
nanobot gateway --port 18791       # 自定义端口
nanobot gateway --verbose          # 详细日志

# 调试相关
pytest tests/ -v                   # 运行测试
pytest tests/test_xxx.py -v        # 运行特定测试
cd bridge && npm install           # 安装 WhatsApp bridge
```

### 关键文件位置

| 文件/目录 | 用途 | 示例路径 |
|----------|------|----------|
| 配置文件 | LLM API key、渠道配置 | `~/.nanobot/config.json` |
| 工作空间 | 会话、记忆、技能 | `~/.nanobot/workspace/` |
| 会话数据 | 对话历史 | `~/.nanobot/workspace/sessions/` |
| 记忆数据 | 长期记忆 | `~/.nanobot/workspace/memory/` |
| 定时任务 | Cron jobs | `~/.nanobot/cron/jobs.json` |
| 日志文件 | 运行日志 | `~/.nanobot/logs/` |
| WhatsApp Bridge | WhatsApp 桥接 | `~/.nanobot/bridge/` |

### 调试快捷键

| 按键 | 功能 |
|------|------|
| `F5` | 开始调试 |
| `F9` | 切换断点 |
| `F10` | 单步跳过 |
| `F11` | 单步进入 |
| `Shift+F11` | 单步跳出 |
| `Ctrl+Shift+F5` | 重新启动 |
| `Ctrl+K Ctrl+B` | 切换断点 |

---

## 💬 获取帮助

### 🐛 遇到问题？

1. **查看日志**: `tail -f ~/.nanobot/logs/nanobot.log`
2. **搜索 Issue**: https://github.com/HKUDS/nanobot/issues
3. **提问讨论**: https://github.com/HKUDS/nanobot/discussions
4. **加入社区**: [Feishu/WeChat/Discord](./COMMUNICATION.md)

### 📝 提问模板

```markdown
**问题描述**: 
简要说明遇到的问题

**复现步骤**:
1. nanobot onboard
2. nanobot agent -m "test"
3. 看到错误...

**错误信息**:
```
完整的错误堆栈
```

**环境信息**:
- Python: 3.12.6
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- nanobot: v0.1.4.post4

**已尝试的解决方案**:
- [x] 重启虚拟环境
- [x] 重新安装依赖
- [ ] ...
```

---

**Happy Debugging! 🐈**

有任何问题欢迎随时提出！
