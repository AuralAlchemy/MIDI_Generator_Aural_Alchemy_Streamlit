import atexit
import os
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

process = None


def is_port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def wait_for_server(host: str, port: int, timeout: int = 45) -> bool:
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


def main() -> None:
    global process
    atexit.register(cleanup)

    host = "127.0.0.1"
    port = 8501
    url = f"http://{host}:{port}"

    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    app_path = base_dir / "app.py"
    streamlit_config_dir = base_dir / ".streamlit"

    env = os.environ.copy()
    env["BROWSER"] = "none"
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

    if streamlit_config_dir.exists():
        env["STREAMLIT_CONFIG_DIR"] = str(streamlit_config_dir)

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
        creationflags = 0
        process = subprocess.Popen(cmd, env=env, creationflags=creationflags)
    else:
        process = subprocess.Popen(cmd, env=env, preexec_fn=os.setsid)

    if wait_for_server(host, port, timeout=45):
        webbrowser.open(url)
        process.wait()
    else:
        print("ERROR: Streamlit server did not start in time.")
        cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
