from pathlib import Path
import runpy

APP_FILE = Path(__file__).resolve().parent / "dashboard" / "dashboard.py"
runpy.run_path(str(APP_FILE), run_name="__main__")
