"""
Booking Interface for Fixit Physio
Handles creating new appointments with full patient and service selection
"""

import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

class BookingInterface:
    def __init__(self, parent, created_by_user_id):
        """
        Initialize booking window
        Parent: main window to attach to
        created_by_user_id: ID of user creating the appointment
        """
        self.created_by = created_by_user_id
        
        # Create booking window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("New Appointment Booking")
        self.window.geometry("700x800")
        self.window.attributes('-topmost', True)
        
        # Colors
        self.primary_color = "#0066CC"
        self.success_color = "#00B894"
        self.danger_color = "#E17055"
        
        # Store customer and service data
        self.customers = []
        self.services = []
        self.physiotherapists = []
        
        # Setup UI
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Create all UI elements for the booking form"""
        
        # Header
        header = ctk.CTkFrame(self.window, fg_color=self.primary_color, corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="📅 New Appointment Booking",
            font=("Arial", 24, "bold"),
            text_color="white"
        ).pack(pady=20)
        
        # Main form container
        form_container = ctk.CTkScrollableFrame(self.window, fg_color="transparent")
        form_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Patient Selection Section
        self.create_section_header(form_container, "👤 Patient Information")
        
        patient_frame = ctk.CTkFrame(form_container, fg_color="#2D2D44", corner_radius=10)
        patient_frame.pack(fill="x", pady=(0, 20))
        
        # Patient dropdown
        ctk.CTkLabel(
            patient_frame,
            text="Select Patient:",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.patient_combo = ctk.CTkComboBox(
            patient_frame,
            width=400,
            height=35,
            font=("Arial", 12),
            values=["Loading patients..."]
        )
        self.patient_combo.pack(padx=20, pady=(0, 10))
        
        # Add new patient button
        ctk.CTkButton(
            patient_frame,
            text="➕ Add New Patient",
            font=("Arial", 12),
            fg_color=self.success_color,
            hover_color="#00956F",
            width=200,
            height=32,
            command=self.add_new_patient
        ).pack(padx=20, pady=(0, 15))
        
        # Service Selection Section
        self.create_section_header(form_container, "⚕️ Service Details")
        
        service_frame = ctk.CTkFrame(form_container, fg_color="#2D2D44", corner_radius=10)
        service_frame.pack(fill="x", pady=(0, 20))
        
        # Service dropdown
        ctk.CTkLabel(
            service_frame,
            text="Select Service:",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.service_combo = ctk.CTkComboBox(
            service_frame,
            width=400,
            height=35,
            font=("Arial", 12),
            values=["Loading services..."],
            command=self.on_service_selected
        )
        self.service_combo.pack(padx=20, pady=(0, 15))
        
        # Service details display
        self.service_details_label = ctk.CTkLabel(
            service_frame,
            text="",
            font=("Arial", 11),
            text_color="lightgray"
        )
        self.service_details_label.pack(padx=20, pady=(0, 15))
        
        # Physiotherapist Selection
        self.create_section_header(form_container, "👨‍⚕️ Assign Physiotherapist")
        
        physio_frame = ctk.CTkFrame(form_container, fg_color="#2D2D44", corner_radius=10)
        physio_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            physio_frame,
            text="Select Physiotherapist:",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.physio_combo = ctk.CTkComboBox(
            physio_frame,
            width=400,
            height=35,
            font=("Arial", 12),
            values=["Loading physiotherapists..."]
        )
        self.physio_combo.pack(padx=20, pady=(0, 15))
        
        # Date and Time Section
        self.create_section_header(form_container, "📅 Date & Time")
        
        datetime_frame = ctk.CTkFrame(form_container, fg_color="#2D2D44", corner_radius=10)
        datetime_frame.pack(fill="x", pady=(0, 20))
        
        # Date selection
        ctk.CTkLabel(
            datetime_frame,
            text="Appointment Date:",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.date_entry = ctk.CTkEntry(
            datetime_frame,
            width=400,
            height=35,
            placeholder_text="YYYY-MM-DD (e.g., 2024-12-25)",
            font=("Arial", 12)
        )
        self.date_entry.pack(padx=20, pady=(0, 5))
        
        # Quick date buttons
        quick_dates = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        quick_dates.pack(padx=20, pady=(5, 10))
        
        ctk.CTkButton(
            quick_dates,
            text="Today",
            width=90,
            height=28,
            fg_color="#636E72",
            font=("Arial", 11),
            command=lambda: self.set_quick_date(0)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            quick_dates,
            text="Tomorrow",
            width=90,
            height=28,
            fg_color="#636E72",
            font=("Arial", 11),
            command=lambda: self.set_quick_date(1)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            quick_dates,
            text="Next Week",
            width=90,
            height=28,
            fg_color="#636E72",
            font=("Arial", 11),
            command=lambda: self.set_quick_date(7)
        ).pack(side="left", padx=2)
        
        # Time selection
        ctk.CTkLabel(
            datetime_frame,
            text="Appointment Time:",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.time_entry = ctk.CTkEntry(
            datetime_frame,
            width=400,
            height=35,
            placeholder_text="HH:MM (e.g., 14:30)",
            font=("Arial", 12)
        )
        self.time_entry.pack(padx=20, pady=(0, 15))
        
        # Additional Notes Section
        self.create_section_header(form_container, "📝 Additional Notes")
        
        notes_frame = ctk.CTkFrame(form_container, fg_color="#2D2D44", corner_radius=10)
        notes_frame.pack(fill="x", pady=(0, 20))
        
        self.notes_text = ctk.CTkTextbox(
            notes_frame,
            width=400,
            height=100,
            font=("Arial", 12)
        )
        self.notes_text.pack(padx=20, pady=15)
        
        # Action Buttons
        button_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        ctk.CTkButton(
            button_frame,
            text="✓ Confirm Booking",
            font=("Arial", 15, "bold"),
            height=50,
            fg_color=self.success_color,
            hover_color="#00956F",
            command=self.save_appointment
        ).pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        ctk.CTkButton(
            button_frame,
            text="✗ Cancel",
            font=("Arial", 15, "bold"),
            height=50,
            fg_color=self.danger_color,
            hover_color="#C94531",
            command=self.window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(10, 0))
    
    def create_section_header(self, parent, text):
        """Create a section header label"""
        ctk.CTkLabel(
            parent,
            text=text,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(10, 10))
    
    def load_data(self):
        """Load patients, services, and physiotherapists from database"""
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            # Load customers
            cursor.execute("SELECT id, first_name, last_name, phone FROM customers ORDER BY last_name")
            self.customers = cursor.fetchall()
            
            customer_names = [f"{c[1]} {c[2]} - {c[3]}" for c in self.customers]
            if customer_names:
                self.patient_combo.configure(values=customer_names)
                self.patient_combo.set(customer_names[0])
            else:
                self.patient_combo.configure(values=["No patients found"])
            
            # Load services
            cursor.execute("SELECT id, service_name, duration, price, description FROM services WHERE is_active = 1")
            self.services = cursor.fetchall()
            
            service_names = [f"{s[1]} - £{s[3]:.2f} ({s[2]} min)" for s in self.services]
            if service_names:
                self.service_combo.configure(values=service_names)
                self.service_combo.set(service_names[0])
                self.on_service_selected(service_names[0])
            else:
                self.service_combo.configure(values=["No services found"])
            
            # Load physiotherapists
            cursor.execute("SELECT id, full_name FROM users WHERE role = 'physio' AND is_active = 1")
            self.physiotherapists = cursor.fetchall()
            
            physio_names = [p[1] for p in self.physiotherapists]
            if physio_names:
                self.physio_combo.configure(values=physio_names)
                self.physio_combo.set(physio_names[0])
            else:
                self.physio_combo.configure(values=["No physiotherapists available"])
            
            conn.close()
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data: {str(e)}")
    
    def on_service_selected(self, choice):
        """Display service details when selected"""
        try:
            # Find selected service
            for service in self.services:
                service_display = f"{service[1]} - £{service[3]:.2f} ({service[2]} min)"
                if service_display == choice:
                    description = service[4] if service[4] else "No description available"
                    self.service_details_label.configure(
                        text=f"ℹ️ {description}\nDuration: {service[2]} minutes | Price: £{service[3]:.2f}"
                    )
                    break
        except:
            pass
    
    def set_quick_date(self, days_offset):
        """Set date using quick buttons"""
        target_date = datetime.now() + timedelta(days=days_offset)
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, target_date.strftime("%Y-%m-%d"))
    
    def add_new_patient(self):
        """Open patient registration dialog"""
        import patient_manager
        patient_manager.PatientManager(self.window, quick_add=True, callback=self.load_data)
    
    def save_appointment(self):
        """Validate and save the appointment to database"""
        
        # Get selected values
        patient_selection = self.patient_combo.get()
        service_selection = self.service_combo.get()
        physio_selection = self.physio_combo.get()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        notes = self.notes_text.get("1.0", "end-1c").strip()
        
        # Validate inputs
        if "No patients" in patient_selection or "Loading" in patient_selection:
            messagebox.showerror("Error", "Please select a valid patient")
            return
        
        if "No services" in service_selection or "Loading" in service_selection:
            messagebox.showerror("Error", "Please select a valid service")
            return
        
        if not date or not time:
            messagebox.showerror("Error", "Please enter both date and time")
            return
        
        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
        
        # Validate time format
        try:
            datetime.strptime(time, "%H:%M")
        except:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM (24-hour)")
            return
        
        # Extract IDs
        try:
            # Get customer ID
            customer_id = self.customers[self.patient_combo.current()][0]
            
            # Get service details
            service_data = self.services[self.service_combo.current()]
            service_name = service_data[1]
            duration = service_data[2]
            price = service_data[3]
            
            # Get physio ID
            physio_id = self.physiotherapists[self.physio_combo.current()][0]
            
            # Save to database
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO appointments 
                (customer_id, physio_id, appointment_date, appointment_time, 
                 service_type, duration, price, status, notes, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'scheduled', ?, ?)
            """, (customer_id, physio_id, date, time, service_name, duration, price, notes, self.created_by))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Appointment booked successfully!\n\nDate: {date}\nTime: {time}")
            self.window.destroy()
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not save appointment: {str(e)}")
    
    def run(self):
        """Keep window open"""
        self.window.wait_window()
