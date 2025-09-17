import random
import tkinter as tk
from tkinter import ttk
import winsound

canvas_fon="#272727"
scores_color="#ffffff"

banch = []

def play_takt():
    
    note_tone=290
    
    note_dur_4=1000
    note_dur_8=500
    note_dur_16=250
    
#-----1-----
    if num1==4:
        winsound.Beep(note_tone, note_dur_4)
    elif num1==8:
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_8)
    elif num1==16:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
    elif num1==168:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_8)
    elif num1==816:
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
    elif num1==686:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_16)

#-----2-----
    if num2==4:
        winsound.Beep(note_tone, note_dur_4)
    elif num2==8:
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_8)
    elif num2==16:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
    elif num2==168:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_8)
    elif num2==816:
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
    elif num2==686:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_16)
#-----3-----
    if num3==4:
        winsound.Beep(note_tone, note_dur_4)
    elif num3==8:
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_8)
    elif num3==16:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
    elif num3==168:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_8)
    elif num3==816:
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
    elif num3==686:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_16)
#-----4-----
    if num4==4:
        winsound.Beep(note_tone, note_dur_4)
    elif num4==8:
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_8)
    elif num4==16:
        winsound.Beep(note_tone, 250)
        winsound.Beep(note_tone, 250)
        winsound.Beep(note_tone, 250)
        winsound.Beep(note_tone, 250)
    elif num4==168:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_8)
    elif num4==816:
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_16)
    elif num4==686:
        winsound.Beep(note_tone, note_dur_16)
        winsound.Beep(note_tone, note_dur_8)
        winsound.Beep(note_tone, note_dur_16)


def takt():
    global num1
    global num2
    global num3
    global num4
  
    if not banch:  
        print("Список пуст")
        num1=0
        num2=0
        num3=0
        num4=0

    else:
        num1=random.choice(banch)
        num2=random.choice(banch)
        num3=random.choice(banch)
        num4=random.choice(banch)


    
#----------Первая доля------------------
    
    canvas1 = tk.Canvas(root, width=250, height=200, bg=canvas_fon)

    if num1==4:
        canvas1.delete("all")
        canvas1.create_line(120, 20, 120, 160, width=3, fill=scores_color)
        canvas1.create_oval(60, 140, 120, 180, fill=scores_color)


    elif num1==8:
        canvas1.delete("all")
        canvas1.create_line(70, 20, 70, 160, width=3, fill=scores_color) #первая
        canvas1.create_oval(10, 140, 70, 180, fill=scores_color) 
        canvas1.create_line(170, 20, 170, 160, width=3, fill=scores_color)#вторая
        canvas1.create_oval(110, 140, 170, 180, fill=scores_color)
        canvas1.create_line(70, 25, 170, 25, width=10, fill=scores_color)#ребро

    elif num1==16:
        canvas1.delete("all")
        canvas1.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas1.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas1.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas1.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas1.create_line(171, 20, 171, 160, width=3, fill=scores_color)#третья
        canvas1.create_oval(116, 140, 171, 180, fill=scores_color)
        canvas1.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas1.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas1.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas1.create_line(57, 45, 228, 45, width=10, fill=scores_color)#ребро

    elif num1==168:
        canvas1.delete("all")
        canvas1.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas1.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas1.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas1.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas1.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas1.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas1.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas1.create_line(57, 45, 114, 45, width=10, fill=scores_color)#ребро

    elif num1==816:
        canvas1.delete("all")
        canvas1.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas1.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas1.create_line(171, 20, 171, 160, width=3, fill=scores_color)#третья
        canvas1.create_oval(116, 140, 171, 180, fill=scores_color)
        canvas1.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas1.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas1.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas1.create_line(171, 45, 228, 45, width=10, fill=scores_color)#ребро

    elif num1==686:
        canvas1.delete("all")
        canvas1.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas1.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas1.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas1.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas1.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas1.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas1.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро общее
        canvas1.create_line(57, 45, 87, 45, width=10, fill=scores_color)#ребро первое
        canvas1.create_line(200, 45, 228, 45, width=10, fill=scores_color)#ребро второе

        
    
    canvas1.grid(row=1, column=1)
#----------Вторая доля------------------

    
    canvas2 = tk.Canvas(root, width=250, height=200, bg=canvas_fon)

    if num2==4:
        canvas2.delete("all")
        canvas2.create_line(120, 20, 120, 160, width=3, fill=scores_color)
        canvas2.create_oval(60, 140, 120, 180, fill=scores_color)

        
    elif num2==8:
        canvas2.delete("all")
        canvas2.create_line(70, 20, 70, 160, width=3, fill=scores_color) #первая
        canvas2.create_oval(10, 140, 70, 180, fill=scores_color) 
        canvas2.create_line(170, 20, 170, 160, width=3, fill=scores_color)#вторая
        canvas2.create_oval(110, 140, 170, 180, fill=scores_color)
        canvas2.create_line(70, 25, 170, 25, width=10, fill=scores_color)#ребро

    elif num2==16:
        canvas2.delete("all")
        canvas2.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas2.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas2.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas2.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas2.create_line(171, 20, 171, 160, width=3, fill=scores_color)#третья
        canvas2.create_oval(116, 140, 171, 180, fill=scores_color)
        canvas2.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas2.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas2.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas2.create_line(57, 45, 228, 45, width=10, fill=scores_color)#ребро
        
    elif num2==168:
        canvas2.delete("all")
        canvas2.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas2.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas2.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas2.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas2.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas2.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas2.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas2.create_line(57, 45, 114, 45, width=10, fill=scores_color)#ребро

    elif num2==816:
        canvas2.delete("all")
        canvas2.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas2.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas2.create_line(171, 20, 171, 160, width=3, fill=scores_color)#третья
        canvas2.create_oval(116, 140, 171, 180, fill=scores_color)
        canvas2.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas2.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas2.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas2.create_line(171, 45, 228, 45, width=10, fill=scores_color)#ребро

    elif num2==686:
        canvas2.delete("all")
        canvas2.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas2.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas2.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas2.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas2.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas2.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas2.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро общее
        canvas2.create_line(57, 45, 87, 45, width=10, fill=scores_color)#ребро первое
        canvas2.create_line(200, 45, 228, 45, width=10, fill=scores_color)#ребро второе        
    
    canvas2.grid(row=1, column=2)
#----------Третья доля------------------

    canvas3 = tk.Canvas(root, width=250, height=200, bg=canvas_fon)

    if num3==4:
        canvas3.delete("all")
        canvas3.create_line(120, 20, 120, 160, width=3, fill=scores_color)
        canvas3.create_oval(60, 140, 120, 180, fill=scores_color)

    elif num3==8:
        canvas3.delete("all")
        canvas3.create_line(70, 20, 70, 160, width=3, fill=scores_color) #первая
        canvas3.create_oval(10, 140, 70, 180, fill=scores_color) 
        canvas3.create_line(170, 20, 170, 160, width=3, fill=scores_color)#вторая
        canvas3.create_oval(110, 140, 170, 180, fill=scores_color)
        canvas3.create_line(70, 25, 170, 25, width=10, fill=scores_color)#ребро

    elif num3==16:
        canvas3.delete("all")
        canvas3.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas3.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas3.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas3.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas3.create_line(171, 20, 171, 160, width=3, fill=scores_color)#третья
        canvas3.create_oval(116, 140, 171, 180, fill=scores_color)
        canvas3.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas3.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas3.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas3.create_line(57, 45, 228, 45, width=10, fill=scores_color)#ребро

    elif num3==168:
        canvas3.delete("all")
        canvas3.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas3.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas3.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas3.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas3.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas3.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas3.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas3.create_line(57, 45, 114, 45, width=10, fill=scores_color)#ребро

    elif num3==816:
        canvas3.delete("all")
        canvas3.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas3.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas3.create_line(171, 20, 171, 160, width=3, fill=scores_color)#третья
        canvas3.create_oval(116, 140, 171, 180, fill=scores_color)
        canvas3.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas3.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas3.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas3.create_line(171, 45, 228, 45, width=10, fill=scores_color)#ребро

    elif num3==686:
        canvas3.delete("all")
        canvas3.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas3.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas3.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas3.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas3.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas3.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas3.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро общее
        canvas3.create_line(57, 45, 87, 45, width=10, fill=scores_color)#ребро первое
        canvas3.create_line(200, 45, 228, 45, width=10, fill=scores_color)#ребро второе  

    canvas3.grid(row=1, column=3)
#----------Четвёртая доля------------------

    canvas4 = tk.Canvas(root, width=250, height=200, bg=canvas_fon)

    if num4==4:
        canvas4.delete("all")
        canvas4.create_line(120, 20, 120, 160, width=3, fill=scores_color)
        canvas4.create_oval(60, 140, 120, 180, fill=scores_color)

    elif num4==8:
        canvas4.delete("all")
        canvas4.create_line(70, 20, 70, 160, width=3, fill=scores_color) #первая
        canvas4.create_oval(10, 140, 70, 180, fill=scores_color) 
        canvas4.create_line(170, 20, 170, 160, width=3, fill=scores_color)#вторая
        canvas4.create_oval(110, 140, 170, 180, fill=scores_color)
        canvas4.create_line(70, 25, 170, 25, width=10, fill=scores_color)#ребро
    
    elif num4==16:
        canvas4.delete("all")
        canvas4.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas4.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas4.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas4.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas4.create_line(171, 20, 171, 160, width=3, fill=scores_color)#третья
        canvas4.create_oval(116, 140, 171, 180, fill=scores_color)
        canvas4.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas4.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas4.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas4.create_line(57, 45, 228, 45, width=10, fill=scores_color)#ребро

    elif num4==168:
        canvas4.delete("all")
        canvas4.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas4.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas4.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas4.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas4.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas4.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas4.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas4.create_line(57, 45, 114, 45, width=10, fill=scores_color)#ребро

    elif num4==816:
        canvas4.delete("all")
        canvas4.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas4.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas4.create_line(171, 20, 171, 160, width=3, fill=scores_color)#третья
        canvas4.create_oval(116, 140, 171, 180, fill=scores_color)
        canvas4.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas4.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas4.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро
        canvas4.create_line(171, 45, 228, 45, width=10, fill=scores_color)#ребро

    elif num4==686:
        canvas4.delete("all")
        canvas4.create_line(57, 20, 57, 160, width=3, fill=scores_color) #первая
        canvas4.create_oval(2, 140, 57, 180, fill=scores_color)
        canvas4.create_line(114, 20, 114, 160, width=3, fill=scores_color) #вторя
        canvas4.create_oval(59, 140, 114, 180, fill=scores_color)
        canvas4.create_line(228, 20, 228, 160, width=3, fill=scores_color)#четвёртая
        canvas4.create_oval(173, 140, 228, 180, fill=scores_color)
        canvas4.create_line(57, 25, 228, 25, width=10, fill=scores_color)#ребро общее
        canvas4.create_line(57, 45, 87, 45, width=10, fill=scores_color)#ребро первое
        canvas4.create_line(200, 45, 228, 45, width=10, fill=scores_color)#ребро второе  
   
    canvas4.grid(row=1, column=4)


    
root = tk.Tk()  
root.title("drumz")  
root.geometry("1000x300")


var4 = tk.IntVar()
var8 = tk.IntVar()
var16 = tk.IntVar()
var168 = tk.IntVar()
var816 = tk.IntVar()
var686 = tk.IntVar()


def on_button_toggle():
    global banch
    banch = []
    if var4.get() == 1:
        banch.append(4)

    if var8.get() == 1:
        banch.append(8)

    if var16.get() == 1:
        banch.append(16)

    if var168.get() == 1:
        banch.append(168)

    if var816.get() == 1:
        banch.append(816)

    if var686.get() == 1:
        banch.append(686)

        
#-----Пустые доли----
canvas1 = tk.Canvas(root, width=250, height=200, bg=canvas_fon)
canvas1.grid(row=1, column=1)

canvas2 = tk.Canvas(root, width=250, height=200, bg=canvas_fon)
canvas2.grid(row=1, column=2)

canvas3 = tk.Canvas(root, width=250, height=200, bg=canvas_fon)
canvas3.grid(row=1, column=3)

canvas4 = tk.Canvas(root, width=250, height=200, bg=canvas_fon)
canvas4.grid(row=1, column=4)


#-----Go и PLAY----
btn = ttk.Button(root, text="Go", command=takt)
btn.grid(row=2, column=1, columnspan=4)

btn_play = ttk.Button(root, text="Play", command=play_takt)
btn_play.grid(row=5, column=1, columnspan=4)

#-----Группы нот-----
btnCheck4 = ttk.Checkbutton(root, text="4", variable=var4, onvalue=1, offvalue=0, command=on_button_toggle)
btnCheck8 = ttk.Checkbutton(root, text="8", variable=var8, onvalue=1, offvalue=0, command=on_button_toggle)
btnCheck16 = ttk.Checkbutton(root, text="16", variable=var16, onvalue=1, offvalue=0, command=on_button_toggle)
btnCheck168 = ttk.Checkbutton(root, text="16-16-8", variable=var168, onvalue=1, offvalue=0, command=on_button_toggle)
btnCheck816 = ttk.Checkbutton(root, text="8-16-16", variable=var816, onvalue=1, offvalue=0, command=on_button_toggle)
btnCheck686 = ttk.Checkbutton(root, text="16-8-16", variable=var686, onvalue=1, offvalue=0, command=on_button_toggle)

btnCheck4.grid(row=3, column=1)
btnCheck8.grid(row=3, column=2)
btnCheck16.grid(row=3, column=3)
btnCheck168.grid(row=4, column=1)
btnCheck816.grid(row=4, column=2)
btnCheck686.grid(row=4, column=3)


root.mainloop()


