import os
import sys
import time
import socket
import threading
import webbrowser
from pathlib import Path

import streamlit.web.bootstrap as bootstrap


def wait_for_server(host="127.0.0.1", port=8501, timeout=45):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def open_browser_when_ready():
    if wait_for_server():
        webbrowser.open("http://127.0.0.1:8501")


if __name__ == "__main__":
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    os.chdir(base_dir)

    app_path = base_dir / "app.py"
    if not app_path.exists():
        raise FileNotFoundError(f"app.py not found at {app_path}")

    threading.Thread(target=open_browser_when_ready, daemon=True).start()

    flag_options = {
        "server.port": 8501,
        "server.address": "127.0.0.1",
        "server.headless": True,
        "browser.gatherUsageStats": False,
        "global.developmentMode": False,
    }

    bootstrap.load_config_options(flag_options=flag_options)
    flag_options["_is_running_with_streamlit"] = True

    bootstrap.run(
        str(app_path),
        "streamlit run",
        [],
        flag_options,
    )
