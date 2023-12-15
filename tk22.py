import tkinter as tk
import random

def generate_random_numbers():
    
    min_value = min_value_var.get()
    max_value = max_value_var.get()
    count = count_var.get()
    exclude_list = chosen_numbers

    available_numbers = set(range(min_value, max_value + 1)) - set(exclude_list)
    if count > len(available_numbers):
        result_var.set("End")
        return

    new_numbers = random.sample(list(available_numbers), count)
    chosen_numbers.extend(new_numbers)
    update_display(new_numbers)
    update_chosen_menu()

def update_display(new_numbers):
    result_var.set(', '.join(map(str, new_numbers)))

def update_chosen_menu():
    chosen_menu_var.set('Chosen Numbers')
    chosen_menu_menu.delete(0, 'end')
    for number in chosen_numbers:
        chosen_menu_menu.add_command(label=str(number), command=lambda n=number: chosen_numbers_var.set(n))

def clear_all():
    chosen_numbers.clear()
    update_display([])
    update_chosen_menu()

root = tk.Tk()
root.title('隨機數字產生器')
root.geometry('400x300')

# 界面樣式
label_font = ('Arial', 12)
entry_font = ('Arial', 12)
button_font = ('Arial', 12, 'bold')

# 變量
min_value_var = tk.IntVar(value=1)
max_value_var = tk.IntVar(value=35)
count_var = tk.IntVar(value=1)
result_var = tk.StringVar()
chosen_numbers_var = tk.StringVar(value='Chosen Numbers')
chosen_numbers = []

# 輸入欄位
def create_input_field(parent, label, variable):
    frame = tk.Frame(parent)
    tk.Label(frame, text=label, font=label_font).pack(side=tk.LEFT)
    tk.Entry(frame, textvariable=variable, font=entry_font).pack(side=tk.LEFT)
    frame.pack(pady=5)

create_input_field(root, "Min:", min_value_var)
create_input_field(root, "Max:", max_value_var)
create_input_field(root, "Count:", count_var)

# 按鈕
tk.Button(root, text='Generate', font=button_font, command=generate_random_numbers).pack(pady=10)
tk.Button(root, text='Clear', font=button_font, command=clear_all).pack(pady=10)

# 顯示結果
tk.Label(root, textvariable=result_var, font=label_font, fg='blue').pack(pady=10)

# 下拉選單顯示已選數字
chosen_menu_var = tk.StringVar(root)
chosen_menu = tk.Menubutton(root, textvariable=chosen_menu_var, font=button_font, relief='raised')
chosen_menu_menu = tk.Menu(chosen_menu, tearoff=0)
chosen_menu['menu'] = chosen_menu_menu
chosen_menu.pack(pady=10)

root.mainloop()
