import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database import DatabaseManager
    from home import HomePage
    from booking import BookingPage
    from reservations import ReservationsPage
    from edit_reservation import EditReservationPage
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all required files are in the same directory.")
    input("Press Enter to exit...")
    sys.exit(1)


class FlightReservationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flight Reservation System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Initialize database
        self.db = DatabaseManager()

        # Configure style
        self.setup_style()

        # Container for different pages
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold different pages
        self.frames = {}

        # Initialize all pages
        self.init_pages()

        # Show home page first
        self.show_frame("HomePage")

    def setup_style(self):
        """Setup the application style"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))

    def init_pages(self):
        """Initialize all application pages"""
        for PageClass in (HomePage, BookingPage, ReservationsPage, EditReservationPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self, db=self.db)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Show a specific frame"""
        frame = self.frames[page_name]
        frame.tkraise()

        # Refresh data if it's reservations page
        if page_name == "ReservationsPage":
            frame.refresh_data()

    def show_edit_page(self, reservation_id):
        """Show edit page with specific reservation data"""
        edit_frame = self.frames["EditReservationPage"]
        edit_frame.load_reservation(reservation_id)
        edit_frame.tkraise()

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main function to run the application"""
    try:
        app = FlightReservationApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()