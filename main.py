# main.py:

from pathlib import Path
from modules.scan_folder_funcs import scan_folder

RELATIVE_PATH = Path("Unilever") / \
    "Productivity Plan - Prueba Bot Controles delivery" / \
    "Mexico" / "Deliver" / "OTB C5.2" / "2026"
ROOT_PATH = Path(__file__).parent / RELATIVE_PATH
FOLDER_PATH = ROOT_PATH / "03 March" / "1. CHI Report + Request"
OUTPUT_FILE = "folder_content.xlsx"

INCLUDE_SUBFOLDERS = True
# False: solamente analiza la carpeta "./"
# True: también analiza todas las subcarpetas

scan_folder(FOLDER_PATH, INCLUDE_SUBFOLDERS, OUTPUT_FILE, RELATIVE_PATH)
