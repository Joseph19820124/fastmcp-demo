# FastMCP Demo Server 🚀

一个功能丰富的Model Context Protocol (MCP)服务器示例，展示如何使用FastMCP框架构建强大的AI工具集成。

## 功能特色

### 🧮 数学计算工具
- 安全的数学表达式计算
- 支持基本运算：+、-、*、/、**、()

### 👥 用户管理系统
- 添加新用户
- 查看用户列表
- 用户信息资源查询

### 📝 笔记系统
- 为用户创建笔记
- 查看所有笔记或特定用户的笔记
- 笔记与用户关联

### 📁 文件操作
- 写入文件
- 读取文件
- 列出文件目录

### 📊 资源查询
- 用户信息资源
- 数据库统计信息

## 安装要求

- Python 3.8+
- FastMCP v2.0+ 或 官方MCP SDK

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Joseph19820124/fastmcp-demo.git
cd fastmcp-demo
```

### 2. 安装依赖

```bash
# 使用pip
pip install -r requirements.txt

# 或使用uv (推荐)
uv pip install -r requirements.txt
```

### 3. 运行服务器

```bash
python server.py
```

## 使用方法

### 与Claude Desktop集成

1. 打开Claude Desktop应用
2. 进入设置 > 开发者设置
3. 点击"编辑配置"
4. 添加以下配置：

```json
{
  "mcpServers": {
    "fastmcp-demo": {
      "command": "python",
      "args": ["/path/to/your/server.py"],
      "cwd": "/path/to/your/fastmcp-demo"
    }
  }
}
```

5. 重启Claude Desktop

### 与其他MCP客户端集成

服务器使用stdio传输协议，可以与任何支持MCP的客户端集成。

## 可用工具

| 工具名称 | 描述 | 参数 |
|---------|------|------|
| `calculate` | 计算数学表达式 | `expression: str` |
| `add_user` | 添加新用户 | `name: str, email: str` |
| `get_users` | 获取用户列表 | 无 |
| `add_note` | 添加笔记 | `title: str, content: str, user_id: int` |
| `get_notes` | 获取笔记 | `user_id: int` (可选) |
| `write_file` | 写入文件 | `filename: str, content: str` |
| `read_file` | 读取文件 | `filename: str` |
| `list_files` | 列出文件 | 无 |

## 可用资源

| 资源URI | 描述 |
|---------|------|
| `user://{user_id}` | 获取指定用户信息 |
| `stats://database` | 获取数据库统计信息 |

## 示例对话

```
用户: 帮我计算 2 + 3 * 4
助手: [使用calculate工具] 2 + 3 * 4 = 14

用户: 添加一个用户，姓名是张三，邮箱是zhangsan@test.com
助手: [使用add_user工具] 成功添加用户: 张三 (ID: 4)

用户: 为用户ID 1 创建一个标题为"学习计划"的笔记
助手: [使用add_note工具] 成功为用户张三添加笔记: 学习计划 (ID: 4)
```

## 项目结构

```
fastmcp-demo/
├── server.py              # 主服务器文件
├── requirements.txt        # 依赖文件
├── README.md              # 说明文档
├── demo_data.db           # SQLite数据库(自动创建)
├── files/                 # 文件存储目录(自动创建)
└── tests/                 # 测试文件(可选)
```

## 开发指南

### 添加新工具

```python
@mcp.tool()
def your_new_tool(param1: str, param2: int) -> str:
    """
    工具描述
    
    参数:
        param1: 参数1描述
        param2: 参数2描述
    
    返回:
        返回值描述
    """
    # 你的逻辑
    return "结果"
```

### 添加新资源

```python
@mcp.resource("your-scheme://{param}")
def your_resource(param: str) -> str:
    """资源描述"""
    # 你的逻辑
    return "资源内容"
```

## 测试

运行包含的测试脚本：

```bash
python test_client.py
```

## 常见问题

### Q: 如何调试MCP服务器？
A: 使用FastMCP内置的调试工具：
```bash
mcp dev server.py
```
这将启动一个Web界面用于测试。

### Q: 支持哪些传输协议？
A: 默认使用stdio，也支持HTTP和WebSocket传输。

### Q: 如何处理错误？
A: 所有工具都包含错误处理，并返回描述性错误消息。

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License - 详见LICENSE文件

## 相关链接

- [FastMCP 官方文档](https://gofastmcp.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)

---

🎉 享受构建AI工具的乐趣！如果这个项目对你有帮助，请给个⭐️