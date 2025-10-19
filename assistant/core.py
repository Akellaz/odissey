# assistant/core.py
import re
import os
from datetime import datetime
from pathlib import Path

class SuperDevAssistant:
    def __init__(self, project_root="."):
        self.project_root = project_root
        self.site_structure = {
            "main": "Главная страница и основные маршруты",
            "music": "Музыкальные инструменты и анализ",
            "sup": "SUP маршруты и карты",
            "books": "Библиотека и управление книгами",
            "study": "Учебная система и занятия",
            "admin": "Админ панель и управление"
        }
    
    def generate_route_file(self, section, features=[]):
        """Генерация route файла для раздела"""
        
        route_templates = {
            "music": self._music_route_template(),
            "sup": self._sup_route_template(),
            "books": self._books_route_template(),
            "study": self._study_route_template(),
            "admin": self._admin_route_template(),
            "custom": self._custom_route_template(section, features)
        }
        
        return route_templates.get(section, route_templates["custom"])
    
    def generate_template_file(self, section, page_name, features=[]):
        """Генерация HTML шаблона в стиле вашего сайта"""
        return self._verti_template(section, page_name, features)
    
    def generate_javascript(self, section, features=[]):
        """Генерация JavaScript кода"""
        return self._generic_js(section, features)
    
    def generate_css(self, section, features=[]):
        """Генерация CSS стилей"""
        return self._generic_css(section, features)
    
    def analyze_existing_code(self, code, task=""):
        """Анализ существующего кода"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "code_snippet": code[:300] + "..." if len(code) > 300 else code,
            "stats": self._get_code_stats(code),
            "suggestions": self._get_suggestions(code),
            "type": self._detect_code_type(code),
            "security_issues": self._check_security(code),
            "optimization_tips": self._get_optimization_tips(code)
        }
        return analysis
    
    def create_full_module(self, section, pages=[], features=[]):
        """Создание полного модуля (routes + templates + js + css)"""
        
        module = {
            "route_file": self.generate_route_file(section, features),
            "templates": {},
            "javascript": self.generate_javascript(section, features),
            "css": self.generate_css(section, features)
        }
        
        # Генерируем шаблоны для каждой страницы
        for page in pages:
            module["templates"][page] = self.generate_template_file(section, page, features)
        
        return module
    
    def _music_route_template(self):
        return '''from flask import Blueprint, render_template, request, jsonify
import os

music_bp = Blueprint('music', __name__)

@music_bp.route('/music')
def music_home():
    """Главная страница музыкального раздела"""
    return render_template('music/index.html', title='Музыка')

@music_bp.route('/music/analyzer')
def music_analyzer():
    """Анализатор музыки"""
    return render_template('music/analyzer.html', title='Анализ мулязыки')

@music_bp.route('/music/sequencer')
def sequencer():
    """Секвенсор"""
    return render_template('music/sequencer.html', title='Секвенсор')'''
    
    def _sup_route_template(self):
        return '''from flask import Blueprint, render_template, request, jsonify
import sqlite3

sup_bp = Blueprint('sup', __name__)

@sup_bp.route('/sup')
def sup_home():
    """Главная страница SUP раздела"""
    routes = get_all_routes()
    return render_template('sup/index.html', title='SUP Маршруты', routes=routes)

def get_all_routes():
    """Получение всех маршрутов из базы данных"""
    try:
        conn = sqlite3.connect('routes.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Routes')
        routes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return routes
    except Exception as e:
        print(f"Ошибка получения маршрутов: {e}")
        return []'''
    
    def _books_route_template(self):
        return '''from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3

books_bp = Blueprint('books', __name__)

@books_bp.route('/books')
def books_list():
    """Список книг"""
    books = get_all_books()
    return render_template('books/index.html', title='Библиотека', books=books)

def get_all_books():
    """Получение всех книг"""
    try:
        # Здесь ваш код для получения книг
        return []
    except Exception as e:
        print(f"Ошибка получения книг: {e}")
        return []'''
    
    def _study_route_template(self):
        return '''from flask import Blueprint, render_template, request, redirect, url_for, flash, session

study_bp = Blueprint('study', __name__)

@study_bp.route('/study')
def study_home():
    """Главная страница учебного раздела"""
    return render_template('study/index.html', title='Учебный кабинет')'''
    
    def _admin_route_template(self):
        return '''from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Вход в админ панель"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('admin/login.html', title='Вход в админ панель')'''
    
    def _custom_route_template(self, section, features):
        return f'''from flask import Blueprint, render_template, request, jsonify

{section}_bp = Blueprint('{section}', __name__)

@{section}_bp.route('/{section}')
def {section}_home():
    """Главная страница раздела {section}"""
    return render_template('{section}/index.html', title='{section.capitalize()}')'''
    
    def _verti_template(self, section, page_name, features):
        """Генерация шаблона в стиле Verti (ваш шаблон)"""
        
        page_titles = {
            "index": f"{section.capitalize()} - Главная",
            "list": f"{section.capitalize()} - Список",
            "detail": f"{section.capitalize()} - Детали",
            "create": f"{section.capitalize()} - Создать",
            "edit": f"{section.capitalize()} - Редактировать"
        }
        
        title = page_titles.get(page_name, f"{page_name.capitalize()} - {section.capitalize()}")
        
        # Определяем содержимое основной части
        content = self._get_page_content(section, page_name, features)
        
        return f'''<!DOCTYPE HTML>
<!--
	Verti by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>{title}</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="{{{{ url_for('static', filename='css/main.css') }}}}">
		<link rel="shortcut icon" href="{{{{ url_for('static', filename='favicon.ico') }}}}">
	</head>
	<body class="is-preload {'left-sidebar' if page_name in ['create', 'edit'] else 'right-sidebar' if page_name == 'detail' else 'homepage'}">
		<div id="page-wrapper">

			{{% include "includes/header.html" %}}

			<!-- Main -->
				<div id="main-wrapper">
					<div class="container">
						<div class="row gtr-200">
							<div class="col-4 col-12-medium">
								<div id="sidebar">

									<!-- Sidebar -->
										<section>
											<h3>Навигация</h3>
											<ul class="style2">
												<li><a href="{{{{ url_for('{section}.{section}_home') }}}}">Главная</a></li>
												<li><a href="#">Список</a></li>
												<li><a href="#">Создать</a></li>
											</ul>
										</section>

								</div>
							</div>
							<div class="col-8 col-12-medium imp-medium">
								<div id="content">

									<!-- Content -->
										<article>
											{content}
										</article>

								</div>
							</div>
						</div>
					</div>
				</div>

			<!-- Footer -->
				<div id="footer-wrapper">
					<footer id="footer" class="container">
						<div class="row">
							<div class="col-3 col-6-medium col-12-small">
								<section class="widget links">
									<h3>Полезные ссылки</h3>
									<ul class="style2">
										<li><a href="/">Главная</a></li>
										<li><a href="/music">Музыка</a></li>
										<li><a href="/sup">SUP</a></li>
										<li><a href="/books">Книги</a></li>
									</ul>
								</section>
							</div>
							<div class="col-3 col-6-medium col-12-small">
								<section class="widget links">
									<h3>Разделы</h3>
									<ul class="style2">
										<li><a href="/music">Музыка</a></li>
										<li><a href="/sup">SUP Маршруты</a></li>
										<li><a href="/study">Обучение</a></li>
										<li><a href="/admin">Админка</a></li>
									</ul>
								</section>
							</div>
							<div class="col-3 col-6-medium col-12-small">
								<section class="widget contact">
									<h3>Контакты</h3>
									<ul>
										<li><a href="#" class="icon brands fa-vk"><span class="label">VK</span></a></li>
										<li><a href="#" class="icon brands fa-telegram"><span class="label">Telegram</span></a></li>
										<li><a href="#" class="icon brands fa-whatsapp"><span class="label">WhatsApp</span></a></li>
									</ul>
									<p>Ваш адрес<br />
									Город, Страна<br />
									+7 (XXX) XXX-XXXX</p>
								</section>
							</div>
						</div>
						<div class="row">
							<div class="col-12">
								<div id="copyright">
									<ul class="menu">
										<li>&copy; Odissey. Все права защищены</li>
										<li>Design: <a href="http://html5up.net">HTML5 UP</a></li>
									</ul>
								</div>
							</div>
						</div>
					</footer>
				</div>

			</div>

		<!-- Scripts -->
			<script src="{{{{ url_for('static', filename='js/jquery.min.js') }}}}"></script>
			<script src="{{{{ url_for('static', filename='js/jquery.dropotron.min.js') }}}}"></script>
			<script src="{{{{ url_for('static', filename='js/browser.min.js') }}}}"></script>
			<script src="{{{{ url_for('static', filename='js/breakpoints.min.js') }}}}"></script>
			<script src="{{{{ url_for('static', filename='js/util.js') }}}}"></script>
			<script src="{{{{ url_for('static', filename='js/main.js') }}}}"></script>

	</body>
</html>'''
    
    def _get_page_content(self, section, page_name, features):
        """Генерация содержимого страницы"""
        
        if page_name == "index":
            return f'''
<h2><i class="fas fa-{self._get_section_icon(section)}"></i> {section.capitalize()} - Главная</h2>
<p>Добро пожаловать в раздел {section}!</p>

<div class="row">
    <div class="col-6 col-12-small">
        <section class="box feature">
            <h3>Основные функции</h3>
            <ul class="style2">
                <li>Просмотр списка</li>
                <li>Добавление новых элементов</li>
                <li>Редактирование</li>
                <li>Удаление</li>
            </ul>
        </section>
    </div>
    <div class="col-6 col-12-small">
        <section class="box feature">
            <h3>Статистика</h3>
            <p>Здесь будет отображаться статистика раздела.</p>
        </section>
    </div>
</div>'''
        
        elif page_name == "list":
            return f'''
<h2><i class="fas fa-list"></i> Список {section}</h2>

<div class="table-wrapper">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Дата создания</th>
                <th>Действия</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Пример элемента</td>
                <td>{{{{ now() }}}}</td>
                <td>
                    <a href="#" class="button small">Просмотр</a>
                    <a href="#" class="button small">Редактировать</a>
                </td>
            </tr>
        </tbody>
    </table>
</div>

<a href="{{{{ url_for('{section}.create_{section}') }}}}" class="button primary">
    <i class="fas fa-plus"></i> Добавить
</a>'''
        
        elif page_name == "create":
            return f'''
<h2><i class="fas fa-plus"></i> Создать {section}</h2>

<form method="POST" action="{{{{ url_for('{section}.create_{section}') }}}}">
    <div class="row gtr-uniform">
        <div class="col-12">
            <input type="text" name="name" placeholder="Название" required />
        </div>
        <div class="col-12">
            <textarea name="description" placeholder="Описание" rows="6"></textarea>
        </div>
        <div class="col-12">
            <ul class="actions">
                <li><input type="submit" class="primary" value="Создать" /></li>
                <li><input type="reset" value="Сброс" /></li>
                <li><a href="{{{{ url_for('{section}.{section}_home') }}}}" class="button">Отмена</a></li>
            </ul>
        </div>
    </div>
</form>'''
        
        else:
            return f'''
<h2><i class="fas fa-file-alt"></i> {page_name.capitalize()} {section}</h2>
<p>Содержимое страницы {page_name} раздела {section}.</p>

<section>
    <h3>Функции страницы</h3>
    <ul class="style2">
        {'</li><li>'.join([f"<li>{feature}</li>" for feature in features]) if features else '<li>Базовые функции</li>'}
    </ul>
</section>'''
    
    def _get_section_icon(self, section):
        """Получение иконки для раздела"""
        icons = {
            "music": "music",
            "sup": "water",
            "books": "book",
            "study": "graduation-cap",
            "admin": "cogs",
            "blog": "blog",
            "gallery": "images",
            "shop": "shopping-cart"
        }
        return icons.get(section, "cog")
    
    def _generic_js(self, section, features):
        return f'''// Функции для раздела {section}
$(document).ready(function() {{
    console.log('Модуль {section} загружен');
    
    // Общие функции для всех страниц раздела
    $('.{section}-form').on('submit', function(e) {{
        e.preventDefault();
        submit{section.capitalize()}Form($(this));
    }});
    
    // Функция для отправки формы
    function submit{section.capitalize()}Form(form) {{
        const formData = form.serialize();
        
        $.ajax({{
            url: form.attr('action'),
            method: 'POST',
            data: formData,
            success: function(response) {{
                showMessage('Данные успешно сохранены!', 'success');
            }},
            error: function(xhr, status, error) {{
                showMessage('Ошибка сохранения: ' + error, 'error');
            }}
        }});
    }}
    
    // Показ сообщений
    function showMessage(message, type) {{
        const alertClass = type === 'error' ? 'alert-danger' : 'alert-success';
        const alertHtml = `
            <div class="alert ${{alertClass}} alert-dismissible fade show" role="alert">
                ${{message}}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        $('#content').prepend(alertHtml);
        
        // Автоматическое скрытие через 5 секунд
        setTimeout(function() {{
            $('.alert').fadeOut();
        }}, 5000);
    }}
}});'''
    
    def _generic_css(self, section, features):
        return f'''/* Стили для раздела {section} */
.{section}-container {{
    margin: 20px 0;
}}

.{section}-header {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}}

.{section}-card {{
    transition: transform 0.2s;
    border: 1px solid #e0e0e0;
}}

.{section}-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}}

/* Формы */
.{section}-form input,
.{section}-form textarea {{
    margin-bottom: 15px;
}}

.{section}-form .button {{
    margin-right: 10px;
}}

/* Таблицы */
.table.{section}-table {{
    background: white;
    border-radius: 5px;
}}

.table.{section}-table th {{
    background: #f8f9fa;
}}

/* Адаптивность */
@media (max-width: 768px) {{
    .{section}-header {{
        padding: 15px;
    }}
    
    .{section}-container {{
        margin: 10px 0;
    }}
}}'''
    
    def _get_code_stats(self, code):
        lines = code.split('\n')
        return {
            "lines": len(lines),
            "characters": len(code),
            "functions": len(re.findall(r'(function|def|class)\s+\w+', code)),
            "comments": len(re.findall(r'(//|/\*|#|<!--)', code)),
            "classes": len(re.findall(r'class\s+\w+', code)),
            "imports": len(re.findall(r'(import|from|require)', code))
        }
    
    def _get_suggestions(self, code):
        suggestions = []
        
        # Проверка безопасности
        if 'eval(' in code:
            suggestions.append("❌ Опасно: использование eval() может быть уязвимостью")
        if 'exec(' in code:
            suggestions.append("❌ Опасно: использование exec() может быть уязвимостью")
        
        # Проверка лучших практик
        if 'var ' in code:
            suggestions.append("💡 Рекомендуется использовать let/const вместо var")
        if 'print(' in code and 'def ' in code:
            suggestions.append("📝 Найдены отладочные print() в Python коде")
        if 'console.log' in code:
            suggestions.append("📝 Найдены отладочные console.log в JavaScript")
        if 'TODO' in code.upper():
            suggestions.append("📋 Найдены задачи для выполнения (TODO)")
        
        # Проверка структуры
        if 'Flask' in code and '@app.route' not in code and 'Blueprint' not in code:
            suggestions.append("⚠️ Flask приложение должно использовать routes или Blueprint")
        
        return suggestions if suggestions else ["✅ Код следует лучшим практикам"]
    
    def _check_security(self, code):
        """Проверка на уязвимости"""
        issues = []
        
        dangerous_patterns = [
            (r'eval\s*\(', "Использование eval() - потенциальная уязвимость"),
            (r'exec\s*\(', "Использование exec() - потенциальная уязвимость"),
            (r'os\.system\s*\(', "Использование os.system() - потенциальная уязвимость"),
            (r'subprocess\.call\s*\(', "Использование subprocess.call() без проверки"),
            (r'password\s*=\s*["\'][^"\']*["\']', "Жестко закодированный пароль"),
            (r'secret\s*=\s*["\'][^"\']*["\']', "Жестко закодированный секрет"),
        ]
        
        for pattern, message in dangerous_patterns:
            if re.search(pattern, code):
                issues.append(f"⚠️ {message}")
        
        return issues
    
    def _get_optimization_tips(self, code):
        """Советы по оптимизации"""
        tips = []
        
        # Проверка на дублирование
        lines = code.split('\n')
        if len(lines) > 100:
            tips.append("📈 Код длинный - рассмотрите возможность разделения на модули")
        
        # Проверка на тяжелые операции
        if 'for.*for.*for' in code.replace(' ', '').replace('\n', ''):
            tips.append("⚡ Вложенные циклы - возможна оптимизация алгоритма")
        
        # Проверка на импорты
        if 'import.*import.*import.*import' in code.replace(' ', '').replace('\n', ''):
            tips.append("📦 Много импортов - рассмотрите группировку или ленивую загрузку")
        
        return tips
    
    def _detect_code_type(self, code):
        """Определение типа кода"""
        if 'from flask import' in code or 'import flask' in code:
            return "Flask Web Application"
        elif 'import librosa' in code:
            return "Audio Processing (Librosa)"
        elif 'import sqlite3' in code:
            return "Database (SQLite)"
        elif 'class.*Blueprint' in code.replace(' ', '').replace('\n', ''):
            return "Flask Blueprint"
        elif 'def.*route' in code.replace(' ', '').replace('\n', ''):
            return "Flask Routes"
        elif '<html' in code.lower():
            return "HTML Template"
        elif 'function' in code and '{' in code:
            return "JavaScript"
        elif 'def ' in code and ':' in code:
            return "Python"
        else:
            return "Unknown"
