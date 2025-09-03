import tkinter as tk
from tkinter import ttk


class HomePage(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        """Setup the home page UI"""
        # Main container
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(expand=True, fill='both')

        # Title
        title_label = ttk.Label(main_frame, text="Flight Reservation System",
                                style='Title.TLabel')
        title_label.pack(pady=(0, 30))

        # Subtitle
        subtitle_label = ttk.Label(main_frame,
                                   text="Welcome to the Flight Reservation Management System",
                                   font=('Arial', 12))
        subtitle_label.pack(pady=(0, 40))

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(expand=True)

        # Book Flight button
        book_btn = ttk.Button(buttons_frame,
                              text="📅 Book Flight",
                              command=lambda: self.controller.show_frame("BookingPage"),
                              style='Action.TButton',
                              width=20)
        book_btn.pack(pady=10)

        # View Reservations button
        view_btn = ttk.Button(buttons_frame,
                              text="📋 View Reservations",
                              command=lambda: self.controller.show_frame("ReservationsPage"),
                              style='Action.TButton',
                              width=20)
        view_btn.pack(pady=10)

        # Exit button
        exit_btn = ttk.Button(buttons_frame,
                              text="❌ Exit",
                              command=self.controller.root.quit,
                              width=20)
        exit_btn.pack(pady=(20, 0))

        # Footer
        footer_label = ttk.Label(main_frame,
                                 text="© 2024 Flight Reservation System",
                                 font=('Arial', 10),
                                 foreground='gray')
        footer_label.pack(side='bottom', pady=20)