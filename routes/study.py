from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import sqlite3
import os

study_bp = Blueprint('study', __name__)

# Путь к базе данных
DB_PATH = 'study.db'

def get_db_connection():
    """Получение соединения с базой данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_study_db():
    """Инициализация базы данных для учебного сервиса"""
    conn = get_db_connection()
    
    # Создание таблиц, если они не существуют
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT,
                  phone TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS lessons
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER,
                  subject TEXT NOT NULL,
                  lesson_date DATE NOT NULL,
                  duration INTEGER NOT NULL,
                  price REAL NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (student_id) REFERENCES students (id))''')
    
    conn.commit()
    conn.close()

# Инициализация БД при импорте blueprint
init_study_db()

@study_bp.route('/study')
def index():
    """Главная страница учебного сервиса"""
    conn = get_db_connection()
    
    students_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    lessons_count = conn.execute("SELECT COUNT(*) FROM lessons").fetchone()[0]
    total_revenue = conn.execute("SELECT SUM(price) FROM lessons").fetchone()[0] or 0
    
    conn.close()
    
    return render_template('study/index.html', 
                         students_count=students_count,
                         lessons_count=lessons_count,
                         total_revenue=total_revenue)

@study_bp.route('/study/students')
def students():
    """Список учеников"""
    conn = get_db_connection()
    students_list = conn.execute("SELECT * FROM students ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template('study/students.html', students=students_list)

@study_bp.route('/study/students/add', methods=['GET', 'POST'])
def add_student():
    """Добавление ученика"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        if name:
            conn = get_db_connection()
            conn.execute("INSERT INTO students (name, email, phone) VALUES (?, ?, ?)",
                        (name, email, phone))
            conn.commit()
            conn.close()
            flash('Ученик успешно добавлен!', 'success')
            return redirect(url_for('study.students'))
        else:
            flash('Имя ученика обязательно!', 'error')
    
    return render_template('study/add_student.html')

@study_bp.route('/study/lessons')
def lessons():
    """Список занятий"""
    conn = get_db_connection()
    lessons_list = conn.execute('''SELECT l.*, s.name as student_name 
                                 FROM lessons l 
                                 JOIN students s ON l.student_id = s.id 
                                 ORDER BY l.lesson_date DESC''').fetchall()
    conn.close()
    return render_template('study/lessons.html', lessons=lessons_list)

@study_bp.route('/study/lessons/add', methods=['GET', 'POST'])
def add_lesson():
    """Добавление занятия"""
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject = request.form.get('subject')
        lesson_date = request.form.get('lesson_date')
        duration = request.form.get('duration')
        price = request.form.get('price')
        
        if all([student_id, subject, lesson_date, duration, price]):
            conn = get_db_connection()
            conn.execute('''INSERT INTO lessons (student_id, subject, lesson_date, duration, price) 
                         VALUES (?, ?, ?, ?, ?)''',
                        (student_id, subject, lesson_date, duration, price))
            conn.commit()
            conn.close()
            flash('Занятие успешно добавлено!', 'success')
            return redirect(url_for('study.lessons'))
        else:
            flash('Все поля обязательны!', 'error')
    
    conn = get_db_connection()
    students_list = conn.execute("SELECT id, name FROM students ORDER BY name").fetchall()
    conn.close()
    
    return render_template('study/add_lesson.html', students=students_list)

@study_bp.route('/study/finance')
def finance():
    """Финансовая статистика"""
    conn = get_db_connection()
    
    total_revenue = conn.execute("SELECT SUM(price) FROM lessons").fetchone()[0] or 0
    
    monthly_revenue = conn.execute('''SELECT strftime('%Y-%m', lesson_date) as month, SUM(price) as revenue
                                    FROM lessons 
                                    GROUP BY month 
                                    ORDER BY month DESC''').fetchall()
    
    student_revenue = conn.execute('''SELECT s.name, COUNT(l.id) as lesson_count, SUM(l.price) as total_price
                                    FROM students s 
                                    LEFT JOIN lessons l ON s.id = l.student_id 
                                    GROUP BY s.id, s.name 
                                    ORDER BY total_price DESC''').fetchall()
    
    conn.close()
    
    return render_template('study/finance.html', 
                         total_revenue=total_revenue,
                         monthly_revenue=monthly_revenue,
                         student_revenue=student_revenue)
