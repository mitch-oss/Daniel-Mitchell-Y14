"""
view_patients.py - Fixit Physio Enhanced System
View, add, edit and delete patients.
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import database
from date_picker import DatePicker


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
        self.window.geometry("440x420")
        self.window.resizable(False, False)
        self.create_widgets()
        if patient_id:
            self.populate()

    def create_widgets(self):
        title = "Edit Patient" if self.patient_id else "Add New Patient"
        tk.Label(self.window, text=title, font=("Arial", 14, "bold")).pack(pady=15)

        form = tk.Frame(self.window, padx=30)
        form.pack()

        # Full Name
        tk.Label(form, text="Full Name:", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form, width=28)
        self.name_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        # Phone
        tk.Label(form, text="Phone Number:", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.phone_entry = tk.Entry(form, width=28)
        self.phone_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        # Email
        tk.Label(form, text="Email Address:", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(form, width=28)
        self.email_entry.grid(row=2, column=1, pady=5, padx=(10, 0))

        # DOB (date picker)
        tk.Label(form, text="Date of Birth:", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
        self.dob_picker = DatePicker(form)
        self.dob_picker.grid(row=3, column=1, pady=5, padx=(10, 0), sticky="w")

        # Notes
        tk.Label(form, text="Notes:", anchor="nw").grid(row=4, column=0, sticky="nw", pady=5)
        self.notes_text = tk.Text(form, width=22, height=3)
        self.notes_text.grid(row=4, column=1, pady=5, padx=(10, 0))

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
        self.name_entry.insert(0, data[1] or "")
        self.phone_entry.insert(0, data[2] or "")
        self.email_entry.insert(0, data[3] or "")
        if data[4]:
            self.dob_picker.set(data[4])
        if data[5]:
            self.notes_text.insert("1.0", data[5])

    def save(self):
        name  = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        dob   = self.dob_picker.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        # Required: name
        if not name:
            messagebox.showerror("Error", "Patient name is required.")
            return

        # Phone (optional, but UK format if entered)
        if phone and not re.match(
                r"^(\+44\s?|0)\d{2,4}\s?\d{3,4}\s?\d{3,4}$", phone):
            messagebox.showerror("Invalid Phone",
                "Phone must be a valid UK number "
                "(e.g. 07891 234567 or 02890 123456).")
            return

        # Email (optional, but valid format if entered)
        if email and not re.match(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            messagebox.showerror("Invalid Email",
                "Email address is not in a valid format.")
            return

        # DOB (optional, but must be a real past date if entered)
        if dob:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                messagebox.showerror("Invalid DOB",
                    "Date of birth must be in YYYY-MM-DD format.")
                return
            try:
                dob_parsed = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Invalid DOB",
                    "That is not a real date.")
                return
            if dob_parsed > date.today():
                messagebox.showerror("Invalid DOB",
                    "Date of birth cannot be in the future.")
                return
            if (date.today().year - dob_parsed.year) > 120:
                messagebox.showerror("Invalid DOB",
                    "Date of birth cannot be more than 120 years ago.")
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