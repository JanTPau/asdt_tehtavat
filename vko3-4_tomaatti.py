import tkinter as tk
from tkinter import Canvas, PhotoImage
import random
import math
import winsound

hit_count = {'tomatoes': 0}

def update_hit_count_label():
    hit_count_label.config(text=f"Tomatoes Hit: {hit_count['tomatoes']}")

def reset_hit_count():
    hit_count['tomatoes'] = 0
    update_hit_count_label()

def move_ernest():
    global ernest_image
    x = window_width - 100
    y = random.randint(50, window_height - 150)
    
    if ernest_image is None:
        ernest_image = canvas.create_image(x, y, image=ernest_image_file)
    else:
        canvas.coords(ernest_image, x, y)

def throw_tomato():
    if ernest_image is None:
        print("Ernest is not placed yet!")
        return

    ernest_x, ernest_y = canvas.coords(ernest_image)
    tomato = canvas.create_image(ernest_x, ernest_y, image=tomato_image_file)
    target_coords = canvas.coords(target_image)
    target_x, target_y = target_coords
    dx = (target_x - ernest_x) / 50
    dy = (target_y - ernest_y) / 50

    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def animate_tomato():
        nonlocal ernest_x, ernest_y
        distance_to_target = calculate_distance(ernest_x, ernest_y, target_x, target_y)
        
        if distance_to_target > 10:
            ernest_x += dx
            ernest_y += dy
            canvas.coords(tomato, ernest_x, ernest_y)
            canvas.after(20, animate_tomato)
        else:
            print("Tomato has reached the center of the target!")
            hit_count['tomatoes'] += 1
            update_hit_count_label()
            winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)

    animate_tomato()

window = tk.Tk()
window.title("Tomaatin Heitto")
window_width = 800
window_height = 600
window.geometry(f"{window_width}x{window_height}")
canvas = Canvas(window, width=window_width, height=window_height)
canvas.pack()

kernest_image_file = PhotoImage(file="asdt_tehtavat/kerne.png")
ernest_image_file = PhotoImage(file="asdt_tehtavat/erne.png")
target_image_file = PhotoImage(file="asdt_tehtavat/maalitaulu.png")
tomato_image_file = PhotoImage(file="asdt_tehtavat/tomaatti.png")

kernest_x = 50
kernest_y = random.randint(50, window_height - 150)
kernest_image = canvas.create_image(kernest_x, kernest_y, image=kernest_image_file)

target_x = window_width // 2
target_y = window_height // 2
target_image = canvas.create_image(target_x, target_y, image=target_image_file)

ernest_image = None

hit_count_label = tk.Label(window, text=f"Tomatoes Hit: {hit_count['tomatoes']}", font=('Arial', 14))
hit_count_label.pack(side=tk.TOP)

move_button = tk.Button(window, text="Move Ernest", command=move_ernest)
move_button.pack(side=tk.LEFT)

throw_button = tk.Button(window, text="Throw Tomato", command=throw_tomato)
throw_button.pack(side=tk.RIGHT)

reset_button = tk.Button(window, text="Reset Counter", command=reset_hit_count)
reset_button.pack(side=tk.TOP)

window.mainloop()
