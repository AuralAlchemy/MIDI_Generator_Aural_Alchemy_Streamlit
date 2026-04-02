# launcher.py - Aural Alchemy MIDI Generator
# Starts the embedded Streamlit server then opens the default browser.
# Shuts down automatically when the browser disconnects.

import os
import sys
import time
import socket
import threading
import webbrowser
import signal
import subprocess
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


def watch_for_disconnect(host: str = "127.0.0.1", port: int = 8501) -> None:
    if not wait_for_server(host=host, port=port, timeout=60):
        return

    time.sleep(8)

    while True:
        time.sleep(3)
        try:
            with socket.create_connection((host, port), timeout=2):
                pass
        except OSError:
            os.kill(os.getpid(), signal.SIGTERM)
            sys.exit(0)


def kill_port(port: int) -> None:
    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        subprocess.call(
            f"lsof -ti tcp:{port} | xargs kill -9",
            shell=True,
            stderr=subprocess.DEVNULL
        )
    elif sys.platform == "win32":
        subprocess.call(
            f"for /f \"tokens=5\" %a in ('netstat -aon ^| find \":{port}\"') do taskkill /F /PID %a",
            shell=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL
        )


if __name__ == "__main__":
    base_dir = get_base_dir()
    os.chdir(base_dir)

    app_path = base_dir / "app.py"
    if not app_path.exists():
        raise FileNotFoundError(f"app.py not found at {app_path}")

    port = 8501

    # Kill any ghost server still on this port
    kill_port(port)
    time.sleep(1)

    # Open browser once server is ready
    threading.Thread(
        target=open_browser_when_ready,
        kwargs={"port": port},
        daemon=True,
    ).start()

    # Shut down when browser disconnects
    threading.Thread(
        target=watch_for_disconnect,
        kwargs={"host": "127.0.0.1", "port": port},
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
