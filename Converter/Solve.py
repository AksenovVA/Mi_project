import flet as ft
import requests
from tkinter import messagebox
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random


def main(page: ft.Page):
    page.title = "Конвертер"
    page.theme_mode = ft.ThemeMode.LIGHT


    page.window.width = 500
    page.window.height = 800
    page.window.resizable = False
    page.window.maximizable = False
    page.update()



    # Меняем страницы
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(main_screen())
        elif page.route == "/valute_converter_screen":
            page.views.append(valute_converter_screen())
        elif page.route == "/time_converter_screen":
            page.views.append(time_converter_screen())
        elif page.route == "/date_converter_screen":
            page.views.append(date_converter_screen())
        elif page.route == "/mass_converter_screen":
            page.views.append(mass_converter_screen())
        elif page.route == "/dist_converter_screen":
            page.views.append(dist_converter_screen())
        elif page.route == "/system_converter_screen":
            page.views.append(system_converter_screen())
        page.update()
    

                                                # Общие элементы
    api_key_timezonedb = "4H4JYI2S7SJY"
    
    def toggle_window(e):
        page.window.always_on_top = not page.window.always_on_top
        if page.window.always_on_top == False:
            always_on_button.icon_color=ft.colors.RED_200
            always_on_button.tooltip="Откреплено"
        else:
            always_on_button.icon_color=ft.colors.GREEN_200
            always_on_button.tooltip="Закреплено"
        page.update()
    
    def change_theme_window(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        if page.theme_mode == ft.ThemeMode.LIGHT:
            change_theme_button.icon = ft.icons.DARK_MODE
            change_theme_button.icon_color=ft.colors.BLUE_200
        else:
            change_theme_button.icon = ft.icons.LIGHT_MODE
            change_theme_button.icon_color=ft.colors.YELLOW_200
        page.update()

    always_on_button = ft.IconButton(
        icon=ft.icons.EXPAND_ROUNDED,
        icon_color=ft.colors.RED_200,
        icon_size=25,
        tooltip="Откреплено",
        on_click=toggle_window
    )

    change_theme_button = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        icon_color=ft.colors.BLUE_200,
        icon_size=25,
        on_click=change_theme_window
    )

    


    def main_screen():                          # Главная страница
        return ft.View(
            "/",
            controls=[
                ft.Column(
                    [   
                        ft.Text(
                            value='',
                            selectable=False,
                            height=200,
                            width=100
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(icon=ft.icons.CURRENCY_RUBLE, text='Курсы валют', on_click=lambda _: page.go("/valute_converter_screen")),
                                ft.ElevatedButton(icon=ft.icons.TIMELAPSE_OUTLINED, text='Время', on_click=lambda _: page.go("/time_converter_screen")),
                                ft.ElevatedButton(icon=ft.icons.CALENDAR_MONTH, text='Даты', on_click=lambda _: page.go("/date_converter_screen"))
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(icon=ft.icons.FITNESS_CENTER, text='Массы', on_click=lambda _: page.go("/mass_converter_screen")),
                                ft.ElevatedButton(icon=ft.icons.DIRECTIONS_WALK, text='Расстояния', on_click=lambda _: page.go("/dist_converter_screen")),
                                ft.ElevatedButton(icon=ft.icons.CALCULATE, text='Системы\nсчисления', on_click=lambda _: page.go("/system_converter_screen")),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Text(
                            value='',
                            selectable=False,
                            height=150,
                            width=100
                        ),
                        ft.Row(
                            [
                                change_theme_button,
                                ft.Text(
                                    value='',
                                    selectable=False,
                                    height=30,
                                    width=75
                                ),
                                always_on_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
                
                
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    def valute_converter_screen():              # Страница конвертера валют
        def valute_names():
            url = "https://www.cbr.ru/scripts/XML_daily.asp"
            response = requests.get(url)
            if response.status_code == 200:
                xml_data = response.content
                tree = ET.fromstring(xml_data)
                list_names = ["Российский рубль"]
                
                for valute in tree.findall("Valute"):
                    name = valute.find("Name").text  # извлекаем название валюты
                    list_names.append(name)
                
                return list_names, [ft.dropdown.Option(name) for name in list_names]
            else:
                messagebox.showerror("Ошибка", "Ошибка соединения с сервером")
                return list_names, [ft.dropdown.Option("Российский рубль")]


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


        def convert_valute(e):
            start = valute_converter_text_from.value
            try:
                start = float(start)
                first_valute = valute_converter_drop_from.value # переводим из
                second_valute = valute_converter_drop_to.value # переводим в
                
                if first_valute in valute_names_list and second_valute in valute_names_list:
                    mul = request_valute(second_valute) / request_valute(first_valute)
                    valute_converter_text_to.value = f"{round(mul * start, 3)}"
                else:
                    messagebox.showerror("Ошибка", "Выбранное значение не найдено в списке")
            except ValueError:
                messagebox.showerror("Ошибка", "Введенная строка не является десятичной дробью")
            page.update()

        valute_names_list, valute_names_list_options = valute_names()


        valute_converter_text_from = ft.TextField(
            value='1.0000',
            autofocus=True,
            width=180,
            height=40
        )
        
        valute_converter_drop_from = ft.Dropdown(
            editable=True,
            label="Валюта",
            value="Российский рубль",
            options=valute_names_list_options,
            width=180,
            max_menu_height=80
        )

        valute_converter_text_to = ft.Text(
            '',
            size=18,
            selectable=True,
            width=180,
            height=40
        )

        valute_converter_drop_to = ft.Dropdown(
            editable=True,
            label="Валюта",
            value="Доллар США",
            options=valute_names_list_options,
            width=180,
            max_menu_height=80
        )
        def valute_converter_swap(e):
            valute_converter_drop_from.value, valute_converter_drop_to.value = valute_converter_drop_to.value, valute_converter_drop_from.value
            valute_converter_text_from.value, valute_converter_text_to.value = valute_converter_text_to.value, valute_converter_text_from.value
            page.update()
        return ft.View(
            "/valute_converter_screen",
            controls=[

                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    'Конвертер валют',
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    selectable=True
                                    )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        valute_converter_drop_from,
                                        valute_converter_text_from
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.IconButton(
                                    icon=ft.icons.SWAP_HORIZ,
                                    icon_size=40,
                                    on_click=valute_converter_swap

                                ),
                                ft.Column(
                                    [
                                        valute_converter_drop_to,
                                        valute_converter_text_to
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),

                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text='Конвертировать',
                                    height=50,
                                    width=300,
                                    on_click=convert_valute
                                    
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                change_theme_button,
                                ft.ElevatedButton(
                                    icon=ft.icons.ARROW_BACK,
                                    text='Назад',
                                    on_click=lambda _: page.go("/"),
                                    height=50,
                                    width=200
                                ),
                                always_on_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    spacing=90,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],


            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
                    
    def time_converter_screen():                # Конвертер времени
        
        def time_region_names():
            url = f"http://api.timezonedb.com/v2.1/list-time-zone?key={api_key_timezonedb}&format=json"
            response = requests.get(url)
            data = response.json()
            
            first_zones_list = [zone["zoneName"] for zone in data["zones"]]
            zones_dict_for_requests = dict()
            zones_list = []
            for el in first_zones_list:
                reg, tow = el.split('/', 1)
                zones_dict_for_requests[tow] = reg
                zones_list.append(tow)

            zones_list = sorted(zones_list)
            if "zones" in data:
                return zones_list, [ft.dropdown.Option(x) for x in zones_list], zones_dict_for_requests
            else:
                messagebox.showerror("Ошибка", "Ошибка соединения с сервером")
                return [], [], []
        
        region_names_list, region_names_list_options, zones_dict_for_requests = time_region_names()

        def get_timezone_offset(location):
            """Получает UTC-смещение (offset) для указанного часового пояса через TimeZoneDB API."""
            if location not in zones_dict_for_requests:
                messagebox.showerror("Ошибка", f"Город {location} не найден в списке.")
                return None
            
            zone_name = f"{zones_dict_for_requests[location]}/{location}"  # Формируем корректный путь
            url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={api_key_timezonedb}&format=json&by=zone&zone={zone_name}"
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get("gmtOffset") / 3600
            else:
                messagebox.showerror("Ошибка", f"Ошибка запроса ({location}): {response.status_code}")
                return None

        def request_utc(e):
            start = time_converter_text_from.value
            try:
                start = start.split(':')
                if len(start) != 3:
                    messagebox.showerror("Ошибка", "Введена некорректная строка")
                    return

                first_time = time_converter_drop_from.value  # переводим из
                second_time = time_converter_drop_to.value  # переводим в

                if first_time in region_names_list and second_time in region_names_list:
                    offset1 = get_timezone_offset(first_time)
                    offset2 = get_timezone_offset(second_time)

                    if offset1 is not None and offset2 is not None:
                        time_diff = offset2 - offset1

                        hours, minutes, seconds = map(int, start)
                        if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                            messagebox.showerror("Ошибка", "Введена некорректная строка")
                            return
                        new_hours = hours + time_diff
                        if (new_hours <= 0):
                            time_converter_count_days.value = 'The previous day'
                        elif new_hours <= 24:
                            time_converter_count_days.value = 'The same day'
                        else:
                            time_converter_count_days.value = 'The next day'
                        new_hours = (new_hours + 24) % 24
                        time_converter_text_to.value = f"{int(new_hours):02}:{minutes:02}:{seconds:02}"
                    else:
                        messagebox.showerror("Ошибка", "Не удалось получить данные о часовом поясе")
                else:
                    messagebox.showerror("Ошибка", "Выбранное значение не найдено в списке")
            except ValueError:
                messagebox.showerror("Ошибка", "Введена некорректная строка")
            
            page.update()

        def get_now_time(e):
            region = time_converter_drop_from.value
            url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={api_key_timezonedb}&format=json&by=zone&zone={zones_dict_for_requests[region]}/{region}"
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                current_time = data.get("formatted")  # Время в формате "YYYY-MM-DD HH:MM:SS"
                time_converter_text_from.value = current_time.split()[1]
                page.update()
            else:
                messagebox.showerror("Ошибка", "Отсутствует соединение с сервером")



        time_converter_text_from = ft.TextField(
            value='00:00:00',
            autofocus=True,
            width=180,
            height=40
        )
        
        time_converter_drop_from = ft.Dropdown(
            editable=True,
            label="Time by",
            value="London",
            options=region_names_list_options,
            width=180,
            max_menu_height=80
        )

        time_converter_text_to = ft.Text(
            '',
            size=18,
            selectable=True,
            width=180,
            height=40,
            
        )

        time_converter_drop_to = ft.Dropdown(
            editable=True,
            label="Time in",
            value="Moscow",
            options=region_names_list_options,
            width=180,
            max_menu_height=80
        )

        time_converter_count_days = ft.Text(
            value='',
            selectable=True,
            height=30,
            width=180
        )


        def time_converter_swap(e):
            time_converter_drop_from.value, time_converter_drop_to.value = time_converter_drop_to.value, time_converter_drop_from.value
            time_converter_text_from.value, time_converter_text_to.value = time_converter_text_to.value, time_converter_text_from.value
            page.update()
        return ft.View(
            "/time_converter_screen",
            controls=[
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    'Конвертер времени',
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    selectable=True
                                    )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        time_converter_drop_from,
                                        time_converter_text_from,
                                        ft.ElevatedButton(
                                            text='Current time',
                                            height=30,
                                            width=180,
                                            on_click=get_now_time

                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.IconButton(
                                    icon=ft.icons.SWAP_HORIZ,
                                    icon_size=40,
                                    on_click=time_converter_swap


                                ),
                                ft.Column(
                                    [
                                        time_converter_drop_to,
                                        time_converter_text_to,
                                        time_converter_count_days
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),

                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text='Конвертировать',
                                    height=50,
                                    width=300,
                                    on_click=request_utc
                                    
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                change_theme_button,
                                ft.ElevatedButton(
                                    icon=ft.icons.ARROW_BACK,
                                    text='Назад',
                                    on_click=lambda _: page.go("/"),
                                    height=50,
                                    width=200
                                ),
                                always_on_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    spacing=90,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    def date_converter_screen():                # Работа с датами
        def date_drop_mode_on_change(e):
            if date_converter_drop_mode.value == 'Разница':
                date_converter_text_second.label='Date'
                date_converter_text_second.hint_text='дд.мм.гггг'
            else:
                date_converter_text_second.label='Number of days'
                date_converter_text_second.hint_text='Count'
            page.update()
        
        def get_day_suffix(days: int):
            """Возвращает правильное окончание слова 'день'."""
            if 11 <= days % 100 <= 14:
                return "дней"
            elif days % 10 == 1:
                return "день"
            elif 2 <= days % 10 <= 4:
                return "дня"
            else:
                return "дней"

        def generate_funny_phrase_for_number_of_days(days: int):
            suffix = get_day_suffix(days)

            # Базовые фразы
            phrases = [
                f"{days} {suffix} – время идет, а ты готов? ⏳",
                f"Представь, сколько всего можно успеть за {days} {suffix}!💪",
                f"Если бы ты откладывал дела каждый день, то их накопилось бы {days}! 📅"
            ]

            # Дополнительные фразы в зависимости от количества дней
            if days == 0:
                phrases += [
                    f"0 {suffix} – момент настал, не упусти его! ⏳",
                    f"0 {suffix} – этот день будет важным, поверь! 🌱"
                ]
            elif 1 <= days <= 6:
                phrases += [
                    f"{days} {suffix} – маленький срок, но большие возможности! 🚀",
                    f"У тебя есть {days} {suffix}, чтобы придумать, что делать дальше! 🤔",
                    f"{days} {suffix} – время достаточно, чтобы изменить что-то. Или просто подождать... ⏳"
                ]
            elif 7 <= days <= 30:
                phrases += [
                    f"{days} {suffix} – целая стратегическая операция по ожиданию. 🎯",
                    f"Еще {days} {suffix} – можно подготовиться, а можно просто расслабиться. 🏖",
                    f"{days} {suffix} – это почти как месяц, но без календарных ограничений! 📆",
                    f"Всего {days} {suffix} – успеешь больше, чем думаешь! ⏳"
                ]
            elif 31 <= days <= 100:
                phrases += [
                    f"{days} {suffix} ожидания – можно написать книгу или просто посмотреть 50 сериалов. 📺",
                    f"Так много времени... {days} {suffix} – может, записать об этом дневник? 📖",
                    f"Главное – не потерять счёт дней. Хотя, {days} {suffix} – кто их считает? 🤷"
                ]
            elif 101 <= days <= 365:
                phrases += [
                    f"{days} {suffix} – возможно, этого хватит на великие свершения! Или хотя бы на хороший отдых. 🏝",
                    f"Терпение, {days} {suffix} – это не так уж и долго, если смотреть с Марса! 🚀",
                    f"Достаточно долгое ожидание в {days} {suffix}, чтобы забыть, с чего все началось. 🤔"
                ]
            else:
                phrases += [
                    f"Прошло бы уже {days} {suffix}, если бы ты начал обратный отсчет раньше! ⏳",
                    f"{days} {suffix} – звучит как легенда! Или просто очень долгий отпуск... 🌍",
                    f"Интересно, через {days} {suffix} уже изобретут летающие автомобили? 🚗",
                    f"Через {days} {suffix} ты будешь оглядываться назад и удивляться, сколько всего успел! ✨"
                ]

            return random.choice(phrases)
        
        def generate_date_comment(date_str: str, days: int):
            phrases = [f"Хмм... Интересная дата - {date_str} 😊"]
            suffix = get_day_suffix(days)
            # Комментарии по количеству дней
            if days == 1:
                phrases += [
                    "Один день – почти незаметно! ⏳",
                    "Осталось подождать всего день! 😊"
                ]
            elif 2 <= days <= 6:
                phrases += [
                    f"{days} {suffix} – пролетит быстро! ⏱️",
                    f"{days} {suffix} – это чуть больше, чем просто ожидание! 🤔"
                ]
            elif 7 <= days <= 30:
                phrases += [
                    f"{days} {suffix} – это уже внушительно! 📅",
                    "Почти месяц? Ну, это уже достойно внимания! 🔥"
                ]
            elif 31 <= days <= 180:
                phrases += [
                    f"{days} {suffix} – полгода почти! ⏳",
                    "К этому времени многое изменится! 🔄"
                ]
            elif 181 <= days <= 365:
                phrases += [
                    f"{days} {suffix} – целый год на подходе! 🎉",
                    "Что-то серьёзное! Время летит! ⏰"
                ]
            else:
                phrases += [
                    f"{days} {suffix} – целая вечность! ⌛",
                    "Ты планируешь очень далеко вперёд! 🚀",
                    "Когда этот день настанет, ты уже забудешь об этом ожидании! 🤯"
                ]

            # Комментарии по интересной дате
            special_dates = {
                "01.01": "С Новым годом! 🎉",
                "14.02": "День святого Валентина! 💖",
                "29.02": "Ого, это високосный год! Такое бывает раз в 4 года!",
                "01.09": "День знаний! Время в школу или универ!",
                "08.03": "Поздравляем с 8 марта! 🌸",
                "23.02": "С Днём защитника Отечества! 💪"
            }

            date_obj = datetime.strptime(date_str, "%d.%m.%Y")
            date_key = date_obj.strftime("%d.%m")

            if date_key in special_dates:
                phrases.append(special_dates[date_key])

            if date_obj.weekday() == 4 and date_obj.day == 13:
                phrases.append("Пятница, 13-е... Жутковато! 😱")

            return random.choice(phrases)


        def detailed_date_difference(e):
            answer = ''
            if date_converter_drop_mode.value == 'Разница':
                try:
                    d1 = datetime.strptime(date_converter_text_first.value, "%d.%m.%Y")
                    d2 = datetime.strptime(date_converter_text_second.value, "%d.%m.%Y")

                    if d1 > d2:
                        d1, d2 = d2, d1
                    delta = relativedelta(d2, d1)
                    parts = []
                    if delta.years:
                        parts.append(f"{delta.years} {'лет' if 11 <= delta.years % 100 <= 14 else 'год' if delta.years % 10 == 1 else 'года' if 2 <= delta.years % 10 <= 4 else 'лет'}")
                    if delta.months:
                        parts.append(f"{delta.months} {'месяц' if delta.months == 1 else 'месяцев' if delta.months > 4 else 'месяца'}")
                    if delta.days:
                        parts.append(f"{delta.days} {get_day_suffix(delta.days)}")
                    answer = ", ".join(parts) if parts else "0 дней"

                    answer += '\n' + generate_funny_phrase_for_number_of_days(abs((d1 - d2).days))
                    
                    
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат даты")
            else:
                try:
                    date = datetime.strptime(date_converter_text_first.value, "%d.%m.%Y")
                    days_to_add = int(date_converter_text_second.value)
                    delt = timedelta(days=days_to_add)
                    if date_converter_drop_mode.value == 'Добавить дни':
                        new_date = date + delt
                        answer = new_date.strftime("%d.%m.%Y")
                        answer += '\n' + generate_date_comment(new_date.strftime("%d.%m.%Y"), days_to_add)
                    elif date_converter_drop_mode.value == 'Вычесть дни':
                        new_date = date - delt
                        answer = new_date.strftime("%d.%m.%Y")
                        answer += '\n' + generate_date_comment(new_date.strftime("%d.%m.%Y"), days_to_add)
                    else:
                        messagebox.showerror("Ошибка", "Неверный формат данных")
                        
                    
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат данных")
                except ValueError as e:
                    messagebox.showerror("Ошибка", f"Неверный ввод для количества дней: {e}")
            date_converter_answer.value = answer
            page.update()

        date_converter_drop_mode = ft.Dropdown(
            editable=True,
            label="Chose mode",
            value="Разница",
            options=[ft.dropdown.Option('Разница'), ft.dropdown.Option('Добавить дни'), ft.dropdown.Option('Вычесть дни')],
            on_change=date_drop_mode_on_change,
            width=350,
            max_menu_height=80
        )

        date_converter_text_first = ft.TextField(
            label='Date',
            hint_text='дд.мм.гггг',
            autofocus=True,
            width=350,
            height=40
        )

        date_converter_text_second = ft.TextField(
            label='Date',
            hint_text='дд.мм.гггг',
            autofocus=True,
            width=350,
            height=40
        )

        date_converter_answer = ft.Text(
            '',
            size=18,
            selectable=True,
            width=400,
            height=80
        )


        return ft.View(
            "/date_converter_screen",
            controls=[
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    'Калькулятор дат',
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    selectable=True
                                    )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        date_converter_drop_mode,
                                        date_converter_text_first,
                                        date_converter_text_second,
                                        date_converter_answer
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),



                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text='Расчитать',
                                    height=50,
                                    width=300,
                                    on_click=detailed_date_difference
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                change_theme_button,
                                ft.ElevatedButton(
                                    icon=ft.icons.ARROW_BACK,
                                    text='Назад',
                                    on_click=lambda _: page.go("/"),
                                    height=50,
                                    width=200
                                ),
                                always_on_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    spacing=90,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    def mass_converter_screen():                # Страница конвертера масс
        def mass_names():
            mass_units = [
                # Метрическая система
                "Микрограмм",
                "Миллиграмм",
                "Грамм",
                "Килограмм",
                "Центнер",
                "Тонна",

                # Американская система
                "Гран",
                "Драхма",
                "Унция",
                "Фунт",
                "Стоун",
                "Короткая тонна"
            ]
            return [ft.dropdown.Option(x) for x in mass_units]


        def convert_mass(e):
            # Словарь коэффициентов преобразования относительно грамма
            conversion_factors = {
                'Микрограмм': 1e-6,
                'Миллиграмм': 1e-3,
                'Грамм': 1,
                'Килограмм': 1e3,
                'Центнер': 1e5,
                'Тонна': 1e6,
                'Гран': 0.06479891,
                'Драхма': 1.7718451953125,
                'Унция': 28.349523125,
                'Фунт': 453.59237,
                'Стоун': 6350.29318,
                'Короткая тонна': 907184.74
            }
            value = float(mass_converter_text_from.value)
            from_unit = mass_converter_drop_from.value
            to_unit = mass_converter_drop_to.value
            if from_unit not in conversion_factors or to_unit not in conversion_factors:
                messagebox.showerror("Ошибка", "Неверный формат массы")
            
            value_in_grams = value * conversion_factors[from_unit]
            converted_value = value_in_grams / conversion_factors[to_unit]
            mass_converter_text_to.value = round(converted_value, 7)
            page.update()

        

        mass_names_list_options = mass_names()


        mass_converter_text_from = ft.TextField(
            value='1.000',
            autofocus=True,
            width=180,
            height=40
        )
        
        mass_converter_drop_from = ft.Dropdown(
            editable=True,
            label="Единица массы",
            value="Килограмм",
            options=mass_names_list_options,
            width=180,
            max_menu_height=80
        )

        mass_converter_text_to = ft.Text(
            '',
            size=18,
            selectable=True,
            width=180,
            height=40
        )

        mass_converter_drop_to = ft.Dropdown(
            editable=True,
            label="Единица массы",
            value="Тонна",
            options=mass_names_list_options,
            width=180,
            max_menu_height=80
        )
        def mass_converter_swap(e):
            mass_converter_drop_from.value, mass_converter_drop_to.value = mass_converter_drop_to.value, mass_converter_drop_from.value
            mass_converter_text_from.value, mass_converter_text_to.value = mass_converter_text_to.value, mass_converter_text_from.value
            page.update()
        return ft.View(
            "/mass_converter_screen",
            controls=[

                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    'Конвертер масс',
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    selectable=True
                                    )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        mass_converter_drop_from,
                                        mass_converter_text_from
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.IconButton(
                                    icon=ft.icons.SWAP_HORIZ,
                                    icon_size=40,
                                    on_click=mass_converter_swap

                                ),
                                ft.Column(
                                    [
                                        mass_converter_drop_to,
                                        mass_converter_text_to
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),

                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text='Конвертировать',
                                    height=50,
                                    width=300,
                                    on_click=convert_mass
                                    
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                change_theme_button,
                                ft.ElevatedButton(
                                    icon=ft.icons.ARROW_BACK,
                                    text='Назад',
                                    on_click=lambda _: page.go("/"),
                                    height=50,
                                    width=200
                                ),
                                always_on_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    spacing=90,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],


            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
    
    def dist_converter_screen():                # Страница конвертера расстояний
        def dist_names():
            dist_units = [
                # Метрическая система
                "Миллиметр",
                "Сантиметр",
                "Дециметр",
                "Метр",
                "Километр",

                # Американская система
                "Дюйм",
                "Фут",
                "Ярд",
                "Миля"
            ]
            return [ft.dropdown.Option(x) for x in dist_units]


        def convert_dist(e):
            # Словарь коэффициентов преобразования относительно грамма
            conversion_factors = {
                'Миллиметр': 1e-3,
                'Сантиметр': 1e-2,
                'Дециметр': 1e-1,
                'Метр': 1,
                'Километр': 1e3,
                'Дюйм': 0.0254,
                'Фут': 0.3048,
                'Ярд': 0.9144,
                'Миля': 1609.344
            }
            value = float(dist_converter_text_from.value)
            from_unit = dist_converter_drop_from.value
            to_unit = dist_converter_drop_to.value
            if from_unit not in conversion_factors or to_unit not in conversion_factors:
                messagebox.showerror("Ошибка", "Неверный формат массы")
            
            value_in_grams = value * conversion_factors[from_unit]
            converted_value = value_in_grams / conversion_factors[to_unit]
            dist_converter_text_to.value = round(converted_value, 7)
            page.update()

        

        dist_names_list_options = dist_names()


        dist_converter_text_from = ft.TextField(
            value='1.000',
            autofocus=True,
            width=180,
            height=40
        )
        
        dist_converter_drop_from = ft.Dropdown(
            editable=True,
            label="Расстояние",
            value="Метр",
            options=dist_names_list_options,
            width=180,
            max_menu_height=80
        )

        dist_converter_text_to = ft.Text(
            '',
            size=18,
            selectable=True,
            width=180,
            height=40
        )

        dist_converter_drop_to = ft.Dropdown(
            editable=True,
            label="Расстояние",
            value="Сантиметр",
            options=dist_names_list_options,
            width=180,
            max_menu_height=80
        )
        def dist_converter_swap(e):
            dist_converter_drop_from.value, dist_converter_drop_to.value = dist_converter_drop_to.value, dist_converter_drop_from.value
            dist_converter_text_from.value, dist_converter_text_to.value = dist_converter_text_to.value, dist_converter_text_from.value
            page.update()
        return ft.View(
            "/dist_converter_screen",
            controls=[

                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    'Конвертер расстояний',
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    selectable=True
                                    )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        dist_converter_drop_from,
                                        dist_converter_text_from
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.IconButton(
                                    icon=ft.icons.SWAP_HORIZ,
                                    icon_size=40,
                                    on_click=dist_converter_swap

                                ),
                                ft.Column(
                                    [
                                        dist_converter_drop_to,
                                        dist_converter_text_to
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),

                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text='Конвертировать',
                                    height=50,
                                    width=300,
                                    on_click=convert_dist
                                    
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                change_theme_button,
                                ft.ElevatedButton(
                                    icon=ft.icons.ARROW_BACK,
                                    text='Назад',
                                    on_click=lambda _: page.go("/"),
                                    height=50,
                                    width=200
                                ),
                                always_on_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    spacing=90,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],


            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    def system_converter_screen():                # Работа с системами счисления
        
        def system_drop_mode_on_change(e):
            if system_converter_drop_mode.value == 'Конвертация':
                system_scr.controls = [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        'Конвертация систем счисления',
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        selectable=True
                                        )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            system_converter_drop_mode,
                                            ft.Row(
                                                [
                                                    system_converter_text_first,
                                                    system_converter_input
                                                    
                                                ]
                                            ),
                                            ft.Row(
                                                [
                                                    system_converter_text_second,
                                                    system_converter_answer
                                                ]
                                            )
                                            
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),



                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        text='Расчитать',
                                        height=50,
                                        width=300,
                                        on_click=system_converter_get_answer
                                    ),
                                    
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    change_theme_button,
                                    ft.ElevatedButton(
                                        icon=ft.icons.ARROW_BACK,
                                        text='Назад',
                                        on_click=lambda _: page.go("/"),
                                        height=50,
                                        width=200
                                    ),
                                    always_on_button
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        spacing=90,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            elif system_converter_drop_mode.value in ['Сложение', 'Вычитание', 'Умножение']:
                system_scr.controls = [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        'Калькулятор систем счисления',
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        selectable=True
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            system_converter_drop_mode,
                                            ft.Row(
                                                [
                                                    system_converter_text_first,
                                                    system_converter_input
                                                    
                                                ]
                                            ),
                                            ft.Row(
                                                [
                                                    system_converter_text_first_mod,
                                                    system_converter_input_mod
                                                    
                                                ]
                                            ),
                                            ft.Row(
                                                [
                                                    system_converter_text_second,
                                                    system_converter_answer
                                                ]
                                            )
                                            
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),



                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        text='Расчитать',
                                        height=50,
                                        width=300,
                                        on_click=system_converter_get_answer
                                    ),
                                    
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    change_theme_button,
                                    ft.ElevatedButton(
                                        icon=ft.icons.ARROW_BACK,
                                        text='Назад',
                                        on_click=lambda _: page.go("/"),
                                        height=50,
                                        width=200
                                    ),
                                    always_on_button
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        spacing=90,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            else:
                messagebox.showerror("Ошибка", "Такой функции не существует")
                
            page.update()

        def system_converter_to_10(number, system_from):
            try:
                to_int = {
                    '0': 0,
                    '1': 1,
                    '2': 2,
                    '3': 3,
                    '4': 4,
                    '5': 5,
                    '6': 6,
                    '7': 7,
                    '8': 8,
                    '9': 9,
                    'a': 10,
                    'b': 11,
                    'c': 12,
                    'd': 13,
                    'e': 14,
                    'f': 15
                }

                number = number.lower().replace(',', '.')
                if number[0] == '-':
                    number = number[1:]
                    f = True
                else:
                    f = False
                

                if '.' not in number:
                    number += '.0'
                elif number[-1] == '.':
                    number += '0'
                
                int_part, frac_part = number.split('.')
                result = sum(to_int[digit] * (system_from ** i) for i, digit in enumerate(int_part[::-1]))
                
                frac_value = sum(to_int[digit] * (system_from ** -(i + 1)) for i, digit in enumerate(frac_part) if digit != '(')
                if f:
                    return -round(result + frac_value, 5)
                else:
                    return round(result + frac_value, 5)
            except:
                messagebox.showerror("Ошибка", "Неверный формат ввода")
                return 0.0

        def system_converter_from_10(number, system_to):
            to_str = {
                0: '0',
                1: '1',
                2: '2',
                3: '3',
                4: '4',
                5: '5',
                6: '6',
                7: '7',
                8: '8',
                9: '9',
                10: 'a',
                11: 'b',
                12: 'c',
                13: 'd',
                14: 'e',
                15: 'f'
            }
            if (number < 0):
                number = - number
                f = True
            else:
                f = False

            int_part = int(number)
            frac_part = number - int_part  

            int_res = ""
            while int_part:
                int_res = to_str[int_part % system_to] + int_res
                int_part //= system_to
            int_res = int_res or "0"

            frac_res = ""
            precision = 6  # Количество знаков после запятой
            while frac_part and precision:
                frac_part *= system_to
                digit = int(frac_part)
                frac_res += to_str[digit]
                frac_part -= digit
                precision -= 1
            if f:
                return f'-{int_res + ("." + frac_res if frac_res else "")}'
            else:
                return f'{int_res + ("." + frac_res if frac_res else "")}'

        def system_converter_check(value, system):
            value = value.lower()
            if system > 16 or system < 2 or int(system) != system:
                return False
            if '-' in value:
                if value[0] != '-' or value.count('-') != 1:
                    return False
            if value.count('.') > 1:
                return False

            st = '0123456789abcdef'
            for el in value:
                if el != '-' and el != '.' and (el not in st[:system]):
                    return False
            return True


        def system_converter_get_answer(e):
            if system_converter_drop_mode.value == 'Конвертация':
                try:
                    sys_from = int(system_converter_text_first.value)
                    sys_to = int(system_converter_text_second.value)
                    sys_input = system_converter_input.value

                    if not (system_converter_check(sys_input, sys_from) and 2 <= sys_to <= 16):
                        messagebox.showerror("Ошибка", "Неверный формат ввода")
                        return
                    
                    if (sys_from == sys_to):
                        system_converter_answer.value = float(sys_input)
                        page.update()
                        return

                    if (sys_from != 10):
                        sys_input_in_10 = system_converter_to_10(sys_input, sys_from)
                    else:
                        sys_input_in_10 = float(sys_input)
                    
                    if (sys_to == 10):
                        system_converter_answer.value = sys_input_in_10
                    else:
                        sys_output_in_system = system_converter_from_10(sys_input_in_10, sys_to)
                        system_converter_answer.value = sys_output_in_system
                    
                except:
                    messagebox.showerror("Ошибка", "Неверный формат ввода")
                    return
            elif system_converter_drop_mode.value in ['Сложение', 'Вычитание', 'Умножение']:
                try:
                    sys_from = int(system_converter_text_first.value)
                    sys_mod_from = int(int(system_converter_text_first_mod.value))
                    sys_to = int(system_converter_text_second.value)
                    sys_input = system_converter_input.value
                    sys_input_mod = system_converter_input_mod.value

                    if not (2 <= sys_from <= 16 and 2 <= sys_to <= 16 and 2 <= sys_mod_from <= 16):
                        messagebox.showerror("Ошибка", "Неверный формат ввода")
                        return
                    if not (system_converter_check(sys_input, sys_from) and system_converter_check(sys_input_mod, sys_from)):
                        messagebox.showerror("Ошибка", "Неверный формат ввода")
                        return
                    


                    if (sys_from != 10):
                        sys_input_in_10 = system_converter_to_10(sys_input, sys_from)
                    else:
                        sys_input_in_10 = float(sys_input)
                    
                    if (sys_mod_from != 10):
                        sys_input_mod_in_10 = system_converter_to_10(sys_input_mod, sys_mod_from)
                    else:
                        sys_input_mod_in_10 = float(sys_input_mod)
                    
                    if system_converter_drop_mode.value == 'Сложение':
                        sys_answer_in_10 = sys_input_in_10 + sys_input_mod_in_10
                    elif system_converter_drop_mode.value == 'Вычитание':
                        sys_answer_in_10 = sys_input_in_10 - sys_input_mod_in_10
                    else:
                        sys_answer_in_10 = sys_input_in_10 * sys_input_mod_in_10

                    if (sys_to == 10):
                        system_converter_answer.value = sys_answer_in_10
                    else:
                        sys_output_in_system = system_converter_from_10(sys_answer_in_10, sys_to)
                        system_converter_answer.value = sys_output_in_system
                    
                except:
                    messagebox.showerror("Ошибка", "Неверный формат ввода")
                    return
            else:
                messagebox.showerror("Ошибка", "Введенная функция отсутствует в списке")
            page.update()


        system_converter_drop_mode = ft.Dropdown(
            editable=True,
            label="Chose mode",
            value="Конвертация",
            options=[ft.dropdown.Option('Конвертация'), ft.dropdown.Option('Сложение'), ft.dropdown.Option('Вычитание'), ft.dropdown.Option('Умножение')],
            on_change=system_drop_mode_on_change,
            width=350,
            max_menu_height=80
        )

        system_converter_text_first = ft.TextField(
            label='system',
            hint_text='',
            autofocus=True,
            width=90,
            height=40
        )
        
        system_converter_input = ft.TextField(
            label='number',
            hint_text='',
            autofocus=True,
            width=250,
            height=40
        )

        system_converter_text_first_mod = ft.TextField(
            label='system',
            hint_text='',
            autofocus=True,
            width=90,
            height=40
        )
        
        system_converter_input_mod = ft.TextField(
            label='number',
            hint_text='',
            autofocus=True,
            width=250,
            height=40
        )

        system_converter_text_second = ft.TextField(
            label='system',
            hint_text='',
            autofocus=True,
            width=90,
            height=40
        )

        system_converter_answer = ft.Text(
            '  answer',
            size=18,
            selectable=True,
            width=250,
            height=40
        )


        system_scr = ft.View(
            "/system_converter_screen",
            controls=[
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    'Конвертация систем счисления',
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    selectable=True
                                    )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        system_converter_drop_mode,
                                        ft.Row(
                                            [
                                                system_converter_text_first,
                                                system_converter_input
                                                
                                            ]
                                        ),
                                        ft.Row(
                                            [
                                                system_converter_text_second,
                                                system_converter_answer
                                            ]
                                        )
                                        
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),



                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text='Расчитать',
                                    height=50,
                                    width=300,
                                    on_click=system_converter_get_answer
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                change_theme_button,
                                ft.ElevatedButton(
                                    icon=ft.icons.ARROW_BACK,
                                    text='Назад',
                                    on_click=lambda _: page.go("/"),
                                    height=50,
                                    width=200
                                ),
                                always_on_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    spacing=90,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        return system_scr



    # Первая страница + обработчик страниц
    page.on_route_change = route_change
    page.go("/")

ft.app(target=main, view=ft.FLET_APP)
