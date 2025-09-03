import tkinter as tk
from tkinter import ttk, messagebox


class ReservationsPage(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        """Setup the reservations page UI"""
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill='both')

        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))

        # Title
        title_label = ttk.Label(header_frame, text="All Reservations",
                                style='Title.TLabel')
        title_label.pack(side='left')

        # Buttons in header
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.pack(side='right')

        refresh_btn = ttk.Button(buttons_frame, text="🔄 Refresh",
                                 command=self.refresh_data)
        refresh_btn.pack(side='left', padx=(0, 10))

        back_btn = ttk.Button(buttons_frame, text="← Back to Home",
                              command=lambda: self.controller.show_frame("HomePage"))
        back_btn.pack(side='left')

        # Table frame
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill='both', expand=True)

        # Create treeview
        columns = ('ID', 'Name', 'Flight', 'Departure', 'Destination', 'Date', 'Seat')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        # Define headings and column widths
        column_widths = {'ID': 60, 'Name': 150, 'Flight': 100, 'Departure': 120,
                         'Destination': 120, 'Date': 100, 'Seat': 80}

        for col in columns:
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, width=column_widths[col], anchor='center')

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        # Configure grid weights
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Action buttons frame
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill='x', pady=20)

        # Action buttons
        edit_btn = ttk.Button(action_frame, text="✏️ Edit Selected",
                              command=self.edit_selected,
                              style='Action.TButton')
        edit_btn.pack(side='left', padx=(0, 10))

        delete_btn = ttk.Button(action_frame, text="🗑️ Delete Selected",
                                command=self.delete_selected)
        delete_btn.pack(side='left', padx=(0, 10))

        book_new_btn = ttk.Button(action_frame, text="➕ Book New Flight",
                                  command=lambda: self.controller.show_frame("BookingPage"))
        book_new_btn.pack(side='right')

        # Info label
        self.info_label = ttk.Label(main_frame, text="", font=('Arial', 10))
        self.info_label.pack(pady=10)

        # Double-click binding for edit
        self.tree.bind('<Double-1>', lambda e: self.edit_selected())

        # Load initial data
        self.refresh_data()

    def refresh_data(self):
        """Refresh the reservations data"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Load data from database
            reservations = self.db.get_all_reservations()

            if reservations:
                for reservation in reservations:
                    self.tree.insert('', 'end', values=reservation)
                self.info_label.config(text=f"Total reservations: {len(reservations)}")
            else:
                self.info_label.config(text="No reservations found. Click 'Book New Flight' to add one.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reservations: {str(e)}")
            self.info_label.config(text="Error loading data")

    def get_selected_reservation(self):
        """Get the selected reservation"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a reservation first!")
            return None

        item = self.tree.item(selection[0])
        return item['values']

    def edit_selected(self):
        """Edit the selected reservation"""
        reservation = self.get_selected_reservation()
        if reservation:
            reservation_id = reservation[0]
            self.controller.show_edit_page(reservation_id)

    def delete_selected(self):
        """Delete the selected reservation"""
        reservation = self.get_selected_reservation()
        if not reservation:
            return

        # Confirm deletion
        result = messagebox.askyesnocancel(
            "Confirm Delete",
            f"Are you sure you want to delete this reservation?\n\n"
            f"Passenger: {reservation[1]}\n"
            f"Flight: {reservation[2]}\n"
            f"Date: {reservation[5]}"
        )

        if result:
            try:
                reservation_id = reservation[0]
                self.db.delete_reservation(reservation_id)
                messagebox.showinfo("Success", "Reservation deleted successfully!")
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete reservation: {str(e)}")