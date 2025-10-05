from flask import Blueprint, render_template, send_from_directory, request
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index.html')
def index():	
    return render_template('index.html', title='Одиссея')

@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main_bp.root_path, 'static'),
                              'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main_bp.route('/right-sidebar.html')
def right_sidebar():
    return render_template('right-sidebar.html')

@main_bp.route('/syldavia.html')
def syldavia():
    return render_template('syldavia.html', title='Syldavia Consulate')

@main_bp.route('/tintin.html')
def tintin():
    return render_template('tintin.html', title='Tintin')

@main_bp.route('/kroket.html')
def kroket():
    return render_template('kroket.html', title='Крокет')

@main_bp.route('/.well-known/acme-challenge/5MY6SAMpaOwCzMiG1sxvwjBgPreKnxtVIVYqV3HGoFs')
def certbot():
    return render_template('5MY6SAMpaOwCzMiG1sxvwjBgPreKnxtVIVYqV3HGoFs.html')
