import tkinter as tk
import random

def random_number_generator(min_value, max_value, count, exclude_list):
    available_numbers = set(range(min_value, max_value + 1)) - set(exclude_list)
    if count > len(available_numbers):
        result_var.set("Error: Too many numbers requested.")
        return

    chosen_numbers = random.sample(available_numbers, count)
    chosen_list.extend(chosen_numbers)  # Add to the global chosen list
    result_var.set(', '.join(map(str, chosen_numbers)))

def clear_fields():
    min_value_var.set(0)
    max_value_var.set(0)
    count_var.set(0)
    result_var.set('')

def clear_chosen_list():
    chosen_list.clear()
    chosen_list_var.set('Chosen List Cleared')

root = tk.Tk()
root.title('隨機選號器')
root.geometry('400x500')  # Adjusted size

# Styling
label_font = ('Arial', 14)
entry_font = ('Arial', 14)
button_font = ('Arial', 14, 'bold')

# Result and chosen list labels
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=label_font, fg='blue')
result_label.pack(pady=10)

chosen_list_var = tk.StringVar()
chosen_list_label = tk.Label(root, textvariable=chosen_list_var, font=label_font, fg='green')
chosen_list_label.pack(pady=10)

# Global chosen list
chosen_list = []

# Helper function for label and entry
def create_label_entry(label_text, variable):
    label = tk.Label(root, text=label_text, font=label_font)
    label.pack(pady=5)
    entry = tk.Entry(root, textvariable=variable, font=entry_font)
    entry.pack(pady=5)

# Entry variables
min_value_var = tk.IntVar()
max_value_var = tk.IntVar()
count_var = tk.IntVar()

# Entry fields
create_label_entry("最小值 (Min):", min_value_var)
create_label_entry("最大值 (Max):", max_value_var)
create_label_entry("數量 (Count):", count_var)

# Buttons
generate_btn = tk.Button(root, text='生成隨機數', font=button_font, command=lambda: random_number_generator(min_value_var.get(), max_value_var.get(), count_var.get(), chosen_list))
generate_btn.pack(pady=10)

clear_btn = tk.Button(root, text='清除', font=button_font, command=clear_fields)
clear_btn.pack(pady=10)

clear_list_btn = tk.Button(root, text='清除已選數字', font=button_font, command=clear_chosen_list)
clear_list_btn.pack(pady=10)

# Anime Image (if you have an image file)
# img = tk.PhotoImage(file="path_to_your_anime_image.png")
# img_label = tk.Label(root, image=img)
# img_label.pack(pady=10)

root.mainloop()
