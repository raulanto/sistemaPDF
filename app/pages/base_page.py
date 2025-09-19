# Estos métodos deben estar en la clase BasePage (base_page.py)

import flet as ft


class BasePage:
    def __init__(self, page=None):
        self.page = page

    def create_header(self, title, description):
        """Crea el header de la página"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=28, weight=ft.FontWeight.BOLD),
                ft.Text(description, size=14, color=ft.Colors.ON_SURFACE_VARIANT)
            ], spacing=5),
            padding=ft.padding.only(bottom=10)
        )

    def create_scrollable_content(self, content_elements, padding=10):
        """Crea un contenedor scrollable con el contenido"""
        return ft.Container(
            content=ft.Column(
                controls=content_elements,
                scroll=ft.ScrollMode.AUTO,
                spacing=20
            ),
            padding=padding,
            expand=True
        )