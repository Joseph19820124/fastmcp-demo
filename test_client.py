#!/usr/bin/env python3
"""
FastMCP Demo 测试客户端
用于测试MCP服务器的各种功能
"""

import asyncio
import json
from typing import Any, Dict

# 检查FastMCP版本并导入相应的客户端
try:
    from fastmcp import Client
    FASTMCP_V2 = True
    print("使用 FastMCP v2 客户端")
except ImportError:
    try:
        from mcp.client import Client
        FASTMCP_V2 = False
        print("使用 官方MCP SDK 客户端")
    except ImportError:
        raise ImportError("请安装FastMCP或官方MCP SDK")

async def test_mcp_server():
    """测试MCP服务器的功能"""
    
    print("🚀 开始测试FastMCP Demo服务器...")
    
    # 导入服务器
    from server import mcp
    
    try:
        # 创建客户端连接
        if FASTMCP_V2:
            # FastMCP v2 使用内存传输
            async with Client(mcp) as client:
                await run_tests(client)
        else:
            # 官方SDK的连接方式可能不同
            print("注意：官方SDK客户端测试需要不同的连接方式")
            print("建议使用 `mcp dev server.py` 命令进行调试")
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("请确保已正确安装FastMCP并且服务器代码可以正常运行")

async def run_tests(client):
    """运行具体的测试"""
    
    print("\n📋 开始功能测试...\n")
    
    # 测试1: 数学计算
    print("🧮 测试数学计算工具...")
    try:
        result = await client.call_tool("calculate", {"expression": "2 + 3 * 4"})
        print(f"  计算结果: {result}")
    except Exception as e:
        print(f"  ❌ 计算测试失败: {e}")
    
    # 测试2: 添加用户
    print("\n👤 测试用户管理...")
    try:
        result = await client.call_tool("add_user", {
            "name": "测试用户", 
            "email": "test@example.com"
        })
        print(f"  添加用户: {result}")
        
        # 获取用户列表
        result = await client.call_tool("get_users", {})
        print(f"  用户列表: {result}")
    except Exception as e:
        print(f"  ❌ 用户管理测试失败: {e}")
    
    # 测试3: 笔记系统
    print("\n📝 测试笔记系统...")
    try:
        result = await client.call_tool("add_note", {
            "title": "测试笔记",
            "content": "这是一个测试笔记的内容",
            "user_id": 1
        })
        print(f"  添加笔记: {result}")
        
        # 获取笔记列表
        result = await client.call_tool("get_notes", {})
        print(f"  笔记列表: {result[:200]}...")  # 只显示前200个字符
    except Exception as e:
        print(f"  ❌ 笔记系统测试失败: {e}")
    
    # 测试4: 文件操作
    print("\n📁 测试文件操作...")
    try:
        # 写入文件
        result = await client.call_tool("write_file", {
            "filename": "test.txt",
            "content": "这是一个测试文件的内容\\n包含多行文本"
        })
        print(f"  写入文件: {result}")
        
        # 读取文件
        result = await client.call_tool("read_file", {"filename": "test.txt"})
        print(f"  读取文件: {result}")
        
        # 列出文件
        result = await client.call_tool("list_files", {})
        print(f"  文件列表: {result}")
    except Exception as e:
        print(f"  ❌ 文件操作测试失败: {e}")
    
    # 测试5: 资源查询
    print("\n📊 测试资源查询...")
    try:
        # 查询用户资源
        result = await client.read_resource("user://1")
        print(f"  用户资源: {result}")
        
        # 查询数据库统计
        result = await client.read_resource("stats://database")
        print(f"  数据库统计: {result}")
    except Exception as e:
        print(f"  ❌ 资源查询测试失败: {e}")
    
    print("\n✅ 测试完成！")

def run_interactive_test():
    """运行交互式测试"""
    print("🎮 交互式测试模式")
    print("输入要测试的工具名称，或输入 'quit' 退出")
    print("可用工具: calculate, add_user, get_users, add_note, get_notes, write_file, read_file, list_files")
    
    while True:
        try:
            tool_name = input("\\n请输入工具名称: ").strip()
            if tool_name.lower() in ['quit', 'exit', 'q']:
                break
                
            if tool_name == "calculate":
                expr = input("请输入数学表达式: ")
                print(f"你可以在MCP客户端中调用: calculate('{expr}')")
                
            elif tool_name == "add_user":
                name = input("请输入用户姓名: ")
                email = input("请输入用户邮箱: ")
                print(f"你可以在MCP客户端中调用: add_user('{name}', '{email}')")
                
            elif tool_name in ["get_users", "list_files"]:
                print(f"你可以在MCP客户端中调用: {tool_name}()")
                
            else:
                print(f"工具 '{tool_name}' 需要参数，请查看README.md了解详细信息")
                
        except KeyboardInterrupt:
            print("\\n\\n👋 再见！")
            break
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    print("FastMCP Demo 测试客户端")
    print("========================")
    print("1. 自动测试")
    print("2. 交互式测试")
    print("3. 退出")
    
    try:
        choice = input("\\n请选择模式 (1-3): ").strip()
        
        if choice == "1":
            asyncio.run(test_mcp_server())
        elif choice == "2":
            run_interactive_test()
        elif choice == "3":
            print("👋 再见！")
        else:
            print("无效选择")
            
    except KeyboardInterrupt:
        print("\\n\\n👋 再见！")
    except Exception as e:
        print(f"错误: {e}")
