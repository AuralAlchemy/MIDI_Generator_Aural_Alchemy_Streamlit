import subprocess
import time
import webbrowser
import socket
import sys


def wait_for_server(port=8501, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except:
            time.sleep(0.5)
    return False


def main():
    print("Starting AuralAlchemy MIDI Generator...")

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py",
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]

    process = subprocess.Popen(cmd)

    if wait_for_server():
        print("Opening browser...")
        webbrowser.open("http://127.0.0.1:8501")
        process.wait()
    else:
        print("ERROR: Streamlit did not start.")
        process.terminate()


if __name__ == "__main__":
    main()
