# scan_folder_funcs.py: Functions related to scan_folder.py

from pathlib import Path
from datetime import datetime
import pandas as pd


def get_folder_files(
    folder_path: str, recursive: bool = False, exclude_files=None
) -> list[dict]:
    """Obtiene los archivos de una carpeta local.
    Parámetros:
        folder_path:
            Ruta de la carpeta que se desea analizar.
        recursive:
            False: analiza solamente la carpeta indicada.
            True: analiza también todas sus subcarpetas.
        exclude_files:
            Lista opcional de archivos que no deben incluirse.
    """
    folder = Path(folder_path).resolve()
    if not folder.exists():
        raise FileNotFoundError(
            f"La carpeta no existe: {folder}"
        )
    if not folder.is_dir():
        raise NotADirectoryError(
            f"La ruta no corresponde a una carpeta: {folder}"
        )
    exclude_files = exclude_files or []
    excluded_names = {
        Path(file).name.lower()
        for file in exclude_files
    }
    if recursive:
        paths = folder.rglob("*")
    else:
        paths = folder.iterdir()

    files = []
    for path in paths:
        if not path.is_file():
            continue
        if path.name.lower() in excluded_names:
            continue
        try:
            properties = path.stat()
            files.append({
                "path": path,
                "properties": properties
            })
        except (PermissionError, OSError) as error:
            print(
                f"No se pudo leer el archivo "
                f"'{path}': {error}"
            )
    return files


def add_extension_metadata(files: list[dict]) -> list[dict]:
    """Construye las propiedades de cada archivo local."""
    result = []
    # Up one level from modules/ to reach the root project folder
    relative_folder = Path(__file__).parent.parent

    for file in files:
        path = file["path"]
        properties = file["properties"]
        result.append({
            "relative_path": str(path.relative_to(relative_folder)),
            "name": path.name,
            "extension": path.suffix.lower(),
            "size_bytes": properties.st_size,
            "created": datetime.fromtimestamp(
                properties.st_ctime
            ),
            "modified": datetime.fromtimestamp(
                properties.st_mtime
            ),
            "absolute_path": str(path.resolve())
        })
    return result


def summarize_extensions(files: list[dict]) -> dict:
    """Cuenta cuántos archivos existen por extensión."""
    summary = {}
    for file in files:
        extension = file["extension"] or "SIN_EXTENSION"
        summary[extension] = (
            summary.get(extension, 0) + 1
        )
    return summary


def export_to_excel(files: list[dict], summary: dict, output_file: str):
    """Exporta el inventario y el resumen a Excel."""
    df_files = pd.DataFrame(files)
    df_summary = pd.DataFrame([
        {
            "extension": extension,
            "cantidad": quantity
        }
        for extension, quantity
        in summary.items()
    ])

    if not df_files.empty:
        df_files = df_files.sort_values(
            by=["extension", "name"]
        )

    if not df_summary.empty:
        df_summary = df_summary.sort_values(
            by="cantidad",
            ascending=False
        )

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df_files = df_files.sort_values(by=["relative_path"])
        df_files.to_excel(
            writer, sheet_name="Archivos", index=False
        )
        df_summary.to_excel(
            writer, sheet_name="Resumen", index=False
        )


def scan_folder(FOLDER_PATH: Path, INCLUDE_SUBFOLDERS: bool, OUTPUT_FILE: str):
    files = get_folder_files(
        folder_path=FOLDER_PATH,
        recursive=INCLUDE_SUBFOLDERS,
        exclude_files=[OUTPUT_FILE]
    )
    files = add_extension_metadata(files=files)
    summary = summarize_extensions(files)
    export_to_excel(
        files=files,
        summary=summary,
        output_file=OUTPUT_FILE
    )
    print(f"Total de archivos encontrados: {len(files)}")
    print(f"Inventario generado: {OUTPUT_FILE}")
