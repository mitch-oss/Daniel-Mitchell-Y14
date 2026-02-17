"""
Main Menu Module
Displays the main dashboard with navigation options
"""

import tkinter as tk
from tkinter import messagebox


class MainMenu:
    """
    Creates and manages the main menu/dashboard window.
    """
    
    def __init__(self, root, user_id, user_role):
        """
        Initialize the main menu.
        
        Parameters:
            root: The main tkinter window
            user_id: The logged-in user's staff ID
            user_role: The user's role (Receptionist/Physiotherapist/Admin)
        """
        self.root = root
        self.root.title("Fixit Physio - Main Menu")
        self.root.geometry("600x400")
        
        self.user_id = user_id
        self.user_role = user_role
        
        # Create the menu interface
        self.create_widgets()
    
    def create_widgets(self):
        """
        Creates all the widgets for the main menu screen.
        """
        # Header frame
        header_frame = tk.Frame(self.root, bg="lightgray", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Welcome message
        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome back, Staff User",
            font=("Arial", 16, "bold"),
            bg="lightgray"
        )
        welcome_label.pack(pady=10)
        
        # Role display
        role_label = tk.Label(
            header_frame,
            text=f"System Status: Online | Role: {self.user_role}",
            bg="lightgray"
        )
        role_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Sidebar frame
        sidebar_frame = tk.Frame(content_frame, width=150, bg="lightgray")
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_frame.pack_propagate(False)
        
        # Sidebar title
        tk.Label(
            sidebar_frame,
            text="FIXIT\nPHYSIO",
            font=("Arial", 12, "bold"),
            bg="lightgray"
        ).pack(pady=20)
        
        # Sidebar buttons
        sidebar_buttons = [
            "Dashboard",
            "View Schedule",
            "New Booking",
            "Patients",
            "Billing"
        ]
        
        for button_text in sidebar_buttons:
            btn = tk.Button(
                sidebar_frame,
                text=button_text,
                width=15,
                bg="lightgray",
                relief=tk.FLAT
            )
            btn.pack(pady=5, padx=10)
        
        # Logout button at bottom of sidebar
        logout_btn = tk.Button(
            sidebar_frame,
            text="Logout",
            command=self.logout,
            width=15,
            bg="gray"
        )
        logout_btn.pack(side=tk.BOTTOM, pady=20, padx=10)
        
        # Main action area
        action_frame = tk.Frame(content_frame)
        action_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        # Section title
        tk.Label(
            action_frame,
            text="Clinic Management Actions",
            font=("Arial", 14, "bold")
        ).pack(pady=20)
        
        # Action buttons frame
        buttons_frame = tk.Frame(action_frame)
        buttons_frame.pack(pady=20)
        
        # New Appointment button
        new_appt_btn = tk.Button(
            buttons_frame,
            text="+ New Appointment",
            command=self.open_new_appointment,
            width=20,
            height=2,
            bg="lightblue",
            font=("Arial", 11)
        )
        new_appt_btn.pack(side=tk.LEFT, padx=10)
        
        # View Bookings button
        view_bookings_btn = tk.Button(
            buttons_frame,
            text="📅 View All Bookings",
            command=self.open_view_appointments,
            width=20,
            height=2,
            bg="lightgreen",
            font=("Arial", 11)
        )
        view_bookings_btn.pack(side=tk.LEFT, padx=10)
    
    def open_new_appointment(self):
        """
        Opens the add appointment window.
        """
        import add_appointment
        
        # Create new window
        appt_window = tk.Toplevel(self.root)
        add_appointment.AddAppointment(appt_window, self.user_id)
    
    def open_view_appointments(self):
        """
        Opens the view appointments window.
        """
        import view_appointments
        
        # Create new window
        view_window = tk.Toplevel(self.root)
        view_appointments.ViewAppointments(view_window)
    
    def logout(self):
        """
        Logs out the user and returns to login screen.
        """
        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )
        
        if result:
            self.root.destroy()
            
            # Return to login screen
            import login
            login_root = tk.Tk()
            login.LoginScreen(login_root)
            login_root.mainloop()
