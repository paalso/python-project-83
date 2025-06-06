# ruff: noqa: E402, F401

import sys
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(BASE_DIR))

load_dotenv(dotenv_path=BASE_DIR / '.env')

from page_analyzer.app import app as application
