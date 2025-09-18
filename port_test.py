import socket
import time
import os
from dotenv import load_dotenv

load_dotenv()
TARGET_IP = os.getenv("SV_TARGET_IP")
TARGET_PORT = os.getenv("SV_TARGET_PORT")

def check_port(host, port, timeout=2.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

if __name__ == "__main__":
    host = TARGET_IP
    port = TARGET_PORT
    interval = 5

    print(f"Monitoring {host}:{port} every {interval}s.")
    try:
        while True:
            ok = check_port(host, port, timeout=2.0)
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            if ok:
                print(f"[{ts}] {host}:{port} => OPEN")
            else:
                print(f"[{ts}] {host}:{port} => CLOSED / NO RESPONSE")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user")