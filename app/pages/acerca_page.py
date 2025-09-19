import flet as ft
from .base_page import BasePage


class AcercaPage(BasePage):
    def __init__(self,page: ft.Page = None):
        super().__init__(page)
        self.title = "Acerca de"
        self.description = "Información sobre la aplicación"

    def build(self):
        header = self.create_header(
            "Herramientas de PDF",
            "Versión 1.0.0"
        )

        # Información de la app
        app_info = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.CircleAvatar(
                        content=ft.Icon(ft.Icons.PICTURE_AS_PDF, size=40),
                        radius=40,
                        bgcolor=ft.Colors.PRIMARY
                    ),
                    ft.Text(
                        "Herramientas de PDF",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Una aplicación simple y eficiente para trabajar con archivos PDF. "
                        "Separa y une documentos PDF con facilidad.",
                        text_align=ft.TextAlign.CENTER,
                        size=14
                    ),
                    ft.Divider(),
                    ft.Text("Desarrollado con Flet y Python",
                            style=ft.TextThemeStyle.BODY_SMALL),
                    ft.Text("© 2024 - Todos los derechos reservados a raulanto",
                            style=ft.TextThemeStyle.BODY_SMALL),
                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15),
                padding=30
            )
        )

        # Enlaces útiles
        links = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Enlaces útiles", weight=ft.FontWeight.BOLD),
                    ft.TextButton("Documentación", icon=ft.Icons.HELP),
                    ft.TextButton("Reportar un error", icon=ft.Icons.BUG_REPORT),
                    ft.TextButton("Código fuente", icon=ft.Icons.CODE),
                ], spacing=5),
                padding=20
            )
        )

        return ft.Container(
            content=ft.Column([
                header,
                ft.Divider(),
                app_info,
                links
            ], spacing=20),
            padding=20
        )