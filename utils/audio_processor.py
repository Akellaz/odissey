import librosa
import librosa.display
import matplotlib.pyplot as plt
import os

def process_audio_file(file_path, output_path='static/foo.png'):
    """Обработка аудио файла и создание визуализации"""
    y, sr = librosa.load(file_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Audio Waveform')
    plt.savefig(output_path)
    
    return int(tempo)
