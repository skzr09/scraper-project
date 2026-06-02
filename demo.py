
import subprocess
import time
import os

from colorama import init

from config import config
from scripts.init_db import init_db

p1 = None
p2 = None


def start_processes():
    """ Start processed for server and API """
    global p1, p2

    print("[INFO] Starting server...")
    p1 = subprocess.Popen(["python", "-m", "scripts.init_server"])

    print("[INFO] Starting API...")
    p2 = subprocess.Popen(["uvicorn", "api.app:app", "--reload"])

    print(f"[INFO] ✅ Server running (PID: {p1.pid}) See http://localhost:{config.server.port}")
    print(f"[INFO] ✅ API running    (PID: {p2.pid}) See http://localhost:{config.api.port}")


def stop_process(proc, name):
    """ Stop a process if it's still running """
    if proc and proc.poll() is None:  # still running
        print(f"[INFO] Stopping {name} (PID: {proc.pid})...")
        proc.terminate()

        try:
            proc.wait(timeout=5)
            print(f"[OK  ] ✅ {name} stopped")
        except subprocess.TimeoutExpired:
            print(f"[WARN] {name} did not stop, killing...")
            proc.kill()


def cleanup():
    """ Clean up processes on exit """
    print("\n[INFO] Cleaning up processes...")
    stop_process(p1, "Server")
    stop_process(p2, "API")
    print("[INFO] ✅ Shutdown complete")


def init_local_db():
    """ Initialize local database if it doesn't exist """
    if not config.database.path:
        print("[ERR ] Database path is not set in config!")
        exit()

    # Check if database already exists
    if os.path.exists(config.database.path):
        print("[WARN] Database already exists!")
    else:
        init_db()
    print(f"[INFO] ✅ DB Path: {config.database.path}")
    

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    try:
        print("==================[ SCRAPER DEMO ]==================")
        print("[INFO] Initializing demo environment...")

        init_local_db()
        start_processes()

        print("====================================================")

        # Keep main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("====================================================")
        print("\n[INFO] CTRL+C detected")

    finally:
        cleanup()
        print("[INFO] Demo environment cleaned up. Exiting.")