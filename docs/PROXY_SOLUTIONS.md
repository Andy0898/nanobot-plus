# 钉钉代理配置解决方案对比

## 📋 问题背景

**现状**：
- ✅ 公司网络需要代理才能访问外网
- ✅ HTTP_PROXY: http://127.0.0.1:8118
- ❌ 钉钉 WebSocket 不支持通过代理连接
- ❌ 完全禁用代理 → 无法访问 GitHub、境外 LLM API

**需求**：
- ✅ 钉钉相关域名直连（不走代理）
- ✅ 其他域名继续使用代理（GitHub、OpenAI 等）

---

## ✅ 方案对比

| 维度 | **方案 1: 白名单脚本** | **方案 2: 代码优化** |
|------|---------------------|-------------------|
| **实现方式** | PowerShell/Batch 脚本 | 修改 Python 代码 |
| **配置位置** | 操作系统环境变量 | `nanobot/channels/dingtalk.py` |
| **作用范围** | 整个进程 + 所有子进程 | 仅钉钉 Channel |
| **生效时机** | 启动时设置 | HTTP Client 初始化时 |
| **恢复时机** | 终端关闭后自动恢复 | 一直有效（进程生命周期内） |
| **影响范围** | 所有网络请求 | 仅钉钉相关请求 |
| **维护成本** | 低（独立脚本） | 中（代码的一部分） |
| **推荐指数** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🔧 方案 1: 白名单脚本（推荐）

### **原理**

使用 `NO_PROXY` 环境变量，让特定域名不走代理。

### **使用方法**

```powershell
# Windows
.\start_with_dingtalk_whitelist.bat

# Linux/macOS (创建类似的 shell 脚本)
export NO_PROXY="wss-open-connection-union.dingtalk.com,api.dingtalk.com,$NO_PROXY"
python -m nanobot gateway
```

### **核心配置**

```batch
set DINGTALK_DOMAINS=wss-open-connection-union.dingtalk.com;api.dingtalk.com;oapi.dingtalk.com;dingtalk.com
set NO_PROXY=%DINGTALK_DOMAINS%,%NO_PROXY%
```

### **效果验证**

```python
import os
print("HTTP_PROXY:", os.environ.get('HTTP_PROXY'))
print("HTTPS_PROXY:", os.environ.get('HTTPS_PROXY'))
print("NO_PROXY:", os.environ.get('NO_PROXY'))

# 输出示例:
# HTTP_PROXY: http://127.0.0.1:8118
# HTTPS_PROXY: http://127.0.0.1:8118
# NO_PROXY: wss-open-connection-union.dingtalk.com,api.dingtalk.com,...
```

### **优点**

✅ **无需修改代码**：独立脚本，不影响源码  
✅ **灵活配置**：可以随时调整域名列表  
✅ **全局生效**：所有 Python 库都尊重 `NO_PROXY`  
✅ **安全隔离**：只在当前会话有效，关闭终端自动恢复  

### **缺点**

⚠️ **需要手动运行脚本**：不能直接 `nanobot gateway`  
⚠️ **依赖 httpx 支持**：某些旧库可能不识别 `NO_PROXY`  

---

## 🔧 方案 2: 代码优化

### **原理**

在代码中动态设置 `NO_PROXY`，仅针对钉钉 Channel 生效。

### **核心代码**

```python
# nanobot/channels/dingtalk.py
async def start(self) -> None:
    # Save current proxy settings
    import os
    original_http_proxy = os.environ.get('HTTP_PROXY')
    original_https_proxy = os.environ.get('HTTPS_PROXY')
    
    # Add DingTalk domains to NO_PROXY
    if original_http_proxy or original_https_proxy:
        existing_no_proxy = os.environ.get('NO_PROXY', '')
        dingtalk_domains = 'wss-open-connection-union.dingtalk.com,api.dingtalk.com,oapi.dingtalk.com,dingtalk.com'
        
        if existing_no_proxy:
            os.environ['NO_PROXY'] = f"{dingtalk_domains},{existing_no_proxy}"
        else:
            os.environ['NO_PROXY'] = dingtalk_domains
        
        logger.info("NO_PROXY set to: {}", os.environ['NO_PROXY'])
    
    # Initialize HTTP client - will respect NO_PROXY settings
    self._http = httpx.AsyncClient()
```

### **工作流程**

```mermaid
sequenceDiagram
    participant User as 用户
    participant Gateway as nanobot gateway
    participant DingTalk as DingTalkChannel
    participant Env as 环境变量
    participant HTTP as httpx.AsyncClient
    
    User->>Gateway: 启动命令
    
    Gateway->>DingTalk: 调用 start()
    
    DingTalk->>Env: 读取 HTTP_PROXY/HTTPS_PROXY
    
    alt 检测到代理
        DingTalk->>Env: 读取现有 NO_PROXY
        DingTalk->>Env: 追加钉钉域名到 NO_PROXY
        DingTalk->>DingTalk: 记录日志
    end
    
    DingTalk->>HTTP: 初始化 HTTP Client
    Note over HTTP: 自动遵循 NO_PROXY 配置
    
    DingTalk->>DingTalk: 建立 WebSocket 连接
    Note over DingTalk: 钉钉域名走直连<br/>其他域名走代理
    
    loop 运行中
        DingTalk->>DingTalk: 处理消息
        Note over DingTalk: NO_PROXY 一直有效
    end
```

### **关键时间点**

| 时间 | 事件 | 代理状态 |
|------|------|---------|
| **T0** | Gateway 启动 | 使用系统代理配置 |
| **T1** | DingTalkChannel.start() 被调用 | 设置 NO_PROXY（追加模式） |
| **T2** | httpx.AsyncClient 初始化 | 遵循 NO_PROXY 配置 |
| **T3** | WebSocket 连接建立 | 钉钉域名直连成功 |
| **T4** | Gateway 运行中 | NO_PROXY 保持有效 |
| **T5** | Gateway 停止 | 进程结束，环境变量释放 |

**关键点**：
- ✅ `NO_PROXY` 是**追加**而不是覆盖
- ✅ 设置后**一直有效**直到进程结束
- ✅ **不需要恢复**（因为只是追加，没有删除原有配置）

---

### **优点**

✅ **自动化**：无需额外脚本，直接启动即可  
✅ **精确控制**：只影响钉钉 Channel  
✅ **持久生效**：重连时也自动使用 NO_PROXY  

### **缺点**

⚠️ **修改源码**：需要维护代码变更  
⚠️ **全局影响**：虽然只追加，但会影响同进程的其他请求  
⚠️ **不可逆**：进程生命周期内无法撤销（除非重启）  

---

## 🎯 推荐选择

### **选择方案 1（白名单脚本）如果：**

- ✅ 你不想修改源码
- ✅ 你有多个项目需要类似配置
- ✅ 你喜欢配置与代码分离
- ✅ 你需要灵活的开关控制

### **选择方案 2（代码优化）如果：**

- ✅ 你希望开箱即用
- ✅ 你是项目维护者，可以提交 PR
- ✅ 你希望所有用户都受益
- ✅ 你不介意修改源码

---

## 📊 实际测试对比

### **测试场景**

```bash
# 环境
HTTP_PROXY=http://127.0.0.1:8118
HTTPS_PROXY=http://127.0.0.1:8118

# 测试 1: 访问钉钉
curl https://api.dingtalk.com/v1.0/oauth2/accessToken
# 期望：直连成功

# 测试 2: 访问 GitHub
curl https://api.github.com/repos/HKUDS/nanobot-plus
# 期望：通过代理成功

# 测试 3: 访问 OpenAI
curl https://api.openai.com/v1/models
# 期望：通过代理成功
```

### **预期结果**

| 方案 | 钉钉 | GitHub | OpenAI |
|------|------|--------|--------|
| **方案 1** | ✅ 直连 | ✅ 代理 | ✅ 代理 |
| **方案 2** | ✅ 直连 | ✅ 代理 | ✅ 代理 |
| **无配置** | ❌ 超时 | ✅ 代理 | ✅ 代理 |

---

## 🛠️ 扩展配置

### **如果需要更多域名**

#### **方案 1: 修改脚本**

```batch
# 添加飞书、企业微信等
set IM_DOMAINS=wss-open-connection-union.dingtalk.com,api.dingtalk.com,msg-frontier.feishu.cn,wecom.qq.com
set NO_PROXY=%IM_DOMAINS%,%NO_PROXY%
```

#### **方案 2: 修改代码**

```python
# nanobot/channels/dingtalk.py
dingtalk_domains = (
    'wss-open-connection-union.dingtalk.com,'
    'api.dingtalk.com,'
    'oapi.dingtalk.com,'
    'dingtalk.com'
)

# 或者提取为配置文件
# ~/.nanobot/config.json
{
  "network": {
    "no_proxy_domains": [
      "wss-open-connection-union.dingtalk.com",
      "api.dingtalk.com"
    ]
  }
}
```

---

## 💡 最佳实践建议

### **开发环境**

```bash
# 使用方案 1（脚本）
# 灵活切换不同配置

# 配置文件 1: 公司网络
.\start_with_proxy_and_whitelist.bat

# 配置文件 2: 家庭网络（无代理）
.\start_without_proxy.bat
```

### **生产环境**

```bash
# 使用方案 2（代码）
# 提交 PR 到主分支，让所有用户受益

# 或者部署时使用方案 1
# 在 Docker 镜像或 systemd 服务中设置环境变量
Environment=NO_PROXY=wss-open-connection-union.dingtalk.com,api.dingtalk.com
```

---

## 🔍 故障排查

### **问题 1: 设置了 NO_PROXY 但仍然超时**

**检查**：
```python
import os
print("NO_PROXY:", os.environ.get('NO_PROXY'))

# 确认域名格式正确
# ✅ 正确：wss-open-connection-union.dingtalk.com
# ❌ 错误：https://wss-open-connection-union.dingtalk.com
```

**解决**：
- 确保域名不带协议前缀（`http://` 或 `https://`）
- 确保域名之间用逗号分隔

---

### **问题 2: 某些库不识别 NO_PROXY**

**原因**：
- 老旧的 HTTP 库可能不支持 `NO_PROXY`

**解决**：
```python
# 强制使用 httpx（支持 NO_PROXY）
import httpx
client = httpx.AsyncClient()

# 避免使用 requests 2.9.0 以下版本
# requests >= 2.10.0 才支持 NO_PROXY
```

---

### **问题 3: 代理认证失败**

**现象**：
```
Proxy authentication required
```

**解决**：
```bash
# 在代理 URL 中包含认证信息
export HTTP_PROXY="http://user:password@proxy.company.com:8080"
export HTTPS_PROXY="http://user:password@proxy.company.com:8080"

# NO_PROXY 仍然生效
export NO_PROXY="dingtalk.com,$NO_PROXY"
```

---

## 📝 总结

### **核心结论**

1. ✅ **两个方案都能解决问题**
2. ✅ **方案 1 更灵活**（推荐用于个人开发环境）
3. ✅ **方案 2 更优雅**（推荐用于产品化）

### **行动建议**

**立即执行**：
```bash
# 1. 先使用方案 1（脚本）快速解决问题
.\start_with_dingtalk_whitelist.bat

# 2. 同时应用方案 2（代码），作为长期解决方案
# 代码已修改，下次启动自动生效
```

**长期优化**：
- 将方案 2 提交为项目的 Bug Fix
- 考虑为其他 Channel（飞书、Telegram）也添加类似逻辑
- 在文档中添加代理配置说明

---

现在你可以根据实际情况选择合适的方案了！🎉
