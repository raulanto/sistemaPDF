import flet as ft


class SnackBarManager:
    """Gestor centralizado para SnackBars"""

    @staticmethod
    def show_success(page, message, action="OK"):
        """Muestra SnackBar de éxito"""
        if page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.GREEN,
                action=action
            )
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()

    @staticmethod
    def show_error(page, message, action="CERRAR"):
        """Muestra SnackBar de error"""
        if page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED,
                action=action
            )
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()

    @staticmethod
    def show_info(page, message, action="OK", duration=3000):
        """Muestra SnackBar informativo"""
        if page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.BLUE,
                action=action,
                duration=duration
            )
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()

    @staticmethod
    def show_warning(page, message, action="ENTENDIDO"):
        """Muestra SnackBar de advertencia"""
        if page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.ORANGE,
                action=action
            )
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()
