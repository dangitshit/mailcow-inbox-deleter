# MAIL-DELETER

A CLI tool to bulk-delete Mailcow mailboxes from a domain via the Mailcow REST API — without touching the domain itself.

---

## Requirements

- Python 3.10+
- `requests` library

```bash
python -m pip install -r requirements.txt
```

---

## Configuration

Update `mailcow_deleter.py` or use `config.yml` to set credentials. Example env or top-of-file values:

```python
MAILCOW_HOST = "https://mail.yourdomain.com"
API_KEY      = "YOUR-MAILCOW-API-KEY"
DOMAIN       = "yourdomain.com"
```

Your API key can be found in your Mailcow admin panel under **Configuration → Access → API**.

---

## Usage

```bash
python mailcow_deleter.py
```

The tool will:

1. Fetch all mailboxes under the configured domain
2. Ask how many mailboxes you want to delete
3. Ask for confirmation before doing anything (unless `--confirm` is used)
4. Delete mailbox accounts via the Mailcow admin API endpoint (configurable)

---

## Console UI and Example Output

The script prints aligned, timestamped logs and a final tabular summary (using `tabulate`). Example:

```
12:01:10  INF  Fetching mailboxes for example.com
12:01:12  INF  Threads: 1283

  How many mailboxes to delete? (max 1283): 10

12:01:13  INF  Checking | user1@example.com [1/10]
12:01:13  COP  Deleted | user1@example.com
12:01:14  INF  Checking | user2@example.com [2/10]
12:01:14  DBG  Failed  | user2@example.com | {"type":"error","msg":"not found"}
...

Summary:
Mailbox               Result     Info
--------------------  ---------  ----------------------------------
user1@example.com     SUCCESS    [...]
user2@example.com     FAILED     {"type":"error","msg":"not found"}

12:01:20  COP  Done | 10 mailboxes processed. Domain untouched.
```

- `INF` — informational messages
- `COP` — successful operations (green)
- `DBG` — failures/errors (red)

Use `--dry-run` first to preview actions; the summary will show matched vs deleted counts.

---

## Notes

- Only mailbox accounts are deleted — aliases, domains, and settings are left completely intact
- Deletion is irreversible — all emails in deleted mailboxes are permanently gone
-- SSL verification is disabled by default for self-signed certificates

---

## License

MIT