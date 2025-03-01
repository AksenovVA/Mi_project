import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
import requests
import xml.etree.ElementTree as ET



def clear_screen(): # очищаем экран
    for widget in root.winfo_children():
        widget.destroy()


def on_enter(event): # изменяем фон при наведении
    event.widget.config(bg="#fad844")

def on_leave(event): # возвращаем исходный фон
    event.widget.config(bg="#e4e4e4")



def main_screen(): # основной экран
    clear_screen()
    
    # основной фон
    global background_main
    background_main = PhotoImage(file="C:\_My_Folder\Working\Py_projects\project\_back_main.png")
    background_l_main = tk.Label(root, image=background_main)
    background_l_main.place(x=0, y=0, relwidth=1, relheight=1)
    
    
    # первая строка
    main_label = tk.Label(root, text="Дополнения к калькулятору", font=("Helvetica", 36, "bold"), fg="black", padx=20, pady=20)
    main_label.place(x=460, y=40)
    
    # кнопка валют
    exchange_rate_logo = PhotoImage(file="C:\_My_Folder\Working\Py_projects\project\Exchange_rate.png")
    exchange_rate_button = tk.Button(root, text="Валюты", command=calculation_valute_screen, image=exchange_rate_logo, compound="left", width=300, height=150, borderwidth=1, font=("Verdana", 24, "bold"))
    exchange_rate_button.image = exchange_rate_logo
    exchange_rate_button.place(x=70, y=230)
    exchange_rate_button.bind("<Enter>", on_enter)
    exchange_rate_button.bind("<Leave>", on_leave)
    
    # кнопка масс
    weight_logo = PhotoImage(file="C:\_My_Folder\Working\Py_projects\project\Exchange_rate.png")
    weight_button = tk.Button(root, text="Вес,\nМасса", command=calculation_weight_screen, image=weight_logo, compound="left", width=300, height=150, borderwidth=1, font=("Verdana", 24, "bold"))
    weight_button.image = weight_logo
    weight_button.place(x=570, y=230)
    weight_button.bind("<Enter>", on_enter)
    weight_button.bind("<Leave>", on_leave)    
    

def calculation_valute_screen(): # экран калькулятора валют
    clear_screen()
    
    global background_valute
    background_valute = PhotoImage(file="C:\_My_Folder\Working\Py_projects\project\_back_valute.png")
    background_l_valute = tk.Label(root, image=background_valute)
    background_l_valute.place(x=0, y=0, relwidth=1, relheight=1)
    
    # первая строка
    main_label = tk.Label(root, text="Конвертер валют", font=("Helvetica", 36, "bold"), fg="black", bg="white", padx=20, pady=5)
    main_label.place(x=560, y=150)
    
    global back_logo, swap_logo
    back_logo = PhotoImage(file="D:/_My Folders/project/back.png")
    back_button = tk.Button(root, text="Назад", command=main_screen, image=back_logo, compound="left", padx=100, pady=30, borderwidth=1, font=("Verdana", 24, "bold"))
    back_button.place(x=100, y=670)
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    
    
    def valute_names(): # генерируем список валют
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
        response = requests.get(url)
        
        if response.status_code == 200:
            xml_data = response.content
            tree = ET.fromstring(xml_data)
            list_names = ["Российский рубль"]
            
            for valute in tree.findall("Valute"):
                name = valute.find("Name").text  # извлекаем название валюты
                list_names.append(name)
            
            return list_names
        else:
            messagebox.showerror("Ошибка", "Ошибка соединения с сервером")
            return ["Российский рубль"]
    options = valute_names()
    
    def request_valute(name):
        if (name == "Российский рубль"):
            return 1.0
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
        response = requests.get(url)
        if response.status_code == 200:
            xml_data = response.content
            tree = ET.fromstring(xml_data)
            for valute in tree.findall("Valute"):
                currency_name = valute.find("Name").text  # Название валюты
                
                if currency_name == name:
                    nominal = int(valute.find("Nominal").text)
                    value = float(valute.find("Value").text.replace(",", "."))  # курс
                    rate_per_ruble = nominal / value  # сколько валюты за 1 рубль
                    return rate_per_ruble
        else:
            messagebox.showerror("Ошибка", "Ошибка соединения с сервером")
            return 0.0
    
    # поле выбора валюты
    def convert_valute():
        start = input_valute.get()
        #answer.config(text=f"{1.5 * start}")
        try:
            start = float(start)
            first_valute = list_one.get() # переводим из
            second_valute = list_two.get() # переводим в
            
            if first_valute in options and second_valute in options:
                mul = request_valute(second_valute) / request_valute(first_valute)
                answer.config(text=f"{round(mul * start, 2)}")
            else:
                messagebox.showerror("Ошибка", "Выбранное значение не найдено в списке")
        except ValueError:
            messagebox.showerror("Ошибка", "Введенная строка не является десятичной дробью")
    def swap_but():
        first_valute = list_one.get()
        first_num = input_valute.get()
        second_valute = list_two.get()
        second_num = answer['text']
        
        list_one.set(second_valute)
        list_two.set(first_valute)
        input_valute.delete(0, tk.END)
        input_valute.insert(0, second_num)
        answer.config(text=first_num)
        
        
        
    
    list_one = ttk.Combobox(root, values=options, font=("Helvetica", 24), state="normal")
    list_one.set("Российский рубль")  # текст по умолчанию
    list_one.place(x=210, y=250)

    list_two = ttk.Combobox(root, values=options, font=("Helvetica", 24), state="normal")
    list_two.set("Доллар США")  # текст по умолчанию
    list_two.place(x=1015, y=250)
    
    # ввод чисел
    input_valute = tk.Entry(root, textvariable=tk.StringVar(value="1"), font=("Helvetica", 24), width=21)
    input_valute.place(x=210, y=300)
    
    
    answer = tk.Label(root, text=f"", font=("Helvetica", 24), bg="white")
    answer.place(x=1015, y=300)
    convert_valute()
    
    # кнопка конвертировать
    check_button = tk.Button(root, text="Конвертировать", command=convert_valute, font=("Helvetica", 20), bg="#e4e4e4", fg="black", padx=100, pady=15)
    check_button.place(x=590, y=400)
    check_button.bind("<Enter>", on_enter)
    check_button.bind("<Leave>", on_leave)
    
    # кнопка swap
    swap_logo = PhotoImage(file="C:\_My_Folder\Working\Py_projects\project\Two_arrows.png")
    swap_button = tk.Button(root, text="", command=swap_but, image=swap_logo, bg="#e4e4e4", width=70, height=70)
    swap_button.place(x=760, y=250)
    swap_button.bind("<Enter>", on_enter)
    swap_button.bind("<Leave>", on_leave)


def calculation_weight_screen(): # экран калькулятора масс
    clear_screen()
    
    global background_image
    background_image = PhotoImage(file="C:\_My_Folder\Working\Py_projects\project\_back_weight.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # первая строка
    main_label = tk.Label(root, text="Конвертер масс", font=("Helvetica", 36, "bold"), fg="black", bg="#f7f9f8", padx=20, pady=5)
    main_label.place(x=560, y=140)
    
    global back_logo, swap_logo
    back_logo = PhotoImage(file="D:/_My Folders/project/back.png")
    back_button = tk.Button(root, text="Назад", command=main_screen, image=back_logo, compound="left", width=585, height=150, borderwidth=1, font=("Verdana", 24, "bold"))
    back_button.place(x=500, y=670)
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    
    
    # генерируем список масс
    options = {
    "Тонна": 1000,
    "Центнер": 100,
    "Килограмм": 1,
    "Карат": 5000, 
    "Грамм": 0.001,
    "Миллиграмм": 0.000001,
    "Микрограмм": 0.000000001,
    "Фунт": 0.453592,
    "Пуд": 16.38,
    "Длинная тонна": 1016.05,
    "Короткая тонна": 907.184,
    "Длинный центнер": 48.5,
    "Короткий центнер": 45.36,
    "Стоун": 6.35029,
    "Фунт": 0.453592,
    "Унция": 0.0283495,
    "Драхма": 0.001771,
    "Гран": 0.0000648
    }
    options_list = list(options.keys())

    
    
    def convert_weight():
        start = input_weight.get()
        
        try:
            start = float(start)
            first_weight = list_one.get() # переводим из
            second_weight = list_two.get() # переводим в
            
            if first_weight in options_list and second_weight in options_list:
                mul = options[first_weight] /  options[second_weight] 
                answer.config(text=f"{mul * start:.7f}")
            else:
                messagebox.showerror("Ошибка", "Выбранное значение не найдено в списке")
        except ValueError:
            messagebox.showerror("Ошибка", "Введенная строка не является десятичной дробью")
    
    def swap_but():
        first_weight = list_one.get()
        first_num = input_weight.get()
        second_weight = list_two.get()
        second_num = answer['text']
        
        list_one.set(second_weight)
        list_two.set(first_weight)
        input_weight.delete(0, tk.END)
        input_weight.insert(0, second_num)
        answer.config(text=first_num)
        
        
        
    # поле выбора массы
    list_one = ttk.Combobox(root, values=options_list, font=("Helvetica", 20), state="normal")
    list_one.set("Килограмм")  # текст по умолчанию
    list_one.place(x=410, y=250)

    list_two = ttk.Combobox(root, values=options_list, font=("Helvetica", 20), state="normal")
    list_two.set("Тонна")  # текст по умолчанию
    list_two.place(x=868, y=250)
    
    # ввод чисел
    input_weight = tk.Entry(root, textvariable=tk.StringVar(value="1"), font=("Helvetica", 20), width=21)
    input_weight.place(x=410, y=300)
    
    
    answer = tk.Label(root, text=f"", font=("Helvetica", 20), bg="white")
    answer.place(x=868, y=300)
    convert_weight()
    
    # кнопка конвертировать
    check_button = tk.Button(root, text="Конвертировать", command=convert_weight, font=("Helvetica", 20), bg="#e4e4e4", fg="black", padx=100, pady=30)
    check_button.place(x=590, y=400)
    check_button.bind("<Enter>", on_enter)
    check_button.bind("<Leave>", on_leave)
    
    # кнопка swap
    swap_logo = PhotoImage(file="C:\_My_Folder\Working\Py_projects\project\Two_arrows.png")
    swap_button = tk.Button(root, text="", command=swap_but, image=swap_logo, bg="#e4e4e4", width=70, height=70)
    swap_button.place(x=760, y=250)
    swap_button.bind("<Enter>", on_enter)
    swap_button.bind("<Leave>", on_leave)     

    
    
    
    
root = tk.Tk()
root.geometry("3200x2000")
root.title("My application")

main_screen()
root.mainloop()