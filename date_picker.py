"""
date_picker.py - Fixit Physio Enhanced System
Custom date picker widget with Today/Tomorrow shortcuts.
No external libraries needed.
"""

import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
import calendar


class DatePicker(tk.Frame):
    """
    A date picker widget with Today/Tomorrow buttons
    and a simple dropdown calendar.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=parent.cget("bg") if hasattr(parent, "cget") else "#ffffff", **kwargs)
        self._date = date.today()
        self._build()

    def _build(self):
        # Display entry (read-only, shows selected date)
        self.display_var = tk.StringVar(value=self._date.strftime("%Y-%m-%d"))
        entry = tk.Entry(self, textvariable=self.display_var,
                         width=12, state="readonly",
                         readonlybackground="white",
                         font=("Arial", 10))
        entry.pack(side=tk.LEFT)

        # Today button
        tk.Button(self, text="Today", command=self._set_today,
                  bg="#27ae60", fg="white", relief=tk.FLAT,
                  font=("Arial", 9), padx=6).pack(side=tk.LEFT, padx=(4, 2))

        # Tomorrow button
        tk.Button(self, text="Tomorrow", command=self._set_tomorrow,
                  bg="#2E75B6", fg="white", relief=tk.FLAT,
                  font=("Arial", 9), padx=6).pack(side=tk.LEFT, padx=(0, 2))

        # Calendar popup button
        tk.Button(self, text="📅", command=self._open_calendar,
                  relief=tk.FLAT, font=("Arial", 10),
                  bg="#f0f0f0").pack(side=tk.LEFT)

    def _set_today(self):
        self._date = date.today()
        self.display_var.set(self._date.strftime("%Y-%m-%d"))

    def _set_tomorrow(self):
        self._date = date.today() + timedelta(days=1)
        self.display_var.set(self._date.strftime("%Y-%m-%d"))

    def _open_calendar(self):
        CalendarPopup(self, self._date, self._on_date_selected)

    def _on_date_selected(self, selected_date):
        self._date = selected_date
        self.display_var.set(self._date.strftime("%Y-%m-%d"))

    def get(self):
        """Returns selected date as YYYY-MM-DD string."""
        return self.display_var.get()

    def set(self, date_str):
        """Sets the date from a YYYY-MM-DD string."""
        try:
            self._date = date.fromisoformat(date_str)
            self.display_var.set(date_str)
        except (ValueError, TypeError):
            self._set_today()


class CalendarPopup(tk.Toplevel):
    """
    A popup calendar for month/day selection.
    """

    DAYS   = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    MONTHS = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]

    def __init__(self, parent, current_date, callback):
        super().__init__(parent)
        self.callback     = callback
        self.viewing_year  = current_date.year
        self.viewing_month = current_date.month
        self.selected_day  = current_date.day

        self.title("Pick a Date")
        self.resizable(False, False)
        self.grab_set()
        self.focus()
        self._build()
        self._render_days()

    def _build(self):
        self.configure(bg="white", padx=8, pady=8)

        # Month/year navigation
        nav = tk.Frame(self, bg="white")
        nav.pack(fill=tk.X, pady=(0, 5))

        tk.Button(nav, text="◀", command=self._prev_month,
                  relief=tk.FLAT, bg="white", font=("Arial", 12)).pack(side=tk.LEFT)
        self.month_label = tk.Label(nav, text="", font=("Arial", 11, "bold"),
                                    bg="white", width=18, anchor="center")
        self.month_label.pack(side=tk.LEFT, expand=True)
        tk.Button(nav, text="▶", command=self._next_month,
                  relief=tk.FLAT, bg="white", font=("Arial", 12)).pack(side=tk.RIGHT)

        # Day headers
        hdr = tk.Frame(self, bg="white")
        hdr.pack()
        for day in self.DAYS:
            color = "#e74c3c" if day in ("Sa", "Su") else "#2E75B6"
            tk.Label(hdr, text=day, width=4, font=("Arial", 9, "bold"),
                     fg=color, bg="white").pack(side=tk.LEFT)

        # Day grid container
        self.grid_frame = tk.Frame(self, bg="white")
        self.grid_frame.pack()

    def _render_days(self):
        # Clear old buttons
        for w in self.grid_frame.winfo_children():
            w.destroy()

        self.month_label.config(
            text=f"{self.MONTHS[self.viewing_month - 1]}  {self.viewing_year}"
        )

        # Get calendar matrix
        cal = calendar.monthcalendar(self.viewing_year, self.viewing_month)
        today = date.today()

        for week in cal:
            row_frame = tk.Frame(self.grid_frame, bg="white")
            row_frame.pack()
            for day in week:
                if day == 0:
                    tk.Label(row_frame, text="", width=4, bg="white").pack(side=tk.LEFT)
                else:
                    is_today    = (day == today.day and
                                   self.viewing_month == today.month and
                                   self.viewing_year  == today.year)
                    is_selected = (day == self.selected_day and
                                   self.viewing_month == self.selected_day and
                                   self.viewing_year  == self.viewing_year)

                    if is_today:
                        bg, fg = "#2E75B6", "white"
                    else:
                        bg, fg = "white", "black"

                    btn = tk.Button(
                        row_frame, text=str(day), width=3,
                        bg=bg, fg=fg, relief=tk.FLAT,
                        font=("Arial", 9),
                        command=lambda d=day: self._pick(d),
                        activebackground="#cce4f7"
                    )
                    btn.pack(side=tk.LEFT, padx=1, pady=1)

    def _prev_month(self):
        if self.viewing_month == 1:
            self.viewing_month = 12
            self.viewing_year -= 1
        else:
            self.viewing_month -= 1
        self._render_days()

    def _next_month(self):
        if self.viewing_month == 12:
            self.viewing_month = 1
            self.viewing_year += 1
        else:
            self.viewing_month += 1
        self._render_days()

    def _pick(self, day):
        selected = date(self.viewing_year, self.viewing_month, day)
        self.callback(selected)
        self.destroy()
