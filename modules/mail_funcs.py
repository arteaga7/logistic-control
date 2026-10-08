# read_mail.py

from pathlib import Path
import extract_msg
from modules.chi_report_funcs import get_filenames
import re
import html


def extract_emails(texto: str) -> list[str]:
    """Extrae el contenido dentro de <...> del texto y retorna una lista."""
    # convierte &lt; &gt; en < >, por si vienen escapados
    texto = html.unescape(texto)
    patron = re.compile(r"<([^<>]+)>")
    return [m.strip() for m in patron.findall(texto)]


def read_msg(folder_path: Path, n_mails: int | None = None,
             extension: str = "*.msg", property: str = "to") -> list[str]:
    """
    Extrae todas las direcciones de correo de la propiedad indicada
    ("to", "cc" o "sender") de los archivos .msg.
    """
    msg_names = get_filenames(folder_path, extension)
    if n_mails is not None:
        msg_names = msg_names[:n_mails]

    addresses = []
    for msg_name in msg_names:
        file_path = folder_path / msg_name
        message = None
        try:
            message = extract_msg.Message(file_path)
            value = getattr(message, property, None)
            if value:
                addresses.extend(extract_emails(value))

        except Exception:
            pass

        finally:
            if message is not None:
                message.close()

    return addresses
