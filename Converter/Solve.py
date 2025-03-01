import flet as ft

def main(page: ft.Page):
    page.title = "Конвертер"
    page.theme_mode = 'light'
    

    # Функция смены страницы
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(main_screen())
        elif page.route == "/valute_converter_screen":
            page.views.append(valute_converter_screen())

        page.update()

    # Главная страница
    def main_screen():
        return ft.View(
            "/",
            controls=[
                ft.Row(
                    [
                        ft.Text("Главная страница", size=30, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Конвертер длины", on_click=lambda _: page.go("/valute_converter_screen")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
        )

    # Страница конвертера длины
    def valute_converter_screen():
        return ft.View(
            "/valute_converter_screen",
            controls=[
                ft.Text("Конвертер длины", size=30, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("На главную", on_click=lambda _: page.go("/")),
            ],
        )

    # Устанавливаем обработчик маршрутов
    page.on_route_change = route_change
    page.go("/")  # Открываем главную страницу

ft.app(target=main, view=ft.FLET_APP)
