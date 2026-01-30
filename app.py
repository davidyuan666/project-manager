from flask import Flask, render_template, jsonify, request
import subprocess
import psutil
import os
import json
from datetime import datetime

app = Flask(__name__)

# 配置文件路径
CONFIG_FILE = 'projects_config.json'

# 默认项目配置
DEFAULT_PROJECTS = {
    'petricode': {
        'name': 'PetriCode',
        'path': '../PetriCode',
        'start_command': 'venv\\Scripts\\python.exe -m petircode.main',
        'process_name': 'python.exe',
        'process_args': 'petircode.main',
        'description': 'PetriCode Telegram Bot'
    }
}

def load_config():
    """加载项目配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_PROJECTS

def save_config(config):
    """保存项目配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_process_by_name_and_args(process_name, process_args):
    """通过进程名称和参数查找进程"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if process_args in cmdline:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def check_project_status(project_id):
    """检查项目运行状态"""
    projects = load_config()
    if project_id not in projects:
        return {'status': 'unknown', 'message': '项目不存在'}

    project = projects[project_id]
    process_name = project.get('process_name')
    process_args = project.get('process_args')

    if process_name and process_args:
        proc = get_process_by_name_and_args(process_name, process_args)
        if proc:
            try:
                return {
                    'status': 'running',
                    'pid': proc.pid,
                    'cpu_percent': proc.cpu_percent(),
                    'memory_mb': proc.memory_info().rss / 1024 / 1024
                }
            except:
                pass

    return {'status': 'stopped'}

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/projects')
def get_projects():
    """获取所有项目列表及状态"""
    projects = load_config()
    result = []

    for project_id, project in projects.items():
        status = check_project_status(project_id)
        result.append({
            'id': project_id,
            'name': project['name'],
            'description': project.get('description', ''),
            'path': project['path'],
            'port': project.get('port'),
            'status': status
        })

    return jsonify(result)

@app.route('/api/projects/<project_id>/start', methods=['POST'])
def start_project(project_id):
    """启动项目"""
    projects = load_config()

    if project_id not in projects:
        return jsonify({'success': False, 'message': '项目不存在'}), 404

    project = projects[project_id]
    status = check_project_status(project_id)

    if status['status'] == 'running':
        return jsonify({'success': False, 'message': '项目已在运行中'})

    try:
        project_path = os.path.abspath(project['path'])
        command = project['start_command']

        # 在项目目录下启动进程
        subprocess.Popen(
            command,
            shell=True,
            cwd=project_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return jsonify({'success': True, 'message': '项目启动成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'启动失败: {str(e)}'})

@app.route('/api/projects/<project_id>/stop', methods=['POST'])
def stop_project(project_id):
    """停止项目"""
    projects = load_config()

    if project_id not in projects:
        return jsonify({'success': False, 'message': '项目不存在'}), 404

    project = projects[project_id]
    status = check_project_status(project_id)

    if status['status'] != 'running':
        return jsonify({'success': False, 'message': '项目未运行'})

    try:
        process_name = project.get('process_name')
        process_args = project.get('process_args')

        if process_name and process_args:
            proc = get_process_by_name_and_args(process_name, process_args)
            if proc:
                proc.terminate()
                proc.wait(timeout=5)
                return jsonify({'success': True, 'message': '项目已停止'})

        return jsonify({'success': False, 'message': '未找到运行的进程'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'停止失败: {str(e)}'})

if __name__ == '__main__':
    # 初始化配置文件
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_PROJECTS)

    app.run(host='0.0.0.0', port=5001, debug=True)
