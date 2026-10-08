# main.py:
from pathlib import Path
from modules.scan_folder_funcs import scan_folder
from modules.chi_report_funcs import read_xlsm, compare_col_content, save_excel
from modules.mail_funcs import read_msg
from datetime import datetime

PROJECT_DIR = Path(__file__).resolve().parent
FOLDER_PATH = (
    PROJECT_DIR / "Unilever"
    / "Productivity Plan - Prueba Bot Controles delivery"
    / "Mexico" / "Deliver" / "OTB C5.2" / "2026"
)
INCLUDE_SUBFOLDERS = True  # Analyze subfolders
OUTPUT_FILE = "folder_content.xlsx"
MONTH = "03 March"
COLS_CHI_REPORT = ["Responsable", "Approver", "Justificación"]
CHI_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / "1. CHI Report + Request"
JUSTIFICATION_FOLDER = Path(FOLDER_PATH) / MONTH / "2. Justifications"
APPOVAL_FOLDER = Path(FOLDER_PATH) / MONTH / "3. Approvals"
date = datetime.now().strftime('%Y%m%d_%H%M%S')
FINAL_REPORT = "Report_" + MONTH + f"_{date}" + ".xlsx"
FINAL_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / FINAL_REPORT

if __name__ == "__main__":
    scan_folder(FOLDER_PATH, INCLUDE_SUBFOLDERS, OUTPUT_FILE)
    df = read_xlsm(CHI_REPORT_FOLDER, COLS_CHI_REPORT)
    mailto_chi_report = read_msg(folder_path=CHI_REPORT_FOLDER, n_mails=1,
                                 extension="*.msg", property="to")
    from_justifications = read_msg(folder_path=JUSTIFICATION_FOLDER,
                                   extension="*.msg", property="sender")
    from_approver = read_msg(folder_path=APPOVAL_FOLDER,
                             extension="*.msg", property="sender")
    # Step 1
    df = compare_col_content(df=df, col="Responsable",
                             new_col="Enviado", mails=mailto_chi_report)
    # Step 2
    df = compare_col_content(df=df, col="Responsable",
                             new_col="Feedback", mails=from_justifications)
    # Step 3
    df = compare_col_content(df=df, col="Approver",
                             new_col="Aprobacion", mails=from_approver)

    df_final = df[["Responsable", "Enviado", "Feedback",
                   "Approver", "Aprobacion", "Justificación"]]
    save_excel(df_final, FINAL_REPORT)
    save_excel(df_final, FINAL_REPORT_FOLDER)
