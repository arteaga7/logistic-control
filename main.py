# main.py:

from pathlib import Path
from modules.scan_folder_funcs import scan_folder
from modules.chi_report_funcs import read_xlsm, compare_col_content, save_excel
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
MONTH = "03 March"
CHI_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / "1. CHI Report + Request"
JUSTIFICATION_FOLDER = Path(FOLDER_PATH) / MONTH / "2. Justifications"
APPOVAL_FOLDER = Path(FOLDER_PATH) / MONTH / "3. Approvals"
# Columns to extract of the CHI Report
COLS_CHI_REPORT = ["Responsable", "Approver", "Justificación"]
FINAL_REPORT = "chi_report_processed.xlsx"


# scan_folder(FOLDER_PATH, INCLUDE_SUBFOLDERS, OUTPUT_FILE)
df = read_xlsm(CHI_REPORT_FOLDER, COLS_CHI_REPORT)
# print(df.head())
mailto_chi_report = read_msg(folder_path=CHI_REPORT_FOLDER, n_mails=1,
                             extension="*.msg", property="to")
# print(f"\nmailto: {mailto_chi_report}")

from_justifications = read_msg(folder_path=JUSTIFICATION_FOLDER,
                               extension="*.msg", property="sender")
# print(f"\nfrom: {from_justifications}")


df = compare_col_content(df=df, col="Responsable",
                         new_col="Enviado", mails=mailto_chi_report)
df = compare_col_content(df=df, col="Responsable",
                         new_col="Feedback", mails=from_justifications)

save_excel(df, FINAL_REPORT)
"""

if __name__ == "__main__":
    main()
"""
