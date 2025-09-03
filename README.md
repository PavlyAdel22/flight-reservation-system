Flight Reservation System

A simple desktop application for managing flight reservations built with Python, Tkinter, and SQLite.

Features



Book Flight: Add new flight reservations

View Reservations: Display all reservations in a table format

Edit Reservations: Update existing reservation details

Delete Reservations: Remove reservations from the system

User-friendly GUI: Clean and intuitive interface

Local Database: SQLite database for data persistence



Screenshots

The application includes:



Home page with navigation options

Flight booking form with validation

Reservations list with search and filter options

Edit/Delete functionality



Requirements



Python 3.6 or higher

tkinter (included with Python)

sqlite3 (included with Python)



Installation \& Setup



Clone or Download this repository

Navigate to the project directory

Install dependencies (optional, for creating .exe):

bashpip install -r requirements.txt





How to Run

Method 1: Run from Source

bashpython main.py

Method 2: Run Executable (if available)



Double-click on main.exe in the dist/ folder



Project Structure

flight\_reservation\_app/

├── main.py                 # Main application entry point

├── database.py             # SQLite database management

├── home.py                 # Home page UI

├── booking.py              # Flight booking form

├── reservations.py         # View all reservations

├── edit\_reservation.py     # Edit/Delete functionality

├── flights.db              # SQLite database file (auto-created)

├── requirements.txt        # Python dependencies

├── README.md               # This file

└── dist/                   # Executable files (if created)

    └── main.exe

Usage Instructions

Booking a Flight



Click "Book Flight" on the home page

Fill in all required fields:



Passenger Name

Flight Number (e.g., AA1234)

Departure City

Destination City

Date (YYYY-MM-DD format)

Seat Number (e.g., 12A)





Click "Book Flight" to save



Viewing Reservations



Click "View Reservations" on the home page

All reservations will be displayed in a table

Use "Refresh" to reload data



Editing Reservations



In the reservations page, select a reservation

Click "Edit Selected" or double-click the row

Modify the desired fields

Click "Update Reservation" to save changes



Deleting Reservations



In the reservations page, select a reservation

Click "Delete Selected"

Confirm the deletion in the dialog box



Database Schema

The application uses SQLite with the following table structure:

sqlCREATE TABLE reservations (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    flight\_number TEXT NOT NULL,

    departure TEXT NOT NULL,

    destination TEXT NOT NULL,

    date TEXT NOT NULL,

    seat\_number TEXT NOT NULL

);

Creating Executable File

To create a standalone .exe file:

bash# Install PyInstaller

pip install pyinstaller



\# Create executable

pyinstaller --onefile --windowed main.py



\# The .exe file will be in the dist/ folder

Troubleshooting

Common Issues



"No module named 'database'"



Make sure all Python files are in the same directory

Run from the project root directory





Database errors



The SQLite database file will be created automatically

Make sure you have write permissions in the project directory





GUI not displaying properly



Ensure you have tkinter installed (comes with Python)

Try running with Python 3.6+







Error Reporting

If you encounter any issues, please check:



Python version (3.6+)

All files are in the correct directory

No syntax errors in the Python files



Development

Adding New Features



Database operations are handled in database.py

UI components are separated into individual files

Follow the existing naming convention



Code Structure



Each page is a separate class inheriting from tk.Frame

Database manager handles all SQLite operations

Main application manages page navigation



License

This project is for educational purposes. Feel free to modify and use as needed.

Contact

For questions or support, please refer to the project documentation or create an issue in the repository.



Built with Python 3.x, Tkinter, and SQLite

