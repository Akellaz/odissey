from flask import Blueprint, render_template, request, jsonify
import os
import json
import random
import sqlite3
from ipyleaflet import Map, GeoJSON
import sys


# Добавляем директорию app в путь поиска
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_path not in sys.path:
    sys.path.insert(0, app_path)

from utils.water_temperature import get_water_temperatures


sup_bp = Blueprint('sup', __name__)

# Инициализация карты
m = Map(center=(55.42901, 37.85339), zoom=7, scroll_wheel_zoom=True, double_click_zoom=True)

@sup_bp.route('/sup')
def sup():
    # Загружаем маршруты из БД
    connection = sqlite3.connect('routes.db')
    cursor = connection.cursor()
    cursor.execute('SELECT route_name, route_color FROM Routes')
    rsum = cursor.fetchall()
    connection.close()

    # Передаем пустые значения для температур (будут загружены по кнопке)
    return render_template('sup/sup.html', 
                         title='Сап-борд',
                         rsum=rsum,
                         t_moskva=None,
                         t_protva=None,
                         t_oka=None,
                         t_ugra=None)

@sup_bp.route('/get_water_temperature', methods=['POST'])
def get_water_temperature():
    """Endpoint для получения температуры воды по кнопке"""
    try:
        temperatures = get_water_temperatures()
        return jsonify({
            'success': True,
            'temperatures': temperatures
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Остальные ваши маршруты остаются без изменений...
@sup_bp.route('/upload_gpx', methods=['POST'])
def handle_file_upload_gpx():
    # ... ваш существующий код ...
    pass

@sup_bp.route('/upload_json', methods=['POST'])
def handle_file_upload_json():
    # ... ваш существующий код ...
    pass

# Страницы маршрутов
@sup_bp.route('/moscow.html')
def moscow():
    return render_template('sup/moscow.html', title='Москва')

@sup_bp.route('/istra.html')
def istra():
    return render_template('sup/istra.html', title='Истра')

@sup_bp.route('/nerskaya.html')
def nerskaya():
    return render_template('sup/nerskaya.html', title='Нерская')

@sup_bp.route('/desna.html')
def desna():
    return render_template('sup/desna.html', title='Десна')

@sup_bp.route('/oka.html')
def oka():
    return render_template('sup/oka.html', title='Ока')

@sup_bp.route('/sup_map_istra.html')
def sup_map_istra():
    return render_template('sup/sup_map_istra.html', title='Сап-карта Истра')

@sup_bp.route('/sup_map.html')
def sup_map():
    return render_template('sup/sup_map.html', title='Сап')

@sup_bp.route('/sup_del')
def sup_del():	
    return render_template('sup/sup.html', title='Одиссея')
