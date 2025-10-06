from flask import Blueprint, render_template, redirect, url_for, flash, request, session
import sqlite3
from datetime import datetime

admin_bp = Blueprint('admin_routes', __name__, url_prefix='/admin')

# Простая проверка авторизации
def is_admin():
    return session.get('admin_logged_in', False)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not is_admin():
            return redirect(url_for('admin_routes.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Страница входа
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        # В продакшене используйте безопасное хранение паролей!
        if password == 'admin123':  # Простой пароль для тестирования
            session['admin_logged_in'] = True
            return redirect(url_for('admin_routes.dashboard'))
        else:
            flash('Неверный пароль!', 'error')
    
    return render_template('admin/login.html')

# Выход
@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_routes.login'))

# Дашборд админки
# Замените существующую функцию dashboard на эту:

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Статистика по учебному сервису
    try:
        conn = sqlite3.connect('study.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        students_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM lessons")
        lessons_count = cursor.fetchone()[0]
        # Общая прибыль для дашборда
        cursor.execute("SELECT SUM(price) FROM lessons")
        total_revenue = cursor.fetchone()[0] or 0
        # Прибыль по месяцам для дашборда
        cursor.execute('''SELECT strftime('%Y-%m', lesson_date) as month, SUM(price) as revenue
                        FROM lessons 
                        GROUP BY month 
                        ORDER BY month DESC
                        LIMIT 5''')
        monthly_revenue = cursor.fetchall()
        conn.close()
    except:
        students_count = 0
        lessons_count = 0
        total_revenue = 0
        monthly_revenue = []
    
    # Статистика по бронированиям
    try:
        conn = sqlite3.connect('ak_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM book")
        bookings_count = cursor.fetchone()[0]
        conn.close()
    except:
        bookings_count = 0
    
    return render_template('admin/dashboard.html', 
                         students_count=students_count,
                         lessons_count=lessons_count,
                         bookings_count=bookings_count,
                         total_revenue=total_revenue,
                         monthly_revenue=monthly_revenue)


# === УЧЕБНЫЙ СЕРВИС ===

# Список учеников
@admin_bp.route('/students')
@admin_required
def students():
    try:
        conn = sqlite3.connect('study.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY created_at DESC")
        students = cursor.fetchall()
        conn.close()
    except Exception as e:
        students = []
        flash(f'Ошибка загрузки учеников: {str(e)}', 'error')
    
    return render_template('admin/students.html', students=students)

# Добавление ученика
@admin_bp.route('/students/add', methods=['GET', 'POST'])
@admin_required
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        if name:
            try:
                conn = sqlite3.connect('study.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students (name, email, phone) VALUES (?, ?, ?)",
                             (name, email, phone))
                conn.commit()
                conn.close()
                flash('Ученик успешно добавлен!', 'success')
                return redirect(url_for('admin_routes.students'))
            except Exception as e:
                flash(f'Ошибка добавления ученика: {str(e)}', 'error')
        else:
            flash('Имя ученика обязательно!', 'error')
    
    return render_template('admin/add_student.html')

# Удаление ученика
@admin_bp.route('/students/delete/<int:student_id>')
@admin_required
def delete_student(student_id):
    try:
        conn = sqlite3.connect('study.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        flash('Ученик удален!', 'success')
    except Exception as e:
        flash(f'Ошибка удаления ученика: {str(e)}', 'error')
    
    return redirect(url_for('admin_routes.students'))

# Список занятий
@admin_bp.route('/lessons')
@admin_required
def lessons():
    try:
        conn = sqlite3.connect('study.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT l.*, s.name as student_name 
                         FROM lessons l 
                         JOIN students s ON l.student_id = s.id 
                         ORDER BY l.lesson_date DESC''')
        lessons = cursor.fetchall()
        conn.close()
    except Exception as e:
        lessons = []
        flash(f'Ошибка загрузки занятий: {str(e)}', 'error')
    
    return render_template('admin/lessons.html', lessons=lessons)

# Добавление занятия
@admin_bp.route('/lessons/add', methods=['GET', 'POST'])
@admin_required
def add_lesson():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject = request.form.get('subject')
        lesson_date = request.form.get('lesson_date')
        duration = request.form.get('duration')
        price = request.form.get('price')
        
        if all([student_id, subject, lesson_date, duration, price]):
            try:
                conn = sqlite3.connect('study.db')
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO lessons (student_id, subject, lesson_date, duration, price) 
                                 VALUES (?, ?, ?, ?, ?)''',
                             (student_id, subject, lesson_date, duration, price))
                conn.commit()
                conn.close()
                flash('Занятие успешно добавлено!', 'success')
                return redirect(url_for('admin_routes.lessons'))
            except Exception as e:
                flash(f'Ошибка добавления занятия: {str(e)}', 'error')
        else:
            flash('Все поля обязательны!', 'error')
    
    # Получаем список учеников
    try:
        conn = sqlite3.connect('study.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM students ORDER BY name")
        students = cursor.fetchall()
        conn.close()
    except:
        students = []
    
    return render_template('admin/add_lesson.html', students=students)

# === БРОНИРОВАНИЯ ===

@admin_bp.route('/bookings')
@admin_required
def bookings():
    try:
        conn = sqlite3.connect('ak_data.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM book ORDER BY date DESC, time DESC')
        bookings = cursor.fetchall()
        conn.close()
    except Exception as e:
        bookings = []
        flash(f'Ошибка загрузки бронирований: {str(e)}', 'error')
    
    return render_template('admin/bookings.html', bookings=bookings)

# === SUP МАРШРУТЫ ===

@admin_bp.route('/routes')
@admin_required
def routes():
    try:
        conn = sqlite3.connect('routes.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Routes')
        routes = cursor.fetchall()
        conn.close()
    except Exception as e:
        routes = []
        flash(f'Ошибка загрузки маршрутов: {str(e)}', 'error')
    
    return render_template('admin/routes.html', routes=routes)

# Добавьте этот код в конец файла, перед последней строкой

# === ФИНАНСОВАЯ СТАТИСТИКА ===

@admin_bp.route('/finance')
@admin_required
def finance():
    try:
        conn = sqlite3.connect('study.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Общая прибыль
        cursor.execute("SELECT SUM(price) FROM lessons")
        total_revenue = cursor.fetchone()[0] or 0
        
        # Прибыль по месяцам
        cursor.execute('''SELECT strftime('%Y-%m', lesson_date) as month, SUM(price) as revenue
                        FROM lessons 
                        GROUP BY month 
                        ORDER BY month DESC
                        LIMIT 12''')
        monthly_revenue = cursor.fetchall()
        
        # Прибыль по ученикам
        cursor.execute('''SELECT s.name, COUNT(l.id) as lesson_count, SUM(l.price) as total_price
                        FROM students s 
                        LEFT JOIN lessons l ON s.id = l.student_id 
                        GROUP BY s.id, s.name 
                        ORDER BY total_price DESC NULLS LAST''')
        student_revenue = cursor.fetchall()
        
        conn.close()
    except Exception as e:
        total_revenue = 0
        monthly_revenue = []
        student_revenue = []
        flash(f'Ошибка загрузки финансовой статистики: {str(e)}', 'error')
    
    return render_template('admin/finance.html', 
                         total_revenue=total_revenue,
                         monthly_revenue=monthly_revenue,
                         student_revenue=student_revenue)
