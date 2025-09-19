import flet as ft
from app.pages.separar_page import SepararPage
from app.pages.unir_page import UnirPage
from app.pages.configuracion_page import ConfiguracionPage
from app.pages.acerca_page import AcercaPage
from app.utils.config_manager import config_manager


class MainLayout:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_index = 0

        # Aplicar configuración inicial
        self._apply_initial_config()

        # Inicializar páginas pasando la referencia de page
        self.pages = {
            0: SepararPage(page),
            1: UnirPage(page),
            2: ConfiguracionPage(page),
            3: AcercaPage(page)
        }

        # Contenedor para el contenido principal
        self.content_area = ft.Column(
            controls=[self.pages[0].build()],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        )

    def _apply_initial_config(self):
        """Aplica la configuración inicial a la página"""
        # Aplicar tema
        self.page.theme_mode = config_manager.get_theme_mode()

        # Aplicar tamaño de ventana - aumentado para mejor visualización
        window_width = config_manager.get("general", "window_width", 1400)
        window_height = config_manager.get("general", "window_height", 900)
        self.page.window_width = window_width
        self.page.window_height = window_height

        # Otras configuraciones de página
        self.page.title = "Herramientas de PDF"
        self.page.padding = 0

    def build(self):
        """Construye el layout principal"""
        # AppBar
        self.page.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.PICTURE_AS_PDF),
            leading_width=40,
            title=ft.Text("Herramientas de PDF"),
            center_title=False,
            actions=[
                ft.IconButton(
                    ft.Icons.WB_SUNNY_OUTLINED,
                    tooltip="Cambiar tema",
                    on_click=self.toggle_theme
                ),
            ],
        )

        # Navigation Rail
        rail = ft.NavigationRail(
            selected_index=self.selected_index,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.FloatingActionButton(
                icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
                text="Nuevo",
                on_click=self.fab_clicked
            ),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.CONTENT_CUT_OUTLINED,
                    selected_icon=ft.Icons.CONTENT_CUT,
                    label="Separar PDF",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.MERGE_TYPE_OUTLINED,
                    selected_icon=ft.Icons.MERGE_TYPE,
                    label="Unir PDF",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Configuración",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INFO_OUTLINE,
                    selected_icon=ft.Icons.INFO,
                    label="Acerca de",
                ),
            ],
            on_change=self.navigation_changed,
        )

        # Layout principal
        main_row = ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                self.content_area,
            ],
            expand=True,
        )

        self.page.add(main_row)
        self.page.update()

    def navigation_changed(self, e):
        """Maneja el cambio de navegación"""
        self.selected_index = e.control.selected_index

        # Limpiar contenido actual
        self.content_area.controls.clear()

        # Agregar nueva página
        new_page = self.pages[self.selected_index]
        self.content_area.controls.append(new_page.build())

        self.page.update()

    def fab_clicked(self, e):
        """Maneja el click del FloatingActionButton"""
        # Si ya estamos en separar PDF, limpiar el formulario
        if self.selected_index == 0:
            if hasattr(self.pages[0], 'clear_form'):
                self.pages[0].clear_form()
                # Reconstruir la página
                self.content_area.controls.clear()
                self.content_area.controls.append(self.pages[0].build())
        else:
            # Ir a la página de separar PDF
            self.selected_index = 0
            self.content_area.controls.clear()
            self.content_area.controls.append(self.pages[0].build())

        self.page.update()

    def toggle_theme(self, e):
        """Cambia el tema usando el gestor de configuración"""
        new_theme = config_manager.toggle_theme()
        self.page.theme_mode = new_theme
        self.page.update()