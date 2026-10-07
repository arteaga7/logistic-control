# main.py:

from pathlib import Path
from modules.scan_folder_funcs import scan_folder
from modules.chi_report_funcs import read_xlsm
from modules.mail_funcs import read_msg


PROJECT_DIR = Path(__file__).resolve().parent
FOLDER_PATH = (
    PROJECT_DIR
    / "Unilever"
    / "Productivity Plan - Prueba Bot Controles delivery"
    / "Mexico"
    / "Deliver"
    / "OTB C5.2"
    / "2026"
)
INCLUDE_SUBFOLDERS = True  # Analyze subfolders
OUTPUT_FILE = "folder_content.xlsx"
# Constants related to CHI Report ----------------------
MONTH = "04 April"
CHI_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / "1. CHI Report + Request"
# CHI_REPORT_NAME = "chi report.xlsx"
# Columns to extract of the CHI Report
COLS_CHI_REPORT = ["Responsable", "Approver", "Justificación"]
FINAL_REPORT = "chi_report_processed.xlsx"


scan_folder(FOLDER_PATH, INCLUDE_SUBFOLDERS, OUTPUT_FILE)
df = read_xlsm(CHI_REPORT_FOLDER, COLS_CHI_REPORT)
print(df.head())
email_dict = read_msg(CHI_REPORT_FOLDER)
print(f"From: {email_dict["sender"]}")
print(f"Cc: {email_dict["cc"]}")

"""
mailto_chi_report = ['Antonio.Arteaga@unilever.com', 'juan@example.com']
from_justifications = ['ilya@example.com', 'juan@example.com']
print(f"From: {email_dict["sender"]}")
print(f"Cc: {email_dict["cc"]}")


df = compare_col_content(df=df, col="Responsable",
                         new_col="Enviado", list=mailto_list)
# print(df.head())
df = compare_col_content(df=df, col="Responsable",
                         new_col="Feedback", list=feedback_list)
print(df.head())

if __name__ == "__main__":
    main()
"""
