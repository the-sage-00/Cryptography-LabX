"""
Crypto-LabX - Logger
Records date, time, and selected menu option for every execution.
Log entries are appended to outputs/cryptolabx.log.
"""

import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
LOG_FILE = os.path.join(LOG_DIR, "cryptolabx.log")


def _ensure_log_dir():
    """Create the log directory if it doesn't exist."""
    os.makedirs(LOG_DIR, exist_ok=True)


def log_action(option_name):
    """
    Append a timestamped log entry for the selected menu option.

    Args:
        option_name: Name of the menu option selected (e.g. Encrypt, Decrypt).
    """
    _ensure_log_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] Selected: {option_name}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
