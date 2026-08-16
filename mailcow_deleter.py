import requests
import imaplib
import urllib3
from tabulate import tabulate

MAILCOW_HOST = "Mail Server URL here"
API_KEY = "Mail Server API Key here"
DOMAIN = "Your domain here"  

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

RED = "\033[91m"
BLUE = "\033[94m"
GREEN = "\033[92m"
DIM = "\033[90m"
RESET = "\033[0m"

def log(level, msg):
    from datetime import datetime
    ts = datetime.now().strftime("%H:%M:%S")
    colors = {"INF": BLUE, "DBG": RED, "COP": GREEN}
    c = colors.get(level, DIM)
    # Level padded to 3 chars for alignment
    lvl = level.ljust(3)
    print(f"{DIM}{ts}{RESET}  {c}{lvl}{RESET}  {msg}")


def print_summary(results):
    """Print a final summary table of mailbox deletion results."""
    rows = []
    for r in results:
        user = r.get('username')
        ok = r.get('ok')
        info = r.get('info', '')
        status = f"{GREEN}SUCCESS{RESET}" if ok else f"{RED}FAILED{RESET}"
        rows.append([user, status, info])
    print()
    print(f"{BLUE}Summary:{RESET}")
    print(tabulate(rows, headers=["Mailbox", "Result", "Info"]))

def get_mailboxes():
    url = f"{MAILCOW_HOST}/api/v1/get/mailbox/all/{DOMAIN}"
    r = requests.get(url, headers=HEADERS, verify=False)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict):
        log("DBG", f"No mailboxes or error: {data}")
        return []
    return [mb["username"] for mb in data]

def delete_mailbox(username):
    url = f"{MAILCOW_HOST}/api/v1/delete/mailbox"
    try:
        r = requests.post(url, headers=HEADERS, json=[username], verify=False, timeout=15)
        result = r.json()
        if isinstance(result, list) and result[0].get("type") == "success":
            log("COP", f"Deleted | {username}")
            return True, result
        else:
            log("DBG", f"Failed  | {username} | {result}")
            return False, result
    except Exception as e:
        log("DBG", f"Error   | {username} | {e}")
        return False, str(e)

if __name__ == "__main__":
    urllib3.disable_warnings()

    log("INF", f"Fetching mailboxes for {DOMAIN}")
    mailboxes = get_mailboxes()
    log("INF", f"Threads: {len(mailboxes)}")

    count = input(f"\n  How many mailboxes to delete? (max {len(mailboxes)}): ").strip()
    try:
        count = int(count)
        count = min(count, len(mailboxes))
    except ValueError:
        log("DBG", "Invalid number. Exiting.")
        exit(1)


    targets = mailboxes[:count]
    log("INF", f"Starting deletion of {count} mailboxes...")
    print()

    results = []
    for i, mb in enumerate(targets, 1):
        log("INF", f"Checking | {mb} [{i}/{count}]")
        ok, info = delete_mailbox(mb)
        results.append({"username": mb, "ok": ok, "info": info})

    print_summary(results)
    log("COP", f"Done | {count} mailboxes processed. Domain untouched.")