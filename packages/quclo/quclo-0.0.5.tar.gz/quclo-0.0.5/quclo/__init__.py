"""
.. include:: ../README.md
   :start-line: 1
"""

from importlib.metadata import version
from pathlib import Path
from .backend import Backend
from .circuit import Circuit
from .config import Config
from .execution import Execution
from .models import Priority
from .proxy import proxy
from .user import User
from .utils import APP_NAME, CONFIG_FILE

__all__ = [
    "Backend",
    "Circuit",
    "Config",
    "Execution",
    "Priority",
    "User",
    "proxy",
]

__version__ = version(APP_NAME)

if not Path(CONFIG_FILE).exists():
    path = Path(CONFIG_FILE)
    path.parent.mkdir(exist_ok=True)
    path.touch()
