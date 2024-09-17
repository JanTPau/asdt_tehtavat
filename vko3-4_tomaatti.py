import tkinter as tk
from tkinter import Canvas, PhotoImage
import random
import math
import winsound

hit_count = {'ernest': 0, 'kernest': 0}

def update_hit_count_label():
    ernest_hit_count_label.config(text=f"Ernest Tomatoes Hit: {hit_count['ernest']}")
    kernest_hit_count_label.config(text=f"Kernest Tomatoes Hit: {hit_count['kernest']}")

def reset_hit_count():
    hit_count['ernest'] = 0
    hit_count['kernest'] = 0
    update_hit_count_label()

def move_ernest():
    global ernest_image
    x = window_width - 100
    y = random.randint(50, window_height - 150)
    
    if ernest_image is None:
        ernest_image = canvas.create_image(x, y, image=ernest_image_file)
    else:
        canvas.coords(ernest_image, x, y)

def move_kernest():
    global kernest_image
    x = 50
    y = random.randint(50, window_height - 150)
    
    if kernest_image is None:
        kernest_image = canvas.create_image(x, y, image=kernest_image_file)
    else:
        canvas.coords(kernest_image, x, y)

def throw_tomato(from_who):
    if from_who == "ernest" and ernest_image is None:
        print("Ernest is not placed yet!")
        return
    elif from_who == "kernest" and kernest_image is None:
        print("Kernest is not placed yet!")
        return

    if from_who == "ernest":
        from_x, from_y = canvas.coords(ernest_image)
        tomato = canvas.create_image(from_x, from_y, image=tomato_image_file)
        target_coords = canvas.coords(target_image)
        target_x, target_y = target_coords
        dx = (target_x - from_x) / 50
        dy = (target_y - from_y) / 50

    elif from_who == "kernest":
        from_x, from_y = canvas.coords(kernest_image)
        tomato = canvas.create_image(from_x, from_y, image=tomato_image_file)
        target_coords = canvas.coords(target_image)
        target_x, target_y = target_coords
        dx = (target_x - from_x) / 50
        dy = (target_y - from_y) / 50

    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def animate_tomato():
        nonlocal from_x, from_y
        distance_to_target = calculate_distance(from_x, from_y, target_x, target_y)
        if distance_to_target > 10:
            from_x += dx
            from_y += dy
            canvas.coords(tomato, from_x, from_y)
            canvas.after(20, animate_tomato)
        else:
            canvas.itemconfig(tomato, image=splat_image_file)
            if from_who == "ernest":
                hit_count['ernest'] += 1
            else:
                hit_count['kernest'] += 1
            update_hit_count_label()
            winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)

    animate_tomato()

def throw_tomato_between_characters():
    if hit_count['ernest'] >= hit_count['kernest'] + 2:
        print("Ernest throws a tomato at Kernest!")
        throw_between("ernest", "kernest")
    elif hit_count['kernest'] >= hit_count['ernest'] + 2:
        print("Kernest throws a tomato at Ernest!")
        throw_between("kernest", "ernest")

def throw_between(from_who, to_who):
    if from_who == "ernest" and ernest_image is None:
        print("Ernest is not placed yet!")
        return
    elif from_who == "kernest" and kernest_image is None:
        print("Kernest is not placed yet!")
        return

    if from_who == "ernest":
        from_x, from_y = canvas.coords(ernest_image)
        target_coords = canvas.coords(kernest_image)
    else:
        from_x, from_y = canvas.coords(kernest_image)
        target_coords = canvas.coords(ernest_image)

    target_x, target_y = target_coords
    dx = (target_x - from_x) / 50
    dy = (target_y - from_y) / 50
    tomato = canvas.create_image(from_x, from_y, image=tomato_image_file)

    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def animate_tomato():
        nonlocal from_x, from_y
        distance_to_target = calculate_distance(from_x, from_y, target_x, target_y)
        if distance_to_target > 10:
            from_x += dx
            from_y += dy
            canvas.coords(tomato, from_x, from_y)
            canvas.after(20, animate_tomato)
        else:
            canvas.itemconfig(tomato, image=splat_image_file)
        if from_who == "ernest":
            hit_count['ernest'] += 1
        else:
            winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
            print(f"{from_who} hit {to_who}!")

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
splat_image_file = PhotoImage(file="asdt_tehtavat/splat.png")


kernest_x = 50
kernest_y = random.randint(50, window_height - 150)
kernest_image = canvas.create_image(kernest_x, kernest_y, image=kernest_image_file)

target_x = window_width // 2
target_y = window_height // 2
target_image = canvas.create_image(target_x, target_y, image=target_image_file)

ernest_image = None

top_frame = tk.Frame(window)
top_frame.pack(side=tk.TOP, fill=tk.X)

kernest_hit_count_label = tk.Label(top_frame, text=f"Kernestin osumat: {hit_count['kernest']}", font=('Arial', 14))
kernest_hit_count_label.pack(side=tk.LEFT, padx=10)

ernest_hit_count_label = tk.Label(top_frame, text=f"Ernestin osumat: {hit_count['ernest']}", font=('Arial', 14))
ernest_hit_count_label.pack(side=tk.RIGHT, padx=10)

control_frame = tk.Frame(window)
control_frame.pack(side=tk.BOTTOM, fill=tk.X)

move_kernest_button = tk.Button(control_frame, text="Liikuta Kernestiä", command=move_kernest)
move_kernest_button.pack(side=tk.LEFT, padx=5, pady=5)

move_ernest_button = tk.Button(control_frame, text="Lisää ja liikuta Ernestiä", command=move_ernest)
move_ernest_button.pack(side=tk.LEFT, padx=5, pady=5)

throw_kernest_button = tk.Button(control_frame, text="Kernestin heitto", command=lambda: throw_tomato('kernest'))
throw_kernest_button.pack(side=tk.LEFT, padx=5, pady=5)

reset_button = tk.Button(control_frame, text="Reset", command=reset_hit_count)
reset_button.pack(side=tk.LEFT, padx=5, pady=5)

throw_between_button = tk.Button(control_frame, text="Rangaistuslaukaus", command=throw_tomato_between_characters)
throw_between_button.pack(side=tk.LEFT, padx=5, pady=5)

throw_button = tk.Button(control_frame, text="Ernestin heitto", command=lambda: throw_tomato('ernest'))
throw_button.pack(side=tk.RIGHT, padx=5, pady=5)

window.mainloop()
