# UMSL Explore Engineering Day — Registration App

A simple Flask app with SQLite to collect registrations for the event.

## Setup

```bash
cd umsl-explore-engineering-registration
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app.py init-db
flask --app app.py run
# Visit http://127.0.0.1:5000
```

## Environment

- SECRET_KEY (optional): set to a strong value for production.

## Notes

- Admin list is available at `/admin`.
- Database file: `registrations.db` in project root.
