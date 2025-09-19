import flet as ft
from .base_page import BasePage
from app.utils.config_manager import config_manager


class ConfiguracionPage(BasePage):
    def __init__(self, page: ft.Page = None):
        super().__init__(page)
        self.title = "Configuración"
        self.description = "Ajustes de la aplicación"

        # Referencias a controles
        self.controls = {}
        self.has_changes = False

    def build(self):
        header = self.create_header(
            "Configuración",
            "Personaliza el comportamiento de la aplicación"
        )

        # Configuraciones generales
        general_config = self._create_general_config()

        # Configuraciones de PDF
        pdf_config = self._create_pdf_config()

        # Configuraciones de rutas
        paths_config = self._create_paths_config()

        # Configuraciones de interfaz
        ui_config = self._create_ui_config()

        # Configuraciones avanzadas (nueva sección)
        advanced_config = self._create_advanced_config()

        # Información del sistema
        system_info = self._create_system_info()

        # Botones de acción
        action_buttons = self._create_action_buttons()

        # Indicador de cambios
        self.changes_indicator = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO, color=ft.Colors.ORANGE),
                ft.Text("Hay cambios sin guardar", color=ft.Colors.ORANGE)
            ]),
            visible=False,
            margin=ft.margin.symmetric(vertical=10)
        )

        # Lista de elementos para hacer scrolleable
        content_elements = [
            header,
            ft.Divider(),
            self.changes_indicator,
            general_config,
            pdf_config,
            paths_config,
            ui_config,
            advanced_config,  # Sección adicional
            system_info,  # Información del sistema
            action_buttons
        ]

        # Usar el método de la clase base para hacer scrolleable
        return self.create_scrollable_content(content_elements, padding=20)

    def _create_advanced_config(self):
        """Crea una sección de configuración avanzada adicional"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("🔧 Configuración Avanzada", size=18, weight=ft.FontWeight.BOLD),

                    ft.TextField(
                        label="Prefijo personalizado para archivos",
                        value="mi_documento",
                        helper_text="Prefijo que se agregará a todos los archivos generados"
                    ),

                    ft.Dropdown(
                        label="Algoritmo de compresión",
                        options=[
                            ft.dropdown.Option("ZIP_DEFLATED", "Deflate (recomendado)"),
                            ft.dropdown.Option("ZIP_STORED", "Sin compresión"),
                            ft.dropdown.Option("ZIP_BZIP2", "BZip2"),
                            ft.dropdown.Option("ZIP_LZMA", "LZMA"),
                        ],
                        value="ZIP_DEFLATED"
                    ),

                    ft.Row([
                        ft.Text("Número de hilos para procesamiento:"),
                        ft.Slider(
                            min=1,
                            max=8,
                            divisions=7,
                            value=4,
                            label="4 hilos"
                        )
                    ]),

                    ft.Switch(label="Modo debug habilitado", value=False),
                    ft.Switch(label="Guardar logs de procesamiento", value=True),
                    ft.Switch(label="Notificaciones del sistema", value=True),

                ], spacing=15),
                padding=20
            )
        )

    def _create_system_info(self):
        """Crea una sección con información del sistema"""
        import platform
        import os

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("💻 Información del Sistema", size=18, weight=ft.FontWeight.BOLD),

                    ft.Row([
                        ft.Text("Sistema Operativo:", weight=ft.FontWeight.W_500),
                        ft.Text(platform.system())
                    ]),

                    ft.Row([
                        ft.Text("Versión:", weight=ft.FontWeight.W_500),
                        ft.Text(platform.release())
                    ]),

                    ft.Row([
                        ft.Text("Arquitectura:", weight=ft.FontWeight.W_500),
                        ft.Text(platform.machine())
                    ]),

                    ft.Row([
                        ft.Text("Usuario:", weight=ft.FontWeight.W_500),
                        ft.Text(os.getenv('USERNAME') or os.getenv('USER') or 'Desconocido')
                    ]),

                    ft.Divider(),

                    ft.Text("📁 Rutas del sistema:", weight=ft.FontWeight.W_500),
                    ft.Text(f"Configuración: {config_manager.config_file}",
                            size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Text(f"Directorio home: {str(config_manager.config_dir)}",
                            size=12, color=ft.Colors.ON_SURFACE_VARIANT),

                ], spacing=10),
                padding=20
            )
        )

    def _create_general_config(self):
        """Crea la sección de configuración general"""
        self.controls["dark_mode"] = ft.Switch(
            label="Modo oscuro",
            value=config_manager.get("general", "dark_mode", False),
            on_change=self._on_dark_mode_change
        )

        self.controls["confirm_delete"] = ft.Switch(
            label="Confirmación antes de eliminar",
            value=config_manager.get("general", "confirm_delete", True),
            on_change=self._mark_changes
        )

        self.controls["open_folder"] = ft.Switch(
            label="Abrir carpeta después de procesar",
            value=config_manager.get("general", "open_folder_after_process", True),
            on_change=self._mark_changes
        )

        self.controls["auto_save"] = ft.Switch(
            label="Guardar configuración automáticamente",
            value=config_manager.get("general", "auto_save_config", True),
            on_change=self._mark_changes
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("🔧 General", size=18, weight=ft.FontWeight.BOLD),
                    self.controls["dark_mode"],
                    self.controls["confirm_delete"],
                    self.controls["open_folder"],
                    self.controls["auto_save"],
                ], spacing=10),
                padding=20
            )
        )

    def _create_pdf_config(self):
        """Crea la sección de configuración PDF"""
        self.controls["compression"] = ft.Dropdown(
            label="Calidad de compresión",
            options=[
                ft.dropdown.Option("Alta", "Alta"),
                ft.dropdown.Option("Media", "Media"),
                ft.dropdown.Option("Baja", "Baja"),
            ],
            value=config_manager.get("pdf", "compression_quality", "Media"),
            on_change=self._mark_changes
        )

        self.controls["keep_metadata"] = ft.Switch(
            label="Mantener metadatos originales",
            value=config_manager.get("pdf", "keep_metadata", True),
            on_change=self._mark_changes
        )

        self.controls["optimize_web"] = ft.Switch(
            label="Optimizar para web",
            value=config_manager.get("pdf", "optimize_for_web", False),
            on_change=self._mark_changes
        )

        self.controls["default_format"] = ft.TextField(
            label="Formato de nombre por defecto",
            value=config_manager.get("pdf", "default_output_format", "pagina_{:03d}"),
            helper_text="Usa {:03d} para numeración",
            on_change=self._mark_changes
        )

        self.controls["create_zip"] = ft.Switch(
            label="Crear ZIP por defecto",
            value=config_manager.get("pdf", "create_zip_by_default", True),
            on_change=self._mark_changes
        )

        self.controls["max_size"] = ft.TextField(
            label="Tamaño máximo de archivo (MB)",
            value=str(config_manager.get("pdf", "max_file_size_mb", 100)),
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._mark_changes
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📄 Configuración PDF", size=18, weight=ft.FontWeight.BOLD),
                    self.controls["compression"],
                    self.controls["keep_metadata"],
                    self.controls["optimize_web"],
                    self.controls["default_format"],
                    self.controls["create_zip"],
                    self.controls["max_size"],
                ], spacing=10),
                padding=20
            )
        )

    def _create_paths_config(self):
        """Crea la sección de configuración de rutas"""
        self.controls["default_output"] = ft.TextField(
            label="Carpeta de salida por defecto",
            value=config_manager.get("paths", "default_output_folder", ""),
            helper_text="Deja vacío para usar la carpeta del archivo original",
            on_change=self._mark_changes,
            expand=True
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📁 Rutas y Carpetas", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.controls["default_output"],
                        ft.ElevatedButton(
                            "Examinar",
                            icon=ft.Icons.FOLDER,
                            on_click=self._pick_default_folder
                        )
                    ]),
                ], spacing=10),
                padding=20
            )
        )

    def _create_ui_config(self):
        """Crea la sección de configuración de interfaz"""
        self.controls["language"] = ft.Dropdown(
            label="Idioma",
            options=[
                ft.dropdown.Option("es", "Español"),
                ft.dropdown.Option("en", "English"),
            ],
            value=config_manager.get("ui", "language", "es"),
            on_change=self._mark_changes
        )

        self.controls["show_tooltips"] = ft.Switch(
            label="Mostrar ayudas emergentes",
            value=config_manager.get("ui", "show_tooltips", True),
            on_change=self._mark_changes
        )

        self.controls["animations"] = ft.Switch(
            label="Animaciones habilitadas",
            value=config_manager.get("ui", "animation_enabled", True),
            on_change=self._mark_changes
        )

        self.controls["compact_mode"] = ft.Switch(
            label="Modo compacto",
            value=config_manager.get("ui", "compact_mode", False),
            on_change=self._mark_changes
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("🎨 Interfaz de Usuario", size=18, weight=ft.FontWeight.BOLD),
                    self.controls["language"],
                    self.controls["show_tooltips"],
                    self.controls["animations"],
                    self.controls["compact_mode"],
                ], spacing=10),
                padding=20
            )
        )

    def _create_action_buttons(self):
        """Crea los botones de acción"""
        return ft.Row([
            ft.ElevatedButton(
                "Guardar configuración",
                icon=ft.Icons.SAVE,
                on_click=self.save_config
            ),
            ft.OutlinedButton(
                "Restablecer por defecto",
                icon=ft.Icons.RESTORE,
                on_click=self._reset_to_defaults
            ),
            ft.OutlinedButton(
                "Cancelar cambios",
                icon=ft.Icons.CANCEL,
                on_click=self._cancel_changes
            )
        ], alignment=ft.MainAxisAlignment.START)

    def _on_dark_mode_change(self, e):
        """Maneja el cambio de tema inmediatamente"""
        # Aplicar tema inmediatamente
        if self.page:
            self.page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
            self.page.update()

        # Marcar cambios
        self._mark_changes(e)

    def _mark_changes(self, e=None):
        """Marca que hay cambios pendientes"""
        self.has_changes = True
        if hasattr(self, 'changes_indicator'):
            self.changes_indicator.visible = True
            if self.page:
                self.page.update()

    def _pick_default_folder(self, e):
        """Selecciona carpeta de salida por defecto"""

        def folder_picker_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.controls["default_output"].value = e.path
                self._mark_changes()
                if self.page:
                    self.page.update()

        folder_picker = ft.FilePicker(on_result=folder_picker_result)
        self.page.overlay.append(folder_picker)
        self.page.update()
        folder_picker.get_directory_path(dialog_title="Carpeta de salida por defecto")

    def _reset_to_defaults(self, e):
        """Resetea a configuración por defecto"""

        def confirm_reset(e):
            if e.control.text == "Sí":
                config_manager.reset_to_defaults()
                self._reload_controls()
                self.has_changes = False
                self.changes_indicator.visible = False
                self._show_success_message("Configuración restablecida")
            dialog.open = False
            if self.page:
                self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar restablecimiento"),
            content=ft.Text(
                "¿Estás seguro de que quieres restablecer toda la configuración a los valores por defecto?"),
            actions=[
                ft.TextButton("Sí", on_click=confirm_reset),
                ft.TextButton("No", on_click=confirm_reset),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _cancel_changes(self, e):
        """Cancela los cambios y recarga valores originales"""
        self._reload_controls()
        self.has_changes = False
        self.changes_indicator.visible = False
        if self.page:
            self.page.update()

    def _reload_controls(self):
        """Recarga los controles con los valores de configuración"""
        # Recargar configuración
        config_manager.load_config()

        # Actualizar controles
        self.controls["dark_mode"].value = config_manager.get("general", "dark_mode", False)
        self.controls["confirm_delete"].value = config_manager.get("general", "confirm_delete", True)
        self.controls["open_folder"].value = config_manager.get("general", "open_folder_after_process", True)
        self.controls["auto_save"].value = config_manager.get("general", "auto_save_config", True)

        self.controls["compression"].value = config_manager.get("pdf", "compression_quality", "Media")
        self.controls["keep_metadata"].value = config_manager.get("pdf", "keep_metadata", True)
        self.controls["optimize_web"].value = config_manager.get("pdf", "optimize_for_web", False)
        self.controls["default_format"].value = config_manager.get("pdf", "default_output_format", "pagina_{:03d}")
        self.controls["create_zip"].value = config_manager.get("pdf", "create_zip_by_default", True)
        self.controls["max_size"].value = str(config_manager.get("pdf", "max_file_size_mb", 100))

        self.controls["default_output"].value = config_manager.get("paths", "default_output_folder", "")

        self.controls["language"].value = config_manager.get("ui", "language", "es")
        self.controls["show_tooltips"].value = config_manager.get("ui", "show_tooltips", True)
        self.controls["animations"].value = config_manager.get("ui", "animation_enabled", True)
        self.controls["compact_mode"].value = config_manager.get("ui", "compact_mode", False)

        # Aplicar tema
        if self.page:
            self.page.theme_mode = config_manager.get_theme_mode()
    ##
    def _show_success_message(self, message):
        """Muestra mensaje de éxito (método corregido)"""
        if self.page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.GREEN,
                action="OK"
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()

    def _show_error_message(self, message):
        """Muestra mensaje de error (método corregido)"""
        if self.page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED,
                action="CERRAR"
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()

    def _show_info_message(self, message):
        """Muestra mensaje informativo"""
        if self.page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.BLUE,
                action="OK",
                duration=2000
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()

    def save_config(self, e=None):
        """Guarda toda la configuración (método mejorado)"""
        try:
            # Validar datos antes de guardar
            try:
                max_size = int(self.controls["max_size"].value)
                if max_size < 0:
                    raise ValueError("El tamaño máximo no puede ser negativo")
            except ValueError:
                self._show_error_message("El tamaño máximo debe ser un número válido")
                return

            # Validar formato de nombre
            try:
                test_format = self.controls["default_format"].value.format(1)
                if not test_format:
                    raise ValueError("Formato inválido")
            except:
                self._show_error_message("El formato de nombre es inválido. Debe contener {} o {:03d}")
                return

            # Actualizar configuración general
            config_manager.set("general", "dark_mode", self.controls["dark_mode"].value)
            config_manager.set("general", "confirm_delete", self.controls["confirm_delete"].value)
            config_manager.set("general", "open_folder_after_process", self.controls["open_folder"].value)
            config_manager.set("general", "auto_save_config", self.controls["auto_save"].value)

            # Actualizar configuración PDF
            config_manager.set("pdf", "compression_quality", self.controls["compression"].value)
            config_manager.set("pdf", "keep_metadata", self.controls["keep_metadata"].value)
            config_manager.set("pdf", "optimize_for_web", self.controls["optimize_web"].value)
            config_manager.set("pdf", "default_output_format", self.controls["default_format"].value)
            config_manager.set("pdf", "create_zip_by_default", self.controls["create_zip"].value)
            config_manager.set("pdf", "max_file_size_mb", max_size)

            # Actualizar rutas
            config_manager.set("paths", "default_output_folder", self.controls["default_output"].value)

            # Actualizar interfaz
            config_manager.set("ui", "language", self.controls["language"].value)
            config_manager.set("ui", "show_tooltips", self.controls["show_tooltips"].value)
            config_manager.set("ui", "animation_enabled", self.controls["animations"].value)
            config_manager.set("ui", "compact_mode", self.controls["compact_mode"].value)

            # Forzar guardado
            if config_manager.save_config():
                self.has_changes = False
                self.changes_indicator.visible = False
                self._show_success_message("Configuración guardada exitosamente")
            else:
                self._show_error_message("Error al guardar la configuración")

        except Exception as ex:
            self._show_error_message(f"Error inesperado: {str(ex)}")
