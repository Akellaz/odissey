from flask import Blueprint, render_template, jsonify, request
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import json

music_bp = Blueprint('music', __name__)

# Хранилище паттернов
patterns_storage = {}

@music_bp.route('/')
def music_index():
    return render_template('music/drum.html', title='Музыка')

@music_bp.route('/drum')  # Это будет доступно как /music/drum
def drum_sequencer():
    return render_template('music/drum.html', title='Барабанная секвенция')

@music_bp.route('/test')  # Добавим тестовый маршрут
def test():
    return "Music blueprint работает!"

# API маршруты
@music_bp.route('/api/drum/patterns', methods=['GET'])
def get_drum_patterns():
    return jsonify(list(patterns_storage.keys()))

@music_bp.route('/api/drum/pattern/<name>', methods=['GET'])
def get_drum_pattern(name):
    pattern = patterns_storage.get(name)
    if pattern:
        return jsonify(pattern)
    return jsonify({'error': 'Pattern not found'}), 404

@music_bp.route('/api/drum/pattern/<name>', methods=['POST'])
def save_drum_pattern(name):
    try:
        data = request.get_json()
        patterns_storage[name] = data
        return jsonify({'status': 'saved', 'name': name})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@music_bp.route('/api/drum/pattern/<name>', methods=['DELETE'])
def delete_drum_pattern(name):
    if name in patterns_storage:
        del patterns_storage[name]
        return jsonify({'status': 'deleted'})
    return jsonify({'error': 'Pattern not found'}), 404

@music_bp.route('/music')
def music():
    return render_template('music.html', title='Музыка')

@music_bp.route('/mus_analize.html')
def mus_analize():
    return render_template('mus_analize.html', title='Анализатор')

@music_bp.route('/upload', methods=['POST'])
def handle_file_upload():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file")
        
        for uploaded_file in uploaded_files:
            filename = uploaded_file.filename
            file_path = os.path.join(music_bp.root_path, '..', 'uploads', filename)
            uploaded_file.save(file_path)

    y, sr = librosa.load(file_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Audio Waveform')
    plt.savefig('static/foo.png')
    
    return render_template('mus_analize.html', 
                         title='Музыка | Успешно', 
                         source='static/foo.png', 
                         temp='Темп: '+str(int(tempo))+' BPM')
