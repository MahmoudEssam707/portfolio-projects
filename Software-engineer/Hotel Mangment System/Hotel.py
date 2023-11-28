import tkinter as tk
import sqlite3
from tkinter import filedialog


# Function to display information in the result box
def display_result(data):
    result_text.config(state="normal")
    result_text.delete(1.0, "end")
    for info in data:
        result_text.insert("end", str(info) + "\n")
    result_text.config(state="disabled")


# Function to display hotel information
def show_hotel_info():
    conn = sqlite3.connect(root.filename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Hotel")
    hotel_info = cursor.fetchall()
    display_result(hotel_info)


# Function to display event information
def show_event_info():
    conn = sqlite3.connect(root.filename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Event")
    event_info = cursor.fetchall()
    display_result(event_info)


# Function to display room information
def show_room_info():
    conn = sqlite3.connect(root.filename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Room")
    room_info = cursor.fetchall()
    display_result(room_info)


# Function to display customer information
def show_customer_info():
    conn = sqlite3.connect(root.filename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer")
    customer_info = cursor.fetchall()
    display_result(customer_info)


# Function to display worker information
def show_worker_info():
    conn = sqlite3.connect(root.filename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Worker")
    worker_info = cursor.fetchall()
    display_result(worker_info)


# Function to display manager information
def show_manager_info():
    conn = sqlite3.connect(root.filename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Manager")
    manager_info = cursor.fetchall()
    display_result(manager_info)


# Function to display event Working At Manager and workers
def show_Working_At():
    conn = sqlite3.connect(root.filename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Working_AT")
    Working_AT = cursor.fetchall()
    display_result(Working_AT)


# Function to choose the database file path
def choose_db_path():
    root.filename = filedialog.askopenfilename(
        title="Select Database File",
        filetypes=(("Database files", "*.db"), ("All files", "*.*")),
    )
    # Check if the user selected a file
    if root.filename:
        conn = sqlite3.connect(root.filename)
        cursor = conn.cursor()
        # Close the connection after getting the cursor
        conn.close()
    else:
        # Display an error message if no file selected
        tk.messagebox.showerror(
            "Error", "No database file selected. Please choose a file."
        )


root = tk.Tk()
root.title("Hotel Management System")

root.geometry("1000x500")  # Set initial window size

title_label = tk.Label(root, text="Hotel Management System", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# Buttons to view information
btn_show_hotel = tk.Button(
    button_frame, text="View Hotel Info", command=show_hotel_info
)
btn_show_hotel.grid(row=0, column=0, padx=10, pady=5)

btn_show_event = tk.Button(
    button_frame, text="View Event Info", command=show_event_info
)
btn_show_event.grid(row=0, column=1, padx=10, pady=5)

btn_show_room = tk.Button(button_frame, text="View Room Info", command=show_room_info)
btn_show_room.grid(row=0, column=2, padx=10, pady=5)

btn_show_customer = tk.Button(
    button_frame, text="View Customer Info", command=show_customer_info
)
btn_show_customer.grid(row=0, column=3, padx=10, pady=5)

btn_show_worker = tk.Button(
    button_frame, text="View Worker Info", command=show_worker_info
)
btn_show_worker.grid(row=0, column=4, padx=10, pady=5)

btn_show_manager = tk.Button(
    button_frame, text="View Manager Info", command=show_manager_info
)
btn_show_manager.grid(row=0, column=5, padx=10, pady=5)

btn_show_manager = tk.Button(
    button_frame, text="View Who Works Where", command=show_Working_At
)
btn_show_manager.grid(row=0, column=6, padx=10, pady=5)


result_frame = tk.LabelFrame(root, text="Query Results", font=("Arial", 14))
result_frame.pack(padx=20, pady=20)

result_text = tk.Text(result_frame, height=10, width=60, font=("Arial", 12))
result_text.pack(padx=10, pady=10)
result_text.config(state="disabled")

choose_button = tk.Button(root, text="Choose Database File", command=choose_db_path)
choose_button.pack(pady=10)

root.mainloop()
