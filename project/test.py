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
    back_logo = PhotoImage(file="C:\_My_Folder\Working\Py_projects\project/back.png")
    back_button = tk.Button(root, text="Назад", command=calculation_valute_screen, image=back_logo, compound="left", padx=40, pady=15, borderwidth=1, font=("Verdana", 24, "bold"))
    back_button.place(x=650, y=670)
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
    list_one.place(x=210, y=300)

    list_two = ttk.Combobox(root, values=options, font=("Helvetica", 24), state="normal")
    list_two.set("Доллар США")  # текст по умолчанию
    list_two.place(x=1015, y=300)
    
    # ввод чисел
    input_valute = tk.Entry(root, textvariable=tk.StringVar(value="1"), font=("Helvetica", 24), width=21)
    input_valute.place(x=210, y=350)
    
    
    answer = tk.Label(root, text=f"", font=("Helvetica", 24), bg="white")
    answer.place(x=1015, y=350)
    convert_valute()
    
    # кнопка конвертировать
    check_button = tk.Button(root, text="Конвертировать", command=convert_valute, font=("Helvetica", 20), bg="#e4e4e4", fg="black", borderwidth=1, padx=100, pady=15)
    check_button.place(x=590, y=450)
    check_button.bind("<Enter>", on_enter)
    check_button.bind("<Leave>", on_leave)
    
    # кнопка swap
    swap_logo = PhotoImage(file="C:\_My_Folder\Working\Py_projects\project\Two_arrows.png")
    swap_button = tk.Button(root, text="", command=swap_but, image=swap_logo, bg="#e4e4e4", borderwidth=1, width=70, height=70)
    swap_button.place(x=760, y=300)
    swap_button.bind("<Enter>", on_enter)
    swap_button.bind("<Leave>", on_leave)    
    
    
    
root = tk.Tk()
root.geometry("3200x2000")
root.title("My application")

calculation_valute_screen()
root.mainloop()