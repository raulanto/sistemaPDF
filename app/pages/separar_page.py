import os
import threading

import flet as ft

from app.utils.config_manager import config_manager
from app.utils.pdf_processor import dividir_pdf_avanzado
from .base_page import BasePage


class SepararPage(BasePage):
    def __init__(self, page=None):
        super().__init__(page)
        self.title = "Separar PDF"
        self.description = "Separa páginas de un archivo PDF"
        self.selected_file = None
        self.output_folder = None
        self.is_processing = False
        self.pdf_pages_info = []
        self.selected_pages = set()
        self.extraction_mode = "all"

        # Referencias a controles que necesitamos actualizar
        self.file_text = None
        self.folder_text = None
        self.progress_bar = None
        self.progress_text = None
        self.format_field = None
        self.create_zip_switch = None
        self.separate_button = None
        self.result_container = None

    def build(self):
        # Header de la página
        header = self.create_header(
            "Separar PDF",
            "Selecciona un archivo PDF y configura las opciones de división"
        )

        # Obtener valores por defecto de la configuración
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
                ], spacing=10),
                padding=20
            )
        )

        # Sección de configuración avanzada
        default_output_folder = config_manager.get("paths", "default_output_folder", "")
        self.folder_text = ft.Text(
            default_output_folder or "Se creará automáticamente",
            color=ft.Colors.ON_SURFACE_VARIANT
        )

        self.format_field = ft.TextField(
            label="Formato de nombre",
            hint_text=default_format,
            value=default_format,
            helper_text="Usa {:03d} para numeración con ceros. Ej: pagina_001.pdf",
            expand=True
        )

        self.create_zip_switch = ft.Switch(
            label="Crear archivo ZIP",
            value=default_zip
        )

        config_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("⚙️ Configuración avanzada", size=16, weight=ft.FontWeight.BOLD),

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

                    # Opciones adicionales
                    ft.Text("Opciones:", weight=ft.FontWeight.W_500),
                    self.create_zip_switch,

                    # Información adicional
                    ft.Container(
                        content=ft.Column([
                            ft.Text("ℹ️ Información:", weight=ft.FontWeight.W_500),
                            ft.Text("• El formato {:03d} crea nombres como: pagina_001.pdf, pagina_002.pdf",
                                    size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                            ft.Text("• El archivo ZIP contiene todas las páginas separadas",
                                    size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                            ft.Text("• La carpeta se creará automáticamente si no existe",
                                    size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                        ], spacing=5),

                        padding=15,
                        border_radius=8,
                        margin=ft.margin.only(top=10)
                    )

                ], spacing=15),
                padding=20
            )
        )

        # Sección de progreso
        self.progress_bar = ft.ProgressBar(
            width=400,
            color="amber",
            bgcolor="#eeeeee",
            visible=False
        )

        self.progress_text = ft.Text(
            "",
            size=12,
            visible=False
        )

        progress_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📈 Progreso del procesamiento", size=16, weight=ft.FontWeight.BOLD),
                    self.progress_bar,
                    self.progress_text
                ], spacing=10),
                padding=20
            ),
            visible=True
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
                            "Limpiar formulario",
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

        # Sección de ayuda adicional
        help_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("❓ Ayuda", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Formatos de nombre soportados:", weight=ft.FontWeight.W_500),
                    ft.Column([
                        ft.Text("• pagina_{:03d} → pagina_001.pdf, pagina_002.pdf", size=12),
                        ft.Text("• documento_{} → documento_1.pdf, documento_2.pdf", size=12),
                        ft.Text("• capitulo_{:02d} → capitulo_01.pdf, capitulo_02.pdf", size=12),
                        ft.Text("• seccion_A_{} → seccion_A_1.pdf, seccion_A_2.pdf", size=12),
                    ], spacing=5),
                    ft.Divider(),
                    ft.Text("Límites y recomendaciones:", weight=ft.FontWeight.W_500),
                    ft.Column([
                        ft.Text(f"• Tamaño máximo: {config_manager.get('pdf', 'max_file_size_mb', 100)} MB", size=12),
                        ft.Text("• Formatos soportados: PDF únicamente", size=12),
                        ft.Text("• Se preservan los metadatos originales", size=12),
                        ft.Text("• El proceso puede tomar tiempo para archivos grandes", size=12),
                    ], spacing=5)
                ], spacing=10),
                padding=20
            ),
            # Esta sección solo se muestra si hay espacio o el usuario hace scroll
        )

        # Lista de todos los elementos usando el método scrolleable de la clase base
        content_elements = [
            header,
            ft.Divider(),
            file_section,
            config_section,
            progress_section,
            action_buttons,
            self.result_container,
            help_section  # Esta sección adicional solo se ve con scroll
        ]

        # Usar el método de la clase base que hace el contenido scrolleable
        return self.create_scrollable_content(content_elements, padding=20)


    def pick_file(self, e):
        """Abre un diálogo para seleccionar archivo PDF (método mejorado)"""

        def file_picker_result(e: ft.FilePickerResultEvent):
            try:
                if e.files and len(e.files) > 0:
                    self.selected_file = e.files[0].path
                    self.file_text.value = os.path.basename(self.selected_file)
                    self.separate_button.disabled = False

                    # Validar que es un archivo PDF
                    if not self.selected_file.lower().endswith('.pdf'):
                        self._show_error_message("Por favor selecciona un archivo PDF válido")
                        self.selected_file = None
                        self.file_text.value = "Ningún archivo seleccionado"
                        self.separate_button.disabled = True
                        self.page.update()
                        return

                    # Validar que el archivo existe y es accesible
                    if not os.path.exists(self.selected_file):
                        self._show_error_message("El archivo seleccionado no existe")
                        self.selected_file = None
                        self.file_text.value = "Ningún archivo seleccionado"
                        self.separate_button.disabled = True
                        self.page.update()
                        return

                    # Auto-configurar carpeta de salida usando configuración
                    if not self.output_folder:
                        default_output = config_manager.get("paths", "default_output_folder", "")
                        if default_output and os.path.exists(default_output):
                            base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
                            self.output_folder = os.path.join(default_output, f"{base_name}_pages")
                        else:
                            base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
                            self.output_folder = os.path.join(os.path.dirname(self.selected_file), f"{base_name}_pages")

                        self.folder_text.value = self.output_folder

                    # Guardar última carpeta usada
                    config_manager.set("paths", "last_input_folder", os.path.dirname(self.selected_file))

                    # Mostrar información del archivo
                    try:
                        file_size = os.path.getsize(self.selected_file) / (1024 * 1024)  # MB
                        self._show_info_message(f"Archivo seleccionado: {file_size:.1f} MB")
                    except:
                        pass

                    self.page.update()
                else:
                    # Usuario canceló la selección
                    pass

            except Exception as ex:
                self._show_error_message(f"Error al seleccionar archivo: {str(ex)}")

        try:
            # Crear FilePicker
            file_picker = ft.FilePicker(on_result=file_picker_result)
            self.page.overlay.append(file_picker)
            self.page.update()

            # Obtener la última carpeta usada
            last_folder = config_manager.get("paths", "last_input_folder", "")

            # Abrir diálogo
            file_picker.pick_files(
                dialog_title="Seleccionar archivo PDF",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["pdf"],
                initial_directory=last_folder if last_folder and os.path.exists(last_folder) else None
            )

        except Exception as ex:
            self._show_error_message(f"Error al abrir selector de archivos: {str(ex)}")

    def pick_folder(self, e):
        """Abre un diálogo para seleccionar carpeta de destino (método mejorado)"""

        def folder_picker_result(e: ft.FilePickerResultEvent):
            try:
                if e.path:
                    if self.selected_file:
                        base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
                        self.output_folder = os.path.join(e.path, f"{base_name}_pages")
                    else:
                        self.output_folder = os.path.join(e.path, "pdf_pages")

                    self.folder_text.value = self.output_folder

                    # Guardar última carpeta de salida
                    config_manager.set("paths", "last_output_folder", e.path)
                    self._show_success_message("Carpeta de destino actualizada")
                    self.page.update()
            except Exception as ex:
                self._show_error_message(f"Error al seleccionar carpeta: {str(ex)}")

        try:
            # Crear DirectoryPicker
            folder_picker = ft.FilePicker(on_result=folder_picker_result)
            self.page.overlay.append(folder_picker)
            self.page.update()

            # Obtener la última carpeta usada
            last_output = config_manager.get("paths", "last_output_folder", "")

            # Abrir diálogo
            folder_picker.get_directory_path(
                dialog_title="Seleccionar carpeta de destino",
                initial_directory=last_output if last_output and os.path.exists(last_output) else None
            )

        except Exception as ex:
            self._show_error_message(f"Error al abrir selector de carpeta: {str(ex)}")

    def update_progress(self, progress, message):
        """Actualiza la barra de progreso y mensaje"""
        if progress == -1:  # Error
            self.progress_bar.color = ft.Colors.ERROR
            self.progress_bar.value = 1.0
            self.progress_text.value = f"❌ {message}"
            self.progress_text.color = ft.Colors.ERROR
        elif progress == 100:  # Completado
            self.progress_bar.color = ft.Colors.GREEN
            self.progress_bar.value = 1.0
            self.progress_text.value = f"✅ {message}"
            self.progress_text.color = ft.Colors.GREEN

        else:  # En progreso
            self.progress_bar.color = ft.Colors.AMBER
            self.progress_bar.value = progress / 100
            self.progress_text.value = f"📝 {message} ({progress}%)"
            self.progress_text.color = ft.Colors.ON_SURFACE

        self.page.update()

    def separate_pdf_thread(self):
        """Ejecuta la separación del PDF en un hilo separado (método mejorado)"""
        try:
            formato_nombre = self.format_field.value or config_manager.get("pdf", "default_output_format",
                                                                           "pagina_{:03d}")
            crear_zip = self.create_zip_switch.value

            # Validar formato de nombre
            try:
                test_format = formato_nombre.format(1)
                if not test_format:
                    raise ValueError("Formato inválido")
            except:
                self.update_progress(-1, "Formato de nombre inválido. Usa {:03d} o {} para numeración.")
                return

            # Validar tamaño de archivo si está configurado
            max_size_mb = config_manager.get("pdf", "max_file_size_mb", 100)
            if max_size_mb > 0:
                try:
                    file_size_mb = os.path.getsize(self.selected_file) / (1024 * 1024)
                    if file_size_mb > max_size_mb:
                        self.update_progress(-1, f"Archivo demasiado grande ({file_size_mb:.1f}MB > {max_size_mb}MB)")
                        return
                except:
                    self.update_progress(-1, "No se pudo verificar el tamaño del archivo")
                    return

            # Validar que el archivo es un PDF válido
            try:
                import PyPDF2
                with open(self.selected_file, 'rb') as test_file:
                    reader = PyPDF2.PdfReader(test_file)
                    if len(reader.pages) == 0:
                        self.update_progress(-1, "El archivo PDF está vacío o dañado")
                        return
                    self.update_progress(5, f"PDF válido con {len(reader.pages)} páginas")
            except Exception as pdf_error:
                self.update_progress(-1, f"Error al leer PDF: {str(pdf_error)}")
                return

            # Ejecutar la función de división
            resultado = dividir_pdf_avanzado(
                ruta_pdf=self.selected_file,
                carpeta_salida=self.output_folder,
                formato_nombre=formato_nombre,
                crear_zip=crear_zip,
                callback_progreso=self.update_progress
            )

            # Mostrar resultados
            self.show_results(resultado)

        except Exception as e:
            self.update_progress(-1, f"Error durante el procesamiento: {str(e)}")
        finally:
            self.is_processing = False
            self.separate_button.disabled = False
            if self.page:
                self.page.update()

    def separate_pdf(self, e):
        """Inicia la separación del PDF"""
        if not self.selected_file:
            return

        if self.is_processing:
            return

        # Validar configuración antes de procesar
        if config_manager.get("general", "confirm_delete", True):
            if os.path.exists(self.output_folder):
                # Mostrar confirmación si la carpeta ya existe
                self._show_confirmation_dialog()
                return

        self._start_processing()

    def _show_confirmation_dialog(self):
        """Muestra diálogo de confirmación"""

        def handle_response(e):
            if e.control.text == "Continuar":
                self._start_processing()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Carpeta ya existe"),
            content=ft.Text(f"La carpeta '{os.path.basename(self.output_folder)}' ya existe. ¿Continuar?"),
            actions=[
                ft.TextButton("Continuar", on_click=handle_response),
                ft.TextButton("Cancelar", on_click=handle_response),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _start_processing(self):
        """Inicia el procesamiento"""
        self.is_processing = True
        self.separate_button.disabled = True
        self.progress_bar.visible = True
        self.progress_text.visible = True
        self.result_container.visible = False
        self.page.update()

        # Ejecutar en hilo separado para no bloquear la UI
        thread = threading.Thread(target=self.separate_pdf_thread)
        thread.daemon = True
        thread.start()

    def show_results(self, resultado):
        """Muestra los resultados de la operación"""
        # Crear card con resultados
        result_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=30),
                        ft.Text("División completada exitosamente",
                                size=18, weight=ft.FontWeight.BOLD)
                    ]),

                    ft.Divider(),

                    ft.Row([
                        ft.Icon(ft.Icons.PAGES, color=ft.Colors.BLUE),
                        ft.Text(f"Páginas procesadas: {resultado['total_paginas']}")
                    ]),

                    ft.Row([
                        ft.Icon(ft.Icons.FOLDER, color=ft.Colors.ORANGE),
                        ft.Text(f"Carpeta: {os.path.basename(resultado['carpeta'])}")
                    ]),

                    ft.Row([
                        ft.Icon(ft.Icons.ARCHIVE, color=ft.Colors.PURPLE),
                        ft.Text(f"ZIP creado: {'Sí' if resultado['zip'] else 'No'}")
                    ]) if resultado['zip'] else ft.Container(),

                    ft.Divider(),

                    self._create_result_buttons(resultado)

                ], spacing=10),
                padding=20
            )
        )

        self.result_container.content = result_card
        self.result_container.visible = True
        self.page.update()

        # Abrir carpeta automáticamente si está configurado
        if config_manager.get("general", "open_folder_after_process", True):
            self.open_folder(resultado['carpeta'])

    def _create_result_buttons(self, resultado):
        """Crea los botones de resultado"""
        buttons = [
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
        ]

        # Agregar botón de ZIP si existe
        if resultado['zip']:
            buttons.insert(1, ft.ElevatedButton(
                "Abrir ZIP",
                icon=ft.Icons.ARCHIVE,
                on_click=lambda _: self.open_folder(os.path.dirname(resultado['zip']))
            ))

        return ft.Row(buttons)

    def open_folder(self, folder_path):
        """Abre la carpeta de resultados (método corregido)"""
        import subprocess
        import platform

        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", folder_path], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder_path], check=True)
            else:  # Linux
                subprocess.run(["xdg-open", folder_path], check=True)

            # Mensaje de éxito
            self._show_success_message("Carpeta abierta exitosamente")

        except subprocess.CalledProcessError:
            self._show_error_message("No se pudo abrir la carpeta automáticamente")
        except FileNotFoundError:
            self._show_error_message("Comando no encontrado para abrir carpetas")
        except Exception as e:
            self._show_error_message(f"Error inesperado: {str(e)}")

    def clear_form(self, e):
        """Limpia el formulario y restaura valores por defecto de configuración"""
        self.selected_file = None
        self.output_folder = None
        self.file_text.value = "Ningún archivo seleccionado"

        # Restaurar valores de configuración
        default_output = config_manager.get("paths", "default_output_folder", "")
        self.folder_text.value = default_output or "Se creará automáticamente"

        self.format_field.value = config_manager.get("pdf", "default_output_format", "pagina_{:03d}")
        self.create_zip_switch.value = config_manager.get("pdf", "create_zip_by_default", True)

        self.separate_button.disabled = True
        self.progress_bar.visible = False
        self.progress_text.visible = False
        self.result_container.visible = False

        self.page.update()

    def _show_info_message(self, message, duration=3000):
        """Muestra mensaje informativo"""
        if self.page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.BLUE,
                action="OK",
                duration=duration
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