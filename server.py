#!/usr/bin/env python3
"""
FastMCP Demo Server
一个功能丰富的MCP服务器示例，展示各种MCP功能
"""

import json
import sqlite3
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass

# 检查是否安装了FastMCP v2
try:
    from fastmcp import FastMCP
    FASTMCP_V2 = True
except ImportError:
    # 如果没有v2，尝试从官方SDK导入
    try:
        from mcp.server.fastmcp import FastMCP
        FASTMCP_V2 = False
    except ImportError:
        raise ImportError("请安装FastMCP: pip install fastmcp 或者 pip install mcp")

# 初始化MCP服务器
mcp = FastMCP("FastMCP Demo Server 🚀")

# 数据库初始化
DB_PATH = "demo_data.db"

def init_database():
    """初始化SQLite数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建笔记表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # 插入示例数据
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        sample_users = [
            ("张三", "zhangsan@example.com"),
            ("李四", "lisi@example.com"),
            ("王五", "wangwu@example.com")
        ]
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", sample_users)
        
        sample_notes = [
            ("Python学习笔记", "今天学习了FastMCP的使用", 1),
            ("项目计划", "下周要完成MCP服务器的开发", 2),
            ("会议记录", "团队讨论了新功能的实现方案", 1)
        ]
        cursor.executemany("INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)", sample_notes)
    
    conn.commit()
    conn.close()

# 初始化数据库
init_database()

# ==================== 工具函数 ====================

@mcp.tool()
def calculate(expression: str) -> str:
    """
    安全计算数学表达式
    支持基本的数学运算：+, -, *, /, **, ()
    
    参数:
        expression: 要计算的数学表达式，如 "2 + 3 * 4"
    
    返回:
        计算结果
    """
    try:
        # 安全的表达式计算，只允许基本数学运算
        allowed_chars = set("0123456789+-*/().() ")
        if not all(c in allowed_chars for c in expression):
            return "错误：表达式包含不允许的字符"
        
        # 使用eval进行计算（在受控环境中）
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

@mcp.tool()
def add_user(name: str, email: str) -> str:
    """
    添加新用户到数据库
    
    参数:
        name: 用户姓名
        email: 用户邮箱
    
    返回:
        操作结果
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return f"成功添加用户: {name} (ID: {user_id})"
    except sqlite3.IntegrityError:
        return f"错误：邮箱 {email} 已存在"
    except Exception as e:
        return f"添加用户失败: {str(e)}"

@mcp.tool()
def get_users() -> str:
    """
    获取所有用户列表
    
    返回:
        格式化的用户列表
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        conn.close()
        
        if not users:
            return "暂无用户数据"
        
        result = "用户列表:\n"
        for user in users:
            result += f"ID: {user[0]}, 姓名: {user[1]}, 邮箱: {user[2]}, 创建时间: {user[3]}\n"
        
        return result
    except Exception as e:
        return f"获取用户列表失败: {str(e)}"

@mcp.tool()
def add_note(title: str, content: str, user_id: int) -> str:
    """
    为用户添加笔记
    
    参数:
        title: 笔记标题
        content: 笔记内容
        user_id: 用户ID
    
    返回:
        操作结果
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查用户是否存在
        cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return f"错误：用户ID {user_id} 不存在"
        
        cursor.execute("INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)", 
                      (title, content, user_id))
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return f"成功为用户 {user[0]} 添加笔记: {title} (ID: {note_id})"
    except Exception as e:
        return f"添加笔记失败: {str(e)}"

@mcp.tool()
def get_notes(user_id: int = None) -> str:
    """
    获取笔记列表
    
    参数:
        user_id: 可选，指定用户ID获取该用户的笔记，不指定则获取所有笔记
    
    返回:
        格式化的笔记列表
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("""
                SELECT n.id, n.title, n.content, u.name, n.created_at 
                FROM notes n 
                JOIN users u ON n.user_id = u.id 
                WHERE n.user_id = ? 
                ORDER BY n.created_at DESC
            """, (user_id,))
        else:
            cursor.execute("""
                SELECT n.id, n.title, n.content, u.name, n.created_at 
                FROM notes n 
                JOIN users u ON n.user_id = u.id 
                ORDER BY n.created_at DESC
            """)
        
        notes = cursor.fetchall()
        conn.close()
        
        if not notes:
            return "暂无笔记数据"
        
        result = f"笔记列表 {'(用户ID: ' + str(user_id) + ')' if user_id else '(所有用户)'}:\n"
        for note in notes:
            result += f"ID: {note[0]}, 标题: {note[1]}, 作者: {note[3]}, 创建时间: {note[4]}\n"
            result += f"内容: {note[2]}\n---\n"
        
        return result
    except Exception as e:
        return f"获取笔记失败: {str(e)}"

@mcp.tool()
def write_file(filename: str, content: str) -> str:
    """
    写入文件
    
    参数:
        filename: 文件名
        content: 文件内容
    
    返回:
        操作结果
    """
    try:
        # 创建files目录（如果不存在）
        files_dir = Path("files")
        files_dir.mkdir(exist_ok=True)
        
        file_path = files_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"成功写入文件: {file_path}"
    except Exception as e:
        return f"写入文件失败: {str(e)}"

@mcp.tool()
def read_file(filename: str) -> str:
    """
    读取文件内容
    
    参数:
        filename: 文件名
    
    返回:
        文件内容或错误信息
    """
    try:
        file_path = Path("files") / filename
        if not file_path.exists():
            return f"错误：文件 {filename} 不存在"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"文件 {filename} 的内容:\n{content}"
    except Exception as e:
        return f"读取文件失败: {str(e)}"

@mcp.tool()
def list_files() -> str:
    """
    列出files目录中的所有文件
    
    返回:
        文件列表
    """
    try:
        files_dir = Path("files")
        if not files_dir.exists():
            return "files目录不存在"
        
        files = list(files_dir.glob("*"))
        if not files:
            return "files目录为空"
        
        result = "文件列表:\n"
        for file_path in files:
            if file_path.is_file():
                stat = file_path.stat()
                result += f"- {file_path.name} (大小: {stat.st_size} 字节, 修改时间: {datetime.fromtimestamp(stat.st_mtime)})\n"
        
        return result
    except Exception as e:
        return f"列出文件失败: {str(e)}"

# ==================== 资源 ====================

@mcp.resource("user://{user_id}")
def get_user_resource(user_id: str) -> str:
    """获取用户信息资源"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (int(user_id),))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return f"用户 {user_id} 不存在"
        
        return f"用户信息:\nID: {user[0]}\n姓名: {user[1]}\n邮箱: {user[2]}\n创建时间: {user[3]}"
    except Exception as e:
        return f"获取用户信息失败: {str(e)}"

@mcp.resource("stats://database")
def get_database_stats() -> str:
    """获取数据库统计信息"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM notes")
        note_count = cursor.fetchone()[0]
        
        conn.close()
        
        return f"数据库统计:\n用户总数: {user_count}\n笔记总数: {note_count}\n数据库文件: {DB_PATH}"
    except Exception as e:
        return f"获取统计信息失败: {str(e)}"

# ==================== 主函数 ====================

if __name__ == "__main__":
    print("🚀 启动FastMCP Demo服务器...")
    print("功能包括:")
    print("- 数学计算工具")
    print("- 用户管理")
    print("- 笔记系统") 
    print("- 文件操作")
    print("- 资源查询")
    print("\n服务器正在运行，等待连接...")
    
    if FASTMCP_V2:
        # FastMCP v2
        mcp.run()
    else:
        # 官方SDK中的FastMCP
        mcp.run()
