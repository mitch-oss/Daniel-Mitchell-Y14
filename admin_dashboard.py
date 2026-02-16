"""
Admin Dashboard for Fixit Physio
Full system access including user management and system settings
"""

import customtkinter as ctk
from tkinter import messagebox
import sqlite3

class AdminDashboard:
    def __init__(self, user_id, username, full_name):
        """
        Initialize admin dashboard
        Admin has full access to all system features
        """
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        
        # Create main window
        self.app = ctk.CTk()
        self.app.title("Fixit Physio - Admin Dashboard")
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
        Contains all available admin functions
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
            text="Administrator",
            font=("Arial", 10),
            text_color=self.warning_color
        ).pack(pady=(0, 10))
        
        # Navigation menu
        ctk.CTkLabel(
            sidebar,
            text="NAVIGATION",
            font=("Arial", 11, "bold"),
            text_color="gray"
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        # Menu buttons
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("📅 All Appointments", self.view_all_appointments),
            ("➕ New Booking", self.new_appointment),
            ("👥 Manage Patients", self.manage_patients),
            ("👨‍⚕️ Manage Staff", self.manage_staff),
            ("⚙️ System Settings", self.system_settings),
            ("📈 Reports", self.view_reports),
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
        
        # Logout button at bottom
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
        """
        Create main content area
        This is where different views will be displayed
        """
        # Main content frame
        self.main_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def clear_main_frame(self):
        """Remove all widgets from main content area"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """
        Display main dashboard with statistics and quick actions
        Shows overview of system status
        """
        self.clear_main_frame()
        
        # Page title
        ctk.CTkLabel(
            self.main_frame,
            text="Administrator Dashboard",
            font=("Arial", 28, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            self.main_frame,
            text="System Overview and Quick Actions",
            font=("Arial", 13),
            text_color="gray"
        ).pack(anchor="w", pady=(0, 30))
        
        # Statistics cards
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        
        # Get statistics from database
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            # Today's appointments
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = date('now') AND status = 'scheduled'")
            today_appointments = cursor.fetchone()[0]
            
            # Total patients
            cursor.execute("SELECT COUNT(*) FROM customers")
            total_patients = cursor.fetchone()[0]
            
            # Active staff
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1 AND role != 'admin'")
            active_staff = cursor.fetchone()[0]
            
            # This week's revenue
            cursor.execute("SELECT SUM(price) FROM appointments WHERE status = 'completed' AND appointment_date >= date('now', '-7 days')")
            week_revenue = cursor.fetchone()[0] or 0
            
            conn.close()
            
            # Create stat cards
            stats = [
                ("Today's Appointments", str(today_appointments), "📅", self.primary_color),
                ("Total Patients", str(total_patients), "👥", self.success_color),
                ("Active Staff", str(active_staff), "👨‍⚕️", self.warning_color),
                ("Week Revenue", f"£{week_revenue:.2f}", "💰", "#9B59B6"),
            ]
            
            for i, (label, value, icon, color) in enumerate(stats):
                card = ctk.CTkFrame(stats_frame, fg_color="#2D2D44", corner_radius=15)
                card.grid(row=0, column=i, padx=10, sticky="ew")
                stats_frame.grid_columnconfigure(i, weight=1)
                
                ctk.CTkLabel(
                    card,
                    text=icon,
                    font=("Arial", 30)
                ).pack(pady=(20, 5))
                
                ctk.CTkLabel(
                    card,
                    text=value,
                    font=("Arial", 26, "bold"),
                    text_color=color
                ).pack(pady=5)
                
                ctk.CTkLabel(
                    card,
                    text=label,
                    font=("Arial", 11),
                    text_color="gray"
                ).pack(pady=(0, 20))
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load statistics: {str(e)}")
        
        # Quick actions section
        ctk.CTkLabel(
            self.main_frame,
            text="Quick Actions",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(30, 15))
        
        actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=10)
        
        # Action buttons
        ctk.CTkButton(
            actions_frame,
            text="➕ New Appointment",
            font=("Arial", 14, "bold"),
            height=50,
            fg_color=self.success_color,
            hover_color="#00956F",
            command=self.new_appointment
        ).pack(side="left", padx=(0, 10), expand=True, fill="x")
        
        ctk.CTkButton(
            actions_frame,
            text="👥 Add New Patient",
            font=("Arial", 14, "bold"),
            height=50,
            fg_color=self.primary_color,
            hover_color="#0052A3",
            command=self.add_patient
        ).pack(side="left", padx=10, expand=True, fill="x")
        
        ctk.CTkButton(
            actions_frame,
            text="📊 View Reports",
            font=("Arial", 14, "bold"),
            height=50,
            fg_color="#9B59B6",
            hover_color="#7D3C98",
            command=self.view_reports
        ).pack(side="left", padx=10, expand=True, fill="x")
    
    def view_all_appointments(self):
        """Show appointment viewer"""
        import appointment_system
        appointment_system.AppointmentViewer(self.app, self.user_id)
    
    def new_appointment(self):
        """Open new appointment booking window"""
        import booking_interface
        booking_interface.BookingInterface(self.app, self.user_id)
    
    def manage_patients(self):
        """Open patient management window"""
        import patient_manager
        patient_manager.PatientManager(self.app)
    
    def manage_staff(self):
        """Open staff management interface"""
        messagebox.showinfo("Coming Soon", "Staff management interface will be available soon!")
    
    def system_settings(self):
        """Open system settings"""
        messagebox.showinfo("Coming Soon", "System settings interface will be available soon!")
    
    def view_reports(self):
        """Show reports and analytics"""
        messagebox.showinfo("Coming Soon", "Reports module will be available soon!")
    
    def add_patient(self):
        """Quick add patient dialog"""
        import patient_manager
        patient_manager.PatientManager(self.app, quick_add=True)
    
    def logout(self):
        """
        Logout and return to login screen
        Confirms before closing
        """
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.app.destroy()
            import auth_system
            auth_system.LoginWindow().run()
    
    def run(self):
        """Start the dashboard"""
        self.app.mainloop()
