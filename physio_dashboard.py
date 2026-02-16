"""
Physiotherapist Dashboard for Fixit Physio
For physiotherapists to view their schedule and patient information
"""

import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class PhysioDashboard:
    def __init__(self, user_id, username, full_name):
        """
        Initialize physio dashboard
        Physios can view their appointments and patient details
        """
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        
        # Create main window
        self.app = ctk.CTk()
        self.app.title("Fixit Physio - Physiotherapist Dashboard")
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
        Physio menu focused on their schedule and patients
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
            text=f"👨‍⚕️ {self.full_name}",
            font=("Arial", 13, "bold")
        ).pack(pady=(10, 2))
        
        ctk.CTkLabel(
            user_frame,
            text="Physiotherapist",
            font=("Arial", 10),
            text_color=self.primary_color
        ).pack(pady=(0, 10))
        
        # Navigation menu
        ctk.CTkLabel(
            sidebar,
            text="NAVIGATION",
            font=("Arial", 11, "bold"),
            text_color="gray"
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        # Menu buttons - physio specific
        menu_items = [
            ("📊 My Dashboard", self.show_dashboard),
            ("📅 Today's Patients", self.view_today_schedule),
            ("📆 My Schedule", self.view_my_schedule),
            ("👥 My Patients", self.view_my_patients),
            ("📝 Patient Notes", self.patient_notes),
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
        """Display main dashboard with today's patient schedule"""
        self.clear_main_frame()
        
        # Welcome header
        ctk.CTkLabel(
            self.main_frame,
            text=f"Good day, Dr. {self.full_name.split()[-1]}! 👨‍⚕️",
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
            
            # Today's appointments for this physio
            cursor.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE physio_id = ? AND appointment_date = ?
            """, (self.user_id, today))
            total_today = cursor.fetchone()[0]
            
            # Today's pending
            cursor.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE physio_id = ? AND appointment_date = ? AND status = 'scheduled'
            """, (self.user_id, today))
            pending_today = cursor.fetchone()[0]
            
            # Today's completed
            cursor.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE physio_id = ? AND appointment_date = ? AND status = 'completed'
            """, (self.user_id, today))
            completed_today = cursor.fetchone()[0]
            
            # Total patients treated
            cursor.execute("""
                SELECT COUNT(DISTINCT customer_id) FROM appointments 
                WHERE physio_id = ? AND status = 'completed'
            """, (self.user_id,))
            total_patients = cursor.fetchone()[0]
            
            conn.close()
            
            # Create stat cards
            stats = [
                ("Today's Appointments", str(total_today), "📅", self.primary_color),
                ("Pending", str(pending_today), "⏳", self.warning_color),
                ("Completed Today", str(completed_today), "✅", self.success_color),
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
        
        # Today's schedule preview
        ctk.CTkLabel(
            self.main_frame,
            text="Today's Schedule",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(30, 15))
        
        # Schedule frame with scroll
        schedule_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="#2D2D44",
            corner_radius=15,
            height=300
        )
        schedule_frame.pack(fill="both", expand=True, pady=10)
        
        self.load_today_appointments(schedule_frame)
        
        # Quick actions
        actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            actions_frame,
            text="📅 View Full Schedule",
            font=("Arial", 14, "bold"),
            height=50,
            fg_color=self.primary_color,
            hover_color="#0052A3",
            command=self.view_my_schedule
        ).pack(side="left", padx=(0, 10), expand=True, fill="x")
        
        ctk.CTkButton(
            actions_frame,
            text="👥 My Patients",
            font=("Arial", 14, "bold"),
            height=50,
            fg_color=self.success_color,
            hover_color="#00956F",
            command=self.view_my_patients
        ).pack(side="left", padx=10, expand=True, fill="x")
    
    def load_today_appointments(self, parent_frame):
        """Load and display today's appointments"""
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            cursor.execute("""
                SELECT a.id, a.appointment_time, 
                       c.first_name || ' ' || c.last_name as patient_name,
                       a.service_type, a.status
                FROM appointments a
                LEFT JOIN customers c ON a.customer_id = c.id
                WHERE a.physio_id = ? AND a.appointment_date = ?
                ORDER BY a.appointment_time
            """, (self.user_id, today))
            
            appointments = cursor.fetchall()
            conn.close()
            
            if not appointments:
                ctk.CTkLabel(
                    parent_frame,
                    text="No appointments scheduled for today ✨",
                    font=("Arial", 14),
                    text_color="gray"
                ).pack(pady=50)
                return
            
            # Display each appointment
            for appt in appointments:
                appt_id, time, patient, service, status = appt
                
                # Status color
                status_colors = {
                    'scheduled': self.warning_color,
                    'completed': self.success_color,
                    'cancelled': self.danger_color
                }
                status_color = status_colors.get(status, 'gray')
                
                # Appointment card
                card = ctk.CTkFrame(parent_frame, fg_color="#3A3A5C", corner_radius=10)
                card.pack(fill="x", padx=10, pady=5)
                
                # Time
                ctk.CTkLabel(
                    card,
                    text=time,
                    font=("Arial", 16, "bold"),
                    width=100
                ).grid(row=0, column=0, padx=15, pady=15, sticky="w")
                
                # Patient name
                ctk.CTkLabel(
                    card,
                    text=patient or "Unknown Patient",
                    font=("Arial", 14),
                    width=200
                ).grid(row=0, column=1, padx=10, pady=15, sticky="w")
                
                # Service
                ctk.CTkLabel(
                    card,
                    text=service,
                    font=("Arial", 12),
                    text_color="lightgray",
                    width=180
                ).grid(row=0, column=2, padx=10, pady=15, sticky="w")
                
                # Status
                ctk.CTkLabel(
                    card,
                    text=status.upper(),
                    font=("Arial", 11, "bold"),
                    text_color=status_color,
                    width=100
                ).grid(row=0, column=3, padx=10, pady=15)
                
                # Action button
                if status == 'scheduled':
                    ctk.CTkButton(
                        card,
                        text="✓ Complete",
                        width=100,
                        height=30,
                        fg_color=self.success_color,
                        command=lambda a=appt_id: self.mark_complete(a)
                    ).grid(row=0, column=4, padx=15, pady=15)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load appointments: {str(e)}")
    
    def mark_complete(self, appointment_id):
        """Mark appointment as completed"""
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE appointments SET status = 'completed' WHERE id = ?",
                (appointment_id,)
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Appointment marked as completed!")
            self.show_dashboard()
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not update appointment: {str(e)}")
    
    def view_today_schedule(self):
        """View today's full schedule"""
        import appointment_system
        today = datetime.now().strftime("%Y-%m-%d")
        appointment_system.AppointmentViewer(self.app, self.user_id, specific_date=today, physio_filter=self.user_id)
    
    def view_my_schedule(self):
        """View all appointments for this physio"""
        import appointment_system
        appointment_system.AppointmentViewer(self.app, self.user_id, physio_filter=self.user_id)
    
    def view_my_patients(self):
        """View all patients treated by this physio"""
        messagebox.showinfo("Coming Soon", "Patient history view will be available soon!")
    
    def patient_notes(self):
        """Access patient notes"""
        messagebox.showinfo("Coming Soon", "Patient notes module will be available soon!")
    
    def logout(self):
        """Logout and return to login"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.app.destroy()
            import auth_system
            auth_system.LoginWindow().run()
    
    def run(self):
        """Start the dashboard"""
        self.app.mainloop()
