import os
import threading
import flet as ft
from app.utils.config_manager import config_manager
from app.utils.pdf_processor import dividir_pdf_optimizado, estimar_tiempo_procesamiento
from .base_page import BasePage


class SepararPage(BasePage):
    def __init__(self, page=None):
        super().__init__(page)
        self.title = "Separar PDF"
        self.description = "Separa páginas de un archivo PDF"
        self.selected_file = None
        self.output_folder = None
        self.is_processing = False
        self.total_pages = 0

        # Referencias a controles
        self.file_text = None
        self.folder_text = None
        self.progress_bar = None
        self.progress_text = None
        self.format_field = None
        self.create_zip_switch = None
        self.separate_button = None
        self.result_container = None

        # Nuevos controles para optimización
        self.batch_size_field = None
        self.workers_field = None
        self.page_range_start = None
        self.page_range_end = None
        self.use_page_range = None
        self.estimation_text = None

    def build(self):
        header = self.create_header(
            "Separar PDF",
            "Separa páginas de un archivo PDF (optimizado para archivos grandes)"
        )

        default_format = config_manager.get("pdf", "default_output_format", "pagina_{:03d}")
        default_zip = config_manager.get("pdf", "create_zip_by_default", True)

        # Sección de selección de archivo
        self.file_text = ft.Text(
            "Ningún archivo seleccionado",
            color=ft.Colors.ON_SURFACE_VARIANT
        )

        file_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📁 Archivo PDF", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton(
                            "Examinar archivo",
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=self.pick_file
                        ),
                        ft.Container(
                            content=self.file_text,
                            expand=True,
                            padding=ft.padding.only(left=10)
                        )
                    ]),
                    # Información del archivo
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Información del archivo:",
                                    weight=ft.FontWeight.W_500,
                                    size=14),
                            ft.Text("", key="file_info", size=12,
                                    color=ft.Colors.ON_SURFACE_VARIANT)
                        ], spacing=5),
                        visible=False,
                        key="info_container"
                    )
                ], spacing=10),
                padding=20
            )
        )

        # Sección de rango de páginas (NUEVO)
        self.use_page_range = ft.Checkbox(
            label="Extraer solo un rango específico de páginas",
            value=False,
            on_change=self.toggle_page_range
        )

        self.page_range_start = ft.TextField(
            label="Página inicial",
            hint_text="1",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            disabled=True
        )

        self.page_range_end = ft.TextField(
            label="Página final",
            hint_text="Última",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            disabled=True
        )

        page_range_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(" Rango de páginas", size=16, weight=ft.FontWeight.BOLD),
                    self.use_page_range,
                    ft.Row([
                        self.page_range_start,
                        ft.Text("hasta", size=14),
                        self.page_range_end,
                    ], spacing=10),
                    ft.Text(
                        " Útil para archivos muy grandes. Deja vacío para procesar todas.",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT
                    )
                ], spacing=10),
                padding=20
            )
        )

        # Sección de configuración avanzada (MEJORADA)
        default_output_folder = config_manager.get("paths", "default_output_folder", "")
        self.folder_text = ft.Text(
            default_output_folder or "Se creará automáticamente",
            color=ft.Colors.ON_SURFACE_VARIANT
        )

        self.format_field = ft.TextField(
            label="Formato de nombre",
            hint_text=default_format,
            value=default_format,
            helper_text="Usa {:03d} para numeración con ceros",
            expand=True
        )

        self.create_zip_switch = ft.Switch(
            label="Crear archivo ZIP",
            value=default_zip,
            on_change=self.update_estimation
        )

        # Campos de optimización (NUEVO)
        self.batch_size_field = ft.TextField(
            label="Tamaño de lote",
            hint_text="1000",
            value="1000",
            helper_text="Páginas por lote (mayor = más memoria, menor = más lento)",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        self.workers_field = ft.TextField(
            label="Procesos paralelos",
            hint_text="Auto",
            value="",
            helper_text="Dejar vacío para detección automática (CPU cores - 1)",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        config_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Configuración", size=16, weight=ft.FontWeight.BOLD),

                    # Carpeta de salida
                    ft.Text("Carpeta de destino:", weight=ft.FontWeight.W_500),
                    ft.Row([
                        ft.ElevatedButton(
                            "Cambiar carpeta",
                            icon=ft.Icons.FOLDER,
                            on_click=self.pick_folder
                        ),
                        ft.Container(
                            content=self.folder_text,
                            expand=True,
                            padding=ft.padding.only(left=10)
                        )
                    ]),

                    ft.Divider(),

                    # Formato de nombre
                    ft.Text("Formato de nombres:", weight=ft.FontWeight.W_500),
                    self.format_field,

                    ft.Divider(),

                    # Opciones de optimización
                    ft.Text("⚡ Optimización (para archivos grandes):",
                            weight=ft.FontWeight.W_500),
                    ft.Row([
                        self.batch_size_field,
                        self.workers_field,
                    ], spacing=15),

                    ft.Divider(),

                    # Opciones adicionales
                    ft.Text("Opciones:", weight=ft.FontWeight.W_500),
                    self.create_zip_switch,

                    # Advertencia para archivos grandes
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.WARNING, color=ft.Colors.ORANGE, size=20),
                            ft.Text(
                                "Para PDFs >50k páginas, considera desactivar el ZIP",
                                size=12,
                                color=ft.Colors.ORANGE
                            )
                        ]),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE),
                        padding=10,
                        border_radius=8,
                        visible=False,
                        key="large_file_warning"
                    )

                ], spacing=15),
                padding=20
            )
        )

        # Estimación de tiempo (NUEVO)
        self.estimation_text = ft.Text(
            "",
            size=12,
            color=ft.Colors.BLUE,
            visible=False
        )

        estimation_section = ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.SCHEDULE, color=ft.Colors.BLUE, size=20),
                            ft.Text("Estimación de tiempo",
                                    size=14,
                                    weight=ft.FontWeight.BOLD)
                        ]),
                        self.estimation_text
                    ], spacing=10),
                    padding=15
                )
            ),
            visible=False,
            key="estimation_container"
        )

        # Sección de progreso
        self.progress_bar = ft.ProgressBar(
            width=400,
            color="amber",
            bgcolor="#eeeeee",
            visible=False
        )

        self.progress_text = ft.Text("", size=12, visible=False)

        progress_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📈 Progreso", size=16, weight=ft.FontWeight.BOLD),
                    self.progress_bar,
                    self.progress_text
                ], spacing=10),
                padding=20
            )
        )

        # Botones de acción
        self.separate_button = ft.ElevatedButton(
            "Separar PDF",
            icon=ft.Icons.CONTENT_CUT,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PRIMARY,
                color=ft.Colors.ON_PRIMARY
            ),
            on_click=self.separate_pdf,
            disabled=True
        )

        action_buttons = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("🚀 Acciones", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.separate_button,
                        ft.OutlinedButton(
                            "Limpiar",
                            icon=ft.Icons.CLEAR,
                            on_click=self.clear_form
                        ),
                    ], alignment=ft.MainAxisAlignment.START)
                ], spacing=10),
                padding=20
            )
        )

        # Sección de resultados
        self.result_container = ft.Container(
            visible=False,
            margin=ft.margin.only(top=20)
        )

        # Lista de elementos
        content_elements = [
            header,
            ft.Divider(),
            file_section,
            page_range_section,
            config_section,
            estimation_section,
            progress_section,
            action_buttons,
            self.result_container,
        ]

        return self.create_scrollable_content(content_elements, padding=20)

    def toggle_page_range(self, e):
        """Activa/desactiva los campos de rango de páginas"""
        enabled = self.use_page_range.value
        self.page_range_start.disabled = not enabled
        self.page_range_end.disabled = not enabled
        self.page.update()
        self.update_estimation(None)

    def pick_file(self, e):
        """Selecciona archivo PDF"""

        def file_picker_result(e: ft.FilePickerResultEvent):
            try:
                if e.files and len(e.files) > 0:
                    self.selected_file = e.files[0].path
                    self.file_text.value = os.path.basename(self.selected_file)

                    if not self.selected_file.lower().endswith('.pdf'):
                        self._show_error_message("Selecciona un archivo PDF válido")
                        self.selected_file = None
                        self.file_text.value = "Ningún archivo seleccionado"
                        self.separate_button.disabled = True
                        self.page.update()
                        return

                    # Leer información del PDF
                    self.analyze_pdf_file()

                    self.separate_button.disabled = False
                    self.page.update()

            except Exception as ex:
                self._show_error_message(f"Error: {str(ex)}")

        try:
            file_picker = ft.FilePicker(on_result=file_picker_result)
            self.page.overlay.append(file_picker)
            self.page.update()

            last_folder = config_manager.get("paths", "last_input_folder", "")
            file_picker.pick_files(
                dialog_title="Seleccionar archivo PDF",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["pdf"],
                initial_directory=last_folder if last_folder and os.path.exists(last_folder) else None
            )
        except Exception as ex:
            self._show_error_message(f"Error: {str(ex)}")

    def analyze_pdf_file(self):
        """Analiza el archivo PDF y muestra información"""
        try:
            import PyPDF2

            with open(self.selected_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                self.total_pages = len(reader.pages)

            file_size = os.path.getsize(self.selected_file) / (1024 * 1024)

            # Mostrar información
            info_text = f"Total de páginas: {self.total_pages:,} | Tamaño: {file_size:.1f} MB"

            # Buscar el contenedor de información
            for control in self.page.controls:
                if hasattr(control, 'content'):
                    self._find_and_update_control(control, "file_info", info_text)
                    self._find_and_update_control(control, "info_container", None, visible=True)

            # Mostrar advertencia si es archivo grande
            if self.total_pages > 50000:
                self._show_large_file_warning()

            # Actualizar estimación
            self.update_estimation(None)

            # Auto-configurar carpeta
            if not self.output_folder:
                default_output = config_manager.get("paths", "default_output_folder", "")
                base_name = os.path.splitext(os.path.basename(self.selected_file))[0]

                if default_output and os.path.exists(default_output):
                    self.output_folder = os.path.join(default_output, f"{base_name}_pages")
                else:
                    self.output_folder = os.path.join(
                        os.path.dirname(self.selected_file),
                        f"{base_name}_pages"
                    )

                self.folder_text.value = self.output_folder

            config_manager.set("paths", "last_input_folder",
                               os.path.dirname(self.selected_file))

            self.page.update()

        except Exception as e:
            self._show_error_message(f"Error al analizar PDF: {str(e)}")

    def _find_and_update_control(self, container, key, value=None, visible=None):
        """Busca y actualiza un control por su key"""
        if hasattr(container, 'key') and container.key == key:
            if value is not None:
                container.value = value
            if visible is not None:
                container.visible = visible
            return True

        if hasattr(container, 'content'):
            return self._find_and_update_control(container.content, key, value, visible)

        if hasattr(container, 'controls'):
            for control in container.controls:
                if self._find_and_update_control(control, key, value, visible):
                    return True

        return False

    def _show_large_file_warning(self):
        """Muestra advertencia para archivos grandes"""
        for control in self.page.controls:
            if hasattr(control, 'content'):
                self._find_and_update_control(control, "large_file_warning", None, visible=True)

    def update_estimation(self, e):
        """Actualiza la estimación de tiempo"""
        if not self.selected_file or self.total_pages == 0:
            return

        try:
            # Obtener rango de páginas
            if self.use_page_range.value:
                try:
                    start = int(self.page_range_start.value) if self.page_range_start.value else 1
                    end = int(self.page_range_end.value) if self.page_range_end.value else self.total_pages
                    pages_to_process = end - start + 1
                except:
                    pages_to_process = self.total_pages
            else:
                pages_to_process = self.total_pages

            crear_zip = self.create_zip_switch.value
            estimacion = estimar_tiempo_procesamiento(pages_to_process, crear_zip)

            # Construir mensaje de estimación
            if estimacion['horas'] > 0:
                tiempo_str = f"~{estimacion['horas']}h {estimacion['minutos'] % 60}min"
            else:
                tiempo_str = f"~{estimacion['minutos']}min"

            mensaje = f"Tiempo estimado: {tiempo_str} para {pages_to_process:,} páginas"

            if estimacion['advertencia_muy_grande']:
                mensaje += " ⚠️ (archivo muy grande, tiempo aproximado)"

            self.estimation_text.value = mensaje
            self.estimation_text.visible = True

            # Mostrar contenedor de estimación
            for control in self.page.controls:
                if hasattr(control, 'content'):
                    self._find_and_update_control(control, "estimation_container", None, visible=True)

            self.page.update()

        except Exception as e:
            print(f"Error en estimación: {e}")

    def pick_folder(self, e):
        """Selecciona carpeta de destino"""

        def folder_picker_result(e: ft.FilePickerResultEvent):
            try:
                if e.path:
                    if self.selected_file:
                        base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
                        self.output_folder = os.path.join(e.path, f"{base_name}_pages")
                    else:
                        self.output_folder = os.path.join(e.path, "pdf_pages")

                    self.folder_text.value = self.output_folder
                    config_manager.set("paths", "last_output_folder", e.path)
                    self._show_success_message("Carpeta actualizada")
                    self.page.update()
            except Exception as ex:
                self._show_error_message(f"Error: {str(ex)}")

        try:
            folder_picker = ft.FilePicker(on_result=folder_picker_result)
            self.page.overlay.append(folder_picker)
            self.page.update()

            last_output = config_manager.get("paths", "last_output_folder", "")
            folder_picker.get_directory_path(
                dialog_title="Seleccionar carpeta de destino",
                initial_directory=last_output if last_output and os.path.exists(last_output) else None
            )
        except Exception as ex:
            self._show_error_message(f"Error: {str(ex)}")

    def update_progress(self, progress, message):
        """Actualiza la barra de progreso"""
        if progress == -1:
            self.progress_bar.color = ft.Colors.ERROR
            self.progress_bar.value = 1.0
            self.progress_text.value = f"❌ {message}"
            self.progress_text.color = ft.Colors.ERROR
        elif progress == 100:
            self.progress_bar.color = ft.Colors.GREEN
            self.progress_bar.value = 1.0
            self.progress_text.value = f"✅ {message}"
            self.progress_text.color = ft.Colors.GREEN
        else:
            self.progress_bar.color = ft.Colors.AMBER
            self.progress_bar.value = progress / 100
            self.progress_text.value = f"⏳ {message} ({progress}%)"
            self.progress_text.color = ft.Colors.ON_SURFACE

        self.page.update()

    def separate_pdf_thread(self):
        """Ejecuta la separación optimizada del PDF"""
        try:
            formato_nombre = self.format_field.value or "pagina_{:03d}"
            crear_zip = self.create_zip_switch.value

            # Validar formato
            try:
                test_format = formato_nombre.format(1)
                if not test_format:
                    raise ValueError("Formato inválido")
            except:
                self.update_progress(-1, "Formato de nombre inválido")
                return

            # Obtener parámetros de optimización
            try:
                batch_size = int(self.batch_size_field.value) if self.batch_size_field.value else 1000
                batch_size = max(100, min(batch_size, 10000))  # Limitar entre 100 y 10000
            except:
                batch_size = 1000

            try:
                max_workers = int(self.workers_field.value) if self.workers_field.value else None
            except:
                max_workers = None

            # Obtener rango de páginas
            rango_paginas = None
            if self.use_page_range.value:
                try:
                    start = int(self.page_range_start.value) if self.page_range_start.value else 1
                    end = int(self.page_range_end.value) if self.page_range_end.value else self.total_pages
                    rango_paginas = (start, end)
                except:
                    pass

            # Ejecutar división optimizada
            resultado = dividir_pdf_optimizado(
                ruta_pdf=self.selected_file,
                carpeta_salida=self.output_folder,
                formato_nombre=formato_nombre,
                crear_zip=crear_zip,
                callback_progreso=self.update_progress,
                batch_size=batch_size,
                max_workers=max_workers,
                rango_paginas=rango_paginas
            )

            self.show_results(resultado)

        except Exception as e:
            self.update_progress(-1, f"Error: {str(e)}")
        finally:
            self.is_processing = False
            self.separate_button.disabled = False
            if self.page:
                self.page.update()

    def separate_pdf(self, e):
        """Inicia la separación"""
        if not self.selected_file or self.is_processing:
            return

        self.is_processing = True
        self.separate_button.disabled = True
        self.progress_bar.visible = True
        self.progress_text.visible = True
        self.result_container.visible = False
        self.page.update()

        thread = threading.Thread(target=self.separate_pdf_thread)
        thread.daemon = True
        thread.start()

    def show_results(self, resultado):
        """Muestra resultados"""
        result_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=30),
                        ft.Text("División completada", size=18, weight=ft.FontWeight.BOLD)
                    ]),
                    ft.Divider(),
                    ft.Row([
                        ft.Icon(ft.Icons.PAGES, color=ft.Colors.BLUE),
                        ft.Text(f"Páginas: {resultado['total_paginas']:,}")
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.FOLDER, color=ft.Colors.ORANGE),
                        ft.Text(f"Carpeta: {os.path.basename(resultado['carpeta'])}")
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.ARCHIVE, color=ft.Colors.PURPLE),
                        ft.Text(f"ZIP: {'Sí' if resultado['zip'] else 'No'}")
                    ]) if resultado['zip'] else ft.Container(),
                    ft.Divider(),
                    ft.Row([
                        ft.ElevatedButton(
                            "Abrir carpeta",
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=lambda _: self.open_folder(resultado['carpeta'])
                        ),
                        ft.ElevatedButton(
                            "Nueva división",
                            icon=ft.Icons.REFRESH,
                            on_click=self.clear_form
                        )
                    ])
                ], spacing=10),
                padding=20
            )
        )

        self.result_container.content = result_card
        self.result_container.visible = True
        self.page.update()

        if config_manager.get("general", "open_folder_after_process", True):
            self.open_folder(resultado['carpeta'])

    def open_folder(self, folder_path):
        """Abre la carpeta de resultados"""
        import subprocess
        import platform

        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", folder_path], check=True)
            elif platform.system() == "Darwin":
                subprocess.run(["open", folder_path], check=True)
            else:
                subprocess.run(["xdg-open", folder_path], check=True)

            self._show_success_message("Carpeta abierta")
        except:
            self._show_error_message("No se pudo abrir la carpeta")

    def clear_form(self, e):
        """Limpia el formulario"""
        self.selected_file = None
        self.output_folder = None
        self.total_pages = 0
        self.file_text.value = "Ningún archivo seleccionado"

        default_output = config_manager.get("paths", "default_output_folder", "")
        self.folder_text.value = default_output or "Se creará automáticamente"

        self.format_field.value = config_manager.get("pdf", "default_output_format", "pagina_{:03d}")
        self.create_zip_switch.value = config_manager.get("pdf", "create_zip_by_default", True)
        self.batch_size_field.value = "1000"
        self.workers_field.value = ""

        self.use_page_range.value = False
        self.page_range_start.value = ""
        self.page_range_start.disabled = True
        self.page_range_end.value = ""
        self.page_range_end.disabled = True

        self.separate_button.disabled = True
        self.progress_bar.visible = False
        self.progress_text.visible = False
        self.result_container.visible = False
        self.estimation_text.visible = False

        # Ocultar advertencias e info
        for control in self.page.controls:
            if hasattr(control, 'content'):
                self._find_and_update_control(control, "info_container", None, visible=False)
                self._find_and_update_control(control, "large_file_warning", None, visible=False)
                self._find_and_update_control(control, "estimation_container", None, visible=False)

        self.page.update()

    def _show_info_message(self, message, duration=3000):
        """Muestra mensaje informativo"""
        if self.page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.BLUE,
                duration=duration
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()

    def _show_error_message(self, message):
        """Muestra mensaje de error"""
        if self.page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()

    def _show_success_message(self, message):
        """Muestra mensaje de éxito"""
        if self.page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.GREEN
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()