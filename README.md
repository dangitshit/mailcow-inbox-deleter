# MAIL-DELETER

A fast CLI tool to bulk-delete Mailcow mailboxes from a specific domain via the Mailcow REST API — without touching the domain itself.

---

## Requirements

- Python 3.10+
- `requests` library

```bash
pip install requests
```

---

## Configuration

Open `main.py` and set your values at the top:

```python
MAILCOW_HOST = "https://mail.yourdomain.com"
API_KEY      = "YOUR-MAILCOW-API-KEY"
DOMAIN       = "yourdomain.com"
```

Your API key can be found in your Mailcow admin panel under **Configuration → Access → API**.

---

## Usage

```bash
python main.py
```

The tool will:

1. Fetch all mailboxes under the configured domain
2. Ask how many mailboxes you want to delete
3. Ask for confirmation before doing anything
4. Delete only the mailbox accounts — the domain is never modified

---

## Example Output

```
06:37:44  INF  Fetching mailboxes for yourdomain.com
06:37:51  INF  Threads: 1283

  How many mailboxes to delete? (max 1283): 500

  Delete 500 mailboxes from yourdomain.com? (yes/no): yes

06:37:52  INF  Checking | user1@yourdomain.com [1/500]
06:37:52  COK  Deleted  | user1@yourdomain.com
06:37:53  INF  Checking | user2@yourdomain.com [2/500]
06:37:53  COK  Deleted  | user2@yourdomain.com
...
06:42:10  COK  Done | 500 mailboxes deleted. Domain untouched.
```

---

## Notes

- Only mailbox accounts are deleted — aliases, domains, and settings are left completely intact
- Deletion is irreversible — all emails in deleted mailboxes are permanently gone
- SSL verification is disabled by default for self-signed certificates

---

## License

MIT