import flet as ft
from app.components.layout import MainLayout
from app.utils.config_manager import config_manager


def main(page: ft.Page):
    """Función principal de la aplicación"""
    # Aplicar configuración inicial desde el gestor
    page.title = "Herramientas de PDF"
    page.theme_mode = config_manager.get_theme_mode()
    page.padding = 0

    # Aplicar tamaño de ventana desde configuración
    page.window_width = config_manager.get("general", "window_width", 1200)
    page.window_height = config_manager.get("general", "window_height", 800)

    # Configurar ventana
    page.window_resizable = True
    page.window_minimizable = True
    page.window_maximizable = True

    # Crear e inicializar el layout principal
    layout = MainLayout(page)
    layout.build()

    # Guardar tamaño de ventana al cerrar (si es posible)
    def on_window_event(e):
        if e.data == "close":
            # Guardar configuración final antes de cerrar
            config_manager.save_config()

    page.window_prevent_close = False

    # Aplicar configuración de interfaz
    if config_manager.get("ui", "show_tooltips", True):
        # Los tooltips ya están configurados en los controles
        pass


if __name__ == "__main__":
    ft.app(main)
