# import os
# import time
# import zipfile
# from pathlib import Path
#
# import PyPDF2
#
#
# def dividir_pdf_paginas_seleccionadas(ruta_pdf, carpeta_salida=None, paginas_seleccionadas=None,
#                                       formato_nombre="pagina_{:03d}", crear_zip=True, callback_progreso=None):
#     """
#     Divide un PDF extrayendo solo las páginas seleccionadas.
#
#     Args:
#         ruta_pdf (str): Ruta del archivo PDF de entrada
#         carpeta_salida (str, optional): Carpeta donde guardar los archivos
#         paginas_seleccionadas (list): Lista de números de página a extraer (base 1)
#         formato_nombre (str): Formato para nombrar las páginas
#         crear_zip (bool): Si crear un ZIP además de los archivos individuales
#         callback_progreso (callable): Función callback para reportar progreso
#
#     Returns:
#         dict: Información sobre los archivos creados
#     """
#
#     if not os.path.exists(ruta_pdf):
#         raise FileNotFoundError(f"El archivo PDF no existe: {ruta_pdf}")
#
#     if not paginas_seleccionadas:
#         raise ValueError("Debe especificar al menos una página para extraer")
#
#     # Configurar carpeta de salida
#     if carpeta_salida is None:
#         carpeta_salida = Path(ruta_pdf).stem + "_selected_pages"
#
#     # Crear carpeta si no existe
#     Path(carpeta_salida).mkdir(exist_ok=True)
#
#     archivos_creados = []
#
#     try:
#         with open(ruta_pdf, 'rb') as archivo_pdf:
#             lector_pdf = PyPDF2.PdfReader(archivo_pdf)
#             total_paginas_pdf = len(lector_pdf.pages)
#             total_paginas_extraer = len(paginas_seleccionadas)
#
#             if callback_progreso:
#                 callback_progreso(0, f"Iniciando extracción de {total_paginas_extraer} páginas seleccionadas...")
#
#             # Validar que las páginas seleccionadas existen
#             paginas_invalidas = [p for p in paginas_seleccionadas if p < 1 or p > total_paginas_pdf]
#             if paginas_invalidas:
#                 raise ValueError(f"Páginas inválidas: {paginas_invalidas}. El PDF tiene {total_paginas_pdf} páginas.")
#
#             # Crear archivos individuales para páginas seleccionadas
#             for i, numero_pagina in enumerate(paginas_seleccionadas):
#                 escritor_pdf = PyPDF2.PdfWriter()
#                 # PyPDF2 usa índice base 0
#                 pagina_index = numero_pagina - 1
#                 escritor_pdf.add_page(lector_pdf.pages[pagina_index])
#
#                 # Nombre del archivo usando numeración secuencial
#                 nombre_archivo = formato_nombre.format(i + 1) + ".pdf"
#                 ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)
#
#                 # Guardar archivo individual
#                 with open(ruta_archivo, 'wb') as archivo_pagina:
#                     escritor_pdf.write(archivo_pagina)
#
#                 archivos_creados.append(ruta_archivo)
#
#                 # Reportar progreso
#                 progreso = int(((i + 1) / total_paginas_extraer) * 80)  # 80% para archivos individuales
#                 if callback_progreso:
#                     callback_progreso(progreso, f"Extraída página {numero_pagina} ({i + 1} de {total_paginas_extraer})")
#
#                 # Pequeña pausa para permitir actualización de UI
#                 time.sleep(0.01)
#
#             # Crear ZIP si se solicita
#             ruta_zip = None
#             if crear_zip:
#                 if callback_progreso:
#                     callback_progreso(85, "Creando archivo ZIP...")
#
#                 ruta_zip = f"{carpeta_salida}.zip"
#                 with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
#                     for i, archivo in enumerate(archivos_creados):
#                         nombre_en_zip = os.path.basename(archivo)
#                         archivo_zip.write(archivo, nombre_en_zip)
#
#                         # Progreso del ZIP (15% restante)
#                         progreso_zip = 85 + int((i / len(archivos_creados)) * 15)
#                         if callback_progreso:
#                             callback_progreso(progreso_zip, f"Comprimiendo archivo {i + 1} de {len(archivos_creados)}")
#
#             if callback_progreso:
#                 callback_progreso(100, f"¡Extracción completada! {total_paginas_extraer} páginas procesadas.")
#
#     except Exception as e:
#         if callback_progreso:
#             callback_progreso(-1, f"Error: {str(e)}")
#         raise Exception(f"Error al procesar el PDF: {str(e)}")
#
#     return {
#         'archivos_individuales': archivos_creados,
#         'carpeta': carpeta_salida,
#         'zip': ruta_zip,
#         'total_paginas': total_paginas_extraer,
#         'paginas_seleccionadas': paginas_seleccionadas
#     }
#
#
# # Función original dividir_pdf_avanzado ya existente (sin cambios)
# def dividir_pdf_avanzado(ruta_pdf, carpeta_salida=None, formato_nombre="pagina_{:03d}", crear_zip=True,
#                          callback_progreso=None):
#     """
#     Versión avanzada para dividir PDF con más opciones de personalización.
#
#     Args:
#         ruta_pdf (str): Ruta del archivo PDF de entrada
#         carpeta_salida (str, optional): Carpeta donde guardar los archivos
#         formato_nombre (str): Formato para nombrar las páginas (debe incluir {})
#         crear_zip (bool): Si crear un ZIP además de los archivos individuales
#         callback_progreso (callable): Función callback para reportar progreso
#
#     Returns:
#         dict: Información sobre los archivos creados
#     """
#
#     if not os.path.exists(ruta_pdf):
#         raise FileNotFoundError(f"El archivo PDF no existe: {ruta_pdf}")
#
#     # Configurar carpeta de salida
#     if carpeta_salida is None:
#         carpeta_salida = Path(ruta_pdf).stem + "_pages"
#
#     # Crear carpeta si no existe
#     Path(carpeta_salida).mkdir(exist_ok=True)
#
#     archivos_creados = []
#
#     try:
#         with open(ruta_pdf, 'rb') as archivo_pdf:
#             lector_pdf = PyPDF2.PdfReader(archivo_pdf)
#             total_paginas = len(lector_pdf.pages)
#
#             if callback_progreso:
#                 callback_progreso(0, f"Iniciando división de {total_paginas} páginas...")
#
#             # Crear archivos individuales
#             for numero_pagina in range(total_paginas):
#                 escritor_pdf = PyPDF2.PdfWriter()
#                 escritor_pdf.add_page(lector_pdf.pages[numero_pagina])
#
#                 # Nombre del archivo
#                 nombre_archivo = formato_nombre.format(numero_pagina + 1) + ".pdf"
#                 ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)
#
#                 # Guardar archivo individual
#                 with open(ruta_archivo, 'wb') as archivo_pagina:
#                     escritor_pdf.write(archivo_pagina)
#
#                 archivos_creados.append(ruta_archivo)
#
#                 # Reportar progreso
#                 progreso = int(((numero_pagina + 1) / total_paginas) * 80)  # 80% para archivos individuales
#                 if callback_progreso:
#                     callback_progreso(progreso, f"Creada página {numero_pagina + 1} de {total_paginas}")
#
#                 # Pequeña pausa para permitir actualización de UI
#                 time.sleep(0.01)
#
#             # Crear ZIP si se solicita
#             ruta_zip = None
#             if crear_zip:
#                 if callback_progreso:
#                     callback_progreso(85, "Creando archivo ZIP...")
#
#                 ruta_zip = f"{carpeta_salida}.zip"
#                 with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
#                     for i, archivo in enumerate(archivos_creados):
#                         nombre_en_zip = os.path.basename(archivo)
#                         archivo_zip.write(archivo, nombre_en_zip)
#
#                         # Progreso del ZIP (15% restante)
#                         progreso_zip = 85 + int((i / len(archivos_creados)) * 15)
#                         if callback_progreso:
#                             callback_progreso(progreso_zip, f"Comprimiendo archivo {i + 1} de {len(archivos_creados)}")
#
#             if callback_progreso:
#                 callback_progreso(100, "¡División completada exitosamente!")
#
#     except Exception as e:
#         if callback_progreso:
#             callback_progreso(-1, f"Error: {str(e)}")
#         raise Exception(f"Error al procesar el PDF: {str(e)}")
#
#     return {
#         'archivos_individuales': archivos_creados,
#         'carpeta': carpeta_salida,
#         'zip': ruta_zip,
#         'total_paginas': total_paginas
#     }


import os
import time
import zipfile
from pathlib import Path
from multiprocessing import Pool, cpu_count
import PyPDF2


def dividir_pdf_optimizado(ruta_pdf, carpeta_salida=None, formato_nombre="pagina_{:03d}",
                           crear_zip=True, callback_progreso=None,
                           batch_size=1000, max_workers=None, rango_paginas=None):
    """
    Versión optimizada para dividir PDFs grandes (incluso 400k+ páginas).

    Mejoras:
    - Procesamiento por lotes para gestionar memoria
    - Multiprocessing para paralelizar operaciones
    - Opción de rango de páginas específicas
    - Gestión eficiente de memoria

    Args:
        ruta_pdf (str): Ruta del archivo PDF
        carpeta_salida (str): Carpeta destino
        formato_nombre (str): Formato para nombres
        crear_zip (bool): Crear archivo ZIP
        callback_progreso (callable): Callback para progreso
        batch_size (int): Páginas por lote (default: 1000)
        max_workers (int): Procesos paralelos (default: CPU cores - 1)
        rango_paginas (tuple): (inicio, fin) o None para todas

    Returns:
        dict: Información de archivos creados
    """

    if not os.path.exists(ruta_pdf):
        raise FileNotFoundError(f"El archivo PDF no existe: {ruta_pdf}")

    # Configurar carpeta de salida
    if carpeta_salida is None:
        carpeta_salida = Path(ruta_pdf).stem + "_pages"

    Path(carpeta_salida).mkdir(exist_ok=True)

    # Determinar número de workers
    if max_workers is None:
        max_workers = max(1, cpu_count() - 1)

    archivos_creados = []

    try:
        # Obtener información básica del PDF
        with open(ruta_pdf, 'rb') as archivo_pdf:
            lector_pdf = PyPDF2.PdfReader(archivo_pdf)
            total_paginas = len(lector_pdf.pages)

        # Validar rango de páginas
        if rango_paginas:
            inicio, fin = rango_paginas
            inicio = max(0, inicio - 1)  # Convertir a índice 0-based
            fin = min(total_paginas, fin)
            paginas_a_procesar = list(range(inicio, fin))
        else:
            paginas_a_procesar = list(range(total_paginas))

        total_a_procesar = len(paginas_a_procesar)

        if callback_progreso:
            callback_progreso(0, f"Preparando división de {total_a_procesar} páginas...")

        # Dividir en lotes para procesamiento
        lotes = [paginas_a_procesar[i:i + batch_size]
                 for i in range(0, total_a_procesar, batch_size)]

        total_lotes = len(lotes)

        # Procesar cada lote
        for idx_lote, lote in enumerate(lotes):
            # Preparar argumentos para procesamiento paralelo
            args_lote = [
                (ruta_pdf, num_pagina, carpeta_salida, formato_nombre)
                for num_pagina in lote
            ]

            # Procesar lote en paralelo
            with Pool(processes=max_workers) as pool:
                resultados_lote = pool.map(procesar_pagina_individual, args_lote)

            # Agregar archivos creados
            archivos_creados.extend([r for r in resultados_lote if r])

            # Calcular progreso (80% para extracción de páginas)
            progreso = int(((idx_lote + 1) / total_lotes) * 80)
            if callback_progreso:
                paginas_completadas = (idx_lote + 1) * batch_size
                paginas_completadas = min(paginas_completadas, total_a_procesar)
                callback_progreso(
                    progreso,
                    f"Procesadas {paginas_completadas:,} de {total_a_procesar:,} páginas"
                )

            # Pequeña pausa para actualización de UI
            time.sleep(0.01)

        # Crear ZIP si se solicita (y el total no es excesivo)
        ruta_zip = None
        if crear_zip:
            # Advertencia para archivos muy grandes
            if total_a_procesar > 50000:
                if callback_progreso:
                    callback_progreso(
                        85,
                        f"⚠️ Comprimiendo {total_a_procesar:,} archivos. Esto puede tomar mucho tiempo..."
                    )
            else:
                if callback_progreso:
                    callback_progreso(85, "Creando archivo ZIP...")

            ruta_zip = f"{carpeta_salida}.zip"

            # Crear ZIP con compresión por lotes para mejor rendimiento
            with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archivo_zip:
                total_archivos = len(archivos_creados)

                for i, archivo in enumerate(archivos_creados):
                    nombre_en_zip = os.path.basename(archivo)
                    archivo_zip.write(archivo, nombre_en_zip)

                    # Actualizar progreso cada 100 archivos para no saturar
                    if i % 100 == 0 or i == total_archivos - 1:
                        progreso_zip = 85 + int((i / total_archivos) * 15)
                        if callback_progreso:
                            callback_progreso(
                                progreso_zip,
                                f"Comprimiendo: {i + 1:,} / {total_archivos:,} archivos"
                            )

        if callback_progreso:
            callback_progreso(100, f"¡División completada! {total_a_procesar:,} páginas procesadas")

    except Exception as e:
        if callback_progreso:
            callback_progreso(-1, f"Error: {str(e)}")
        raise Exception(f"Error al procesar el PDF: {str(e)}")

    return {
        'archivos_individuales': archivos_creados,
        'carpeta': carpeta_salida,
        'zip': ruta_zip,
        'total_paginas': total_a_procesar
    }


def procesar_pagina_individual(args):
    """
    Procesa una página individual del PDF.
    Función separada para permitir multiprocessing.

    Args:
        args: tupla (ruta_pdf, numero_pagina, carpeta_salida, formato_nombre)

    Returns:
        str: Ruta del archivo creado o None si falla
    """
    ruta_pdf, numero_pagina, carpeta_salida, formato_nombre = args

    try:
        # Abrir PDF solo para esta página (gestión eficiente de memoria)
        with open(ruta_pdf, 'rb') as archivo_pdf:
            lector_pdf = PyPDF2.PdfReader(archivo_pdf)

            # Crear nuevo PDF con solo esta página
            escritor_pdf = PyPDF2.PdfWriter()
            escritor_pdf.add_page(lector_pdf.pages[numero_pagina])

            # Generar nombre de archivo
            nombre_archivo = formato_nombre.format(numero_pagina + 1) + ".pdf"
            ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)

            # Guardar archivo
            with open(ruta_archivo, 'wb') as archivo_pagina:
                escritor_pdf.write(archivo_pagina)

            return ruta_archivo

    except Exception as e:
        print(f"Error procesando página {numero_pagina + 1}: {str(e)}")
        return None


def estimar_tiempo_procesamiento(num_paginas, crear_zip=True):
    """
    Estima el tiempo aproximado de procesamiento.

    Args:
        num_paginas (int): Número de páginas a procesar
        crear_zip (bool): Si se creará ZIP

    Returns:
        dict: Estimación de tiempo
    """
    # Estimaciones basadas en benchmarks (ajusta según tu hardware)
    tiempo_por_pagina = 0.05  # segundos por página
    tiempo_zip_por_archivo = 0.02  # segundos por archivo al comprimir

    tiempo_extraccion = num_paginas * tiempo_por_pagina
    tiempo_zip = (num_paginas * tiempo_zip_por_archivo) if crear_zip else 0
    tiempo_total = tiempo_extraccion + tiempo_zip

    # Ajustar por paralelización (asumiendo 4 cores)
    workers = max(1, cpu_count() - 1)
    tiempo_total_paralelo = tiempo_total / min(workers, 4)

    return {
        'minutos': int(tiempo_total_paralelo / 60),
        'horas': int(tiempo_total_paralelo / 3600),
        'advertencia_muy_grande': num_paginas > 100000
    }