import flet as ft
from .base_page import BasePage


class UnirPage(BasePage):
    def __init__(self, page: ft.Page = None):
        super().__init__()
        self.title = "Unir PDF"
        self.description = "Une múltiples archivos PDF en uno solo"
        self.pdf_files = []

    def build(self):
        header = self.create_header(
            "Unir PDFs",
            "Selecciona múltiples archivos PDF para unirlos en un solo documento"
        )

        # Sección de instrucciones
        instructions = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📋 Instrucciones", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("1. Haz clic en 'Agregar archivos' para seleccionar PDFs"),
                    ft.Text("2. Los archivos se unirán en el orden que aparecen en la lista"),
                    ft.Text("3. Puedes reorganizar el orden arrastrando los elementos"),
                    ft.Text("4. Haz clic en 'Unir PDFs' para generar el archivo final"),
                ], spacing=5),
                padding=20
            )
        )

        # Lista de archivos seleccionados (más detallada)
        files_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📁 Archivos seleccionados", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self._create_files_list(),

                        border_radius=8,
                        padding=15,

                    ),
                    ft.Text(f"Total de archivos: {len(self.pdf_files)}",
                            weight=ft.FontWeight.W_500)
                ], spacing=10),
                padding=20
            )
        )

        # Opciones de unión
        options_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("⚙️ Opciones de unión", size=16, weight=ft.FontWeight.BOLD),

                    ft.TextField(
                        label="Nombre del archivo final",
                        value="documento_unido.pdf",
                        helper_text="Nombre para el PDF resultante"
                    ),

                    ft.Switch(label="Mantener marcadores (bookmarks)", value=True),
                    ft.Switch(label="Mantener metadatos del primer archivo", value=True),
                    ft.Switch(label="Optimizar tamaño del archivo final", value=False),

                    ft.Dropdown(
                        label="Calidad de compresión",
                        options=[
                            ft.dropdown.Option("Alta"),
                            ft.dropdown.Option("Media"),
                            ft.dropdown.Option("Baja"),
                        ],
                        value="Media"
                    ),

                ], spacing=10),
                padding=20
            )
        )

        # Controles de acción
        controls_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("🚀 Acciones", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton(
                            "Agregar archivos",
                            icon=ft.Icons.ADD,
                            on_click=self.add_files
                        ),
                        ft.ElevatedButton(
                            "Unir PDFs",
                            icon=ft.Icons.MERGE_TYPE,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.PRIMARY),
                            on_click=self.merge_pdfs,
                            disabled=len(self.pdf_files) < 2
                        ),
                        ft.OutlinedButton(
                            "Limpiar lista",
                            icon=ft.Icons.CLEAR,
                            on_click=self.clear_files
                        )
                    ]),

                    ft.Divider(),

                    ft.Row([
                        ft.OutlinedButton(
                            "Vista previa",
                            icon=ft.Icons.PREVIEW,
                            on_click=self._preview_files
                        ),
                        ft.OutlinedButton(
                            "Reorganizar",
                            icon=ft.Icons.SORT,
                            on_click=self._reorder_files
                        ),
                        ft.OutlinedButton(
                            "Eliminar duplicados",
                            icon=ft.Icons.LAYERS_CLEAR,
                            on_click=self._remove_duplicates
                        )
                    ])
                ], spacing=15),
                padding=20
            )
        )

        # Información adicional
        info_section = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("ℹ️ Información importante", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("• Los archivos se procesan en el orden mostrado", size=12),
                    ft.Text("• Se recomienda tener menos de 50 archivos por operación", size=12),
                    ft.Text("• El tiempo de procesamiento depende del tamaño total", size=12),
                    ft.Text("• Se preservarán las páginas individuales de cada archivo", size=12),
                    ft.Text("• Los archivos dañados serán omitidos automáticamente", size=12),
                ], spacing=5),
                padding=20
            )
        )

        # Lista de elementos para scroll
        content_elements = [
            header,
            ft.Divider(),
            instructions,
            files_section,
            options_section,
            controls_section,
            info_section
        ]

        return self.create_scrollable_content(content_elements, padding=20)

    def _create_files_list(self):
        """Crea la lista visual de archivos"""
        if not self.pdf_files:
            return ft.Text("No hay archivos seleccionados", color=ft.Colors.ON_SURFACE_VARIANT)

        file_widgets = []
        for i, file in enumerate(self.pdf_files, 1):
            file_widgets.append(
                ft.Row([
                    ft.Text(f"{i}.", width=30),
                    ft.Icon(ft.Icons.PICTURE_AS_PDF, color=ft.Colors.RED),
                    ft.Text(file, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Eliminar archivo",
                        on_click=lambda e, idx=i - 1: self._remove_file(idx)
                    )
                ])
            )

        return ft.Column(file_widgets, spacing=5)

    def _remove_file(self, index):
        """Elimina un archivo de la lista"""
        if 0 <= index < len(self.pdf_files):
            self.pdf_files.pop(index)
            if self.page:
                self.page.update()

    def _show_snack_bar(self, message, bgcolor=ft.Colors.BLUE):
        """Método helper para mostrar SnackBar"""
        if self.page:
            snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=bgcolor,
                action="OK"
            )
            self.page.snack_bar = snack_bar
            snack_bar.open = True
            self.page.update()

    def _preview_files(self, e):
        """Muestra vista previa de archivos"""
        self._show_snack_bar("Función de vista previa en desarrollo", ft.Colors.ORANGE)

    def _reorder_files(self, e):
        """Reorganiza archivos"""
        self._show_snack_bar("Función de reorganización en desarrollo", ft.Colors.ORANGE)

    def _remove_duplicates(self, e):
        """Elimina archivos duplicados"""
        original_count = len(self.pdf_files)
        self.pdf_files = list(dict.fromkeys(self.pdf_files))  # Elimina duplicados
        removed = original_count - len(self.pdf_files)

        if removed > 0:
            self._show_snack_bar(f"Se eliminaron {removed} archivos duplicados", ft.Colors.GREEN)
        else:
            self._show_snack_bar("No se encontraron archivos duplicados", ft.Colors.BLUE)

        if self.page:
            self.page.update()

    def add_files(self, e):
        """Agrega archivos a la lista (simulado)"""
        self.pdf_files.append(f"archivo_{len(self.pdf_files) + 1}.pdf")
        self._show_snack_bar(f"Archivo agregado. Total: {len(self.pdf_files)}", ft.Colors.GREEN)
        if self.page:
            self.page.update()

    def merge_pdfs(self, e):
        """Une los PDFs seleccionados"""
        if len(self.pdf_files) < 2:
            self._show_snack_bar("Necesitas al menos 2 archivos para unir", ft.Colors.RED)
        else:
            self._show_snack_bar(f"Uniendo {len(self.pdf_files)} archivos...", ft.Colors.BLUE)

    def clear_files(self, e):
        """Limpia la lista de archivos"""
        count = len(self.pdf_files)
        self.pdf_files.clear()
        self._show_snack_bar(f"Se eliminaron {count} archivos de la lista", ft.Colors.ORANGE)
        if self.page:
            self.page.update()