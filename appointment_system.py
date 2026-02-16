"""
Appointment Viewer for Fixit Physio
Displays, filters, and manages appointments
"""

import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class AppointmentViewer:
    def __init__(self, parent, user_id, specific_date=None, physio_filter=None):
        """
        Initialize appointment viewer
        parent: main window
        user_id: current logged in user
        specific_date: optional date to filter by
        physio_filter: optional physio ID to filter appointments
        """
        self.user_id = user_id
        self.specific_date = specific_date
        self.physio_filter = physio_filter
        
        # Create window
        self.window = ctk.CTkToplevel(parent)
        
        if specific_date:
            self.window.title(f"Schedule - {specific_date}")
        elif physio_filter:
            self.window.title("My Appointments")
        else:
            self.window.title("All Appointments")
        
        self.window.geometry("1300x800")
        
        # Colors
        self.primary_color = "#0066CC"
        self.success_color = "#00B894"
        self.warning_color = "#F39C12"
        self.danger_color = "#E17055"
        
        # Setup UI
        self.setup_ui()
        self.load_appointments()
    
    def setup_ui(self):
        """Create the appointment viewer interface"""
        
        # Header
        header = ctk.CTkFrame(self.window, fg_color=self.primary_color, corner_radius=0)
        header.pack(fill="x")
        
        if self.specific_date:
            title = f"📅 Schedule for {self.specific_date}"
        elif self.physio_filter:
            title = "📅 My Appointments"
        else:
            title = "📅 All Appointments"
        
        ctk.CTkLabel(
            header,
            text=title,
            font=("Arial", 26, "bold"),
            text_color="white"
        ).pack(pady=20)
        
        # Filter controls
        filter_frame = ctk.CTkFrame(self.window, fg_color="#2D2D44", corner_radius=10)
        filter_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            filter_frame,
            text="Filters:",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=(15, 20), pady=10)
        
        # Date filter
        ctk.CTkLabel(filter_frame, text="Date:", font=("Arial", 12)).pack(side="left", padx=(0, 5))
        self.filter_date = ctk.CTkEntry(filter_frame, placeholder_text="YYYY-MM-DD", width=130, height=32)
        self.filter_date.pack(side="left", padx=(0, 20))
        
        # Status filter
        ctk.CTkLabel(filter_frame, text="Status:", font=("Arial", 12)).pack(side="left", padx=(0, 5))
        self.filter_status = ctk.CTkComboBox(
            filter_frame,
            values=["All", "scheduled", "completed", "cancelled", "no-show"],
            width=130,
            height=32
        )
        self.filter_status.pack(side="left", padx=(0, 20))
        self.filter_status.set("All")
        
        # Buttons
        ctk.CTkButton(
            filter_frame,
            text="🔍 Apply Filter",
            command=self.load_appointments,
            fg_color=self.primary_color,
            width=120,
            height=32
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="🔄 Reset",
            command=self.reset_filters,
            fg_color="#636E72",
            width=100,
            height=32
        ).pack(side="left", padx=5)
        
        # Main content area - scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(self.window, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Bottom action bar
        action_bar = ctk.CTkFrame(self.window, fg_color="transparent")
        action_bar.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            action_bar,
            text="📊 View Statistics",
            fg_color="#9B59B6",
            hover_color="#7D3C98",
            width=150,
            height=40,
            command=self.show_statistics
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            action_bar,
            text="✗ Close",
            fg_color=self.danger_color,
            hover_color="#C94531",
            width=120,
            height=40,
            command=self.window.destroy
        ).pack(side="right", padx=5)
    
    def reset_filters(self):
        """Clear all filters"""
        self.filter_date.delete(0, 'end')
        self.filter_status.set("All")
        self.load_appointments()
    
    def load_appointments(self):
        """Load and display appointments based on filters"""
        
        # Clear existing content
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            # Build query
            query = """
                SELECT a.id, a.appointment_date, a.appointment_time,
                       c.first_name || ' ' || c.last_name as customer_name,
                       u.full_name as physio_name,
                       a.service_type, a.duration, a.price, a.status, a.notes
                FROM appointments a
                LEFT JOIN customers c ON a.customer_id = c.id
                LEFT JOIN users u ON a.physio_id = u.id
                WHERE 1=1
            """
            
            params = []
            
            # Apply specific date filter (from constructor)
            if self.specific_date:
                query += " AND a.appointment_date = ?"
                params.append(self.specific_date)
            
            # Apply physio filter (from constructor)
            if self.physio_filter:
                query += " AND a.physio_id = ?"
                params.append(self.physio_filter)
            
            # Apply user input filters
            filter_date_val = self.filter_date.get().strip()
            if filter_date_val:
                query += " AND a.appointment_date = ?"
                params.append(filter_date_val)
            
            filter_status_val = self.filter_status.get()
            if filter_status_val != "All":
                query += " AND a.status = ?"
                params.append(filter_status_val)
            
            query += " ORDER BY a.appointment_date DESC, a.appointment_time"
            
            cursor.execute(query, params)
            appointments = cursor.fetchall()
            conn.close()
            
            if not appointments:
                ctk.CTkLabel(
                    self.scroll_frame,
                    text="No appointments found matching your criteria 🔍",
                    font=("Arial", 16),
                    text_color="gray"
                ).pack(pady=100)
                return
            
            # Create header row
            header_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#1a1a2e", corner_radius=10)
            header_frame.pack(fill="x", pady=(0, 10))
            
            headers = [
                ("Date", 110),
                ("Time", 80),
                ("Patient", 170),
                ("Physiotherapist", 150),
                ("Service", 180),
                ("Duration", 80),
                ("Price", 80),
                ("Status", 100),
                ("Actions", 180)
            ]
            
            for i, (header, width) in enumerate(headers):
                ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=("Arial", 13, "bold"),
                    width=width
                ).grid(row=0, column=i, padx=8, pady=12, sticky="w")
            
            # Display each appointment
            for idx, appt in enumerate(appointments):
                appt_id, date, time, patient, physio, service, duration, price, status, notes = appt
                
                # Status colors
                status_colors = {
                    'scheduled': self.warning_color,
                    'completed': self.success_color,
                    'cancelled': self.danger_color,
                    'no-show': '#E84393'
                }
                status_color = status_colors.get(status, 'gray')
                
                # Appointment row
                row_frame = ctk.CTkFrame(
                    self.scroll_frame,
                    fg_color="#2D2D44" if idx % 2 == 0 else "#3A3A5C",
                    corner_radius=8
                )
                row_frame.pack(fill="x", pady=3)
                
                # Format date
                try:
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    date_str = date_obj.strftime("%d %b %Y")
                except:
                    date_str = date
                
                # Display data
                data = [
                    (date_str, 110),
                    (time, 80),
                    (patient[:20] + "..." if patient and len(patient) > 20 else patient or "N/A", 170),
                    (physio[:18] + "..." if physio and len(physio) > 18 else physio or "Unassigned", 150),
                    (service[:22] + "..." if len(service) > 22 else service, 180),
                    (f"{duration} min", 80),
                    (f"£{price:.2f}", 80),
                ]
                
                for i, (text, width) in enumerate(data):
                    ctk.CTkLabel(
                        row_frame,
                        text=text,
                        font=("Arial", 12),
                        width=width
                    ).grid(row=0, column=i, padx=8, pady=10, sticky="w")
                
                # Status with color
                ctk.CTkLabel(
                    row_frame,
                    text=status.upper(),
                    font=("Arial", 11, "bold"),
                    text_color=status_color,
                    width=100
                ).grid(row=0, column=7, padx=8, pady=10, sticky="w")
                
                # Action buttons
                action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                action_frame.grid(row=0, column=8, padx=8, pady=10)
                
                if status == 'scheduled':
                    # Complete button
                    ctk.CTkButton(
                        action_frame,
                        text="✓",
                        width=50,
                        height=28,
                        fg_color=self.success_color,
                        hover_color="#00956F",
                        command=lambda a=appt_id: self.update_status(a, 'completed')
                    ).pack(side="left", padx=2)
                    
                    # Cancel button
                    ctk.CTkButton(
                        action_frame,
                        text="✗",
                        width=50,
                        height=28,
                        fg_color=self.danger_color,
                        hover_color="#C94531",
                        command=lambda a=appt_id: self.update_status(a, 'cancelled')
                    ).pack(side="left", padx=2)
                
                # Notes indicator
                if notes:
                    ctk.CTkLabel(
                        action_frame,
                        text="📝",
                        font=("Arial", 14)
                    ).pack(side="left", padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load appointments: {str(e)}")
    
    def update_status(self, appointment_id, new_status):
        """Update appointment status"""
        try:
            # Confirm action
            if not messagebox.askyesno("Confirm", f"Mark this appointment as {new_status}?"):
                return
            
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE appointments SET status = ? WHERE id = ?",
                (new_status, appointment_id)
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Appointment status updated to {new_status}")
            self.load_appointments()
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not update status: {str(e)}")
    
    def show_statistics(self):
        """Display appointment statistics"""
        try:
            conn = sqlite3.connect('fixit_physio.db')
            cursor = conn.cursor()
            
            # Get statistics
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'scheduled'")
            scheduled = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'completed'")
            completed = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'cancelled'")
            cancelled = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'no-show'")
            no_show = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(price) FROM appointments WHERE status = 'completed'")
            total_revenue = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT AVG(price) FROM appointments WHERE status = 'completed'")
            avg_price = cursor.fetchone()[0] or 0
            
            conn.close()
            
            # Create statistics window
            stats_window = ctk.CTkToplevel(self.window)
            stats_window.title("Appointment Statistics")
            stats_window.geometry("500x450")
            stats_window.attributes('-topmost', True)
            
            ctk.CTkLabel(
                stats_window,
                text="📊 Appointment Statistics",
                font=("Arial", 22, "bold")
            ).pack(pady=20)
            
            # Statistics grid
            stats_frame = ctk.CTkFrame(stats_window, fg_color="transparent")
            stats_frame.pack(fill="both", expand=True, padx=30, pady=10)
            
            stats = [
                (f"{scheduled}", "Scheduled", self.warning_color),
                (f"{completed}", "Completed", self.success_color),
                (f"{cancelled}", "Cancelled", self.danger_color),
                (f"{no_show}", "No-Show", "#E84393"),
                (f"£{total_revenue:.2f}", "Total Revenue", "#9B59B6"),
                (f"£{avg_price:.2f}", "Avg. Price", self.primary_color),
            ]
            
            for i, (value, label, color) in enumerate(stats):
                card = ctk.CTkFrame(stats_frame, fg_color="#2D2D44", corner_radius=10)
                card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
                stats_frame.grid_columnconfigure(i%2, weight=1)
                stats_frame.grid_rowconfigure(i//2, weight=1)
                
                ctk.CTkLabel(
                    card,
                    text=value,
                    font=("Arial", 28, "bold"),
                    text_color=color
                ).pack(pady=(20, 5))
                
                ctk.CTkLabel(
                    card,
                    text=label,
                    font=("Arial", 13),
                    text_color="lightgray"
                ).pack(pady=(0, 20))
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load statistics: {str(e)}")
