"""
Staff Dashboard for Fixit Physio
For reception/administrative staff handling bookings and patient check-ins
"""

import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class StaffDashboard:
    def __init__(self, user_id, username, full_name):
        """
        Initialize staff dashboard
        Staff can manage appointments and patients but not system settings
        """
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        
        # Create main window
        self.app = ctk.CTk()
        self.app.title("Fixit Physio - Staff Dashboard")
        self.app.geometry("1200x800")
        
        # Color scheme
        self.primary_color = "#0066CC"
        self.success_color = "#00B894"
        self.warning_color = "#F39C12"
        self.danger_color = "#E17055"
        
        # Setup grid layout
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        
        # Build interface
        self.setup_sidebar()
        self.setup_main_content()
    
    def setup_sidebar(self):
        """
        Create sidebar navigation menu
        Staff menu has limited options compared to admin
        """
        # Sidebar frame
        sidebar = ctk.CTkFrame(self.app, width=250, corner_radius=0, fg_color="#1a1a2e")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        # Logo section
        logo_frame = ctk.CTkFrame(sidebar, fg_color=self.primary_color, corner_radius=10)
        logo_frame.pack(fill="x", padx=15, pady=(20, 10))
        
        ctk.CTkLabel(
            logo_frame,
            text="⚕️ FIXIT PHYSIO",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(pady=15)
        
        # User info section
        user_frame = ctk.CTkFrame(sidebar, fg_color="#2D2D44", corner_radius=10)
        user_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.full_name}",
            font=("Arial", 13, "bold")
        ).pack(pady=(10, 2))
        
        ctk.CTkLabel(
            user_frame,
            text="Reception Staff",
            font=("Arial", 10),
            text_color=self.success_color
        ).pack(pady=(0, 10))
        
        # Navigation menu
        ctk.CTkLabel(
            sidebar,
            text="NAVIGATION",
            font=("Arial", 11, "bold"),
            text_color="gray"
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        # Menu buttons - staff specific
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("📅 Today's Schedule", self.view_today_schedule),
            ("📆 All Appointments", self.view_all_appointments),
            ("➕ New Booking", self.new_appointment),
            ("👥 Patient List", self.manage_patients),
            ("🔍 Search Patient", self.search_patient),
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Arial", 13),
                fg_color="transparent",
                text_color="white",
                hover_color="#2D2D44",
                anchor="w",
                height=40,
                command=command
            )
            btn.pack(fill="x", padx=15, pady=5)
        
        # Logout button
        ctk.CTkButton(
            sidebar,
            text="🚪 Logout",
            font=("Arial", 13, "bold"),
            fg_color=self.danger_color,
            hover_color="#C94531",
            height=40,
            command=self.logout
        ).pack(side="bottom", fill="x", padx=15, pady=20)
    
    def setup_main_content(self):
        """Create main content area"""
        self.main_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def clear_main_frame(self):
        """Remove all widgets from main content area"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Display main dashboard with today's overview"""
        self.clear_main_frame()
        
        # Welcome header
        ctk.CTkLabel(
            self.main_frame,
            text=f"Welcome back, {self.full_name.split()[0]}! 👋",
            font=("Arial", 28, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        ctk.CTkLabel(
            self.main_frame,
            text=current_date,
            font=("Arial", 13),
            text_color="gray"
        ).pack(anchor="w", pady=(0, 30))
        
        # Quick stats for today
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Today's total appointments
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", (today,))
            total_today = cursor.fetchone()[0]
            
            # Today's pending appointments
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ? AND status = 'scheduled'", (today,))
            pending_today = cursor.fetchone()[0]
            
            # Today's completed
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ? AND status = 'completed'", (today,))
            completed_today = cursor.fetchone()[0]
            
            # Total patients
            cursor.execute("SELECT COUNT(*) FROM customers")
            total_patients = cursor.fetchone()[0]
            
            conn.close()
            
            # Create stat cards
            stats = [
                ("Today's Total", str(total_today), "📅", self.primary_color),
                ("Pending", str(pending_today), "⏳", self.warning_color),
                ("Completed", str(completed_today), "✅", self.success_color),
                ("Total Patients", str(total_patients), "👥", "#9B59B6"),
            ]
            
            for i, (label, value, icon, color) in enumerate(stats):
                card = ctk.CTkFrame(stats_frame, fg_color="#2D2D44", corner_radius=15)
                card.grid(row=0, column=i, padx=10, sticky="ew")
                stats_frame.grid_columnconfigure(i, weight=1)
                
                ctk.CTkLabel(card, text=icon, font=("Arial", 30)).pack(pady=(20, 5))
                ctk.CTkLabel(card, text=value, font=("Arial", 26, "bold"), text_color=color).pack(pady=5)
                ctk.CTkLabel(card, text=label, font=("Arial", 11), text_color="gray").pack(pady=(0, 20))
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load statistics: {str(e)}")
        
        # Quick actions
        ctk.CTkLabel(
            self.main_frame,
            text="Quick Actions",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(30, 15))
        
        actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=10)
        
        # Quick action buttons
        ctk.CTkButton(
            actions_frame,
            text="➕ Book New Appointment",
            font=("Arial", 14, "bold"),
            height=60,
            fg_color=self.success_color,
            hover_color="#00956F",
            command=self.new_appointment
        ).pack(side="left", padx=(0, 10), expand=True, fill="x")
        
        ctk.CTkButton(
            actions_frame,
            text="📅 View Today's Schedule",
            font=("Arial", 14, "bold"),
            height=60,
            fg_color=self.primary_color,
            hover_color="#0052A3",
            command=self.view_today_schedule
        ).pack(side="left", padx=10, expand=True, fill="x")
        
        ctk.CTkButton(
            actions_frame,
            text="👤 Add New Patient",
            font=("Arial", 14, "bold"),
            height=60,
            fg_color="#9B59B6",
            hover_color="#7D3C98",
            command=self.add_patient
        ).pack(side="left", padx=10, expand=True, fill="x")
    
    def view_today_schedule(self):
        """View today's appointment schedule"""
        import appointment_system
        today = datetime.now().strftime("%Y-%m-%d")
        appointment_system.AppointmentViewer(self.app, self.user_id, specific_date=today)
    
    def view_all_appointments(self):
        """View all appointments"""
        import appointment_system
        appointment_system.AppointmentViewer(self.app, self.user_id)
    
    def new_appointment(self):
        """Open booking interface"""
        import booking_interface
        booking_interface.BookingInterface(self.app, self.user_id)
    
    def manage_patients(self):
        """Open patient management"""
        import patient_manager
        patient_manager.PatientManager(self.app)
    
    def search_patient(self):
        """Quick patient search"""
        import patient_manager
        patient_manager.PatientManager(self.app, search_mode=True)
    
    def add_patient(self):
        """Quick add patient"""
        import patient_manager
        patient_manager.PatientManager(self.app, quick_add=True)
    
    def logout(self):
        """Logout and return to login"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.app.destroy()
            import auth_system
            auth_system.LoginWindow().run()
    
    def run(self):
        """Start the dashboard"""
        self.app.mainloop()
