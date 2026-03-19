import os
import sys
import time
import atexit
import socket
import signal
import webbrowser
import subprocess
from pathlib import Path

process = None


def is_port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def wait_for_server(host: str, port: int, timeout: int = 30) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        if is_port_open(host, port):
            return True
        time.sleep(0.5)
    return False


def cleanup() -> None:
    global process
    if process and process.poll() is None:
        try:
            if sys.platform.startswith("win"):
                process.terminate()
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except Exception:
            pass


def resource_path(relative_path: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent / relative_path


def main() -> None:
    global process
    atexit.register(cleanup)

    host = "127.0.0.1"
    port = 8501
    url = f"http://{host}:{port}"
    app_path = resource_path("app.py")

    env = os.environ.copy()
    env["BROWSER"] = "none"

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
        "--server.address",
        host,
        "--server.port",
        str(port),
    ]

    if sys.platform.startswith("win"):
        process = subprocess.Popen(cmd, env=env)
    else:
        process = subprocess.Popen(cmd, env=env, preexec_fn=os.setsid)

    if wait_for_server(host, port, timeout=30):
        webbrowser.open(url)
        process.wait()
    else:
        print("Streamlit server did not start in time.")
        cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
