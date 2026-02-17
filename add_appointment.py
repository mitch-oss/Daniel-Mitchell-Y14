"""
Add Appointment Module
Handles the interface for creating new appointments
"""

import tkinter as tk
from tkinter import messagebox
import database


class AddAppointment:
    """
    Creates and manages the add appointment window.
    """
    
    def __init__(self, window, user_id):
        """
        Initialize the add appointment window.
        
        Parameters:
            window: The tkinter window
            user_id: The staff ID of the person creating the appointment
        """
        self.window = window
        self.window.title("Add New Appointment")
        self.window.geometry("400x300")
        
        self.user_id = user_id
        
        # Create the interface
        self.create_widgets()
    
    def create_widgets(self):
        """
        Creates all the widgets for the add appointment form.
        """
        # Title
        title_label = tk.Label(
            self.window,
            text="Add New Appointment",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=20)
        
        # Patient Name field
        tk.Label(self.window, text="Patient Name:").pack(pady=5)
        self.patient_name_entry = tk.Entry(self.window, width=30)
        self.patient_name_entry.pack(pady=5)
        
        # Date field
        tk.Label(self.window, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.date_entry = tk.Entry(self.window, width=30)
        self.date_entry.pack(pady=5)
        
        # Time field
        tk.Label(self.window, text="Time (HH:MM):").pack(pady=5)
        self.time_entry = tk.Entry(self.window, width=30)
        self.time_entry.pack(pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=20)
        
        # Confirm button
        confirm_btn = tk.Button(
            buttons_frame,
            text="Confirm Booking",
            command=self.confirm_booking,
            width=15,
            bg="lightblue"
        )
        confirm_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancel",
            command=self.window.destroy,
            width=15
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def confirm_booking(self):
        """
        Called when user clicks Confirm Booking button.
        Validates input and saves to database.
        """
        # Get values from entry boxes
        patient_name = self.patient_name_entry.get()
        appt_date = self.date_entry.get()
        appt_time = self.time_entry.get()
        
        # Check if any fields are empty
        if not patient_name or not appt_date or not appt_time:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Basic validation for date format
        if len(appt_date) != 10 or appt_date[4] != "-" or appt_date[7] != "-":
            messagebox.showerror(
                "Invalid Date",
                "Please use format YYYY-MM-DD (e.g. 2024-03-20)"
            )
            return
        
        # Basic validation for time format
        if len(appt_time) != 5 or appt_time[2] != ":":
            messagebox.showerror(
                "Invalid Time",
                "Please use format HH:MM (e.g. 14:30)"
            )
            return
        
        # Try to save to database
        success = database.add_appointment(
            patient_name,
            appt_date,
            appt_time,
            self.user_id
        )
        
        if success:
            messagebox.showinfo(
                "Success",
                "Appointment created successfully"
            )
            # Clear the form
            self.patient_name_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            
            # Close the window
            self.window.destroy()
        else:
            messagebox.showerror(
                "Error",
                "Failed to create appointment"
            )
