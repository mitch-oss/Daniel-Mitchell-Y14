"""
add_appointment.py - Fixit Physio Enhanced System
Add a new appointment with date picker widget.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database
from date_picker import DatePicker

APPOINTMENT_TYPES = ["Assessment", "Treatment", "Follow-up", "Review", "Discharge"]
HOURS   = [f"{h:02d}" for h in range(8, 19)]
MINUTES = ["00", "15", "30", "45"]


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
        ttk.Combobox(form, textvariable=self.type_var, values=APPOINTMENT_TYPES,
                     width=28, state="readonly").grid(
            row=3, column=1, pady=8, padx=(10, 0))

        # Notes
        tk.Label(form, text="Notes:", anchor="w").grid(
            row=4, column=0, sticky="nw", pady=8)
        self.notes_text = tk.Text(form, width=22, height=4)
        self.notes_text.grid(row=4, column=1, pady=8, padx=(10, 0))

        # Buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Confirm Booking", command=self.save,
                  bg="#2E75B6", fg="white", width=16,
                  font=("Arial", 10, "bold"), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.window.destroy,
                  width=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

    def save(self):
        patient_str = self.patient_var.get()
        appt_date   = self.date_picker.get()
        appt_time   = f"{self.hour_var.get()}:{self.min_var.get()}"
        appt_type   = self.type_var.get()
        notes       = self.notes_text.get("1.0", tk.END).strip()

        if not patient_str:
            messagebox.showerror("Error", "Please select a patient.")
            return

        patient_id = int(patient_str.split(" - ")[0])
        success = database.add_appointment(
            patient_id, appt_date, appt_time, appt_type, notes, self.user_id
        )
        if success:
            messagebox.showinfo("Booked!", f"Appointment booked for {appt_date} at {appt_time}.")
            if self.on_close:
                self.on_close()
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Could not save appointment.")
