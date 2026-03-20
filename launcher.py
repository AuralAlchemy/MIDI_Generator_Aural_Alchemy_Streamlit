import os
import sys
import time
import socket
import threading
import webbrowser
from pathlib import Path


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
    else:
        print("ERROR: Streamlit server did not start in time.")


def main():
    os.environ["BROWSER"] = "none"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    app_path = base_dir / "app.py"

    if not app_path.exists():
        print(f"ERROR: app.py not found at {app_path}")
        sys.exit(1)

    threading.Thread(target=open_browser_when_ready, daemon=True).start()

    from streamlit.web import cli as stcli

    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--server.address=127.0.0.1",
        "--server.port=8501",
    ]

    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
