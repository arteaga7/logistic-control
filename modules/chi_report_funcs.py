# chi_report_processed.py:

from pathlib import Path
import os
import pandas as pd


def chi_report_processed(
    folder_path: str | Path,
    archivo_salida: str = "chi_report_processed.xlsx"
) -> pd.DataFrame:
    """
    Lee y transforma el archivo 'chi report.xlsx'.
    Pasos:
    1. Cambia el directorio de trabajo a folder_path.
    2. Lee la hoja 'Reporte'.
    3. Extrae las columnas "'Delivery", "Responsable" y "Justificación".
    4. Agrega las columnas "Sent" y "feedback".
    5. Guarda el resultado en un nuevo archivo Excel.
    Retorna:
        DataFrame procesado.
    """

    folder_path = Path(folder_path).expanduser().resolve()

    if not folder_path.is_dir():
        raise NotADirectoryError(
            f"La ruta no existe o no es una carpeta: {folder_path}"
        )

    # Mover el directorio de trabajo a FOLDER_PATH
    os.chdir(folder_path)

    archivo_entrada = Path("chi report.xlsx")
    ruta_salida = Path(archivo_salida)

    if not archivo_entrada.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo: {archivo_entrada.resolve()}"
        )

    # Columns to extract
    columnas = ["Delivery", "Responsable", "Justificación"]

    try:
        df = pd.read_excel(
            archivo_entrada,
            sheet_name="Reporte",
            usecols=columnas,
            engine="openpyxl"
        )
    except ValueError as error:
        raise ValueError(
            "No se encontraron todas las columnas esperadas en la hoja "
            f"'Reporte'. Columnas requeridas: {columnas}"
        ) from error

    # Agregar las nuevas columnas vacías
    df["Sent"] = pd.NA
    df["feedback"] = pd.NA

    # Guardar el DataFrame en la ruta actual, que ahora es FOLDER_PATH
    df.to_excel(
        ruta_salida,
        index=False,
        engine="openpyxl"
    )

    print(f"Archivo generado correctamente: {ruta_salida.resolve()}")
    return df


def read_chi_report(folder_path: str | Path, CHI_REPORT_NAME: Path) -> pd.DataFrame:
    """
    Lee y transforma el archivo 'chi report.xlsx'.
    Pasos:
    1. Cambia el directorio de trabajo a folder_path.
    2. Lee la hoja 'Reporte'.
    3. Extrae las columnas "'Delivery", "Responsable" y "Justificación".
    """
    folder_path = Path(folder_path).expanduser().resolve()

    if not folder_path.is_dir():
        raise NotADirectoryError(
            f"La ruta no existe o no es una carpeta: {folder_path}"
        )

    # Mover el directorio de trabajo a FOLDER_PATH
    os.chdir(folder_path)

    if not CHI_REPORT_NAME.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo: {CHI_REPORT_NAME.resolve()}"
        )

    # Columns to extract
    columnas = ["Delivery", "Responsable", "Justificación"]

    try:
        df = pd.read_excel(
            CHI_REPORT_NAME,
            sheet_name="Reporte",
            usecols=columnas,
            engine="openpyxl"
        )
    except ValueError as error:
        raise ValueError(
            "No se encontraron todas las columnas esperadas en la hoja "
            f"'Reporte'. Columnas requeridas: {columnas}"
        ) from error

    return df
