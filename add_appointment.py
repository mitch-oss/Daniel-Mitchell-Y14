"""
add_appointment.py - Fixit Physio Enhanced System
Add a new appointment with date picker widget.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import database
from date_picker import DatePicker

APPOINTMENT_TYPES = ["Assessment", "Treatment", "Follow-up", "Review", "Discharge"]
HOURS   = [f"{h:02d}" for h in range(8, 19)]
MINUTES = ["00", "15", "30", "45"]

# Price list for auto-generated invoices: (amount, description)
APPOINTMENT_PRICES = {
    "Assessment":  (45.00, "Initial Assessment"),
    "Treatment":   (60.00, "Treatment Session"),
    "Follow-up":   (40.00, "Follow-up Session"),
    "Review":      (35.00, "Review Consultation"),
    "Discharge":   (0.00,  "Discharge Consultation"),
}


class AddAppointment:

    def __init__(self, window, user_id, on_close=None):
        self.window   = window
        self.user_id  = user_id
        self.on_close = on_close
        self.window.title("New Appointment")
        self.window.geometry("440x480")
        self.window.resizable(False, False)
        self.patients = database.get_all_patients()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="New Appointment",
                 font=("Arial", 14, "bold")).pack(pady=15)

        form = tk.Frame(self.window, padx=30)
        form.pack(fill=tk.BOTH)

        # Patient dropdown
        tk.Label(form, text="Patient:", anchor="w").grid(
            row=0, column=0, sticky="w", pady=8)
        self.patient_var = tk.StringVar()
        patient_names = [f"{p[0]} - {p[1]}" for p in self.patients]
        self.patient_cb = ttk.Combobox(form, textvariable=self.patient_var,
                                       values=patient_names, width=28, state="readonly")
        self.patient_cb.grid(row=0, column=1, pady=8, padx=(10, 0))
        if patient_names:
            self.patient_cb.current(0)

        # Date picker
        tk.Label(form, text="Date:", anchor="w").grid(
            row=1, column=0, sticky="w", pady=8)
        self.date_picker = DatePicker(form)
        self.date_picker.grid(row=1, column=1, pady=8, padx=(10, 0), sticky="w")

        # Time (hour + minute dropdowns)
        tk.Label(form, text="Time:", anchor="w").grid(
            row=2, column=0, sticky="w", pady=8)
        time_frame = tk.Frame(form)
        time_frame.grid(row=2, column=1, pady=8, padx=(10, 0), sticky="w")
        self.hour_var = tk.StringVar(value="09")
        self.min_var  = tk.StringVar(value="00")
        ttk.Combobox(time_frame, textvariable=self.hour_var,
                     values=HOURS, width=4, state="readonly").pack(side=tk.LEFT)
        tk.Label(time_frame, text=" : ").pack(side=tk.LEFT)
        ttk.Combobox(time_frame, textvariable=self.min_var,
                     values=MINUTES, width=4, state="readonly").pack(side=tk.LEFT)

        # Appointment type
        tk.Label(form, text="Type:", anchor="w").grid(
            row=3, column=0, sticky="w", pady=8)
        self.type_var = tk.StringVar(value="Assessment")
        type_cb = ttk.Combobox(form, textvariable=self.type_var, values=APPOINTMENT_TYPES,
                               width=28, state="readonly")
        type_cb.grid(row=3, column=1, pady=8, padx=(10, 0))
        type_cb.bind("<<ComboboxSelected>>", lambda e: self._update_price_hint())

        # Price hint (shows what invoice will be auto-created)
        self.price_hint = tk.Label(form, text="", fg="#27ae60",
                                   font=("Arial", 9, "italic"))
        self.price_hint.grid(row=4, column=1, sticky="w", padx=(10, 0))
        self._update_price_hint()

        # Notes
        tk.Label(form, text="Notes:", anchor="w").grid(
            row=5, column=0, sticky="nw", pady=8)
        self.notes_text = tk.Text(form, width=22, height=4)
        self.notes_text.grid(row=5, column=1, pady=8, padx=(10, 0))

        # Buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Confirm Booking", command=self.save,
                  bg="#2E75B6", fg="white", width=16,
                  font=("Arial", 10, "bold"), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.window.destroy,
                  width=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

    def _update_price_hint(self):
        """Shows the user what invoice will be auto-created for the selected type."""
        appt_type = self.type_var.get()
        if appt_type in APPOINTMENT_PRICES:
            amount, desc = APPOINTMENT_PRICES[appt_type]
            if amount > 0:
                self.price_hint.config(text=f"Invoice: £{amount:.2f} — {desc}")
            else:
                self.price_hint.config(text="No invoice will be created (free)")

    def save(self):
        patient_str = self.patient_var.get()
        appt_date   = self.date_picker.get()
        appt_time   = f"{self.hour_var.get()}:{self.min_var.get()}"
        appt_type   = self.type_var.get()
        notes       = self.notes_text.get("1.0", tk.END).strip()

        if not patient_str:
            messagebox.showerror("Error", "Please select a patient.")
            return

        # Reject past dates
        try:
            chosen = datetime.strptime(appt_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Invalid Date",
                                 "Date must be in YYYY-MM-DD format.")
            return

        if chosen < date.today():
            messagebox.showerror(
                "Invalid Date",
                f"Cannot book an appointment for {appt_date} — "
                "that date has already passed."
            )
            return

        # Block double bookings
        if database.check_appointment_conflict(appt_date, appt_time):
            messagebox.showerror(
                "Slot Unavailable",
                f"An appointment already exists on {appt_date} at {appt_time}.\n"
                "Please choose a different slot."
            )
            return

        patient_id = int(patient_str.split(" - ")[0])

        # Create the appointment first
        success = database.add_appointment(
            patient_id, appt_date, appt_time, appt_type, notes, self.user_id
        )

        if not success:
            messagebox.showerror("Error", "Could not save appointment.")
            return

        # Auto-create matching invoice (skip if the type is free)
        invoice_msg = ""
        if appt_type in APPOINTMENT_PRICES:
            amount, description = APPOINTMENT_PRICES[appt_type]
            if amount > 0:
                # Grab the appointment we just inserted so we can link the invoice to it
                latest = database.get_latest_appointment_for_patient(patient_id)
                appointment_id = latest[0] if latest else None

                invoice_id = database.create_invoice(
                    patient_id, appointment_id, amount, description, self.user_id
                )
                if invoice_id:
                    invoice_msg = f"\nInvoice #{invoice_id} for £{amount:.2f} created (Unpaid)."
                else:
                    invoice_msg = "\nWarning: invoice could not be created automatically."

        messagebox.showinfo(
            "Booked!",
            f"Appointment booked for {appt_date} at {appt_time}.{invoice_msg}"
        )
        if self.on_close:
            self.on_close()
        self.window.destroy()