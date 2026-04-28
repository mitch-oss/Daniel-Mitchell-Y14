# Fixit Physio

A clinic management system built in Python for a physiotherapy practice. Final A2 Computer Science coursework project (WJEC, Unit 5).

## What it does

Replaces a paper-based clinic workflow with a desktop application that handles:

- Secure staff login with role-based access (Receptionist, Physiotherapist, Admin)
- Patient records (add, edit, delete, search)
- Appointment scheduling with double-booking prevention
- Invoice generation and tracking, linked to appointments
- Staff management (Admin only)
- Input validation across every form using regular expressions
- A custom calendar widget for date entry

## Tech stack

- **Language:** Python 3.14
- **GUI:** Tkinter (standard library)
- **Database:** SQLite via `sqlite3` (standard library)
- **Password security:** SHA-256 hashing via `hashlib` (standard library)
- **Validation:** `re` module for regex pattern matching

No external packages required. Everything runs off the standard library.

## How to run

1. Make sure Python 3.14 is installed
2. Open the project folder in VS Code (or any IDE)
3. Run `main.py` from the terminal:

```bash
python main.py
```

That boots the system and brings up the login screen.

## Default login

The seeded database has the following accounts. The shared company key for all logins is `12345`.

| Staff ID | Password   | Role          |
| -------- | ---------- | ------------- |
| 10001    | password1  | Receptionist  |
| 10002    | password2  | Physiotherapist |
| 10003    | password3  | Admin         |

## Project structure

```
fixit_physio/
├── main.py                  # Entry point
├── database.py              # All SQL and DB connection logic
├── login.py                 # Login screen
├── main_menu.py             # Dashboard with role-based dispatch
├── view_patients.py         # Patient records screen
├── view_appointments.py     # Appointments screen
├── add_appointment.py       # Booking form with conflict check
├── edit_appointment.py      # Edit booking form
├── billing.py               # Invoice screen
├── staff_management.py      # Admin-only staff screen
├── date_picker.py           # Reusable calendar widget
└── fixit_physio.db          # SQLite database file
```

## Key design decisions

- **Object-oriented** — every screen is its own class
- **Centralised database access** — all SQL lives in `database.py`
- **Foreign key enforcement** — `PRAGMA foreign_keys = ON` is set on every connection
- **Three-factor login** — Staff ID, password and company key
- **Pre-insert conflict checks** — appointments are validated against existing bookings before insertion to prevent double-booking

## Author

Daniel Mitchell — St Killian's College
