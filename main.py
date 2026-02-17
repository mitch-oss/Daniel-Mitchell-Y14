"""
Fixit Physio Booking System - Main Program
This is the main entry point for the application.
Run this file to start the program.
"""

import tkinter as tk
import database
import login


def main():
    """
    Main function that starts the application.
    """
    # Initialize the database (create tables if they don't exist)
    database.initialize_database()
    
    # Add sample data for testing
    database.add_sample_users()
    database.add_sample_appointments()
    
    print("\n" + "="*50)
    print("FIXIT PHYSIO BOOKING SYSTEM")
    print("="*50)
    print("\nSample Login Credentials:")
    print("-" * 50)
    print("Receptionist:")
    print("  Staff ID: 10001")
    print("  Password: password1")
    print("\nPhysiotherapist:")
    print("  Staff ID: 10002")
    print("  Password: password2")
    print("\nAdmin:")
    print("  Staff ID: 10003")
    print("  Password: password3")
    print("\nCompany Code: 12345")
    print("="*50 + "\n")
    
    # Create the main window
    root = tk.Tk()
    
    # Create and display the login screen
    login.LoginScreen(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
