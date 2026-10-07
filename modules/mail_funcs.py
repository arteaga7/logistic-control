# read_mail.py

from pathlib import Path
import extract_msg
from modules.chi_report_funcs import get_filename
import re
import html


def extract_emails(texto: str) -> list[str]:
    """Extrae el contenido dentro de <...> del texto y retorna una lista."""
    # convierte &lt; &gt; en < >, por si vienen escapados
    texto = html.unescape(texto)
    patron = re.compile(r"<([^<>]+)>")
    return [m.strip() for m in patron.findall(texto)]


def read_msg(folder_path: Path) -> dict:
    """Extrae cuerpo y metadatos de un archivo .msg"""
    msg_name = get_filename(folder_path, extension="*.msg")

    if not msg_name:
        raise FileNotFoundError(
            f"No se encontró ningún archivo .msg en {folder_path}"
        )

    msg_path = folder_path / msg_name
    msg = extract_msg.Message(msg_path)
    datos = {
        "file": Path(msg_path).name,
        "subject": msg.subject,
        "sender": msg.sender,
        "to": extract_emails(msg.to),
        "cc": extract_emails(msg.cc),
        # "bcc": split_emails(msg.bcc),
        "date": str(msg.date) if msg.date else None,
        # "message_id": getattr(msg, "messageId", None),
        "body": msg.body,
    }
    return datos
