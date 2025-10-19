from flask import Blueprint, render_template, request
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt


music_bp = Blueprint('music', __name__)


@music_bp.route('/music')
def music():
    return render_template('music.html', title='Музыка')


@music_bp.route('/seq')  
def seq():
    return render_template('music/seq.html', title='секвенция')

@music_bp.route('/drum_book')  
def drum_book():
    return render_template('music/drum_book.html', title='Drumgle Book')

@music_bp.route('/game')
def game():
    return render_template('/music/g.html')

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




