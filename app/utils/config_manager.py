# utils/config_manager.py - Gestor de configuración persistente
import json
import os
from pathlib import Path
import flet as ft


class ConfigManager:
    """Gestor de configuración de la aplicación"""

    def __init__(self):
        # Ubicación del archivo de configuración
        # Cambiar a la carpeta del proyecto
        self.config_dir = Path(__file__).parent.parent / "config"  # Carpeta config en raíz del proyecto
        # O simplemente en la raíz del proyecto:
        # self.config_dir = Path(__file__).parent.parent
        self.config_file = self.config_dir / "config.json"

        # Configuración por defecto
        self.default_config = {
            "general": {
                "dark_mode": False,
                "confirm_delete": True,
                "open_folder_after_process": True,
                "auto_save_config": True,
                "window_width": 1200,
                "window_height": 800
            },
            "pdf": {
                "compression_quality": "Media",
                "keep_metadata": True,
                "optimize_for_web": False,
                "default_output_format": "pagina_{:03d}",
                "create_zip_by_default": True,
                "max_file_size_mb": 100
            },
            "paths": {
                "last_input_folder": "",
                "last_output_folder": "",
                "default_output_folder": ""
            },
            "ui": {
                "language": "es",
                "show_tooltips": True,
                "animation_enabled": True,
                "compact_mode": False
            }
        }

        # Crear directorio si no existe
        self.config_dir.mkdir(exist_ok=True)

        # Cargar configuración
        self.config = self.load_config()

    def load_config(self):
        """Carga la configuración desde el archivo"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)

                # Fusionar con configuración por defecto para agregar nuevas opciones
                merged_config = self._merge_configs(self.default_config, loaded_config)
                return merged_config
            else:
                # Primera vez, crear archivo con configuración por defecto
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return self.default_config.copy()

    def save_config(self, config=None):
        """Guarda la configuración al archivo"""
        try:
            config_to_save = config or self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False

    def get(self, category, key, default=None):
        """Obtiene un valor de configuración"""
        try:
            return self.config.get(category, {}).get(key, default)
        except:
            return default

    def set(self, category, key, value):
        """Establece un valor de configuración"""
        if category not in self.config:
            self.config[category] = {}
        self.config[category][key] = value

        # Auto-guardar si está habilitado
        if self.get("general", "auto_save_config", True):
            self.save_config()

    def get_theme_mode(self):
        """Obtiene el modo de tema actual"""
        return ft.ThemeMode.DARK if self.get("general", "dark_mode", False) else ft.ThemeMode.LIGHT

    def toggle_theme(self):
        """Cambia el tema y devuelve el nuevo modo"""
        current_dark = self.get("general", "dark_mode", False)
        self.set("general", "dark_mode", not current_dark)
        return self.get_theme_mode()

    def _merge_configs(self, default, loaded):
        """Fusiona configuración cargada con la por defecto"""
        result = default.copy()
        for category, values in loaded.items():
            if category in result:
                result[category].update(values)
            else:
                result[category] = values
        return result

    def reset_to_defaults(self):
        """Resetea la configuración a valores por defecto"""
        self.config = self.default_config.copy()
        self.save_config()
        return True

config_manager = ConfigManager()
