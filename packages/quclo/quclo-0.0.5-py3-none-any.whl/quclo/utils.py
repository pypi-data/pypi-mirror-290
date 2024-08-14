"""Utility functions for QuClo."""

import os
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
import subprocess
from click import get_app_dir
from openqasm3 import parser
from pyqir import Module, Context

APP_NAME = "quclo"
CONFIG_FILE = os.path.join(get_app_dir(APP_NAME), "config.ini")
QUCLO_API_URL = "https://quclo.com/api/"
IMPORT_TEMPLATE = """
import quclo
quclo.proxy()
""".strip()


def duration_to_expires_at(duration: int | None) -> str | None:
    """Convert a duration to an expiration date."""
    if duration is None:
        return None
    return (datetime.now() + timedelta(days=duration)).isoformat()


def run_file_with_proxy(file: str, token: str, prepend_text: str = IMPORT_TEMPLATE):
    with NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(prepend_text + "\n")
        with open(file, "r") as original_file:
            temp_file.write(original_file.read())
    subprocess.run(["python", temp_file.name], check=True)


def check_qasm(qasm: str) -> bool:
    """Check if the QASM is valid."""
    try:
        parser.parse(qasm)
        return True
    except:
        return False


def check_qir(qir: str | bytes) -> bool:
    """Check if the QIR is valid."""
    try:
        Module.from_ir(Context(), qir)  # type: ignore
        return True
    except:
        try:
            Module.from_bitcode(Context(), qir)  # type: ignore
            return True
        except:
            return False
