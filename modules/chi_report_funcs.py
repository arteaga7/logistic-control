# chi_report_funcs.py:

from pathlib import Path
import pandas as pd


def get_filename(folder_path: Path, extension: str) -> str | None:
    """
    Regresa el nombre del primer archivo .xlsm encontrado
    o None si no existe ninguno.
    """
    for file in folder_path.glob(extension):
        return file.name
    return None


def read_chi_report(file_path: str | Path, cols: list[str]) -> pd.DataFrame:
    """Lee el archivo '.xlsn' en la hoja 'Reporte' y extrae las columnas
    "Responsable", "Approver" y "Justificación"."""
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


def read_xlsm(folder_path: Path, cols: list[str]) -> pd.DataFrame:
    xlsm_name = get_filename(folder_path, extension="*.xlsm")
    if not xlsm_name:
        raise FileNotFoundError(
            f"No se encontró ningún archivo .xlsm en {folder_path}"
        )
    return read_chi_report(
        file_path=folder_path / xlsm_name,
        cols=cols
    )


def compare_col_content(df: pd.DataFrame, col: str, new_col: str, addresses: list[str]) -> pd.DataFrame:
    """
    Compare column "col" with "list", if the content of column is in list,
    assign “si” in "new_col", otherwise assign “no”
    """
    df = df.copy()
    df[new_col] = df[col].isin(addresses)
    return df
