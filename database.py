"""
Database Module for Fixit Physio Booking System
Handles all database operations including table creation and CRUD functions
"""

import sqlite3
from datetime import datetime

# Database filename
DB_NAME = "fixit_physio.db"


def initialize_database():
    """
    Creates the database tables if they don't exist.
    Called when the program starts.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create users table for login authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create appointments table for storing bookings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            created_by TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")


def add_sample_users():
    """
    Adds sample users to the database for testing.
    Only adds if users table is empty.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if users already exist
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Add sample staff members
        sample_users = [
            ("10001", "password1", "Receptionist"),
            ("10002", "password2", "Physiotherapist"),
            ("10003", "password3", "Admin")
        ]
        
        cursor.executemany(
            "INSERT INTO users (staff_id, password, role) VALUES (?, ?, ?)",
            sample_users
        )
        
        conn.commit()
        print("Sample users added successfully")
    
    conn.close()


def authenticate_user(staff_id, password, company_code):
    """
    Checks if user credentials are correct.
    
    Parameters:
        staff_id: The staff member's ID
        password: The staff member's password
        company_code: The company security code (should be "12345")
    
    Returns:
        User role (Receptionist/Physiotherapist/Admin) if successful
        None if authentication fails
    """
    # Check company code first
    if company_code != "12345":
        return None
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Query database for matching credentials
    cursor.execute(
        "SELECT role FROM users WHERE staff_id = ? AND password = ?",
        (staff_id, password)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]  # Return the role
    else:
        return None


def add_appointment(patient_name, appt_date, appt_time, created_by):
    """
    Adds a new appointment to the database.
    
    Parameters:
        patient_name: Name of the patient
        appt_date: Date in YYYY-MM-DD format
        appt_time: Time in HH:MM format
        created_by: Staff ID of person creating the appointment
    
    Returns:
        True if successful, False if error occurs
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT INTO appointments 
               (patient_name, appointment_date, appointment_time, created_by)
               VALUES (?, ?, ?, ?)''',
            (patient_name, appt_date, appt_time, created_by)
        )
        
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def get_all_appointments():
    """
    Retrieves all appointments from the database.
    
    Returns:
        List of tuples containing (id, patient_name, date, time)
        Sorted by date and time
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        '''SELECT id, patient_name, appointment_date, appointment_time
           FROM appointments
           ORDER BY appointment_date, appointment_time'''
    )
    
    appointments = cursor.fetchall()
    conn.close()
    
    return appointments


def delete_appointment(appointment_id):
    """
    Deletes an appointment from the database.
    
    Parameters:
        appointment_id: The ID of the appointment to delete
    
    Returns:
        True if successful, False if error occurs
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM appointments WHERE id = ?",
            (appointment_id,)
        )
        
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def add_sample_appointments():
    """
    Adds sample appointment data for testing.
    Only adds if appointments table is empty.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if appointments already exist
    cursor.execute("SELECT COUNT(*) FROM appointments")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Add sample appointments
        sample_appointments = [
            ("Sarah Johnson", "2024-03-20", "09:00", "10001"),
            ("Michael Chen", "2024-03-20", "10:30", "10001"),
            ("Emma Williams", "2024-03-21", "14:00", "10002"),
            ("James O'Neill", "2024-03-22", "09:30", "10001"),
            ("Patricia Martinez", "2024-03-22", "11:00", "10002")
        ]
        
        cursor.executemany(
            '''INSERT INTO appointments 
               (patient_name, appointment_date, appointment_time, created_by)
               VALUES (?, ?, ?, ?)''',
            sample_appointments
        )
        
        conn.commit()
        print("Sample appointments added successfully")
    
    conn.close()
