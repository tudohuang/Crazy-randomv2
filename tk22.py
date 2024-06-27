import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import random
import threading
import time
from gtts import gTTS
import pygame
import os
import pyfiglet

chosen_numbers = set()
cnt = 0
tts_enabled = False
voice_speed = 1.0
language = 'en'  # 默認語言設置為英語

def create_option_menu(parent, label, variable, options):
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(frame, text=label, font=('Helvetica', 30)).pack(side=tk.LEFT)
    str_options = [str(option) for option in options]
    option_menu = ctk.CTkOptionMenu(frame, variable=variable, values=str_options, font=('Helvetica', 30))
    option_menu.pack(side=tk.LEFT)
    frame.pack(pady=8)
    return option_menu

def fade_in(window, step=10, speed=25):
    alpha = 0
    def update_alpha():
        nonlocal alpha
        alpha += step / 100
        window.attributes("-alpha", alpha)
        if alpha < 1:
            window.after(speed, update_alpha)
    window.after(speed, update_alpha)

def start_fade_in(window):
    fade_thread = threading.Thread(target=fade_in, args=(window,))
    fade_thread.start()

def update_display(final_numbers, index=0, duration=500, interval=50):
    def format_number(num):
        return f".{num}." if num == 24 else str(num)
    if index < len(final_numbers):
        end_time = time.time() + duration / 1000
        def update_spin():
            if time.time() < end_time:
                random_number = random.randint(min_value_var.get(), max_value_var.get())
                current_numbers = [format_number(n) for n in final_numbers[:index]] + [format_number(random_number)] + [format_number(n) for n in final_numbers[index + 1:]]
                result_var.set('，'.join(current_numbers))
                root.after(interval, update_spin)
            else:
                final_number = final_numbers[index]
                final_numbers[index] = format_number(final_number)
                formatted_final_numbers = [format_number(num) for num in final_numbers]
                result_var.set('，'.join(formatted_final_numbers))
                chosen_numbers.add(final_number)
                update_display(final_numbers, index + 1, duration, interval)
                speak_number(final_number)
        update_spin()
    else:
        formatted_numbers = [format_number(num) for num in final_numbers]
        result_var.set('，'.join(formatted_numbers))

def speak_number(number):
    if tts_enabled:
        tts = gTTS(text=str(number), lang=language, slow=(voice_speed < 1.0))
        filename = "temp_number.mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        try:
            os.remove(filename)
        except PermissionError:
            print("Could not delete the audio file. It might still be in use.")

def generate_random_numbers():
    global cnt
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
    weighted_pool = set(range(min_value, max_value + 1)) - set(chosen_numbers)
    if count > len(weighted_pool):
        count = len(weighted_pool)
    weighted_pool_list = list(weighted_pool)
    new_numbers = random.sample(weighted_pool_list, count)
    if new_numbers == 20 or new_numbers == 24:
        cnt += 1
    if cnt >= 2:
        print(pyfiglet.figlet_format("HAPPY 2024!!!"))
    chosen_numbers.update(new_numbers)
    update_display(new_numbers)
    update_chosen_menu()

def update_chosen_menu():
    menu_values = ['已選數字'] + sorted([str(num) for num in chosen_numbers])
    chosen_option_menu.configure(values=menu_values)
    chosen_option_var.set('已選數字')

def clear_all():
    chosen_numbers.clear()
    result_var.set("")
    update_chosen_menu()

def toggle_tts():
    global tts_enabled
    tts_enabled = not tts_enabled
    tts_button.configure(text="TTS On" if tts_enabled else "TTS Off")

def on_new():
    clear_all()

def on_open():
    messagebox.showinfo("Info", "Open functionality not implemented yet.")

def on_save():
    messagebox.showinfo("Info", "Save functionality not implemented yet.")

def on_exit():
    root.quit()

def change_range(variable, option_menu, title, label):
    def update_range():
        try:
            new_range = int(entry.get())
            variable.set(new_range)
            option_menu.configure(values=[str(i) for i in range(1, new_range + 1)])
            top.destroy()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number.")
    
    top = tk.Toplevel(root)
    top.title(title)
    tk.Label(top, text=label).pack(pady=10)
    entry = tk.Entry(top)
    entry.pack(pady=5)
    tk.Button(top, text="OK", command=update_range).pack(pady=10)

def save_numbers():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(','.join(map(str, chosen_numbers)))

def load_numbers():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            loaded_numbers = file.read().strip().split(',')
            chosen_numbers.update(map(int, loaded_numbers))
            update_chosen_menu()

def export_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(result_var.get())

def change_theme():
    global current_theme
    new_theme = "light" if current_theme == "dark" else "dark"
    ctk.set_appearance_mode(new_theme)
    current_theme = new_theme

def set_voice_speed(speed):
    global voice_speed
    voice_speed = speed

def set_language(lang):
    global language
    language = lang

def show_help():
    messagebox.showinfo("Help", "This is a random number generator. Use the menus to adjust settings and generate numbers.")

def show_about():
    messagebox.showinfo("About", "Random Number Generator v1.0\nDeveloped by Your Name")

large_font = ('Helvetica', 70)
root = ctk.CTk()
root.title('隨機數字產生器')
root.geometry('1500x1300')
current_theme = "dark"
ctk.set_appearance_mode(current_theme)
ctk.set_default_color_theme("blue")

min_value_var = tk.IntVar(value=1)
max_value_var = tk.IntVar(value=35)
count_var = tk.IntVar(value=1)
result_var = tk.StringVar()
chosen_numbers_var = tk.StringVar(value='已選數字')

min_options = list(range(1, 36))
max_options = list(range(1, 40))
count_options = list(range(1, 11))
ctk.CTkLabel(root, text="🎲 Random Number 🎲", font=("Helvetica", 90, "bold")).pack(pady=30)
ctk.CTkLabel(root, textvariable=result_var, font=large_font).pack(pady=20)

min_option_menu = create_option_menu(root, "MIN：", min_value_var, min_options)
max_option_menu = create_option_menu(root, "MAX：", max_value_var, max_options)
count_option_menu = create_option_menu(root, "Count：", count_var, count_options)

ctk.CTkButton(root, text='Generate', command=generate_random_numbers).pack(pady=10)
ctk.CTkButton(root, text='Clear', command=clear_all).pack(pady=10)

chosen_option_var = tk.StringVar(root)
chosen_option_menu = ctk.CTkOptionMenu(root, variable=chosen_option_var, values=['已選數字'])
chosen_option_menu.pack(pady=15)

tts_button = ctk.CTkButton(root, text='TTS Off', command=toggle_tts)
tts_button.pack(pady=10)

# 創建菜單
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=on_new)
filemenu.add_command(label="Open", command=on_open)
filemenu.add_command(label="Save", command=on_save)
filemenu.add_command(label="Save Numbers", command=save_numbers)
filemenu.add_command(label="Load Numbers", command=load_numbers)
filemenu.add_command(label="Export to File", command=export_to_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=on_exit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo")
editmenu.add_command(label="Redo")
menubar.add_cascade(label="Edit", menu=editmenu)

range_menu = tk.Menu(menubar, tearoff=0)
range_menu.add_command(label="Change MIN Range", command=lambda: change_range(min_value_var, min_option_menu, "Change MIN Range", "Enter new range for MIN values:"))
range_menu.add_command(label="Change MAX Range", command=lambda: change_range(max_value_var, max_option_menu, "Change MAX Range", "Enter new range for MAX values:"))
range_menu.add_command(label="Change Count Range", command=lambda: change_range(count_var, count_option_menu, "Change Count Range", "Enter new range for Count values:"))
menubar.add_cascade(label="Range", menu=range_menu)

theme_menu = tk.Menu(menubar, tearoff=0)
theme_menu.add_command(label="Toggle Theme", command=change_theme)
menubar.add_cascade(label="Theme", menu=theme_menu)

voice_menu = tk.Menu(menubar, tearoff=0)
voice_menu.add_command(label="Normal Speed", command=lambda: set_voice_speed(1.0))
voice_menu.add_command(label="Fast Speed", command=lambda: set_voice_speed(1.5))
voice_menu.add_command(label="Slow Speed", command=lambda: set_voice_speed(0.75))
menubar.add_cascade(label="Voice Speed", menu=voice_menu)

language_menu = tk.Menu(menubar, tearoff=0)
language_menu.add_command(label="English", command=lambda: set_language('en'))
language_menu.add_command(label="Chinese", command=lambda: set_language('zh-tw'))
language_menu.add_command(label="Spanish", command=lambda: set_language('es'))
language_menu.add_command(label="French", command=lambda: set_language('fr'))
language_menu.add_command(label="Japanese", command=lambda: set_language('ja'))
language_menu.add_command(label="ZH_CN", command=lambda: set_language('zh-cn'))
menubar.add_cascade(label="Language", menu=language_menu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=show_help)
helpmenu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

if __name__ == '__main__':
    root.attributes("-alpha", 0)
    start_fade_in(root)
    root.mainloop()
