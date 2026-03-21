# launcher.py - Aural Alchemy MIDI Generator
# Starts the embedded Streamlit server then opens the default browser.
# Compatible with Streamlit >= 1.28 and PyInstaller bundles.

import os
import sys
import time
import socket
import threading
import webbrowser
from pathlib import Path


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def wait_for_server(host: str = "127.0.0.1", port: int = 8501, timeout: int = 60) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.4)
    return False


def open_browser_when_ready(port: int = 8501) -> None:
    if wait_for_server(port=port):
        webbrowser.open(f"http://127.0.0.1:{port}")


if __name__ == "__main__":
    base_dir = get_base_dir()
    os.chdir(base_dir)

    app_path = base_dir / "app.py"
    if not app_path.exists():
        raise FileNotFoundError(f"app.py not found at {app_path}")

    port = 8501

    threading.Thread(
        target=open_browser_when_ready,
        kwargs={"port": port},
        daemon=True,
    ).start()

    from streamlit.web import cli as stcli
    import click

    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.port", str(port),
        "--server.address", "127.0.0.1",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--global.developmentMode", "false",
    ]

    try:
        stcli.main(standalone_mode=False)
    except SystemExit:
        pass
    except click.exceptions.Abort:
        pass
