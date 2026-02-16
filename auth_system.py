"""
Login System for Fixit Physio
Handles user authentication and role-based access control
"""

import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import hashlib

class LoginWindow:
    def __init__(self):
        """
        Initialize the login window
        Sets up the main application window and UI elements
        """
        # Create main window
        self.app = ctk.CTk()
        self.app.title("Fixit Physio - Login")
        self.app.geometry("500x600")
        
        # Brand colors
        self.primary_color = "#0066CC"
        self.secondary_color = "#00B894"
        self.danger_color = "#E17055"
        
        # Setup the user interface
        self.setup_ui()
    
    def setup_ui(self):
        """
        Creates all UI elements for the login screen
        Includes logo, input fields, and buttons
        """
        # Main container frame
        main_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo and title section
        logo_frame = ctk.CTkFrame(main_frame, fg_color=self.primary_color, corner_radius=15)
        logo_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            logo_frame,
            text="⚕️ FIXIT PHYSIO",
            font=("Arial", 32, "bold"),
            text_color="white"
        ).pack(pady=20)
        
        ctk.CTkLabel(
            logo_frame,
            text="Professional Physiotherapy Management System",
            font=("Arial", 12),
            text_color="white"
        ).pack(pady=(0, 20))
        
        # Login form section
        form_frame = ctk.CTkFrame(main_frame, fg_color="#2D2D44", corner_radius=15)
        form_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(
            form_frame,
            text="Sign In to Your Account",
            font=("Arial", 20, "bold")
        ).pack(pady=(30, 20))
        
        # Username input field
        ctk.CTkLabel(
            form_frame,
            text="Username",
            font=("Arial", 13)
        ).pack(pady=(10, 5), anchor="w", padx=50)
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=40,
            placeholder_text="Enter your username",
            font=("Arial", 13)
        )
        self.username_entry.pack(pady=(0, 15), padx=50)
        
        # Password input field
        ctk.CTkLabel(
            form_frame,
            text="Password",
            font=("Arial", 13)
        ).pack(pady=(10, 5), anchor="w", padx=50)
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=40,
            placeholder_text="Enter your password",
            show="●",  # Hide password characters
            font=("Arial", 13)
        )
        self.password_entry.pack(pady=(0, 25), padx=50)
        
        # Login button
        self.login_button = ctk.CTkButton(
            form_frame,
            text="🔐 Login",
            width=300,
            height=45,
            font=("Arial", 15, "bold"),
            fg_color=self.primary_color,
            hover_color="#0052A3",
            command=self.authenticate_user
        )
        self.login_button.pack(pady=10)
        
        # Help text
        ctk.CTkLabel(
            form_frame,
            text="Contact IT support if you've forgotten your password",
            font=("Arial", 10),
            text_color="gray"
        ).pack(pady=(20, 10))
        
        # Company access key section
        ctk.CTkLabel(
            form_frame,
            text="─── First Time Setup ───",
            font=("Arial", 11),
            text_color="gray"
        ).pack(pady=(20, 10))
        
        ctk.CTkButton(
            form_frame,
            text="🔑 Enter Company Access Key",
            width=250,
            height=35,
            font=("Arial", 12),
            fg_color=self.secondary_color,
            hover_color="#00956F",
            command=self.show_access_key_dialog
        ).pack(pady=(5, 30))
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.authenticate_user())
    
    def hash_password(self, password):
        """
        Hash password using SHA-256
        Takes plain text password and returns hashed version
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self):
        """
        Verify user credentials against database
        If valid, open appropriate dashboard based on role
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validate input fields
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Hash the entered password
        password_hash = self.hash_password(password)
        
        try:
            # Connect to database
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            # Query user credentials
            cursor.execute("""
                SELECT id, username, full_name, role, is_active 
                FROM users 
                WHERE username = ? AND password_hash = ?
            """, (username, password_hash))
            
            user = cursor.fetchone()
            conn.close()
            
            # Check if user exists and is active
            if user:
                user_id, username, full_name, role, is_active = user
                
                if is_active == 0:
                    messagebox.showerror("Access Denied", "Your account has been deactivated.\nPlease contact administration.")
                    return
                
                # Successful login
                messagebox.showinfo("Success", f"Welcome, {full_name}!")
                self.app.destroy()
                
                # Open appropriate dashboard based on role
                self.open_dashboard(user_id, username, full_name, role)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
                self.password_entry.delete(0, 'end')
        
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
    
    def show_access_key_dialog(self):
        """
        Display dialog for entering company access key
        Used for first-time setup verification
        """
        # Create dialog window
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Company Access Key")
        dialog.geometry("400x250")
        dialog.attributes('-topmost', True)
        
        ctk.CTkLabel(
            dialog,
            text="🔑 Enter Company Access Key",
            font=("Arial", 18, "bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            dialog,
            text="This key is required for initial system setup",
            font=("Arial", 11),
            text_color="gray"
        ).pack(pady=5)
        
        # Access key input
        key_entry = ctk.CTkEntry(
            dialog,
            width=250,
            height=40,
            placeholder_text="Enter access key",
            font=("Arial", 13)
        )
        key_entry.pack(pady=20)
        
        def verify_key():
            """Verify the entered access key against database"""
            entered_key = key_entry.get().strip()
            
            if not entered_key:
                messagebox.showerror("Error", "Please enter an access key")
                return
            
            try:
                conn = sqlite3.connect('fixit_physio.db')
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM company_access WHERE access_key = ? AND is_active = 1",
                    (entered_key,)
                )
                
                if cursor.fetchone():
                    conn.close()
                    messagebox.showinfo("Valid Key", "Access key verified!\n\nDefault Login:\nUsername: admin\nPassword: admin123")
                    dialog.destroy()
                else:
                    conn.close()
                    messagebox.showerror("Invalid Key", "The access key you entered is incorrect")
            
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {str(e)}")
        
        # Verify button
        ctk.CTkButton(
            dialog,
            text="Verify Key",
            width=200,
            height=40,
            font=("Arial", 13, "bold"),
            fg_color=self.secondary_color,
            command=verify_key
        ).pack(pady=10)
        
        key_entry.bind('<Return>', lambda e: verify_key())
    
    def open_dashboard(self, user_id, username, full_name, role):
        """
        Open the appropriate dashboard based on user role
        Different roles see different interfaces
        """
        if role == 'admin':
            import admin_dashboard
            admin_dashboard.AdminDashboard(user_id, username, full_name).run()
        elif role == 'staff':
            import staff_dashboard
            staff_dashboard.StaffDashboard(user_id, username, full_name).run()
        elif role == 'physio':
            import physio_dashboard
            physio_dashboard.PhysioDashboard(user_id, username, full_name).run()
    
    def run(self):
        """Start the application main loop"""
        self.app.mainloop()

# Run the application
if __name__ == "__main__":
    from db_config import setup_database
    
    # Ensure database is set up
    setup_database()
    
    # Start login window
    LoginWindow().run()
