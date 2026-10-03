# scan_folder.py: Finds all properties of all files a a folder

from pathlib import Path
from modules.scan_folder_funcs import scan_folder

ROOT_PATH = Path(__file__).parent / "Unilever" / \
    "Productivity Plan - Prueba Bot Controles delivery" / \
    "Mexico" / "Deliver" / "OTB C5.2" / "2026"
ROOT_PATH = Path(__file__).parent / "Unilever"
FOLDER_PATH = ROOT_PATH / "03 March" / "1. CHI Report + Request"
OUTPUT_FILE = "folder_content.xlsx"

# False: solamente analiza la carpeta "./"
# True: también analiza todas las subcarpetas
INCLUDE_SUBFOLDERS = True

scan_folder(FOLDER_PATH, INCLUDE_SUBFOLDERS, OUTPUT_FILE)
