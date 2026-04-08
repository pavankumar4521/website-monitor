import requests
import time
from datetime import datetime
from pathlib import Path
import argparse
import os

# ---------------- CLI ----------------
parser = argparse.ArgumentParser(description="Website Monitor")

parser.add_argument("--interval", type=int, default=5, help="Time between checks")
parser.add_argument("--timeout", type=int, default=3, help="Request timeout")
parser.add_argument("--threshold", type=int, default=1, help="Slow response threshold")

args = parser.parse_args()

interval = args.interval
timeout = args.timeout
threshold = args.threshold

# ---------------- CONFIG ----------------
urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/invalid",
    "https://invalidurl",
    "http://localhost:5000"
]

recovery_map = {
#    "https://jsonplaceholder.typicode.com/posts/1" : "website1",
#    "https://jsonplaceholder.typicode.com/posts/2" : "website2",
#    "https://jsonplaceholder.typicode.com/invalid" : "website3",
#    "https://invalidurl" : "website4",
    "http://localhost:5000": "mywebsite"
}

log_path = Path(__file__).parent / "monitor_logs.txt"

# ---------------- FUNCTIONS ----------------
def recover(url, log_file):
    msg = f"⚙️ Attempting recovery for: {url}"
    print(msg)
    log_file.write(msg + "\n")

    container = recovery_map.get(url)

    if container:
        os.system(f"docker start {container}")
        msg2 = f"🔁 Recovery executed: docker start {container}"
    else:
        msg2 = f"❌ No recovery defined for: {url}"

    print(msg2)
    log_file.write(msg2 + "\n")


def check_url(url):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        start = time.time()
        response = requests.get(url, timeout=timeout)
        response_time = time.time() - start

        if response.status_code == 200:
            icon, status = "✅", "OK"
        else:
            icon, status = "🚨", "DOWN"

        if response_time > threshold:
            icon, status = "⚠️", "SLOW"

        alert = f"{icon} [{status}] | {current_time} | {url} | {response.status_code} | {round(response_time,2)}s"

    except requests.exceptions.RequestException:
        status = "UNREACHABLE"
        alert = f"🚨 [{status}] | {current_time} | {url}"

    return status, alert


# ---------------- MAIN ----------------
def main():
    recovery_triggered = {url: False for url in urls}

    with open(log_path, "a", encoding="utf-8", buffering=1) as log_file:

        while True:
            try:
                print("\n==============================")
                print("Checking at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                print("==============================")

                log_file.write("\n" + "="*60 + "\n")
                log_file.write(f"Check at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Interval: {interval} | Timeout: {timeout}\n")
                log_file.write("="*60 + "\n")

                for url in urls:
                    status, alert = check_url(url)

                    print(alert)
                    log_file.write(alert + "\n")

                    if status in ["DOWN", "SLOW", "UNREACHABLE"] and not recovery_triggered[url]:
                        recover(url, log_file)
                        recovery_triggered[url] = True

                    if status == "OK":
                        recovery_triggered[url] = False

                time.sleep(interval)

            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped by user.")
                break


if __name__ == "__main__":
    main()
