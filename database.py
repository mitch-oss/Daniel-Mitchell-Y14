"""
database.py - Fixit Physio Enhanced System
Handles all database operations for the full system.
Tables: users, patients, appointments, invoices
"""

import sqlite3
import hashlib
import os

DB_NAME = "fixit_physio.db"


# ─────────────────────────────────────────────────────────
# UTILITY
# ─────────────────────────────────────────────────────────

def hash_password(password):
    """
    Converts plain text password to a SHA256 hash.
    Never stores plain text passwords.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def get_connection():
    """
    Returns a database connection with foreign keys enabled.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ─────────────────────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────────────────────

def initialize_database():
    """
    Creates all tables if they don't already exist.
    Called once on startup.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT CHECK(role IN ("Receptionist","Physiotherapist","Admin")) NOT NULL,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Patients table (new - normalized)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                date_of_birth TEXT,
                notes TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Appointments table (uses patient_id instead of patient_name)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                appointment_type TEXT DEFAULT "General",
                status TEXT DEFAULT "Scheduled",
                notes TEXT,
                created_by TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                FOREIGN KEY (created_by) REFERENCES users(staff_id) ON DELETE SET NULL
            )
        ''')

        # Invoices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                appointment_id INTEGER,
                amount REAL NOT NULL,
                description TEXT,
                status TEXT DEFAULT "Unpaid",
                created_by TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL
            )
        ''')

        conn.commit()
        conn.close()
        print("Database initialized.")

    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")


def add_sample_data():
    """
    Adds sample users, patients, appointments, and invoices.
    Only runs if tables are empty.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Sample users
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            users = [
                ("10001", hash_password("password1"), "Receptionist"),
                ("10002", hash_password("password2"), "Physiotherapist"),
                ("10003", hash_password("password3"), "Admin"),
            ]
            cursor.executemany(
                "INSERT INTO users (staff_id, password_hash, role) VALUES (?,?,?)", users
            )

        # Sample patients
        cursor.execute("SELECT COUNT(*) FROM patients")
        if cursor.fetchone()[0] == 0:
            patients = [
                ("Sarah Johnson",  "07700 900123", "sarah.j@email.com",  "1990-05-14", "Knee rehab"),
                ("Michael Chen",   "07700 900456", "m.chen@email.com",   "1985-08-22", "Lower back pain"),
                ("Emma Williams",  "07700 900789", "e.williams@email.com","1978-03-01", "Shoulder injury"),
                ("James O'Neill",  "07700 900321", "j.oneill@email.com", "2000-11-17", "Sports injury"),
                ("Patricia Martinez","07700 900654","p.martinez@email.com","1965-07-30","Post-op recovery"),
            ]
            cursor.executemany(
                "INSERT INTO patients (name, phone, email, date_of_birth, notes) VALUES (?,?,?,?,?)",
                patients
            )

        # Sample appointments
        cursor.execute("SELECT COUNT(*) FROM appointments")
        if cursor.fetchone()[0] == 0:
            appointments = [
                (1, "2026-02-18", "09:00", "Assessment",  "Scheduled", "", "10001"),
                (2, "2026-02-18", "10:30", "Treatment",   "Scheduled", "", "10001"),
                (3, "2026-02-19", "14:00", "Follow-up",   "Scheduled", "", "10002"),
                (4, "2026-02-20", "09:30", "Assessment",  "Scheduled", "", "10001"),
                (5, "2026-02-20", "11:00", "Treatment",   "Scheduled", "", "10002"),
            ]
            cursor.executemany(
                '''INSERT INTO appointments
                   (patient_id, appointment_date, appointment_time,
                    appointment_type, status, notes, created_by)
                   VALUES (?,?,?,?,?,?,?)''',
                appointments
            )

        # Sample invoices
        cursor.execute("SELECT COUNT(*) FROM invoices")
        if cursor.fetchone()[0] == 0:
            invoices = [
                (1, 1, 45.00, "Initial Assessment", "Paid",   "10001"),
                (2, 2, 60.00, "Treatment Session",  "Unpaid", "10001"),
                (3, 3, 60.00, "Follow-up Session",  "Unpaid", "10002"),
            ]
            cursor.executemany(
                '''INSERT INTO invoices
                   (patient_id, appointment_id, amount, description, status, created_by)
                   VALUES (?,?,?,?,?,?)''',
                invoices
            )

        conn.commit()
        conn.close()
        print("Sample data added.")

    except sqlite3.Error as e:
        print(f"Sample data error: {e}")


# ─────────────────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────────────────

def authenticate_user(staff_id, password, company_code):
    """
    Three-factor login check.
    Returns role string if successful, None if failed.
    """
    if company_code != "12345":
        return None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash, role FROM users WHERE staff_id = ?",
            (staff_id,)
        )
        result = cursor.fetchone()
        conn.close()

        if not result:
            return None

        stored_hash, role = result
        if stored_hash == hash_password(password):
            return role
        return None

    except sqlite3.Error as e:
        print(f"Auth error: {e}")
        return None


def get_all_users():
    """Returns list of all staff users."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, staff_id, role, created_date FROM users ORDER BY role, staff_id")
        users = cursor.fetchall()
        conn.close()
        return users
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")
        return []


def add_user(staff_id, password, role):
    """
    Creates a new staff user.
    Returns True if successful, False if staff_id already exists.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (staff_id, password_hash, role) VALUES (?,?,?)",
            (staff_id, hash_password(password), role)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as e:
        print(f"Add user error: {e}")
        return False


def delete_user(staff_id):
    """Deletes a user by staff_id."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE staff_id = ?", (staff_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Delete user error: {e}")
        return False


def change_password(staff_id, new_password):
    """Updates a user's password."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE staff_id = ?",
            (hash_password(new_password), staff_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Change password error: {e}")
        return False


# ─────────────────────────────────────────────────────────
# PATIENTS
# ─────────────────────────────────────────────────────────

def add_patient(name, phone, email, dob, notes):
    """
    Adds a new patient record.
    Returns new patient_id or None on failure.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO patients (name, phone, email, date_of_birth, notes)
               VALUES (?,?,?,?,?)''',
            (name, phone, email, dob, notes)
        )
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return patient_id
    except sqlite3.Error as e:
        print(f"Add patient error: {e}")
        return None


def get_all_patients():
    """
    Returns all patients ordered alphabetically.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT patient_id, name, phone, email, date_of_birth FROM patients ORDER BY name"
        )
        patients = cursor.fetchall()
        conn.close()
        return patients
    except sqlite3.Error as e:
        print(f"Fetch patients error: {e}")
        return []


def get_patient_by_id(patient_id):
    """Returns full details for a single patient."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
        patient = cursor.fetchone()
        conn.close()
        return patient
    except sqlite3.Error as e:
        print(f"Get patient error: {e}")
        return None


def update_patient(patient_id, name, phone, email, dob, notes):
    """Updates an existing patient's details."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE patients SET name=?, phone=?, email=?, date_of_birth=?, notes=?
               WHERE patient_id=?''',
            (name, phone, email, dob, notes, patient_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Update patient error: {e}")
        return False


def delete_patient(patient_id):
    """
    Deletes a patient and all their linked appointments (CASCADE).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Delete patient error: {e}")
        return False


def search_patients(search_term):
    """Returns patients whose name matches the search term."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT patient_id, name, phone, email FROM patients WHERE name LIKE ? ORDER BY name",
            (f"%{search_term}%",)
        )
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Search patients error: {e}")
        return []


# ─────────────────────────────────────────────────────────
# APPOINTMENTS
# ─────────────────────────────────────────────────────────

def add_appointment(patient_id, appt_date, appt_time, appt_type, notes, created_by):
    """
    Creates a new appointment linked to a patient.
    Returns True if successful.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO appointments
               (patient_id, appointment_date, appointment_time, appointment_type, notes, created_by)
               VALUES (?,?,?,?,?,?)''',
            (patient_id, appt_date, appt_time, appt_type, notes, created_by)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Add appointment error: {e}")
        return False


def get_all_appointments(search_term="", date_filter=""):
    """
    Returns all appointments joined with patient names.
    Supports optional search by patient name and date filter.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = '''
            SELECT a.appointment_id, p.name, a.appointment_date,
                   a.appointment_time, a.appointment_type, a.status, a.notes
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            WHERE p.name LIKE ?
        '''
        params = [f"%{search_term}%"]

        if date_filter:
            query += " AND a.appointment_date = ?"
            params.append(date_filter)

        query += " ORDER BY a.appointment_date, a.appointment_time"

        cursor.execute(query, params)
        appointments = cursor.fetchall()
        conn.close()
        return appointments

    except sqlite3.Error as e:
        print(f"Fetch appointments error: {e}")
        return []


def get_appointment_by_id(appointment_id):
    """Returns full details for a single appointment."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT a.*, p.name FROM appointments a
               JOIN patients p ON a.patient_id = p.patient_id
               WHERE a.appointment_id = ?''',
            (appointment_id,)
        )
        appt = cursor.fetchone()
        conn.close()
        return appt
    except sqlite3.Error as e:
        print(f"Get appointment error: {e}")
        return None


def update_appointment(appointment_id, patient_id, appt_date, appt_time, appt_type, status, notes):
    """Updates an existing appointment."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE appointments
               SET patient_id=?, appointment_date=?, appointment_time=?,
                   appointment_type=?, status=?, notes=?
               WHERE appointment_id=?''',
            (patient_id, appt_date, appt_time, appt_type, status, notes, appointment_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Update appointment error: {e}")
        return False


def delete_appointment(appointment_id):
    """Deletes an appointment by ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE appointment_id = ?", (appointment_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Delete appointment error: {e}")
        return False


def get_appointments_by_patient(patient_id):
    """Returns all appointments for a specific patient."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT appointment_id, appointment_date, appointment_time,
                      appointment_type, status
               FROM appointments WHERE patient_id = ?
               ORDER BY appointment_date, appointment_time''',
            (patient_id,)
        )
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Get appointments by patient error: {e}")
        return []


# ─────────────────────────────────────────────────────────
# BILLING / INVOICES
# ─────────────────────────────────────────────────────────

def create_invoice(patient_id, appointment_id, amount, description, created_by):
    """
    Creates a new invoice for a patient.
    Returns new invoice_id or None on failure.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO invoices
               (patient_id, appointment_id, amount, description, created_by)
               VALUES (?,?,?,?,?)''',
            (patient_id, appointment_id, amount, description, created_by)
        )
        invoice_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return invoice_id
    except sqlite3.Error as e:
        print(f"Create invoice error: {e}")
        return None


def get_all_invoices(status_filter=""):
    """
    Returns all invoices joined with patient names.
    Optional filter by status (Paid/Unpaid).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = '''
            SELECT i.invoice_id, p.name, i.amount, i.description,
                   i.status, i.created_at
            FROM invoices i
            JOIN patients p ON i.patient_id = p.patient_id
        '''
        params = []
        if status_filter:
            query += " WHERE i.status = ?"
            params.append(status_filter)

        query += " ORDER BY i.created_at DESC"
        cursor.execute(query, params)
        invoices = cursor.fetchall()
        conn.close()
        return invoices

    except sqlite3.Error as e:
        print(f"Fetch invoices error: {e}")
        return []


def get_invoices_by_patient(patient_id):
    """Returns all invoices for a specific patient."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT invoice_id, amount, description, status, created_at
               FROM invoices WHERE patient_id = ?
               ORDER BY created_at DESC''',
            (patient_id,)
        )
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Get patient invoices error: {e}")
        return []


def update_invoice_status(invoice_id, new_status):
    """Marks an invoice as Paid or Unpaid."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE invoices SET status = ? WHERE invoice_id = ?",
            (new_status, invoice_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Update invoice error: {e}")
        return False


def delete_invoice(invoice_id):
    """Deletes an invoice."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM invoices WHERE invoice_id = ?", (invoice_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Delete invoice error: {e}")
        return False


def get_total_outstanding():
    """Returns total amount of all unpaid invoices."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM invoices WHERE status = 'Unpaid'")
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0.0
    except sqlite3.Error as e:
        print(f"Get outstanding error: {e}")
        return 0.0
