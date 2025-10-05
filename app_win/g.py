import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Угадай длительность ноты")

# Шрифты
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)

# Длительности нот
note_durations = {
    "whole": {"name": "Целая", "beats": 4},
    "half": {"name": "Половинная", "beats": 2},
    "quarter": {"name": "Четвертная", "beats": 1},
    "eighth": {"name": "Восьмая", "beats": 0.5},
    "sixteenth": {"name": "Шестнадцатая", "beats": 0.25}
}

# Список ключей для случайного выбора
note_keys = list(note_durations.keys())

# Переменные игры
current_note = None
options = []
correct_answer = None
message = ""
score = 0
total = 0

def new_question():
    global current_note, options, correct_answer
    current_note = random.choice(note_keys)
    correct_answer = note_durations[current_note]["name"]

    # Генерируем 4 варианта ответа
    options = random.sample(note_keys, 4)
    if current_note not in options:
        options[random.randint(0, 3)] = current_note

new_question()

# Основной цикл игры
running = True
while running:
    screen.fill(WHITE)

    # Отображение текущей ноты (визуально упрощено)
    note_text = font.render(f"Нота: {current_note}", True, BLACK)
    screen.blit(note_text, (50, 50))

    # Отображение вариантов ответа
    y_offset = 150
    for i, key in enumerate(options):
        text = small_font.render(f"{i+1}. {note_durations[key]['name']}", True, BLUE)
        screen.blit(text, (100, y_offset))
        y_offset += 50

    # Отображение результата
    result_text = small_font.render(message, True, GREEN if "Правильно" in message else RED)
    screen.blit(result_text, (50, 400))

    # Отображение счёта
    score_text = small_font.render(f"Счёт: {score}/{total}", True, BLACK)
    screen.blit(score_text, (50, 450))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                index = event.key - pygame.K_1
                if 0 <= index < len(options):
                    total += 1
                    selected = note_durations[options[index]]["name"]
                    if selected == correct_answer:
                        message = "Правильно!"
                        score += 1
                    else:
                        message = f"Неправильно! Это {correct_answer}"
                    pygame.time.delay(1000)
                    new_question()

pygame.quit()
