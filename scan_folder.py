# scan_folder.py: Finds all properties of all files a a folder

from pathlib import Path
from modules.functions import (
    get_folder_files,
    add_extension_metadata,
    summarize_extensions,
    export_to_excel
)

ROOT_PATH = Path(__file__).parent / "Unilever" / \
    "Productivity Plan - Prueba Bot Controles delivery" / \
    "Mexico" / "Deliver" / "OTB C5.2" / "2026"

FOLDER_PATH = ROOT_PATH / "03 March" / "1. CHI Report + Request"
OUTPUT_FILE = "folder_content.xlsx"

# False: solamente analiza la carpeta "./"
# True: también analiza todas las subcarpetas
INCLUDE_SUBFOLDERS = True

files = get_folder_files(
    folder_path=FOLDER_PATH,
    recursive=INCLUDE_SUBFOLDERS,
    exclude_files=[OUTPUT_FILE]
)

files = add_extension_metadata(
    files=files, base_folder=FOLDER_PATH
)

summary = summarize_extensions(files)

export_to_excel(
    files=files,
    summary=summary,
    output_file=OUTPUT_FILE
)

print(f"Total de archivos encontrados: {len(files)}")
print(f"Inventario generado: {OUTPUT_FILE}")
