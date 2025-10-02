import librosa
import numpy as np

def extract_tonics(file_path):
    """
    Функция извлекает тоники аккордов из заданного аудиофайла.
    """
    # Загрузим звук
    y, sr = librosa.load(file_path)

    # Получим хромограмму (хроматический спектр), отражающую частоту появления каждой ноты
    chromagram = librosa.feature.chroma_stft(y=y, sr=sr)

    # Найдем самую громкую ("доминирующую") ноту в каждый временной отрезок
    dominant_notes = np.argmax(chromagram, axis=0)

    # Определим соответствующие ноты
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Переводим индексы доминирующих нот в музыкальные обозначения
    tonics = [notes[note_idx] for note_idx in dominant_notes]

    return tonics


# Пример использования
song_file = '1.mp3'  # укажите правильный путь к вашему файлу
tonic_sequence = extract_tonics(song_file)

# Выведем первые 10 обнаруженных тоник
print('Первые 10 тоник:', tonic_sequence[:100])