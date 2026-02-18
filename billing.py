"""
billing.py - Fixit Physio Enhanced System
Create, view and manage invoices.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database


class BillingScreen:

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
        tk.Label(top, text="Billing & Invoices", font=("Arial", 16, "bold"),
                 bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Button(top, text="+ New Invoice", bg="#e67e22", fg="white",
                  command=self.open_add_invoice,
                  font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10).pack(side=tk.RIGHT)

        # Filter
        ff = tk.Frame(self.parent, bg="#f0f0f0")
        ff.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(ff, text="Filter:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="All")
        for label in ["All", "Paid", "Unpaid"]:
            tk.Radiobutton(ff, text=label, variable=self.filter_var,
                           value=label, bg="#f0f0f0",
                           command=self.refresh).pack(side=tk.LEFT, padx=5)

        # Outstanding total
        self.total_label = tk.Label(self.parent,
                                    text="", font=("Arial", 11, "bold"),
                                    fg="#e74c3c", bg="#f0f0f0")
        self.total_label.pack(anchor="e", padx=15)

        # Table
        tf = tk.Frame(self.parent)
        tf.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        sb = tk.Scrollbar(tf)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        cols = ("ID", "Patient", "Amount (£)", "Description", "Status", "Date")
        self.tree = ttk.Treeview(tf, columns=cols, show="headings",
                                 yscrollcommand=sb.set)
        sb.config(command=self.tree.yview)
        for col, w in zip(cols, [40, 160, 90, 180, 80, 120]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        bf = tk.Frame(self.parent, bg="#f0f0f0")
        bf.pack(fill=tk.X, padx=15, pady=8)
        tk.Button(bf, text="Mark as Paid", command=self.mark_paid,
                  bg="#27ae60", fg="white", width=14, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Mark as Unpaid", command=self.mark_unpaid,
                  bg="#f39c12", fg="white", width=14, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Delete Invoice", command=self.delete_invoice,
                  bg="#e74c3c", fg="white", width=14, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        f = self.filter_var.get() if hasattr(self, "filter_var") else "All"
        status = "" if f == "All" else f
        for inv in database.get_all_invoices(status):
            # inv: invoice_id, patient_name, amount, description, status, created_at
            self.tree.insert("", tk.END, values=(
                inv[0], inv[1], f"£{inv[2]:.2f}", inv[3], inv[4], inv[5][:10]
            ))
        outstanding = database.get_total_outstanding()
        self.total_label.config(text=f"Total Outstanding: £{outstanding:.2f}")

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Nothing selected", "Please select an invoice.")
            return None
        return self.tree.item(sel[0])["values"][0]

    def mark_paid(self):
        inv_id = self.get_selected_id()
        if inv_id and database.update_invoice_status(inv_id, "Paid"):
            self.refresh()

    def mark_unpaid(self):
        inv_id = self.get_selected_id()
        if inv_id and database.update_invoice_status(inv_id, "Unpaid"):
            self.refresh()

    def delete_invoice(self):
        inv_id = self.get_selected_id()
        if not inv_id:
            return
        if messagebox.askyesno("Confirm", "Delete this invoice?"):
            if database.delete_invoice(inv_id):
                messagebox.showinfo("Deleted", "Invoice removed.")
                self.refresh()

    def open_add_invoice(self):
        win = tk.Toplevel()
        win.grab_set()
        AddInvoice(win, self.user_id, on_close=self.refresh)


class AddInvoice:

    def __init__(self, window, user_id, on_close=None):
        self.window   = window
        self.user_id  = user_id
        self.on_close = on_close
        self.window.title("New Invoice")
        self.window.geometry("400x360")
        self.window.resizable(False, False)
        self.patients = database.get_all_patients()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Create Invoice",
                 font=("Arial", 14, "bold")).pack(pady=15)

        form = tk.Frame(self.window, padx=30)
        form.pack()

        # Patient
        tk.Label(form, text="Patient:", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        self.patient_var = tk.StringVar()
        patient_names = [f"{p[0]} - {p[1]}" for p in self.patients]
        ttk.Combobox(form, textvariable=self.patient_var, values=patient_names,
                     width=26, state="readonly").grid(row=0, column=1, pady=6, padx=(10, 0))
        if patient_names:
            self.patient_var.set(patient_names[0])

        # Amount
        tk.Label(form, text="Amount (£):", anchor="w").grid(row=1, column=0, sticky="w", pady=6)
        self.amount_entry = tk.Entry(form, width=28)
        self.amount_entry.grid(row=1, column=1, pady=6, padx=(10, 0))

        # Description
        tk.Label(form, text="Description:", anchor="w").grid(row=2, column=0, sticky="nw", pady=6)
        self.desc_text = tk.Text(form, width=21, height=4)
        self.desc_text.grid(row=2, column=1, pady=6, padx=(10, 0))

        bf = tk.Frame(self.window)
        bf.pack(pady=15)
        tk.Button(bf, text="Create Invoice", command=self.save,
                  bg="#e67e22", fg="white", width=14,
                  font=("Arial", 10, "bold"), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Cancel", command=self.window.destroy,
                  width=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

    def save(self):
        patient_str = self.patient_var.get()
        amount_str  = self.amount_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()

        if not patient_str:
            messagebox.showerror("Error", "Please select a patient.")
            return
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid positive amount.")
            return
        if not description:
            messagebox.showerror("Error", "Please enter a description.")
            return

        patient_id = int(patient_str.split(" - ")[0])
        result = database.create_invoice(patient_id, None, amount, description, self.user_id)
        if result:
            messagebox.showinfo("Success", f"Invoice #{result} created.")
            if self.on_close:
                self.on_close()
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Could not create invoice.")
