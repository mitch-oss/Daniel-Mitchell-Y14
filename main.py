"""
main.py - Fixit Physio Enhanced System
Entry point. Initializes database and opens login screen.
"""

import tkinter as tk
import database
import login


def main():
    # Set up database and sample data
    database.initialize_database()
    database.add_sample_data()

    print("\n" + "=" * 50)
    print("  FIXIT PHYSIO - ENHANCED SYSTEM")
    print("=" * 50)
    print("\n  LOGIN CREDENTIALS (for testing)\n")
    print("  Company Key : 12345")
    print("  ─────────────────────────────")
    print("  Receptionist  10001 / password1")
    print("  Physio        10002 / password2")
    print("  Admin         10003 / password3")
    print("\n  (Passwords are hashed with SHA256)")
    print("=" * 50 + "\n")

    root = tk.Tk()
    login.LoginScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
