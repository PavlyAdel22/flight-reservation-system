import tkinter as tk
from tkinter import ttk, messagebox


class EditReservationPage(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.current_reservation_id = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the edit reservation page UI"""
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill='both')

        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))

        # Title
        self.title_label = ttk.Label(header_frame, text="Edit Reservation",
                                     style='Title.TLabel')
        self.title_label.pack(side='left')

        # Back button
        back_btn = ttk.Button(header_frame, text="← Back to Reservations",
                              command=lambda: self.controller.show_frame("ReservationsPage"))
        back_btn.pack(side='right')

        # Form frame
        form_frame = ttk.LabelFrame(main_frame, text="Reservation Details", padding="20")
        form_frame.pack(fill='both', expand=True)

        # Create entry fields
        self.entries = {}
        fields = [
            ('Name', 'Passenger full name'),
            ('Flight Number', 'e.g., AA1234'),
            ('Departure', 'Departure city'),
            ('Destination', 'Destination city'),
            ('Date', 'YYYY-MM-DD format'),
            ('Seat Number', 'e.g., 12A')
        ]

        for i, (field, placeholder) in enumerate(fields):
            # Label
            label = ttk.Label(form_frame, text=f"{field}:")
            label.grid(row=i, column=0, sticky='w', pady=5, padx=(0, 10))

            # Entry
            entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
            entry.grid(row=i, column=1, sticky='ew', pady=5)

            # Placeholder hint
            hint_label = ttk.Label(form_frame, text=f"({placeholder})",
                                   font=('Arial', 9), foreground='gray')
            hint_label.grid(row=i, column=2, sticky='w', pady=5, padx=(10, 0))

            self.entries[field] = entry

        # Configure column weights
        form_frame.columnconfigure(1, weight=1)

        # Info frame
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='x', pady=10)

        self.info_label = ttk.Label(info_frame, text="", font=('Arial', 10),
                                    foreground='blue')
        self.info_label.pack()

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=20)

        # Update button
        update_btn = ttk.Button(buttons_frame, text="💾 Update Reservation",
                                command=self.update_reservation,
                                style='Action.TButton')
        update_btn.pack(side='left', padx=(0, 10))

        # Delete button
        delete_btn = ttk.Button(buttons_frame, text="🗑️ Delete Reservation",
                                command=self.delete_reservation)
        delete_btn.pack(side='left', padx=(0, 10))

        # Cancel button
        cancel_btn = ttk.Button(buttons_frame, text="❌ Cancel",
                                command=lambda: self.controller.show_frame("ReservationsPage"))
        cancel_btn.pack(side='right')

    def load_reservation(self, reservation_id):
        """Load reservation data into the form"""
        try:
            self.current_reservation_id = reservation_id
            reservation = self.db.get_reservation_by_id(reservation_id)

            if reservation:
                # Clear existing data
                self.clear_form()

                # Load data into fields (skip ID field)
                field_names = ['Name', 'Flight Number', 'Departure', 'Destination', 'Date', 'Seat Number']
                for i, field_name in enumerate(field_names):
                    self.entries[field_name].insert(0, reservation[i + 1])  # Skip ID (index 0)

                self.info_label.config(text=f"Editing Reservation ID: {reservation_id}")
                self.title_label.config(text=f"Edit Reservation #{reservation_id}")
            else:
                messagebox.showerror("Error", "Reservation not found!")
                self.controller.show_frame("ReservationsPage")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reservation: {str(e)}")
            self.controller.show_frame("ReservationsPage")

    def update_reservation(self):
        """Update the reservation"""
        if not self.current_reservation_id:
            messagebox.showerror("Error", "No reservation selected!")
            return

        try:
            # Get values from entries
            values = {}
            for field, entry in self.entries.items():
                value = entry.get().strip()
                if not value:
                    messagebox.showerror("Error", f"Please fill the {field} field!")
                    entry.focus()
                    return
                values[field] = value

            # Update in database
            self.db.update_reservation(
                self.current_reservation_id,
                values['Name'],
                values['Flight Number'],
                values['Departure'],
                values['Destination'],
                values['Date'],
                values['Seat Number']
            )

            messagebox.showinfo("Success", "Reservation updated successfully!")
            self.controller.show_frame("ReservationsPage")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update reservation: {str(e)}")

    def delete_reservation(self):
        """Delete the current reservation"""
        if not self.current_reservation_id:
            messagebox.showerror("Error", "No reservation selected!")
            return

        # Get passenger name for confirmation
        passenger_name = self.entries['Name'].get().strip()

        # Confirm deletion
        result = messagebox.askyesnocancel(
            "Confirm Delete",
            f"Are you sure you want to delete this reservation?\n\n"
            f"Passenger: {passenger_name}\n"
            f"Flight: {self.entries['Flight Number'].get()}\n"
            f"This action cannot be undone!"
        )

        if result:
            try:
                self.db.delete_reservation(self.current_reservation_id)
                messagebox.showinfo("Success", "Reservation deleted successfully!")
                self.controller.show_frame("ReservationsPage")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete reservation: {str(e)}")

    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.current_reservation_id = None
        self.info_label.config(text="")
        self.title_label.config(text="Edit Reservation")