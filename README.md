# 项目管理器

一个简单的 Web 应用，用于管理和监控本地项目的运行状态。

## 功能特性

- 查看项目运行状态（运行中/已停止）
- 启动和停止项目
- 实时监控项目资源使用情况（CPU、内存）
- 自动刷新状态
- 美观的 Web 界面

## 安装

1. 克隆仓库
```bash
git clone <repository-url>
cd project-manager
```

2. 创建虚拟环境
```bash
python -m venv venv
```

3. 激活虚拟环境
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动项目管理器
```bash
python app.py
```

2. 打开浏览器访问
```
http://localhost:5001
```

3. 在界面上可以：
   - 查看所有项目的状态
   - 点击"启动"按钮启动项目
   - 点击"停止"按钮停止项目
   - 查看运行中项目的资源使用情况

## 配置

项目配置保存在 `projects_config.json` 文件中。默认配置包含 PetriCode 项目。

配置格式：
```json
{
  "project_id": {
    "name": "项目名称",
    "path": "项目路径",
    "start_command": "启动命令",
    "port": 端口号,
    "description": "项目描述"
  }
}
```

## 技术栈

- 后端：Flask + Python
- 前端：HTML + CSS + JavaScript
- 进程管理：psutil

## 注意事项

- 项目管理器运行在 5001 端口
- 确保被管理的项目路径正确
- 需要有足够的权限来启动和停止进程
