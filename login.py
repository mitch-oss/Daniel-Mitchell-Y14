"""
login.py - Fixit Physio Enhanced System
Login screen with SHA256 password verification.
"""

import tkinter as tk
from tkinter import messagebox
import database


class LoginScreen:

    def __init__(self, root):
        self.root = root
        self.root.title("Fixit Physio - Staff Login")
        self.root.geometry("420x340")
        self.root.resizable(False, False)
        self.current_user = None
        self.current_role = None
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#2E75B6", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="FIXIT PHYSIO", font=("Arial", 20, "bold"),
                 bg="#2E75B6", fg="white").pack(pady=10)
        tk.Label(header, text="Staff Login Portal", font=("Arial", 11),
                 bg="#2E75B6", fg="#cce4f7").pack()

        # Form
        form = tk.Frame(self.root, padx=40, pady=20)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Staff ID:", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.staff_id_entry = tk.Entry(form, width=28)
        self.staff_id_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        tk.Label(form, text="Password:", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(form, width=28, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        tk.Label(form, text="Company Key:", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.company_entry = tk.Entry(form, width=28)
        self.company_entry.grid(row=2, column=1, pady=5, padx=(10, 0))

        # Login button
        tk.Button(form, text="Login", command=self.attempt_login,
                  bg="#2E75B6", fg="white", width=20,
                  font=("Arial", 11, "bold")).grid(row=3, column=0,
                  columnspan=2, pady=20)

        # Hint
        tk.Label(form, text="Company Key: 12345", fg="gray",
                 font=("Arial", 9)).grid(row=4, column=0, columnspan=2)

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self.attempt_login())

    def attempt_login(self):
        staff_id    = self.staff_id_entry.get().strip()
        password    = self.password_entry.get().strip()
        company_key = self.company_entry.get().strip()

        if not staff_id or not password or not company_key:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        role = database.authenticate_user(staff_id, password, company_key)

        if role:
            self.current_user = staff_id
            self.current_role = role
            self.root.destroy()
            self.open_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")
            self.password_entry.delete(0, tk.END)

    def open_main_menu(self):
        import main_menu
        root = tk.Tk()
        main_menu.MainMenu(root, self.current_user, self.current_role)
        root.mainloop()
