import os
import time
import zipfile
from pathlib import Path

import PyPDF2


def dividir_pdf_paginas_seleccionadas(ruta_pdf, carpeta_salida=None, paginas_seleccionadas=None,
                                      formato_nombre="pagina_{:03d}", crear_zip=True, callback_progreso=None):
    """
    Divide un PDF extrayendo solo las páginas seleccionadas.

    Args:
        ruta_pdf (str): Ruta del archivo PDF de entrada
        carpeta_salida (str, optional): Carpeta donde guardar los archivos
        paginas_seleccionadas (list): Lista de números de página a extraer (base 1)
        formato_nombre (str): Formato para nombrar las páginas
        crear_zip (bool): Si crear un ZIP además de los archivos individuales
        callback_progreso (callable): Función callback para reportar progreso

    Returns:
        dict: Información sobre los archivos creados
    """

    if not os.path.exists(ruta_pdf):
        raise FileNotFoundError(f"El archivo PDF no existe: {ruta_pdf}")

    if not paginas_seleccionadas:
        raise ValueError("Debe especificar al menos una página para extraer")

    # Configurar carpeta de salida
    if carpeta_salida is None:
        carpeta_salida = Path(ruta_pdf).stem + "_selected_pages"

    # Crear carpeta si no existe
    Path(carpeta_salida).mkdir(exist_ok=True)

    archivos_creados = []

    try:
        with open(ruta_pdf, 'rb') as archivo_pdf:
            lector_pdf = PyPDF2.PdfReader(archivo_pdf)
            total_paginas_pdf = len(lector_pdf.pages)
            total_paginas_extraer = len(paginas_seleccionadas)

            if callback_progreso:
                callback_progreso(0, f"Iniciando extracción de {total_paginas_extraer} páginas seleccionadas...")

            # Validar que las páginas seleccionadas existen
            paginas_invalidas = [p for p in paginas_seleccionadas if p < 1 or p > total_paginas_pdf]
            if paginas_invalidas:
                raise ValueError(f"Páginas inválidas: {paginas_invalidas}. El PDF tiene {total_paginas_pdf} páginas.")

            # Crear archivos individuales para páginas seleccionadas
            for i, numero_pagina in enumerate(paginas_seleccionadas):
                escritor_pdf = PyPDF2.PdfWriter()
                # PyPDF2 usa índice base 0
                pagina_index = numero_pagina - 1
                escritor_pdf.add_page(lector_pdf.pages[pagina_index])

                # Nombre del archivo usando numeración secuencial
                nombre_archivo = formato_nombre.format(i + 1) + ".pdf"
                ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)

                # Guardar archivo individual
                with open(ruta_archivo, 'wb') as archivo_pagina:
                    escritor_pdf.write(archivo_pagina)

                archivos_creados.append(ruta_archivo)

                # Reportar progreso
                progreso = int(((i + 1) / total_paginas_extraer) * 80)  # 80% para archivos individuales
                if callback_progreso:
                    callback_progreso(progreso, f"Extraída página {numero_pagina} ({i + 1} de {total_paginas_extraer})")

                # Pequeña pausa para permitir actualización de UI
                time.sleep(0.01)

            # Crear ZIP si se solicita
            ruta_zip = None
            if crear_zip:
                if callback_progreso:
                    callback_progreso(85, "Creando archivo ZIP...")

                ruta_zip = f"{carpeta_salida}.zip"
                with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
                    for i, archivo in enumerate(archivos_creados):
                        nombre_en_zip = os.path.basename(archivo)
                        archivo_zip.write(archivo, nombre_en_zip)

                        # Progreso del ZIP (15% restante)
                        progreso_zip = 85 + int((i / len(archivos_creados)) * 15)
                        if callback_progreso:
                            callback_progreso(progreso_zip, f"Comprimiendo archivo {i + 1} de {len(archivos_creados)}")

            if callback_progreso:
                callback_progreso(100, f"¡Extracción completada! {total_paginas_extraer} páginas procesadas.")

    except Exception as e:
        if callback_progreso:
            callback_progreso(-1, f"Error: {str(e)}")
        raise Exception(f"Error al procesar el PDF: {str(e)}")

    return {
        'archivos_individuales': archivos_creados,
        'carpeta': carpeta_salida,
        'zip': ruta_zip,
        'total_paginas': total_paginas_extraer,
        'paginas_seleccionadas': paginas_seleccionadas
    }


# Función original dividir_pdf_avanzado ya existente (sin cambios)
def dividir_pdf_avanzado(ruta_pdf, carpeta_salida=None, formato_nombre="pagina_{:03d}", crear_zip=True,
                         callback_progreso=None):
    """
    Versión avanzada para dividir PDF con más opciones de personalización.

    Args:
        ruta_pdf (str): Ruta del archivo PDF de entrada
        carpeta_salida (str, optional): Carpeta donde guardar los archivos
        formato_nombre (str): Formato para nombrar las páginas (debe incluir {})
        crear_zip (bool): Si crear un ZIP además de los archivos individuales
        callback_progreso (callable): Función callback para reportar progreso

    Returns:
        dict: Información sobre los archivos creados
    """

    if not os.path.exists(ruta_pdf):
        raise FileNotFoundError(f"El archivo PDF no existe: {ruta_pdf}")

    # Configurar carpeta de salida
    if carpeta_salida is None:
        carpeta_salida = Path(ruta_pdf).stem + "_pages"

    # Crear carpeta si no existe
    Path(carpeta_salida).mkdir(exist_ok=True)

    archivos_creados = []

    try:
        with open(ruta_pdf, 'rb') as archivo_pdf:
            lector_pdf = PyPDF2.PdfReader(archivo_pdf)
            total_paginas = len(lector_pdf.pages)

            if callback_progreso:
                callback_progreso(0, f"Iniciando división de {total_paginas} páginas...")

            # Crear archivos individuales
            for numero_pagina in range(total_paginas):
                escritor_pdf = PyPDF2.PdfWriter()
                escritor_pdf.add_page(lector_pdf.pages[numero_pagina])

                # Nombre del archivo
                nombre_archivo = formato_nombre.format(numero_pagina + 1) + ".pdf"
                ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)

                # Guardar archivo individual
                with open(ruta_archivo, 'wb') as archivo_pagina:
                    escritor_pdf.write(archivo_pagina)

                archivos_creados.append(ruta_archivo)

                # Reportar progreso
                progreso = int(((numero_pagina + 1) / total_paginas) * 80)  # 80% para archivos individuales
                if callback_progreso:
                    callback_progreso(progreso, f"Creada página {numero_pagina + 1} de {total_paginas}")

                # Pequeña pausa para permitir actualización de UI
                time.sleep(0.01)

            # Crear ZIP si se solicita
            ruta_zip = None
            if crear_zip:
                if callback_progreso:
                    callback_progreso(85, "Creando archivo ZIP...")

                ruta_zip = f"{carpeta_salida}.zip"
                with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
                    for i, archivo in enumerate(archivos_creados):
                        nombre_en_zip = os.path.basename(archivo)
                        archivo_zip.write(archivo, nombre_en_zip)

                        # Progreso del ZIP (15% restante)
                        progreso_zip = 85 + int((i / len(archivos_creados)) * 15)
                        if callback_progreso:
                            callback_progreso(progreso_zip, f"Comprimiendo archivo {i + 1} de {len(archivos_creados)}")

            if callback_progreso:
                callback_progreso(100, "¡División completada exitosamente!")

    except Exception as e:
        if callback_progreso:
            callback_progreso(-1, f"Error: {str(e)}")
        raise Exception(f"Error al procesar el PDF: {str(e)}")

    return {
        'archivos_individuales': archivos_creados,
        'carpeta': carpeta_salida,
        'zip': ruta_zip,
        'total_paginas': total_paginas
    }
