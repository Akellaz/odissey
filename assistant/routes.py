# assistant/routes.py
from flask import Blueprint, request, jsonify, render_template_string
import json
import os
from .core import SuperDevAssistant

assistant_bp = Blueprint('assistant', __name__, url_prefix='/assistant')
assistant = SuperDevAssistant()

@assistant_bp.route('/')
def assistant_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Super Dev Assistant - Управление сайтом</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-robot"></i> Super Dev Assistant
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/"><i class="fas fa-home"></i> Сайт</a>
                <a class="nav-link active" href="/assistant"><i class="fas fa-tools"></i> Ассистент</a>
            </div>
        </div>
    </nav>

    <div class="container py-4">
        <div class="row">
            <div class="col-12 text-center mb-4">
                <h1><i class="fas fa-cogs"></i> Управление сайтом</h1>
                <p class="lead">Создавайте, анализируйте и улучшайте ваш сайт с помощью ИИ</p>
            </div>
        </div>

        <div class="row">
            <!-- Панель создания кода -->
            <div class="col-lg-6 mb-4">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0"><i class="fas fa-plus-circle"></i> Создать новый модуль</h5>
                    </div>
                    <div class="card-body">
                        <form id="createModuleForm">
                            <div class="mb-3">
                                <label class="form-label">Название раздела:</label>
                                <input type="text" class="form-control" id="sectionName" 
                                       placeholder="Например: blog, gallery, forum">
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Страницы (через запятую):</label>
                                <input type="text" class="form-control" id="pageNames" 
                                       placeholder="index, list, detail, create">
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Функции (через запятую):</label>
                                <input type="text" class="form-control" id="features" 
                                       placeholder="form, chart, api, auth">
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Тип генерации:</label>
                                <select class="form-select" id="generationType">
                                    <option value="full">Полный модуль (routes+templates+js+css)</option>
                                    <option value="route">Только route файл</option>
                                    <option value="template">Только шаблоны</option>
                                    <option value="javascript">Только JavaScript</option>
                                </select>
                            </div>
                            
                            <button type="button" class="btn btn-primary" onclick="createModule()">
                                <i class="fas fa-magic"></i> Создать модуль
                            </button>
                        </form>
                    </div>
                </div>
                
                <!-- Панель анализа кода -->
                <div class="card shadow mt-4">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0"><i class="fas fa-search"></i> Анализировать код</h5>
                    </div>
                    <div class="card-body">
                        <form id="analyzeForm">
                            <div class="mb-3">
                                <label class="form-label">Код для анализа:</label>
                                <textarea class="form-control" id="codeToAnalyze" rows="8" 
                                          placeholder="Вставьте код для анализа..."></textarea>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Описание задачи:</label>
                                <input type="text" class="form-control" id="analysisTask" 
                                       placeholder="Что нужно проанализировать?">
                            </div>
                            
                            <button type="button" class="btn btn-info" onclick="analyzeCode()">
                                <i class="fas fa-search"></i> Проанализировать
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Результаты -->
            <div class="col-lg-6">
                <div class="card shadow">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0"><i class="fas fa-file-code"></i> Результаты</h5>
                    </div>
                    <div class="card-body">
                        <div id="resultsArea">
                            <div class="text-center text-muted">
                                <i class="fas fa-robot fa-3x mb-3"></i>
                                <p>Здесь появятся результаты работы ассистента</p>
                                <small>Создавайте модули, анализируйте код, улучшайте сайт</small>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Быстрые действия -->
                <div class="card shadow mt-4">
                    <div class="card-header bg-warning text-dark">
                        <h5 class="mb-0"><i class="fas fa-bolt"></i> Быстрые действия</h5>
                    </div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <button class="btn btn-outline-primary" onclick="generateMusicModule()">
                                <i class="fas fa-music"></i> Музыкальный модуль
                            </button>
                            <button class="btn btn-outline-success" onclick="generateSupModule()">
                                <i class="fas fa-water"></i> SUP модуль
                            </button>
                            <button class="btn btn-outline-info" onclick="generateBooksModule()">
                                <i class="fas fa-book"></i> Модуль книг
                            </button>
                            <button class="btn btn-outline-warning" onclick="generateStudyModule()">
                                <i class="fas fa-graduation-cap"></i> Учебный модуль
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function createModule() {
            const section = document.getElementById('sectionName').value;
            const pages = document.getElementById('pageNames').value.split(',').map(p => p.trim()).filter(p => p);
            const features = document.getElementById('features').value.split(',').map(f => f.trim()).filter(f => f);
            const type = document.getElementById('generationType').value;
            
            if (!section) {
                alert('Укажите название раздела');
                return;
            }
            
            showLoading('Создаем модуль...');
            
            fetch('/assistant/create_module', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({section, pages, features, type})
            })
            .then(r => r.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                showError('Ошибка создания модуля: ' + error.message);
            });
        }
        
        function analyzeCode() {
            const code = document.getElementById('codeToAnalyze').value;
            const task = document.getElementById('analysisTask').value;
            
            if (!code.trim()) {
                alert('Введите код для анализа');
                return;
            }
            
            showLoading('Анализируем код...');
            
            fetch('/assistant/analyze_code', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code, task})
            })
            .then(r => r.json())
            .then(data => {
                displayAnalysis(data.analysis);
            })
            .catch(error => {
                showError('Ошибка анализа: ' + error.message);
            });
        }
        
        function generateMusicModule() {
            document.getElementById('sectionName').value = 'music';
            document.getElementById('pageNames').value = 'index, analyzer, sequencer, library';
            document.getElementById('features').value = 'audio, waveform, player';
            document.getElementById('generationType').value = 'full';
            createModule();
        }
        
        function generateSupModule() {
            document.getElementById('sectionName').value = 'sup';
            document.getElementById('pageNames').value = 'index, map, routes, booking';
            document.getElementById('features').value = 'map, gps, booking';
            document.getElementById('generationType').value = 'full';
            createModule();
        }
        
        function generateBooksModule() {
            document.getElementById('sectionName').value = 'books';
            document.getElementById('pageNames').value = 'index, list, detail, create, edit';
            document.getElementById('features').value = 'form, search, pagination';
            document.getElementById('generationType').value = 'full';
            createModule();
        }
        
        function generateStudyModule() {
            document.getElementById('sectionName').value = 'study';
            document.getElementById('pageNames').value = 'index, schedule, lessons, profile';
            document.getElementById('features').value = 'auth, calendar, progress';
            document.getElementById('generationType').value = 'full';
            createModule();
        }
        
        function displayResults(data) {
            hideLoading();
            const resultsArea = document.getElementById('resultsArea');
            
            let html = '<h5><i class="fas fa-check-circle"></i> Модуль создан успешно!</h5>';
            
            if (data.route_file) {
                html += `
                    <div class="mb-3">
                        <h6><i class="fas fa-file-code"></i> Route файл (routes/${data.section}.py):</h6>
                        <button class="btn btn-sm btn-outline-primary mb-2" onclick="copyToClipboard(this, 'route')">
                            <i class="fas fa-copy"></i> Копировать
                        </button>
                        <pre id="route-code" class="bg-light p-3 small">${escapeHtml(data.route_file)}</pre>
                    </div>
                `;
            }
            
            if (data.templates && Object.keys(data.templates).length > 0) {
                html += '<h6><i class="fas fa-file-alt"></i> Шаблоны:</h6>';
                for (const [name, template] of Object.entries(data.templates)) {
                    html += `
                        <div class="mb-3">
                            <h6>templates/${data.section}/${name}.html:</h6>
                            <button class="btn btn-sm btn-outline-primary mb-2" onclick="copyToClipboard(this, 'template-${name}')">
                                <i class="fas fa-copy"></i> Копировать
                            </button>
                            <pre id="template-${name}-code" class="bg-light p-3 small">${escapeHtml(template)}</pre>
                        </div>
                    `;
                }
            }
            
            if (data.javascript) {
                html += `
                    <div class="mb-3">
                        <h6><i class="fas fa-js"></i> JavaScript (static/js/${data.section}.js):</h6>
                        <button class="btn btn-sm btn-outline-primary mb-2" onclick="copyToClipboard(this, 'js')">
                            <i class="fas fa-copy"></i> Копировать
                        </button>
                        <pre id="js-code" class="bg-light p-3 small">${escapeHtml(data.javascript)}</pre>
                    </div>
                `;
            }
            
            if (data.css) {
                html += `
                    <div class="mb-3">
                        <h6><i class="fas fa-css3"></i> CSS (static/css/${data.section}.css):</h6>
                        <button class="btn btn-sm btn-outline-primary mb-2" onclick="copyToClipboard(this, 'css')">
                            <i class="fas fa-copy"></i> Копировать
                        </button>
                        <pre id="css-code" class="bg-light p-3 small">${escapeHtml(data.css)}</pre>
                    </div>
                `;
            }
            
            resultsArea.innerHTML = html;
        }
        
        function displayAnalysis(analysis) {
            hideLoading();
            const resultsArea = document.getElementById('resultsArea');
            
            let html = `
                <h5><i class="fas fa-search"></i> Анализ завершен</h5>
                <p><strong>Задача:</strong> ${analysis.task || 'Общий анализ'}</p>
                <p><strong>Тип кода:</strong> ${analysis.type}</p>
                <p><strong>Время анализа:</strong> ${new Date(analysis.timestamp).toLocaleString()}</p>
                
                <div class="row mb-3">
                    <div class="col-3">
                        <div class="text-center p-2 bg-light rounded">
                            <div class="h5">${analysis.stats.lines}</div>
                            <small>строк</small>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="text-center p-2 bg-light rounded">
                            <div class="h5">${analysis.stats.functions}</div>
                            <small>функций</small>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="text-center p-2 bg-light rounded">
                            <div class="h5">${analysis.stats.classes}</div>
                            <small>классов</small>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="text-center p-2 bg-light rounded">
                            <div class="h5">${analysis.stats.imports}</div>
                            <small>импортов</small>
                        </div>
                    </div>
                </div>
            `;
            
            if (analysis.suggestions.length > 0) {
                html += '<h6><i class="fas fa-lightbulb"></i> Рекомендации:</h6>';
                analysis.suggestions.forEach(s => {
                    html += `<div class="alert alert-warning">${s}</div>`;
                });
            }
            
            if (analysis.security_issues.length > 0) {
                html += '<h6><i class="fas fa-shield-alt"></i> Проблемы безопасности:</h6>';
                analysis.security_issues.forEach(issue => {
                    html += `<div class="alert alert-danger">${issue}</div>`;
                });
            }
            
            if (analysis.optimization_tips.length > 0) {
                html += '<h6><i class="fas fa-bolt"></i> Советы по оптимизации:</h6>';
                analysis.optimization_tips.forEach(tip => {
                    html += `<div class="alert alert-info">${tip}</div>`;
                });
            }
            
            resultsArea.innerHTML = html;
        }
        
        function copyToClipboard(button, elementId) {
            const codeElement = document.getElementById(elementId + '-code');
            if (codeElement) {
                const text = codeElement.textContent;
                navigator.clipboard.writeText(text).then(() => {
                    const originalText = button.innerHTML;
                    button.innerHTML = '<i class="fas fa-check"></i> Скопировано!';
                    setTimeout(() => {
                        button.innerHTML = originalText;
                    }, 2000);
                });
            }
        }
        
        function showLoading(message) {
            document.getElementById('resultsArea').innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">${message}</p>
                </div>
            `;
        }
        
        function hideLoading() {
            // Функция для скрытия загрузки
        }
        
        function showError(message) {
            document.getElementById('resultsArea').innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i> ${message}
                </div>
            `;
        }
        
        function escapeHtml(text) {
            const map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return text.replace(/[&<>"']/g, m => map[m]);
        }
    </script>
</body>
</html>
    ''')

@assistant_bp.route('/create_module', methods=['POST'])
def create_module():
    """Создание полного модуля"""
    data = request.json
    section = data.get('section', '')
    pages = data.get('pages', [])
    features = data.get('features', [])
    generation_type = data.get('type', 'full')
    
    if not section:
        return jsonify({"error": "Укажите название раздела"}), 400
    
    try:
        # Создаем модуль
        module = assistant.create_full_module(section, pages, features)
        
        # Возвращаем только запрошенные части
        result = {"section": section}
        
        if generation_type in ['full', 'route']:
            result["route_file"] = module["route_file"]
        
        if generation_type in ['full', 'template']:
            result["templates"] = module["templates"]
        
        if generation_type in ['full', 'javascript']:
            result["javascript"] = module["javascript"]
            result["css"] = module["css"]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Ошибка создания модуля: {str(e)}"}), 500

@assistant_bp.route('/analyze_code', methods=['POST'])
def analyze_code():
    """Анализ кода"""
    data = request.json
    code = data.get('code', '')
    task = data.get('task', 'Общий анализ')
    
    if not code:
        return jsonify({"error": "Код не предоставлен"}), 400
    
    try:
        analysis = assistant.analyze_existing_code(code, task)
        return jsonify({"analysis": analysis})
    except Exception as e:
        return jsonify({"error": f"Ошибка анализа: {str(e)}"}), 500
