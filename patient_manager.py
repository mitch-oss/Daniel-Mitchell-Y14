"""
Patient Management System for Fixit Physio
Handles patient registration, editing, and viewing
"""

import customtkinter as ctk
from tkinter import messagebox
import sqlite3

class PatientManager:
    def __init__(self, parent, quick_add=False, search_mode=False, callback=None):
        """
        Initialize patient manager
        parent: main window
        quick_add: if True, show only add patient form
        search_mode: if True, show search interface
        callback: function to call after adding patient
        """
        self.callback = callback
        self.quick_add = quick_add
        self.search_mode = search_mode
        
        # Create window
        self.window = ctk.CTkToplevel(parent)
        
        if quick_add:
            self.window.title("Add New Patient")
            self.window.geometry("600x700")
        elif search_mode:
            self.window.title("Search Patients")
            self.window.geometry("900x600")
        else:
            self.window.title("Patient Management")
            self.window.geometry("1100x700")
        
        self.window.attributes('-topmost', True)
        
        # Colors
        self.primary_color = "#0066CC"
        self.success_color = "#00B894"
        self.danger_color = "#E17055"
        
        # Setup UI based on mode
        if quick_add:
            self.setup_add_form()
        elif search_mode:
            self.setup_search_interface()
        else:
            self.setup_full_interface()
    
    def setup_full_interface(self):
        """Setup full patient management interface"""
        
        # Header
        header = ctk.CTkFrame(self.window, fg_color=self.primary_color, corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="👥 Patient Management",
            font=("Arial", 24, "bold"),
            text_color="white"
        ).pack(pady=20)
        
        # Search and add section
        controls = ctk.CTkFrame(self.window, fg_color="#2D2D44", corner_radius=10)
        controls.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            controls,
            text="Search Patient:",
            font=("Arial", 13)
        ).pack(side="left", padx=(15, 10), pady=10)
        
        self.search_entry = ctk.CTkEntry(
            controls,
            placeholder_text="Enter name or phone number...",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            controls,
            text="🔍 Search",
            fg_color=self.primary_color,
            width=100,
            height=35,
            command=self.search_patients
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            controls,
            text="➕ Add New Patient",
            fg_color=self.success_color,
            hover_color="#00956F",
            width=150,
            height=35,
            command=self.show_add_form
        ).pack(side="right", padx=15, pady=10)
        
        # Patient list
        self.scroll_frame = ctk.CTkScrollableFrame(self.window, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Load all patients
        self.load_patients()
        
        # Close button
        ctk.CTkButton(
            self.window,
            text="✗ Close",
            fg_color=self.danger_color,
            hover_color="#C94531",
            width=120,
            height=40,
            command=self.window.destroy
        ).pack(pady=(0, 20))
    
    def setup_add_form(self):
        """Setup quick add patient form"""
        
        # Header
        header = ctk.CTkFrame(self.window, fg_color=self.primary_color, corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="➕ Add New Patient",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=20)
        
        # Form container
        form_frame = ctk.CTkScrollableFrame(self.window, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Create form fields
        self.create_patient_form(form_frame)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        ctk.CTkButton(
            button_frame,
            text="✓ Save Patient",
            font=("Arial", 14, "bold"),
            height=45,
            fg_color=self.success_color,
            hover_color="#00956F",
            command=self.save_patient
        ).pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        ctk.CTkButton(
            button_frame,
            text="✗ Cancel",
            font=("Arial", 14, "bold"),
            height=45,
            fg_color=self.danger_color,
            hover_color="#C94531",
            command=self.window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(10, 0))
    
    def setup_search_interface(self):
        """Setup search-focused interface"""
        
        # Header
        header = ctk.CTkFrame(self.window, fg_color=self.primary_color, corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="🔍 Search Patients",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=20)
        
        # Search bar
        search_frame = ctk.CTkFrame(self.window, fg_color="#2D2D44")
        search_frame.pack(fill="x", padx=20, pady=15)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Enter patient name or phone number...",
            width=400,
            height=40,
            font=("Arial", 13)
        )
        self.search_entry.pack(side="left", padx=15, pady=15)
        
        ctk.CTkButton(
            search_frame,
            text="🔍 Search",
            fg_color=self.primary_color,
            width=120,
            height=40,
            command=self.search_patients
        ).pack(side="left", padx=5)
        
        # Results area
        self.scroll_frame = ctk.CTkScrollableFrame(self.window, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        ctk.CTkLabel(
            self.scroll_frame,
            text="Enter a search term above to find patients",
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=50)
    
    def create_patient_form(self, parent):
        """Create patient registration form fields"""
        
        # Personal Information Section
        ctk.CTkLabel(
            parent,
            text="Personal Information",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(10, 15))
        
        info_frame = ctk.CTkFrame(parent, fg_color="#2D2D44", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        # First Name
        ctk.CTkLabel(info_frame, text="First Name *", font=("Arial", 13)).pack(anchor="w", padx=20, pady=(15, 5))
        self.first_name_entry = ctk.CTkEntry(info_frame, width=400, height=35, font=("Arial", 12))
        self.first_name_entry.pack(padx=20, pady=(0, 10))
        
        # Last Name
        ctk.CTkLabel(info_frame, text="Last Name *", font=("Arial", 13)).pack(anchor="w", padx=20, pady=(5, 5))
        self.last_name_entry = ctk.CTkEntry(info_frame, width=400, height=35, font=("Arial", 12))
        self.last_name_entry.pack(padx=20, pady=(0, 10))
        
        # Date of Birth
        ctk.CTkLabel(info_frame, text="Date of Birth (YYYY-MM-DD)", font=("Arial", 13)).pack(anchor="w", padx=20, pady=(5, 5))
        self.dob_entry = ctk.CTkEntry(info_frame, width=400, height=35, placeholder_text="e.g., 1990-05-15", font=("Arial", 12))
        self.dob_entry.pack(padx=20, pady=(0, 15))
        
        # Contact Information Section
        ctk.CTkLabel(
            parent,
            text="Contact Information",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(10, 15))
        
        contact_frame = ctk.CTkFrame(parent, fg_color="#2D2D44", corner_radius=10)
        contact_frame.pack(fill="x", pady=(0, 20))
        
        # Phone
        ctk.CTkLabel(contact_frame, text="Phone Number *", font=("Arial", 13)).pack(anchor="w", padx=20, pady=(15, 5))
        self.phone_entry = ctk.CTkEntry(contact_frame, width=400, height=35, font=("Arial", 12))
        self.phone_entry.pack(padx=20, pady=(0, 10))
        
        # Email
        ctk.CTkLabel(contact_frame, text="Email Address", font=("Arial", 13)).pack(anchor="w", padx=20, pady=(5, 5))
        self.email_entry = ctk.CTkEntry(contact_frame, width=400, height=35, placeholder_text="optional", font=("Arial", 12))
        self.email_entry.pack(padx=20, pady=(0, 10))
        
        # Address
        ctk.CTkLabel(contact_frame, text="Address", font=("Arial", 13)).pack(anchor="w", padx=20, pady=(5, 5))
        self.address_entry = ctk.CTkTextbox(contact_frame, width=400, height=80, font=("Arial", 12))
        self.address_entry.pack(padx=20, pady=(0, 15))
        
        # Medical Information Section
        ctk.CTkLabel(
            parent,
            text="Medical Notes",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(10, 15))
        
        medical_frame = ctk.CTkFrame(parent, fg_color="#2D2D44", corner_radius=10)
        medical_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            medical_frame,
            text="Any relevant medical history, conditions, or allergies:",
            font=("Arial", 12),
            text_color="lightgray"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.medical_notes = ctk.CTkTextbox(medical_frame, width=400, height=100, font=("Arial", 12))
        self.medical_notes.pack(padx=20, pady=(0, 15))
    
    def save_patient(self):
        """Save new patient to database"""
        
        # Get values
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get("1.0", "end-1c").strip()
        medical = self.medical_notes.get("1.0", "end-1c").strip()
        
        # Validate required fields
        if not first_name or not last_name or not phone:
            messagebox.showerror("Error", "Please fill in all required fields:\n- First Name\n- Last Name\n- Phone Number")
            return
        
        # Validate phone number (basic)
        if len(phone) < 10:
            messagebox.showerror("Error", "Please enter a valid phone number")
            return
        
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO customers (first_name, last_name, email, phone, address, date_of_birth, medical_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, email or None, phone, address or None, dob or None, medical or None))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Patient {first_name} {last_name} has been registered successfully!")
            
            # Call callback if provided
            if self.callback:
                self.callback()
            
            self.window.destroy()
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not save patient: {str(e)}")
    
    def load_patients(self, search_term=None):
        """Load and display patients"""
        
        # Clear existing content
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            if search_term:
                cursor.execute("""
                    SELECT id, first_name, last_name, phone, email, date_of_birth
                    FROM customers
                    WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ?
                    ORDER BY last_name, first_name
                """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            else:
                cursor.execute("""
                    SELECT id, first_name, last_name, phone, email, date_of_birth
                    FROM customers
                    ORDER BY last_name, first_name
                """)
            
            patients = cursor.fetchall()
            conn.close()
            
            if not patients:
                ctk.CTkLabel(
                    self.scroll_frame,
                    text="No patients found" if search_term else "No patients registered yet",
                    font=("Arial", 16),
                    text_color="gray"
                ).pack(pady=50)
                return
            
            # Header
            header_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#1a1a2e", corner_radius=10)
            header_frame.pack(fill="x", pady=(0, 10))
            
            headers = [("Name", 200), ("Phone", 150), ("Email", 200), ("DOB", 120), ("Actions", 150)]
            
            for i, (header, width) in enumerate(headers):
                ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=("Arial", 13, "bold"),
                    width=width
                ).grid(row=0, column=i, padx=10, pady=12, sticky="w")
            
            # Display patients
            for idx, patient in enumerate(patients):
                patient_id, first, last, phone, email, dob = patient
                
                row_frame = ctk.CTkFrame(
                    self.scroll_frame,
                    fg_color="#2D2D44" if idx % 2 == 0 else "#3A3A5C",
                    corner_radius=8
                )
                row_frame.pack(fill="x", pady=3)
                
                # Name
                ctk.CTkLabel(
                    row_frame,
                    text=f"{first} {last}",
                    font=("Arial", 12, "bold"),
                    width=200
                ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
                
                # Phone
                ctk.CTkLabel(
                    row_frame,
                    text=phone,
                    font=("Arial", 12),
                    width=150
                ).grid(row=0, column=1, padx=10, pady=10, sticky="w")
                
                # Email
                ctk.CTkLabel(
                    row_frame,
                    text=email or "N/A",
                    font=("Arial", 12),
                    width=200
                ).grid(row=0, column=2, padx=10, pady=10, sticky="w")
                
                # DOB
                ctk.CTkLabel(
                    row_frame,
                    text=dob or "N/A",
                    font=("Arial", 12),
                    width=120
                ).grid(row=0, column=3, padx=10, pady=10, sticky="w")
                
                # Actions
                action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                action_frame.grid(row=0, column=4, padx=10, pady=10)
                
                ctk.CTkButton(
                    action_frame,
                    text="👁️ View",
                    width=65,
                    height=28,
                    fg_color=self.primary_color,
                    command=lambda p=patient_id: self.view_patient_details(p)
                ).pack(side="left", padx=2)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load patients: {str(e)}")
    
    def search_patients(self):
        """Search for patients"""
        search_term = self.search_entry.get().strip()
        if search_term:
            self.load_patients(search_term)
        else:
            self.load_patients()
    
    def show_add_form(self):
        """Open add patient window"""
        PatientManager(self.window, quick_add=True, callback=lambda: self.load_patients())
    
    def view_patient_details(self, patient_id):
        """View detailed patient information"""
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT first_name, last_name, email, phone, address, date_of_birth, medical_notes, created_date
                FROM customers WHERE id = ?
            """, (patient_id,))
            
            patient = cursor.fetchone()
            
            if not patient:
                conn.close()
                messagebox.showerror("Error", "Patient not found")
                return
            
            first, last, email, phone, address, dob, medical, created = patient
            
            # Count appointments
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE customer_id = ?", (patient_id,))
            total_appts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE customer_id = ? AND status = 'completed'", (patient_id,))
            completed_appts = cursor.fetchone()[0]
            
            conn.close()
            
            # Create details window
            details_window = ctk.CTkToplevel(self.window)
            details_window.title(f"Patient Details - {first} {last}")
            details_window.geometry("600x600")
            details_window.attributes('-topmost', True)
            
            # Header
            header = ctk.CTkFrame(details_window, fg_color=self.primary_color)
            header.pack(fill="x")
            
            ctk.CTkLabel(
                header,
                text=f"👤 {first} {last}",
                font=("Arial", 24, "bold"),
                text_color="white"
            ).pack(pady=20)
            
            # Content
            content = ctk.CTkScrollableFrame(details_window, fg_color="transparent")
            content.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Info sections
            info = [
                ("📧 Email", email or "Not provided"),
                ("📞 Phone", phone),
                ("📍 Address", address or "Not provided"),
                ("🎂 Date of Birth", dob or "Not provided"),
                ("📅 Patient Since", created[:10] if created else "Unknown"),
                ("📊 Total Appointments", str(total_appts)),
                ("✅ Completed Visits", str(completed_appts)),
            ]
            
            for label, value in info:
                info_frame = ctk.CTkFrame(content, fg_color="#2D2D44", corner_radius=10)
                info_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(
                    info_frame,
                    text=label,
                    font=("Arial", 12, "bold")
                ).pack(anchor="w", padx=15, pady=(10, 2))
                
                ctk.CTkLabel(
                    info_frame,
                    text=value,
                    font=("Arial", 12),
                    text_color="lightgray"
                ).pack(anchor="w", padx=15, pady=(0, 10))
            
            # Medical notes
            if medical:
                ctk.CTkLabel(
                    content,
                    text="📋 Medical Notes",
                    font=("Arial", 14, "bold")
                ).pack(anchor="w", pady=(15, 5))
                
                notes_frame = ctk.CTkFrame(content, fg_color="#2D2D44", corner_radius=10)
                notes_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(
                    notes_frame,
                    text=medical,
                    font=("Arial", 11),
                    text_color="lightgray",
                    wraplength=500,
                    justify="left"
                ).pack(padx=15, pady=15)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load patient details: {str(e)}")
