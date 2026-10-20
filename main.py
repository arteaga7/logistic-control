# main.py:
from pathlib import Path
import argparse
from modules.scan_folder_funcs import scan_folder, create_folder_structure
from modules.chi_report_funcs import read_xlsm, compare_col_content, save_excel
from modules.mail_funcs import read_msg
from datetime import datetime
import json

PROJECT_DIR = Path(__file__).resolve().parent
INCLUDE_SUBFOLDERS = True  # Analyze subfolders
folders = ["01 January", "02 February", "03 March", "04 April", "05 May", "06 June",
           "07 July", "08 Augost", "09 September", "10 October", "11 November",
           "12 Dicember"]
subfolders = ["1. CHI Report + Request", "2. Justifications", "3. Approvals"]
parser = argparse.ArgumentParser()
parser.add_argument("--month", default="03 March")
parser.add_argument("--unilever_path", type=Path, default=PROJECT_DIR)
args = parser.parse_args()
MONTH = "08 Augost"  # args.month
UNILEVER_PATH = args.unilever_path

FOLDER_PATH = (
    UNILEVER_PATH / "Unilever"
    / "Productivity Plan - Prueba Bot Controles delivery"
    / "Mexico" / "Deliver" / "OTB C5.2" / "2026"
)
COLS_CHI_REPORT = ["Responsable", "Approver", "Justificación"]
CHI_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / "1. CHI Report + Request"
JUSTIFICATION_FOLDER = Path(FOLDER_PATH) / MONTH / "2. Justifications"
APPOVAL_FOLDER = Path(FOLDER_PATH) / MONTH / "3. Approvals"
date = datetime.now().strftime('%Y%m%d_%H%M%S')
FINAL_REPORT = "Report_local_" + MONTH + f"_{date}" + ".xlsx"
FINAL_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / FINAL_REPORT
OUTPUT_FILE = "folder_content" + f"_{date}" + ".xlsx"

headers = {"Content-Type": "application/json"}
URL = "https://defaultf66fae025d36495bbfe078a6ff9f8e.6e.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/05/workflows/9560f13a31ba4795b346c4b0ae2df14f/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ksORmCQP6YZcCPu2kkxxfA7v_hztHNaX8MJnaCcw1Bk"
json_file = json.dumps({
    "mode": "refresh",
    # "sas_uri": "https://dbstorageda09p930814.blob.core.windows.net/",
    # "blob_path": "unilever/FillRate/Flujo_Casa_Ley.xlsx",
    # "site": "https://unilever.sharepoint.com/sites/SKY_CE",
    # "sharepoint_path": "/Shared Documents/CEX SILVER/CASA LEY/",
    # "file_name": "Flujo_Casa_Ley.xlsx",
    "email": "Antonio.Arteaga@Unilever.com",
    "cc": "",
    "subject": "Pruebita BOT",
    "body": """Estimado cliente:<br><br>

    Este correo se genera de manera automática con el fin de prueba<br><br>

    Saludos cordiales."""
})

if __name__ == "__main__":
    create_folder_structure(FOLDER_PATH, folders, subfolders)
    # scan_folder(FOLDER_PATH, INCLUDE_SUBFOLDERS, OUTPUT_FILE)
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

    # save_excel(df_final, FINAL_REPORT_FOLDER)
