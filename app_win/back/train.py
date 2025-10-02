import tkinter as tk
from random import choice

# Размеры окна и элементов интерфейса
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
CELL_SIZE = WINDOW_WIDTH // 2  # Ячейки будут квадратными

def draw_note(canvas, note_type):
    """Рисует соответствующую фигуру для заданного типа ноты."""
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2
    
    if note_type == 'quarter':
        radius = CELL_SIZE * 0.2
        canvas.create_oval(center_x-radius, center_y-radius,
                           center_x+radius, center_y+radius, fill='black')
        
    elif note_type == 'eighth':
        radius = CELL_SIZE * 0.15
        stem_length = CELL_SIZE * 0.3
        canvas.create_oval(center_x-radius, center_y-radius,
                           center_x+radius, center_y+radius, fill='black')
        canvas.create_line(center_x, center_y + radius, center_x, center_y + radius + stem_length)
        
    elif note_type == 'sixteenth':
        radius = CELL_SIZE * 0.1
        stem_length = CELL_SIZE * 0.4
        flag_radius = CELL_SIZE * 0.05
        canvas.create_oval(center_x-radius, center_y-radius,
                           center_x+radius, center_y+radius, fill='black')
        canvas.create_line(center_x, center_y + radius, center_x, center_y + radius + stem_length)
        canvas.create_arc(center_x-flag_radius*2, center_y+radius+stem_length-flag_radius*2,
                         center_x+flag_radius*2, center_y+radius+stem_length+flag_radius*2,
                         start=0, extent=-180, style="arc")

def generate_random_notes():
    """Генерирует случайные ноты в каждой ячейке"""
    for i in range(len(canvases)):
        canvases[i].delete("all")  # Очищаем предыдущее изображение
        note_type = choice(['quarter', 'eighth', 'sixteenth'])
        draw_note(canvases[i], note_type)

root = tk.Tk()
root.title('Нотный генератор')

# Устанавливаем размеры окна
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

canvases = []
for row in range(2):  # Два ряда клеток
    for col in range(2):  # Две клетки в ряду
        frame = tk.Frame(root, width=CELL_SIZE, height=CELL_SIZE, bg='white', relief='solid', borderwidth=1)
        frame.grid(row=row, column=col, padx=10, pady=10)
        
        canvas = tk.Canvas(frame, width=CELL_SIZE, height=CELL_SIZE, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvases.append(canvas)

start_button = tk.Button(root, text="Старт", command=generate_random_notes)
start_button.grid(row=2, columnspan=2, pady=20)

root.mainloop()
