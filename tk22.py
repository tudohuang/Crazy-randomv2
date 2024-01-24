import customtkinter as ctk
import tkinter as tk
import random
import threading
import time
from gtts import gTTS
import pygame
import os
import pyfiget

chosen_numbers = set()
cnt = 0
tts_enabled = False

def create_option_menu(parent, label, variable, options):
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(frame, text=label,font=('Helvetica', 30)).pack(side=tk.LEFT)
    # 將選項轉換為字符串列表
    str_options = [str(option) for option in options]
    option_menu = ctk.CTkOptionMenu(frame, variable=variable, values=str_options,font=('Helvetica', 30))
    option_menu.pack(side=tk.LEFT)
    frame.pack(pady=8)


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
                chosen_numbers.add(final_number)  # Add the finalized number to chosen numbers

                #update_chosen_menu()  # Update the chosen numbers menu
                update_display(final_numbers, index + 1, duration, interval)
                speak_number(final_number)  # Speak the finalized number

        update_spin()
    else:
        formatted_numbers = [format_number(num) for num in final_numbers]
        result_var.set('，'.join(formatted_numbers))

def speak_number(number):
    if tts_enabled:
        tts = gTTS(text=str(number), lang='en')
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

    # 將集合轉換為列表
    weighted_pool_list = list(weighted_pool)

    # 從列表中隨機選取數字
    new_numbers = random.sample(weighted_pool_list, count)
    if new_numbers == 20 or new_numbers ==24:
        cnt += 1
    if cnt>=2:
        print(pyfiglet.figlet_format("HAPPY 2024!!!"))
    chosen_numbers.update(new_numbers)  # Update the set with new numbers
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

large_font = ('Helvetica', 70)
root = ctk.CTk()
root.title('隨機數字產生器')
root.geometry('1500x1300')
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

min_value_var = tk.IntVar(value=1)
max_value_var = tk.IntVar(value=35)
count_var = tk.IntVar(value=1)
result_var = tk.StringVar()
chosen_numbers_var = tk.StringVar(value='已選數字')

min_options = list(range(1, 36))  # 1 到 35
max_options = list(range(1, 40))  # 1 到 35
count_options = list(range(1, 11))  # 1 到 10
ctk.CTkLabel(root, text="🎲 Random Number 🎲", font=("Helvetica", 90, "bold")).pack(pady=30)
ctk.CTkLabel(root, textvariable=result_var, font=large_font).pack(pady=20)
create_option_menu(root, "MIN：", min_value_var, min_options)
create_option_menu(root, "MAX：", max_value_var, max_options)
create_option_menu(root, "Count：", count_var, count_options)



ctk.CTkButton(root, text='Generate', command=generate_random_numbers).pack(pady=10)
ctk.CTkButton(root, text='Clear', command=clear_all).pack(pady=10)

chosen_option_var = tk.StringVar(root)
chosen_option_menu = ctk.CTkOptionMenu(root, variable=chosen_option_var, values=['已選數字'])
chosen_option_menu.pack(pady=15)

tts_button = ctk.CTkButton(root, text='TTS Off', command=toggle_tts)
tts_button.pack(pady=10)


if __name__ == '__main__':
    root.attributes("-alpha", 0)
    start_fade_in(root)
    root.mainloop()
