# main.py:

from pathlib import Path
from modules.scan_folder_funcs import scan_folder
from modules.chi_report_funcs import *

PROJECT_DIR = Path(__file__).resolve().parent
FOLDER_PATH = (
    PROJECT_DIR
    / "Unilever"
    / "Productivity Plan - Prueba Bot Controles delivery"
    / "Mexico"
    / "Deliver"
    / "OTB C5.2"
    / "2026"
    / "03 March"
)
INCLUDE_SUBFOLDERS = True  # Analyze subfolders
OUTPUT_FILE = "folder_content.xlsx"
# Constants related to CHI Report ----------------------
CHI_REPORT_FOLDER = Path(FOLDER_PATH) / "1. CHI Report + Request"
CHI_REPORT_NAME = "chi report.xlsx"
# Columns to extract of the CHI Report
COLS_CHI_REPORT = ["Delivery", "Responsable", "Justificación"]
FINAL_REPORT = "chi_report_processed.xlsx"
report_path = CHI_REPORT_FOLDER / CHI_REPORT_NAME

scan_folder(FOLDER_PATH, INCLUDE_SUBFOLDERS, OUTPUT_FILE)

df = read_chi_report(file_path=report_path, cols=COLS_CHI_REPORT)
print(df.head())
mailto_chi_report = ['Antonio.Arteaga@unilever.com', 'juan@example.com']
from_justifications = ['ilya@example.com', 'juan@example.com']


"""
df = compare_col_content(df=df, col="Responsable",
                         new_col="Enviado", list=mailto_list)
# print(df.head())
df = compare_col_content(df=df, col="Responsable",
                         new_col="Feedback", list=feedback_list)
print(df.head())
"""
