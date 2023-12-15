import tkinter as tk
import random

def generate_random_numbers():
    min_value = min_value_var.get()
    max_value = max_value_var.get()
    count = count_var.get()
    exclude_list = chosen_numbers

    available_numbers = set(range(min_value, max_value + 1)) - set(exclude_list)
    if count > len(available_numbers):
        result_var.set("Error: Too many numbers requested.")
        return

    new_numbers = random.sample(available_numbers, count)
    chosen_numbers.extend(new_numbers)
    update_display()

def update_display():
    result_var.set(', '.join(map(str, chosen_numbers)))
    chosen_numbers_var.set(f'Chosen Numbers: {len(chosen_numbers)}')

def clear_all():
    chosen_numbers.clear()
    update_display()

def create_input_field(parent, label, variable):
    frame = tk.Frame(parent)
    tk.Label(frame, text=label, font=label_font).pack(side=tk.LEFT)
    tk.Entry(frame, textvariable=variable, font=entry_font).pack(side=tk.LEFT)
    frame.pack(pady=5)

root = tk.Tk()
root.title('Random Number Generator')
root.geometry('400x300')

# Styling
label_font = ('Arial', 12)
entry_font = ('Arial', 12)
button_font = ('Arial', 12, 'bold')

# Variables
min_value_var = tk.IntVar(value=1)
max_value_var = tk.IntVar(value=100)
count_var = tk.IntVar(value=1)
result_var = tk.StringVar()
chosen_numbers_var = tk.StringVar()
chosen_numbers = []

# UI Elements
create_input_field(root, "Min Value:", min_value_var)
create_input_field(root, "Max Value:", max_value_var)
create_input_field(root, "Count:", count_var)

tk.Button(root, text='Generate', font=button_font, command=generate_random_numbers).pack(pady=10)
tk.Button(root, text='Clear', font=button_font, command=clear_all).pack(pady=10)

tk.Label(root, textvariable=result_var, font=label_font, fg='blue').pack(pady=10)
tk.Label(root, textvariable=chosen_numbers_var, font=label_font, fg='green').pack(pady=10)

root.mainloop()
