"""
Initialize the app application FastAPI
Usage:
    python -m scripts.init_app
Notes:
    - This will start only the FastAPI app. The content server is started separately.

    (The command <$uvicorn api.app:app --reload> can be used to start the API server
    without running this script, but this script is useful for testing).
"""

import subprocess
from config import config

try:
    p = subprocess.Popen(["uvicorn", "api.app:app", "--reload"])
    print(f"[INFO] ✅ API server running http://localhost:{config.api.port} (PID: {p.pid})")
except Exception as e:
    print(f"[ERR ] Failed to start API server: {e}")
    exit()
