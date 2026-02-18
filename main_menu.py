"""
main_menu.py - Fixit Physio Enhanced System
Main dashboard with sidebar navigation.
"""

import tkinter as tk
from tkinter import messagebox
import database


class MainMenu:

    def __init__(self, root, user_id, user_role):
        self.root = root
        self.root.title("Fixit Physio - Dashboard")
        self.root.geometry("750x500")
        self.root.resizable(False, False)
        self.user_id   = user_id
        self.user_role = user_role
        self.create_widgets()

    def create_widgets(self):
        # ── Header ──
        header = tk.Frame(self.root, bg="#2E75B6", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="FIXIT PHYSIO - Clinic Management",
                 font=("Arial", 16, "bold"), bg="#2E75B6", fg="white").pack(side=tk.LEFT, padx=20, pady=15)
        tk.Label(header, text=f"Role: {self.user_role}  |  ID: {self.user_id}",
                 font=("Arial", 10), bg="#2E75B6", fg="#cce4f7").pack(side=tk.RIGHT, padx=20)

        # ── Body ──
        body = tk.Frame(self.root)
        body.pack(fill=tk.BOTH, expand=True)

        # ── Sidebar ──
        sidebar = tk.Frame(body, bg="#1a4a7a", width=160)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="NAVIGATION", font=("Arial", 9, "bold"),
                 bg="#1a4a7a", fg="#aaaaaa").pack(pady=(20, 5))

        nav_buttons = [
            ("Dashboard",       self.show_dashboard),
            ("Appointments",    self.open_appointments),
            ("Patients",        self.open_patients),
            ("Billing",         self.open_billing),
        ]

        # Admin only
        if self.user_role == "Admin":
            nav_buttons.append(("Staff Management", self.open_staff))

        for label, cmd in nav_buttons:
            tk.Button(sidebar, text=label, command=cmd,
                      bg="#1a4a7a", fg="white", relief=tk.FLAT,
                      width=18, anchor="w", padx=10,
                      activebackground="#2E75B6",
                      font=("Arial", 10)).pack(pady=2, padx=5)

        tk.Button(sidebar, text="Logout", command=self.logout,
                  bg="#c0392b", fg="white", width=18,
                  font=("Arial", 10, "bold")).pack(side=tk.BOTTOM, pady=20, padx=5)

        # ── Main content area ──
        self.content = tk.Frame(body, bg="#f0f0f0")
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()

        tk.Label(self.content, text="Welcome Back!",
                 font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=(30, 5))
        tk.Label(self.content, text="What would you like to do?",
                 font=("Arial", 11), bg="#f0f0f0", fg="gray").pack(pady=(0, 30))

        btn_frame = tk.Frame(self.content, bg="#f0f0f0")
        btn_frame.pack()

        buttons = [
            ("+ New Appointment",    "#2E75B6", self.open_appointments),
            ("View Appointments",    "#27ae60", self.open_appointments),
            ("Manage Patients",      "#8e44ad", self.open_patients),
            ("Billing",              "#e67e22", self.open_billing),
        ]

        for i, (text, color, cmd) in enumerate(buttons):
            r, c = divmod(i, 2)
            tk.Button(btn_frame, text=text, command=cmd,
                      bg=color, fg="white", width=22, height=3,
                      font=("Arial", 11, "bold"),
                      relief=tk.FLAT).grid(row=r, column=c, padx=10, pady=10)

        # Quick stats
        stats = tk.Frame(self.content, bg="#f0f0f0")
        stats.pack(pady=20)

        outstanding = database.get_total_outstanding()
        patients    = len(database.get_all_patients())
        today_appts = len(database.get_all_appointments())

        for label, value in [
            ("Total Patients", patients),
            ("Total Appointments", today_appts),
            (f"Outstanding (£)", f"£{outstanding:.2f}"),
        ]:
            box = tk.Frame(stats, bg="white", relief=tk.GROOVE, bd=1, width=130, height=70)
            box.pack(side=tk.LEFT, padx=10)
            box.pack_propagate(False)
            tk.Label(box, text=str(value), font=("Arial", 16, "bold"), bg="white").pack(pady=(10, 0))
            tk.Label(box, text=label, font=("Arial", 8), bg="white", fg="gray").pack()

    def open_appointments(self):
        self.clear_content()
        import view_appointments
        view_appointments.ViewAppointments(self.content, self.user_id, self.user_role)

    def open_patients(self):
        self.clear_content()
        import view_patients
        view_patients.ViewPatients(self.content, self.user_id, self.user_role)

    def open_billing(self):
        self.clear_content()
        import billing
        billing.BillingScreen(self.content, self.user_id, self.user_role)

    def open_staff(self):
        self.clear_content()
        import staff_management
        staff_management.StaffManagement(self.content, self.user_id)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            import login
            root = tk.Tk()
            login.LoginScreen(root)
            root.mainloop()
