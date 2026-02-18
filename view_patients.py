"""
view_patients.py - Fixit Physio Enhanced System
View, add, edit and delete patients.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database


class ViewPatients:

    def __init__(self, parent, user_id, user_role):
        self.parent    = parent
        self.user_id   = user_id
        self.user_role = user_role
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        # Title bar
        top = tk.Frame(self.parent, bg="#f0f0f0")
        top.pack(fill=tk.X, padx=15, pady=(15, 5))
        tk.Label(top, text="Patient Records", font=("Arial", 16, "bold"),
                 bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Button(top, text="+ Add Patient", bg="#8e44ad", fg="white",
                  command=self.open_add, font=("Arial", 10, "bold"),
                  relief=tk.FLAT, padx=10).pack(side=tk.RIGHT)

        # Search
        sf = tk.Frame(self.parent, bg="#f0f0f0")
        sf.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(sf, text="Search:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.refresh())
        tk.Entry(sf, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)

        # Table
        table_frame = tk.Frame(self.parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        sb = tk.Scrollbar(table_frame)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        cols = ("ID", "Name", "Phone", "Email", "DOB")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings",
                                 yscrollcommand=sb.set)
        sb.config(command=self.tree.yview)

        for col, w in zip(cols, [40, 180, 120, 200, 100]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        bf = tk.Frame(self.parent, bg="#f0f0f0")
        bf.pack(fill=tk.X, padx=15, pady=8)
        tk.Button(bf, text="View / Edit", command=self.open_edit,
                  bg="#f39c12", fg="white", width=12, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="View Appointments", command=self.view_patient_appts,
                  bg="#2E75B6", fg="white", width=16, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Delete", command=self.delete_selected,
                  bg="#e74c3c", fg="white", width=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        term = self.search_var.get() if hasattr(self, "search_var") else ""
        if term:
            patients = database.search_patients(term)
            for p in patients:
                self.tree.insert("", tk.END, values=p)
        else:
            for p in database.get_all_patients():
                self.tree.insert("", tk.END, values=p)

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Nothing selected", "Please select a patient first.")
            return None
        return self.tree.item(sel[0])["values"][0]

    def open_add(self):
        win = tk.Toplevel()
        win.grab_set()
        PatientForm(win, user_id=self.user_id, on_close=self.refresh)

    def open_edit(self):
        pid = self.get_selected_id()
        if pid:
            win = tk.Toplevel()
            win.grab_set()
            PatientForm(win, user_id=self.user_id, patient_id=pid, on_close=self.refresh)

    def view_patient_appts(self):
        pid = self.get_selected_id()
        if not pid:
            return
        appts = database.get_appointments_by_patient(pid)
        win = tk.Toplevel()
        win.title("Patient Appointments")
        win.geometry("500x300")
        tk.Label(win, text="Appointment History", font=("Arial", 13, "bold")).pack(pady=10)
        cols = ("ID", "Date", "Time", "Type", "Status")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for col, w in zip(cols, [40, 100, 70, 100, 90]):
            tree.heading(col, text=col)
            tree.column(col, width=w)
        for a in appts:
            tree.insert("", tk.END, values=a)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def delete_selected(self):
        pid = self.get_selected_id()
        if not pid:
            return
        name = self.tree.item(self.tree.selection()[0])["values"][1]
        if messagebox.askyesno("Delete Patient",
                               f"Delete {name} and all their appointments?\nThis cannot be undone."):
            if database.delete_patient(pid):
                messagebox.showinfo("Deleted", f"{name} has been removed.")
                self.refresh()
            else:
                messagebox.showerror("Error", "Could not delete patient.")


class PatientForm:
    """Shared form for adding and editing patients."""

    def __init__(self, window, user_id, patient_id=None, on_close=None):
        self.window     = window
        self.user_id    = user_id
        self.patient_id = patient_id
        self.on_close   = on_close
        self.window.title("Edit Patient" if patient_id else "Add Patient")
        self.window.geometry("400x400")
        self.window.resizable(False, False)
        self.create_widgets()
        if patient_id:
            self.populate()

    def create_widgets(self):
        title = "Edit Patient" if self.patient_id else "Add New Patient"
        tk.Label(self.window, text=title, font=("Arial", 14, "bold")).pack(pady=15)

        form = tk.Frame(self.window, padx=30)
        form.pack()

        fields = ["Full Name:", "Phone Number:", "Email Address:", "Date of Birth (YYYY-MM-DD):", "Notes:"]
        self.entries = []
        for i, label in enumerate(fields):
            tk.Label(form, text=label, anchor="w").grid(row=i, column=0, sticky="w", pady=5)
            if label == "Notes:":
                widget = tk.Text(form, width=22, height=3)
            else:
                widget = tk.Entry(form, width=25)
            widget.grid(row=i, column=1, pady=5, padx=(10, 0))
            self.entries.append(widget)

        bf = tk.Frame(self.window)
        bf.pack(pady=15)
        tk.Button(bf, text="Save", command=self.save,
                  bg="#8e44ad", fg="white", width=12,
                  font=("Arial", 10, "bold"), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Cancel", command=self.window.destroy,
                  width=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

    def populate(self):
        data = database.get_patient_by_id(self.patient_id)
        if not data:
            return
        # data: patient_id, name, phone, email, dob, notes, created_date
        vals = [data[1], data[2], data[3], data[4], data[5]]
        for widget, val in zip(self.entries, vals):
            if isinstance(widget, tk.Text):
                widget.insert("1.0", val or "")
            else:
                widget.insert(0, val or "")

    def save(self):
        name  = self.entries[0].get().strip()
        phone = self.entries[1].get().strip()
        email = self.entries[2].get().strip()
        dob   = self.entries[3].get().strip()
        notes = self.entries[4].get("1.0", tk.END).strip()

        if not name:
            messagebox.showerror("Error", "Patient name is required.")
            return

        if self.patient_id:
            success = database.update_patient(self.patient_id, name, phone, email, dob, notes)
            msg = "Patient updated successfully."
        else:
            result = database.add_patient(name, phone, email, dob, notes)
            success = result is not None
            msg = "Patient added successfully."

        if success:
            messagebox.showinfo("Saved", msg)
            if self.on_close:
                self.on_close()
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Could not save patient.")
