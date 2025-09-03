import tkinter as tk
from tkinter import ttk, messagebox


class BookingPage(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        """Setup the booking page UI"""
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill='both')

        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))

        # Title
        title_label = ttk.Label(header_frame, text="Book New Flight",
                                style='Title.TLabel')
        title_label.pack(side='left')

        # Back button
        back_btn = ttk.Button(header_frame, text="← Back to Home",
                              command=lambda: self.controller.show_frame("HomePage"))
        back_btn.pack(side='right')

        # Form frame
        form_frame = ttk.LabelFrame(main_frame, text="Flight Information", padding="20")
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
            entry.insert(0, '')  # Clear any placeholder

            # Placeholder hint
            hint_label = ttk.Label(form_frame, text=f"({placeholder})",
                                   font=('Arial', 9), foreground='gray')
            hint_label.grid(row=i, column=2, sticky='w', pady=5, padx=(10, 0))

            self.entries[field] = entry

        # Configure column weights
        form_frame.columnconfigure(1, weight=1)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=20)

        # Book button
        book_btn = ttk.Button(buttons_frame, text="✈️ Book Flight",
                              command=self.book_flight,
                              style='Action.TButton')
        book_btn.pack(side='left', padx=(0, 10))

        # Clear button
        clear_btn = ttk.Button(buttons_frame, text="🗑️ Clear Form",
                               command=self.clear_form)
        clear_btn.pack(side='left')

    def book_flight(self):
        """Book a new flight reservation"""
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

            # Save to database
            self.db.create_reservation(
                values['Name'],
                values['Flight Number'],
                values['Departure'],
                values['Destination'],
                values['Date'],
                values['Seat Number']
            )

            messagebox.showinfo("Success", "Flight booked successfully!")
            self.clear_form()

            # Ask if user wants to view reservations
            if messagebox.askyesno("Success", "Would you like to view all reservations?"):
                self.controller.show_frame("ReservationsPage")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to book flight: {str(e)}")

    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)