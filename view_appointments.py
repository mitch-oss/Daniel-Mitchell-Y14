"""
View Appointments Module
Displays all scheduled appointments in a table format
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database


class ViewAppointments:
    """
    Creates and manages the view appointments window.
    """
    
    def __init__(self, window):
        """
        Initialize the view appointments window.
        
        Parameters:
            window: The tkinter window
        """
        self.window = window
        self.window.title("View Schedule")
        self.window.geometry("700x400")
        
        # Create the interface
        self.create_widgets()
        
        # Load appointments from database
        self.refresh_appointments()
    
    def create_widgets(self):
        """
        Creates all the widgets for the appointments view.
        """
        # Title
        title_label = tk.Label(
            self.window,
            text="Current Appointments",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)
        
        # Create frame for the table
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview (table) widget
        self.appointments_tree = ttk.Treeview(
            table_frame,
            columns=("Patient Name", "Date", "Time"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configure scrollbar
        scrollbar.config(command=self.appointments_tree.yview)
        
        # Define column headings
        self.appointments_tree.heading("Patient Name", text="Patient Name")
        self.appointments_tree.heading("Date", text="Date")
        self.appointments_tree.heading("Time", text="Time")
        
        # Define column widths
        self.appointments_tree.column("Patient Name", width=250)
        self.appointments_tree.column("Date", width=150)
        self.appointments_tree.column("Time", width=150)
        
        self.appointments_tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            buttons_frame,
            text="Refresh",
            command=self.refresh_appointments,
            width=15,
            bg="lightblue"
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Delete button
        delete_btn = tk.Button(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_appointment,
            width=15,
            bg="lightcoral"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = tk.Button(
            buttons_frame,
            text="Close",
            command=self.window.destroy,
            width=15
        )
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def refresh_appointments(self):
        """
        Loads appointments from database and displays them in the table.
        """
        # Clear existing items in the table
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        # Get appointments from database
        appointments = database.get_all_appointments()
        
        # Add each appointment to the table
        for appt in appointments:
            # appt structure: (id, patient_name, date, time)
            self.appointments_tree.insert(
                "",
                tk.END,
                values=(appt[1], appt[2], appt[3]),
                tags=(appt[0],)  # Store ID in tags for deletion
            )
    
    def delete_appointment(self):
        """
        Deletes the selected appointment from the database.
        """
        # Get selected item
        selection = self.appointments_tree.selection()
        
        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select an appointment to delete"
            )
            return
        
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this appointment?"
        )
        
        if result:
            # Get the appointment ID from tags
            item = selection[0]
            tags = self.appointments_tree.item(item, "tags")
            appointment_id = tags[0]
            
            # Delete from database
            success = database.delete_appointment(appointment_id)
            
            if success:
                messagebox.showinfo("Success", "Appointment deleted")
                # Refresh the display
                self.refresh_appointments()
            else:
                messagebox.showerror("Error", "Failed to delete appointment")
