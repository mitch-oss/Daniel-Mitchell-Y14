"""
Database Configuration for Fixit Physio System
This file sets up all necessary database tables and initial data
"""

import sqlite3
import hashlib

def hash_password(password):
    """
    Hash passwords using SHA-256 for security
    Takes plain text password and returns hashed version
    """
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    """
    Creates all necessary database tables if they don't exist
    Also populates initial user accounts and company access key
    """
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect('fixit_physio.db')
    cursor = conn.cursor()
    
    # Create users table for login system with different roles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            is_active INTEGER DEFAULT 1,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create customers/patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT NOT NULL,
            address TEXT,
            date_of_birth TEXT,
            medical_notes TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create appointments table with all necessary fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            physio_id INTEGER,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            service_type TEXT NOT NULL,
            duration INTEGER DEFAULT 30,
            price REAL NOT NULL,
            status TEXT DEFAULT 'scheduled',
            notes TEXT,
            created_by INTEGER,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (physio_id) REFERENCES users(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # Create services table for different treatment types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            description TEXT,
            duration INTEGER NOT NULL,
            price REAL NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # Create company access table for security
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_access (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            access_key TEXT UNIQUE NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # Check if users table is empty and add default users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Add default users with different roles
        default_users = [
            ('admin', hash_password('admin123'), 'System Administrator', 'admin', 'admin@fixitphysio.com', '01234567890'),
            ('staff01', hash_password('staff123'), 'Sarah Johnson', 'staff', 'sarah@fixitphysio.com', '01234567891'),
            ('physio01', hash_password('physio123'), 'Dr. Michael Chen', 'physio', 'michael@fixitphysio.com', '01234567892'),
            ('physio02', hash_password('physio123'), 'Dr. Emma Wilson', 'physio', 'emma@fixitphysio.com', '01234567893'),
        ]
        
        cursor.executemany('''
            INSERT INTO users (username, password_hash, full_name, role, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', default_users)
        print("✓ Default users created successfully")
    
    # Check if services table is empty and add default services
    cursor.execute("SELECT COUNT(*) FROM services")
    if cursor.fetchone()[0] == 0:
        default_services = [
            ('Initial Consultation', 'First-time patient assessment and treatment plan', 60, 75.00),
            ('Standard Physiotherapy', 'Regular treatment session', 45, 55.00),
            ('Sports Massage', 'Deep tissue massage for athletes', 60, 65.00),
            ('Back Pain Treatment', 'Specialized back pain therapy', 45, 60.00),
            ('Post-Surgery Rehabilitation', 'Recovery therapy after surgery', 60, 70.00),
            ('Acupuncture', 'Traditional acupuncture treatment', 30, 45.00),
        ]
        
        cursor.executemany('''
            INSERT INTO services (service_name, description, duration, price)
            VALUES (?, ?, ?, ?)
        ''', default_services)
        print("✓ Default services created successfully")
    
    # Check if company access key exists
    cursor.execute("SELECT COUNT(*) FROM company_access")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO company_access (access_key) VALUES (?)", ('FIXIT2024',))
        print("✓ Company access key set: FIXIT2024")
    
    # Commit all changes and close connection
    conn.commit()
    conn.close()
    print("✓ Database setup completed successfully!")

if __name__ == "__main__":
    setup_database()
    print("\n=== Database initialized ===")
    print("Login credentials:")
    print("Admin    - Username: admin    | Password: admin123")
    print("Staff    - Username: staff01  | Password: staff123")
    print("Physio   - Username: physio01 | Password: physio123")
    print("Physio   - Username: physio02 | Password: physio123")
