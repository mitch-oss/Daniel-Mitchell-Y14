"""
staff_management.py - Fixit Physio Enhanced System
Admin-only screen to view, add and remove staff accounts.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database

ROLES = ["Receptionist", "Physiotherapist", "Admin"]


class StaffManagement:

    def __init__(self, parent, user_id):
        self.parent  = parent
        self.user_id = user_id
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        top = tk.Frame(self.parent, bg="#f0f0f0")
        top.pack(fill=tk.X, padx=15, pady=(15, 5))
        tk.Label(top, text="Staff Management", font=("Arial", 16, "bold"),
                 bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Button(top, text="+ Add Staff", bg="#1a4a7a", fg="white",
                  command=self.open_add, font=("Arial", 10, "bold"),
                  relief=tk.FLAT, padx=10).pack(side=tk.RIGHT)

        tf = tk.Frame(self.parent)
        tf.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        sb = tk.Scrollbar(tf)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        cols = ("ID", "Staff ID", "Role", "Created")
        self.tree = ttk.Treeview(tf, columns=cols, show="headings",
                                 yscrollcommand=sb.set)
        sb.config(command=self.tree.yview)
        for col, w in zip(cols, [40, 100, 160, 180]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w)
        self.tree.pack(fill=tk.BOTH, expand=True)

        bf = tk.Frame(self.parent, bg="#f0f0f0")
        bf.pack(fill=tk.X, padx=15, pady=8)
        tk.Button(bf, text="Delete Staff", command=self.delete_staff,
                  bg="#e74c3c", fg="white", width=14, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Reset Password", command=self.reset_password,
                  bg="#f39c12", fg="white", width=14, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for user in database.get_all_users():
            self.tree.insert("", tk.END, values=user)

    def get_selected_staff_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Nothing selected", "Please select a staff member.")
            return None
        return self.tree.item(sel[0])["values"][1]

    def delete_staff(self):
        sid = self.get_selected_staff_id()
        if not sid:
            return
        if sid == self.user_id:
            messagebox.showerror("Error", "You cannot delete your own account.")
            return
        if messagebox.askyesno("Confirm", f"Delete staff member {sid}?"):
            if database.delete_user(sid):
                messagebox.showinfo("Deleted", "Staff account removed.")
                self.refresh()
            else:
                messagebox.showerror("Error", "Could not delete staff member.")

    def reset_password(self):
        sid = self.get_selected_staff_id()
        if not sid:
            return
        win = tk.Toplevel()
        win.grab_set()
        win.title("Reset Password")
        win.geometry("300x200")
        win.resizable(False, False)
        tk.Label(win, text=f"Reset password for {sid}",
                 font=("Arial", 11, "bold")).pack(pady=15)
        tk.Label(win, text="New Password:").pack()
        pw1 = tk.Entry(win, show="*", width=25)
        pw1.pack(pady=5)
        tk.Label(win, text="Confirm Password:").pack()
        pw2 = tk.Entry(win, show="*", width=25)
        pw2.pack(pady=5)

        def do_reset():
            if pw1.get() != pw2.get():
                messagebox.showerror("Error", "Passwords do not match.")
                return
            if len(pw1.get()) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters.")
                return
            if database.change_password(sid, pw1.get()):
                messagebox.showinfo("Done", "Password updated successfully.")
                win.destroy()
            else:
                messagebox.showerror("Error", "Could not update password.")

        tk.Button(win, text="Reset", command=do_reset,
                  bg="#1a4a7a", fg="white", width=12,
                  relief=tk.FLAT).pack(pady=10)

    def open_add(self):
        win = tk.Toplevel()
        win.grab_set()
        win.title("Add Staff Member")
        win.geometry("320x280")
        win.resizable(False, False)
        tk.Label(win, text="Add Staff Member",
                 font=("Arial", 13, "bold")).pack(pady=15)

        form = tk.Frame(win, padx=30)
        form.pack()

        tk.Label(form, text="Staff ID (5 digits):").grid(row=0, column=0, sticky="w", pady=5)
        sid_entry = tk.Entry(form, width=20)
        sid_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        tk.Label(form, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        pw_entry = tk.Entry(form, width=20, show="*")
        pw_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        tk.Label(form, text="Role:").grid(row=2, column=0, sticky="w", pady=5)
        role_var = tk.StringVar(value="Receptionist")
        ttk.Combobox(form, textvariable=role_var, values=ROLES,
                     width=18, state="readonly").grid(row=2, column=1, pady=5, padx=(10, 0))

        def do_add():
            sid  = sid_entry.get().strip()
            pw   = pw_entry.get().strip()
            role = role_var.get()
            if len(sid) != 5 or not sid.isdigit():
                messagebox.showerror("Error", "Staff ID must be exactly 5 digits.")
                return
            if len(pw) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters.")
                return
            if database.add_user(sid, pw, role):
                messagebox.showinfo("Added", f"Staff {sid} added as {role}.")
                self.refresh()
                win.destroy()
            else:
                messagebox.showerror("Error", "Staff ID already exists.")

        tk.Button(win, text="Add Staff", command=do_add,
                  bg="#1a4a7a", fg="white", width=14,
                  font=("Arial", 10, "bold"), relief=tk.FLAT).pack(pady=15)
