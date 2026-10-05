# main.py:
import os
from pathlib import Path
from modules.scan_folder_funcs import scan_folder
from modules.chi_report_funcs import *

RELATIVE_PATH = Path("Unilever") / \
    "Productivity Plan - Prueba Bot Controles delivery" / \
    "Mexico" / "Deliver" / "OTB C5.2" / "2026"
ROOT_PATH = Path(__file__).parent / RELATIVE_PATH
FOLDER_PATH = ROOT_PATH / "03 March" / "1. CHI Report + Request"

INCLUDE_SUBFOLDERS = True
# False: solamente analiza la carpeta "./"
# True: también analiza todas las subcarpetas
OUTPUT_FILE = "folder_content.xlsx"
CHI_REPORT_NAME = Path("chi report.xlsx")
FINAL_REPORT = "chi_report_processed.xlsx"

scan_folder(FOLDER_PATH, INCLUDE_SUBFOLDERS, OUTPUT_FILE, RELATIVE_PATH)
df = read_chi_report(folder_path=FOLDER_PATH, CHI_REPORT_NAME=CHI_REPORT_NAME)
mailto_list = ['Antonio.Arteaga@unilever.com']
feedback_list = ['ilya@example.com']
df = compare_col_content(df=df, col="Responsable",
                         new_col="Enviado", list=mailto_list)
# print(df.head())
df = compare_col_content(df=df, col="Responsable",
                         new_col="Feedback", list=feedback_list)
print(df.head())
