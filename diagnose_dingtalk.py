#!/usr/bin/env python3
"""
钉钉连接性诊断工具

用于检查网络、配置和权限问题。
"""

import asyncio
import socket
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))


def test_dns_resolution():
    """测试 DNS 解析"""
    print("\n🔍 测试 DNS 解析...")
    
    domains = [
        "wss-open-connection-union.dingtalk.com",
        "api.dingtalk.com",
    ]
    
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
            print(f"  ✅ {domain} → {ip}")
        except socket.gaierror as e:
            print(f"  ❌ {domain} → DNS 解析失败：{e}")
            return False
    
    return True


def test_tcp_connection(host, port, timeout=5):
    """测试 TCP 连接"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"  ❌ 连接失败：{e}")
        return False


def test_network_connectivity():
    """测试网络连通性"""
    print("\n🌐 测试网络连通性...")
    
    tests = [
        ("钉钉 WebSocket 服务器", "wss-open-connection-union.dingtalk.com", 443),
        ("钉钉 API 服务器", "api.dingtalk.com", 443),
    ]
    
    all_passed = True
    for name, host, port in tests:
        if test_tcp_connection(host, port):
            print(f"  ✅ {name} ({host}:{port}) - 可连接")
        else:
            print(f"  ❌ {name} ({host}:{port}) - 无法连接")
            all_passed = False
    
    return all_passed


def test_config_loading():
    """测试配置文件加载"""
    print("\n📄 测试配置文件加载...")
    
    config_paths = [
        Path.home() / ".nanobot" / "config.json",
        Path("config.json"),
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            print(f"  ✅ 找到配置文件：{config_path}")
            
            try:
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                dingtalk_config = config.get('channels', {}).get('dingtalk', {})
                if dingtalk_config:
                    enabled = dingtalk_config.get('enabled', False)
                    client_id = dingtalk_config.get('clientId', '')
                    
                    print(f"    - 启用状态：{'✅' if enabled else '❌'}")
                    print(f"    - Client ID: {client_id[:20]}..." if len(client_id) > 20 else f"    - Client ID: {client_id}")
                    
                    if not client_id:
                        print(f"    ⚠️  警告：Client ID 为空！")
                        return False
                    
                    return True
                else:
                    print(f"    ⚠️  警告：未找到钉钉配置")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"  ❌ 配置文件解析失败：{e}")
                return False
        else:
            print(f"  ⚠️  未找到：{config_path}")
    
    return False


async def test_dingtalk_sdk():
    """测试钉钉 SDK 可用性"""
    print("\n🤖 测试钉钉 SDK...")
    
    try:
        from dingtalk_stream import Credential, DingTalkStreamClient
        print("  ✅ 钉钉 SDK 已安装")
        
        # 尝试加载配置
        config_ok = test_config_loading()
        if not config_ok:
            print("  ⚠️  配置不完整，跳过连接测试")
            return True  # SDK 本身可用
        
        # 读取配置
        import json
        config_path = Path.home() / ".nanobot" / "config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        dingtalk_config = config.get('channels', {}).get('dingtalk', {})
        client_id = dingtalk_config.get('clientId', '')
        client_secret = dingtalk_config.get('clientSecret', '')
        
        if not client_id or not client_secret:
            print("  ❌ Client ID 或 Secret 为空")
            return False
        
        print(f"  ✅ 配置读取成功")
        
        # 创建凭证（不实际连接）
        credential = Credential(client_id, client_secret)
        client = DingTalkStreamClient(credential)
        
        print("  ✅ SDK 初始化成功")
        print("\n  💡 提示：如果实际连接失败，可能是网络或权限问题")
        return True
        
    except ImportError as e:
        print(f"  ❌ 钉钉 SDK 未安装：{e}")
        print("  💡 运行：pip install dingtalk-stream")
        return False
    except Exception as e:
        print(f"  ❌ SDK 测试失败：{e}")
        return False


def check_firewall():
    """检查防火墙/代理设置"""
    print("\n🛡️  检查防火墙/代理设置...")
    
    import os
    
    # 检查 HTTP 代理
    http_proxy = os.environ.get('HTTP_PROXY', os.environ.get('http_proxy', ''))
    https_proxy = os.environ.get('HTTPS_PROXY', os.environ.get('https_proxy', ''))
    
    if http_proxy or https_proxy:
        print(f"  ⚠️  检测到代理配置：")
        if http_proxy:
            print(f"     HTTP_PROXY: {http_proxy}")
        if https_proxy:
            print(f"     HTTPS_PROXY: {https_proxy}")
        print(f"  💡 提示：钉钉 Stream 模式可能不支持通过代理连接")
    else:
        print(f"  ✅ 未检测到代理配置")
    
    # Windows 防火墙检查
    if sys.platform == 'win32':
        print(f"\n  💡 Windows 防火墙建议：")
        print(f"     1. 确保 Python 可以访问外网")
        print(f"     2. 允许端口 443 (HTTPS)")
        print(f"     3. 如果使用公司网络，可能需要 IT 部门放行钉钉域名")


def print_summary(results):
    """打印诊断总结"""
    print("\n" + "="*60)
    print("📊 诊断总结")
    print("="*60)
    
    labels = {
        'dns': 'DNS 解析',
        'network': '网络连通性',
        'config': '配置文件',
        'sdk': 'SDK 可用性',
    }
    
    all_passed = True
    for key, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {labels[key]}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ 所有检查通过！")
        print("\n💡 如果仍然无法连接，请检查：")
        print("   1. 钉钉应用是否已发布？")
        print("   2. 机器人权限是否已授予？")
        print("   3. Stream 模式是否已开启？")
        print("   4. 查看钉钉开发者后台的错误日志")
    else:
        print("❌ 发现问题！请按上述建议修复后重试。")
    print("="*60)


async def main():
    """主函数"""
    print("="*60)
    print("🔧 钉钉连接性诊断工具")
    print("="*60)
    
    results = {}
    
    # 1. DNS 解析
    results['dns'] = test_dns_resolution()
    
    # 2. 网络连通性
    results['network'] = test_network_connectivity()
    
    # 3. 配置文件
    results['config'] = test_config_loading()
    
    # 4. SDK 可用性
    results['sdk'] = await test_dingtalk_sdk()
    
    # 5. 防火墙检查
    check_firewall()
    
    # 6. 总结
    print_summary(results)


if __name__ == '__main__':
    asyncio.run(main())
