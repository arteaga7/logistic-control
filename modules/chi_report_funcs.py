# chi_report_processed.py:

from pathlib import Path
import os
import pandas as pd


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


def compare_col_content(df: pd.DataFrame, col: str, new_col: str, list: list[str]) -> pd.DataFrame:
    """
    Compare column "col" with "list", if the content of column is in list,
    assign “si” in "new_col", otherwise assign “no”
    """
    df = df.copy()
    df[new_col] = df[col].isin(list).map({
        True: "si",
        False: "no"
    })
    return df
