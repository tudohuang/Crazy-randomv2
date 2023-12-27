import customtkinter as ctk
import tkinter as tk
import random
import threading
import time
weighted_numbers = {}

#---------------------------------------------------------#
def set_weighted_numbers(numbers_str):
    global weighted_numbers
    try:
        pairs = numbers_str.split(',')
        weighted_numbers = {int(pair.split(':')[0]): int(pair.split(':')[1]) for pair in pairs}
        weighted_numbers_var.set("加權數字： " + ', '.join([f"{num}:{weight}" for num, weight in weighted_numbers.items()]))
    except ValueError:
        weighted_numbers_var.set("無效輸入")

def fade_in(window, step=10, speed=25):
    def update_alpha():
        nonlocal alpha
        alpha += step / 100
        window.attributes("-alpha", alpha)
        if alpha < 1:
            window.after(speed, update_alpha)

    alpha = window.attributes("-alpha")
    window.after(speed, update_alpha)

def start_fade_in(window):
    fade_thread = threading.Thread(target=fade_in, args=(window,))
    fade_thread.start()

def update_display(final_numbers, index=0, duration=500, interval=50):
    def format_number(num):
        """Adds a star next to 24."""
        return f"{num}★" if num == 24 else str(num)

    if index < len(final_numbers):
        end_time = time.time() + duration / 1000

        def update_spin():
            if time.time() < end_time:
                random_number = random.randint(min_value_var.get(), max_value_var.get())
                # Ensure all numbers are formatted as strings
                current_numbers = [format_number(n) for n in final_numbers[:index]] + [format_number(random_number)] + [format_number(n) for n in final_numbers[index + 1:]]
                result_var.set('，'.join(current_numbers))
                root.after(interval, update_spin)
            else:
                # Format the final number at the current index
                final_numbers[index] = format_number(final_numbers[index])
                formatted_final_numbers = [format_number(num) for num in final_numbers]
                result_var.set('，'.join(formatted_final_numbers))
                update_display(final_numbers, index + 1, duration, interval)

        update_spin()
    else:
        # Ensure the final display is formatted correctly
        formatted_numbers = [format_number(num) for num in final_numbers]
        result_var.set('，'.join(formatted_numbers))



# Function to generate random numbers
def generate_random_numbers():
    try:
        min_value = min_value_var.get()
        max_value = max_value_var.get()
        count = count_var.get()
    except ValueError:
        result_var.set("Invalid input! Please enter valid numbers.")
        return

    if min_value > max_value:
        result_var.set("Min value cannot be greater than Max value.")
        return

    weighted_pool = [num for num in range(min_value, max_value + 1) if num not in chosen_numbers]
    for num, weight in weighted_numbers.items():
        if min_value <= num <= max_value and num not in chosen_numbers:
            weighted_pool.extend([num] * (weight - 1))

    max_pool_size = 100000
    if len(weighted_pool) > max_pool_size:
        weighted_pool = random.sample(weighted_pool, max_pool_size)

    if count > len(weighted_pool):
        count = len(weighted_pool)

    new_numbers = random.sample(weighted_pool, count)
    
    # Add new numbers to chosen_numbers
    chosen_numbers.extend(new_numbers)

    update_display(new_numbers)
    update_chosen_menu()



def update_chosen_menu():
    menu_values = ['已選數字'] + sorted([str(num) for num in chosen_numbers])
    chosen_option_menu.configure(values=menu_values)
    chosen_option_var.set('已選數字')

def clear_all():
    chosen_numbers.clear()
    repeatable_numbers.clear()
    result_var.set("")
    update_chosen_menu()

def set_repeatable_numbers(numbers_str):
    global repeatable_numbers
    try:
        repeatable_numbers = list(map(int, numbers_str.split(',')))
        repeatable_numbers_var.set("可重複： " + '，'.join(map(str, repeatable_numbers)))
    except ValueError:
        repeatable_numbers_var.set("無效輸入")

def create_input_field(parent, label, variable, is_repeatable=False):
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(frame, text=label).pack(side=tk.LEFT)
    entry = ctk.CTkEntry(frame, textvariable=variable)
    entry.pack(side=tk.LEFT)
    if is_repeatable:
        button = ctk.CTkButton(frame, text="Setup", command=lambda: set_repeatable_numbers(entry.get()))
        button.pack(side=tk.LEFT)
    frame.pack(pady=8)


#---------------------------------------------------------#
large_font = ('Helvetica', 60)
root = ctk.CTk()
root.title('隨機數字產生器')
root.geometry('1200x1000')
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
min_value_var = tk.IntVar(value=1)
max_value_var = tk.IntVar(value=35)
count_var = tk.IntVar(value=1)
result_var = tk.StringVar()
chosen_numbers_var = tk.StringVar(value='已選數字')
repeatable_numbers_var = tk.StringVar(value='可重複數字')
weighted_numbers_var = tk.StringVar(value='加權數字')

chosen_numbers = []
repeatable_numbers = []
title_label = ctk.CTkLabel(root, text="🎲Random Number🎲", font=("Helvetica", 80, "bold")).pack(pady=30)

ctk.CTkLabel(root, textvariable=result_var,font=large_font).pack(pady=20)

create_input_field(root, "MIN：", min_value_var)
create_input_field(root, "MAX：", max_value_var)
create_input_field(root, "Count：", count_var)
create_input_field(root, "Repeatable(Split using ,)：", tk.StringVar(), is_repeatable=True)
create_input_field(root, "Weighted Numbers (e.g. 5:3,7:2)：", weighted_numbers_var, is_repeatable=True)

ctk.CTkButton(root, text='Generate', command=generate_random_numbers).pack(pady=10)
ctk.CTkButton(root, text='Clear', command=clear_all).pack(pady=10)

chosen_option_var = tk.StringVar(root)
chosen_option_menu = ctk.CTkOptionMenu(root, variable=chosen_option_var, values=['已選數字'])
chosen_option_menu.pack(pady=15)

root.attributes("-alpha", 0)
start_fade_in(root)  
print(weighted_numbers)
root.mainloop()
#---------------------------------------------------------#
