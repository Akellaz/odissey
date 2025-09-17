from flask import Flask, render_template, redirect, url_for, request, session
from bs4 import BeautifulSoup
import requests
import re
import os
import random
import sqlite3
#import librosa
#import librosa.display
#import matplotlib.pyplot as plt
import folium
import json
from ipyleaflet import Map, GeoJSON, AntPath
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book
import subprocess
import sys


app = Flask(__name__)
 
#  #FLASK_APP
# Подключаемся и создаем сессию базы данных
engine = create_engine('sqlite:///ak_data.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
#####

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#----Карта---
m = Map(center=(55.42901,37.85339), zoom=7, scroll_wheel_zoom=True, double_click_zoom=True)
 
                       
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')
'''
#----Music_Analize---
@app.route('/upload', methods=['POST'])
def handle_file_upload():
    
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file")
        
        for uploaded_file in uploaded_files:
            filename = uploaded_file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

    y, sr = librosa.load(file_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Audio Waveform')
    plt.savefig('static/foo.png')
    
    
    return render_template('mus_analize.html', title='Музыка | Успешно', source='static/foo.png', temp='Темп: '+str(int(tempo))+' BPM')
'''
#----GPX_TO_JSON---
@app.route('/upload_gpx', methods=['POST'])
def handle_file_upload_gpx():
    
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file")
        
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            uploaded_file.save(file_path)

    file_name = os.path.splitext(os.path.basename(file_name))
    file_name_gpx = file_name[0]+'.gpx'
    file_name_json = 'static/json/'+file_name[0]+'.json'

    with open(file_name_json, 'a') as f1:
        header='{"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"coordinates": ['
        f1.write(header + '\n')
    f1.close()

    word_lat = 'lat="(.*?)"'
    word_lon = 'lon="(.*?)"'  

    fd_lat = open(file_name_gpx,"r")
    fd_lon = open(file_name_gpx,"r")  
    file_contents_lat = re.findall(word_lat, fd_lat.read())
    file_contents_lon = re.findall(word_lon, fd_lon.read())

    lon_lat=[]

    for i in file_contents_lon:
        lon_lat.append('[ '+i+', ')
        for i in file_contents_lat:
            lon_lat.append(i+' ],')
            file_contents_lat.remove(i)
            break

    last=re.sub(r'\],', ']', lon_lat[-1])
    lon_lat[-1] = last

    lon_lat_count=len(lon_lat)
      
    with open(file_name_json, 'a') as f:
        for ix in range(lon_lat_count):
            f.write(lon_lat[ix] + '\n')
            
    f.close()

    with open(file_name_json, 'a') as f2:
        footer='], "type": "LineString"}}]}'
        f2.write(footer + '\n')
    f2.close()

    fd_lat.close() 
    fd_lon.close()   

    
    
    return render_template('sup/sup.html', title='Сап-борд | Успешно', link=file_name[0])

#----JSON_TO_MAP---
@app.route('/upload_json', methods=['POST'])
 
def handle_file_upload_json():

    connection = sqlite3.connect('routes.db')
    cursor = connection.cursor()
    
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file") 
        uploaded_title = request.form['rout_title']  
        uploaded_color = request.form['favcolor']
        
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            uploaded_file.save(file_path)
            
    #----В базу--
    cursor.execute('INSERT INTO Routes (route_name, route_path, route_color) VALUES (?, ?, ?)', (uploaded_title, file_path, uploaded_color))
    connection.commit()

    #----add_R--
    cursor.execute('SELECT * FROM Routes')

    for line in cursor.fetchall():
        Data = os.path.join(line[2])
        with open(Data, 'r') as f:
            data = json.load(f)
        def random_color(feature):
            return {
                'color': line[3],
                'fillColor': random.choice(['red', 'yellow', 'green', 'orange']),
            }
        geo_json = GeoJSON(
            data=data,
            style={
                'opacity': 1, 'dashArray': '9', 'fillOpacity': 0.1, 'weight': 5
            },
            hover_style={
                'color': 'white', 'dashArray': '0', 'fillOpacity': 0.5
            },
            style_callback=random_color
        )
        m.add(geo_json)
        
        
        
    connection.commit()
    connection.close()

    m.save("templates/sup/sup_map.html")    
    
    return render_template('sup/sup.html', title='Сап-борд | Успешно', line1=line[1], line2=line[2], line3=line[3])


@app.route('/')
@app.route('/index.html')
def index():	
    return render_template('index.html', title='Одиссея')

@app.route('/sup.html')
def sup():
#----Температура воды
    word = r'\+(\d+)°C'

    url_moskva='https://ru-meteo.com/temperatura-vody/reki/moskva'
    url_protva='https://ru-meteo.com/temperatura-vody/reki/protva'
    url_oka='https://ru-meteo.com/temperatura-vody/reki/oka'
    url_ugra='https://ru-meteo.com/temperatura-vody/reki/ugra'

    page_moskva = requests.get(url_moskva)
    soup_moskva = BeautifulSoup(page_moskva.text, "html.parser")
    result_moskva = soup_moskva.findAll('div', class_='bloc_one_days daybl_txt w-tomorrow__text')
    temp_moskva = re.findall(word, str(result_moskva))

    page_protva = requests.get(url_protva)
    soup_protva = BeautifulSoup(page_protva.text, "html.parser")
    result_protva = soup_protva.findAll('div', class_='bloc_one_days daybl_txt w-tomorrow__text')
    temp_protva = re.findall(word, str(result_protva))

    page_oka = requests.get(url_oka)
    soup_oka = BeautifulSoup(page_oka.text, "html.parser")
    result_oka = soup_oka.findAll('div', class_='bloc_one_days daybl_txt w-tomorrow__text')
    temp_oka = re.findall(word, str(result_oka))

    page_ugra = requests.get(url_ugra)
    soup_ugra = BeautifulSoup(page_ugra.text, "html.parser")
    result_ugra = soup_ugra.findAll('div', class_='bloc_one_days daybl_txt w-tomorrow__text')
    temp_ugra = re.findall(word, str(result_ugra))

#----Список маршрутов
    connection = sqlite3.connect('routes.db')
    cursor = connection.cursor()
    cursor.execute('SELECT route_name, route_color FROM Routes')
    rsum=[]

    for i in cursor.fetchall():
        rsum.append(i)

    return render_template('sup/sup.html', title='Сап-борд',rsum=rsum, t_moskva=temp_moskva[0], t_protva=temp_protva[0], t_oka=temp_oka[0], t_ugra=temp_ugra[0])


@app.route('/sup_del')
def sup_del():	
    
    connection = sqlite3.connect('routes.db')
    cursor = connection.cursor()
    cursor.execute('SELECT route_name, route_color FROM Routes')
    
    
    return render_template('sup/sup.html', title='Одиссея')


@app.route('/music.html')
def music():
    return render_template('music.html', title='Музыка')
'''
@app.route('/mus_analize.html')
def mus_analize():
    return render_template('mus_analize.html', title='Анализатор')
'''
@app.route('/right-sidebar.html')
def right_sidebar():
    return render_template('right-sidebar.html')


@app.route('/syldavia.html')
def syldavia():
    return render_template('syldavia.html', title='Syldavia Consulate')

@app.route('/tintin.html')
def tintin():
    return render_template('tintin.html', title='Tintin')

@app.route('/kroket.html')
def kroket():
    return render_template('kroket.html', title='Крокет')

@app.route('/moscow.html')
def moscow():
    return render_template('sup/moscow.html', title='Москва')

@app.route('/istra.html')
def istra():
    return render_template('sup/istra.html', title='Истра')

@app.route('/nerskaya.html')
def nerskaya():
    return render_template('sup/nerskaya.html', title='Нерская')

@app.route('/desna.html')
def desna():
    return render_template('sup/desna.html', title='Десна')

@app.route('/oka.html')
def oka():
    return render_template('sup/oka.html', title='Ока')

@app.route('/sup_12.html')
def sup_map_oka():
    return render_template('sup/sup_12.html', title='Сап-12')

@app.route('/sup_map_istra.html')
def sup_map_istra():
    return render_template('sup/sup_map_istra.html', title='Сап-карта Истра')

@app.route('/sup_map.html')
def sup_map():
    return render_template('sup/sup_map.html', title='Сап')

@app.route('/ak_bot')
def ak_bot():
     subprocess.Popen([sys.executable, 'ak_bot.py'], shell = True)
     return render_template("books.html")


# страница, которая будет отображать все книги в базе данных
# Эта функция работает в режиме чтения.
@app.route('/books')
def showBooks():
    books = session.query(Book).all()
    return render_template("books.html", books=books)


# Эта функция позволит создать новую книгу и сохранить ее в базе данных.
@app.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newBook = Book(name=request.form['name'], date=request.form['date'], time=request.form['time'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('showBooks'))
    else:
        return render_template('newBook.html')


# Эта функция позволит нам обновить книги и сохранить их в базе данных.
@app.route("/books/<int:book_id>/edit/", methods=['GET', 'POST'])
def editBook(book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBook.name = request.form['name']
            return redirect(url_for('showBooks'))
    else:
        return render_template('editBook.html', book=editedBook)


# Эта функция для удаления книг
@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        return redirect(url_for('showBooks', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)






if __name__ == "__main__":
    app.run(host='192.168.0.149', port=5000, debug=True)
