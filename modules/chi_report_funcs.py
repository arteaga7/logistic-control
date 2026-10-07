# chi_report_funcs.py:

from pathlib import Path
import pandas as pd


def read_chi_report(file_path: str | Path, cols: list[str]) -> pd.DataFrame:
    """
    Lee el archivo 'chi report.xlsx'. Pasos:
    1. Cambia el directorio de trabajo a folder_path.
    2. Lee la hoja 'Reporte'.
    3. Extrae las columnas "'Delivery", "Responsable" y "Justificación".
    """
    if not file_path.is_file():
        raise FileNotFoundError(
            f"No se encontró el CHI Report: {file_path}"
        )
    try:
        df = pd.read_excel(
            file_path,
            sheet_name="Reporte",
            usecols=cols,
            engine="openpyxl"
        )
    except ValueError as error:
        raise ValueError(
            "No se encontro la hoja o las columnas esperadas"
            f"'Reporte'. Columnas requeridas: {cols}"
        ) from error
    return df


def compare_col_content(df: pd.DataFrame, col: str, new_col: str, addresses: list[str]) -> pd.DataFrame:
    """
    Compare column "col" with "list", if the content of column is in list,
    assign “si” in "new_col", otherwise assign “no”
    """
    df = df.copy()
    df[new_col] = df[col].isin(addresses)
    return df
