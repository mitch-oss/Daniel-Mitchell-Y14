"""
view_appointments.py - Fixit Physio Enhanced System
View, search, edit and delete appointments.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database


class ViewAppointments:

    def __init__(self, parent, user_id, user_role):
        self.parent    = parent
        self.user_id   = user_id
        self.user_role = user_role
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        # ── Title bar ──
        top = tk.Frame(self.parent, bg="#f0f0f0")
        top.pack(fill=tk.X, padx=15, pady=(15, 5))
        tk.Label(top, text="Appointments", font=("Arial", 16, "bold"),
                 bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Button(top, text="+ New Appointment", bg="#2E75B6", fg="white",
                  command=self.open_add, font=("Arial", 10, "bold"),
                  relief=tk.FLAT, padx=10).pack(side=tk.RIGHT)

        # ── Search bar ──
        search_frame = tk.Frame(self.parent, bg="#f0f0f0")
        search_frame.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(search_frame, text="Search patient:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.refresh())
        tk.Entry(search_frame, textvariable=self.search_var, width=25).pack(side=tk.LEFT, padx=5)
        tk.Label(search_frame, text="  Filter by date (YYYY-MM-DD):", bg="#f0f0f0").pack(side=tk.LEFT)
        self.date_var = tk.StringVar()
        self.date_var.trace("w", lambda *a: self.refresh())
        tk.Entry(search_frame, textvariable=self.date_var, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Clear", command=self.clear_filters,
                  bg="#aaaaaa", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        # ── Table ──
        table_frame = tk.Frame(self.parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        cols = ("ID", "Patient", "Date", "Time", "Type", "Status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings",
                                 yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        widths = [40, 180, 100, 70, 100, 90]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # ── Buttons ──
        btn_frame = tk.Frame(self.parent, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, padx=15, pady=8)

        tk.Button(btn_frame, text="Edit Selected", command=self.open_edit,
                  bg="#f39c12", fg="white", width=14, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected,
                  bg="#e74c3c", fg="white", width=14, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh,
                  bg="#27ae60", fg="white", width=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        search = self.search_var.get() if hasattr(self, "search_var") else ""
        date   = self.date_var.get()   if hasattr(self, "date_var")   else ""
        for appt in database.get_all_appointments(search, date):
            self.tree.insert("", tk.END, values=appt, tags=(appt[0],))

    def clear_filters(self):
        self.search_var.set("")
        self.date_var.set("")

    def open_add(self):
        import add_appointment
        win = tk.Toplevel()
        win.grab_set()
        add_appointment.AddAppointment(win, self.user_id, on_close=self.refresh)

    def open_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Nothing selected", "Please select an appointment to edit.")
            return
        appt_id = self.tree.item(sel[0])["values"][0]
        import edit_appointment
        win = tk.Toplevel()
        win.grab_set()
        edit_appointment.EditAppointment(win, appt_id, self.user_id, on_close=self.refresh)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Nothing selected", "Please select an appointment to delete.")
            return
        appt_id  = self.tree.item(sel[0])["values"][0]
        pat_name = self.tree.item(sel[0])["values"][1]
        if messagebox.askyesno("Confirm Delete",
                               f"Delete appointment for {pat_name}?"):
            if database.delete_appointment(appt_id):
                messagebox.showinfo("Deleted", "Appointment removed.")
                self.refresh()
            else:
                messagebox.showerror("Error", "Could not delete appointment.")
