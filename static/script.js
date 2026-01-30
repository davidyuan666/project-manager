// 全局变量
let projects = [];
let refreshInterval = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    // 每5秒自动刷新一次
    refreshInterval = setInterval(loadProjects, 5000);
});

// 加载项目列表
async function loadProjects() {
    try {
        const response = await fetch('/api/projects');
        projects = await response.json();
        renderProjects();
    } catch (error) {
        console.error('加载项目失败:', error);
        showMessage('加载项目失败', 'error');
    }
}

// 渲染项目列表
function renderProjects() {
    const container = document.getElementById('projects-container');

    if (projects.length === 0) {
        container.innerHTML = '<div class="loading">暂无项目</div>';
        return;
    }

    container.innerHTML = projects.map(project => `
        <div class="project-card">
            <div class="project-header">
                <div class="project-name">${project.name}</div>
                <span class="status-badge status-${project.status.status}">
                    ${getStatusText(project.status.status)}
                </span>
            </div>

            ${project.description ? `
                <div class="project-description">${project.description}</div>
            ` : ''}

            <div class="project-info">
                <div class="info-item">
                    <span class="info-label">路径</span>
                    <span class="info-value">${project.path}</span>
                </div>
                ${project.port ? `
                    <div class="info-item">
                        <span class="info-label">端口</span>
                        <span class="info-value">${project.port}</span>
                    </div>
                ` : ''}
            </div>

            ${project.status.status === 'running' ? `
                <div class="project-stats show">
                    <div class="stat-item">
                        <span class="stat-label">进程 ID</span>
                        <span class="stat-value">${project.status.pid}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">CPU 使用率</span>
                        <span class="stat-value">${project.status.cpu_percent?.toFixed(1) || 0}%</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">内存使用</span>
                        <span class="stat-value">${project.status.memory_mb?.toFixed(1) || 0} MB</span>
                    </div>
                </div>
            ` : ''}

            <div class="project-actions">
                <button
                    class="btn btn-start"
                    onclick="startProject('${project.id}')"
                    ${project.status.status === 'running' ? 'disabled' : ''}>
                    启动
                </button>
                <button
                    class="btn btn-stop"
                    onclick="stopProject('${project.id}')"
                    ${project.status.status !== 'running' ? 'disabled' : ''}>
                    停止
                </button>
            </div>
        </div>
    `).join('');
}

// 获取状态文本
function getStatusText(status) {
    const statusMap = {
        'running': '运行中',
        'stopped': '已停止',
        'unknown': '未知'
    };
    return statusMap[status] || '未知';
}

// 启动项目
async function startProject(projectId) {
    try {
        const response = await fetch(`/api/projects/${projectId}/start`, {
            method: 'POST'
        });
        const result = await response.json();

        if (result.success) {
            showMessage('项目启动成功', 'success');
            setTimeout(loadProjects, 1000);
        } else {
            showMessage(result.message, 'error');
        }
    } catch (error) {
        console.error('启动项目失败:', error);
        showMessage('启动项目失败', 'error');
    }
}

// 停止项目
async function stopProject(projectId) {
    try {
        const response = await fetch(`/api/projects/${projectId}/stop`, {
            method: 'POST'
        });
        const result = await response.json();

        if (result.success) {
            showMessage('项目已停止', 'success');
            setTimeout(loadProjects, 1000);
        } else {
            showMessage(result.message, 'error');
        }
    } catch (error) {
        console.error('停止项目失败:', error);
        showMessage('停止项目失败', 'error');
    }
}

// 显示消息提示
function showMessage(text, type = 'success') {
    const message = document.createElement('div');
    message.className = `message message-${type}`;
    message.textContent = text;
    document.body.appendChild(message);

    setTimeout(() => {
        message.remove();
    }, 3000);
}
