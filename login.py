"""
Login Screen Module
Handles user authentication and displays the login interface
"""

import tkinter as tk
from tkinter import messagebox
import database


class LoginScreen:
    """
    Creates and manages the login screen window.
    """
    
    def __init__(self, root):
        """
        Initialize the login screen.
        
        Parameters:
            root: The main tkinter window
        """
        self.root = root
        self.root.title("Fixit Physio - Login")
        self.root.geometry("400x300")
        
        # Store the logged-in user's information
        self.current_user = None
        self.current_role = None
        
        # Create the login interface
        self.create_widgets()
    
    def create_widgets(self):
        """
        Creates all the widgets (labels, entry boxes, buttons) for the login screen.
        """
        # Title label
        title_label = tk.Label(
            self.root,
            text="Fixit Physio",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=20)
        
        # Staff ID entry
        tk.Label(self.root, text="Enter 5-Digit Staff ID:").pack(pady=5)
        self.staff_id_entry = tk.Entry(self.root, width=30)
        self.staff_id_entry.pack(pady=5)
        
        # Password entry (masked with asterisks)
        tk.Label(self.root, text="Enter Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        # Company code entry
        tk.Label(self.root, text="Enter 5-Digit Company Key:").pack(pady=5)
        self.company_code_entry = tk.Entry(self.root, width=30)
        self.company_code_entry.pack(pady=5)
        
        # Login button
        login_button = tk.Button(
            self.root,
            text="Enter System",
            command=self.attempt_login,
            width=20,
            bg="lightblue"
        )
        login_button.pack(pady=20)
    
    def attempt_login(self):
        """
        Called when the user clicks the login button.
        Validates credentials and opens main menu if successful.
        """
        # Get values from entry boxes
        staff_id = self.staff_id_entry.get()
        password = self.password_entry.get()
        company_code = self.company_code_entry.get()
        
        # Check if any fields are empty
        if not staff_id or not password or not company_code:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Authenticate using database
        role = database.authenticate_user(staff_id, password, company_code)
        
        if role:
            # Login successful
            self.current_user = staff_id
            self.current_role = role
            
            # Close login window and open main menu
            self.root.destroy()
            self.open_main_menu()
        else:
            # Login failed
            messagebox.showerror("Login Failed", "Invalid credentials")
            # Clear password field
            self.password_entry.delete(0, tk.END)
    
    def open_main_menu(self):
        """
        Opens the main menu window after successful login.
        """
        # Import here to avoid circular imports
        import main_menu
        
        # Create new window for main menu
        menu_root = tk.Tk()
        main_menu.MainMenu(menu_root, self.current_user, self.current_role)
        menu_root.mainloop()
