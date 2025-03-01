import flet as ft
import requests
import xml.etree.ElementTree as ET

# Функция для получения списка валют с сайта ЦБ РФ
def get_currency_list():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)

    if response.status_code == 200:
        xml_data = response.content
        tree = ET.fromstring(xml_data)
        currencies = ["Российский рубль"]

        for valute in tree.findall("Valute"):
            name = valute.find("Name").text
            currencies.append(name)

        return currencies
    else:
        return ["Ошибка загрузки данных"]

# Функция для получения курса валюты
def get_exchange_rate(currency_name):
    if currency_name == "Российский рубль":
        return 1.0

    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)

    if response.status_code == 200:
        xml_data = response.content
        tree = ET.fromstring(xml_data)

        for valute in tree.findall("Valute"):
            name = valute.find("Name").text
            if name == currency_name:
                nominal = int(valute.find("Nominal").text)
                value = float(valute.find("Value").text.replace(",", "."))
                return nominal / value  # Сколько валюты за 1 рубль

    return 0.0  # В случае ошибки


# Главная функция Flet
def main(page: ft.Page):
    page.title = "Калькулятор"
    page.window_width = 800
    page.window_height = 600

    # Переключение экранов
    def show_main():
        page.controls.clear()
        page.add(
            ft.Text("Дополнения к калькулятору", size=30, weight="bold"),
            ft.ElevatedButton("Конвертер валют", on_click=lambda _: show_currency_converter()),
            ft.ElevatedButton("Конвертер массы", on_click=lambda _: page.snack_bar(ft.SnackBar(ft.Text("Пока не реализовано"))))
        )
        page.update()

    # Экран конвертера валют
    def show_currency_converter():
        page.controls.clear()
        currencies = get_currency_list()

        # Выпадающие списки
        currency_from = ft.Dropdown(options=[ft.dropdown.Option(c) for c in currencies], value="Российский рубль")
        currency_to = ft.Dropdown(options=[ft.dropdown.Option(c) for c in currencies], value="Доллар США")

        # Поле ввода и кнопка
        amount_input = ft.TextField(value="1", label="Введите сумму")
        result_text = ft.Text("")

        def convert_currency(e):
            try:
                amount = float(amount_input.value)
                rate_from = get_exchange_rate(currency_from.value)
                rate_to = get_exchange_rate(currency_to.value)
                converted = round(amount * (rate_to / rate_from), 2)
                result_text.value = f"{converted} {currency_to.value}"
                page.update()
            except ValueError:
                result_text.value = "Ошибка ввода!"
                page.update()

        page.add(
            ft.Text("Конвертер валют", size=24, weight="bold"),
            currency_from,
            currency_to,
            amount_input,
            ft.ElevatedButton("Конвертировать", on_click=convert_currency),
            result_text,
            ft.ElevatedButton("Назад", on_click=lambda _: show_main())
        )
        page.update()

    show_main()  # Показываем главное меню при запуске

ft.app(target=main)
