from tkinter import *
from tkinter import messagebox, ttk
import backend

# Initialize backend
backend.create_tables()

# ---------------------------
# Window setup
# ---------------------------
root = Tk()
root.title("🚗 Vehicle Rental Management System")
root.geometry("1280x720")  # 16:9 ratio
root.configure(bg="#e8f0f2")
root.resizable(False, False)

# Fonts
TITLE_FONT = ("Helvetica", 20, "bold")
SUB_FONT = ("Helvetica", 14, "bold")
TEXT_FONT = ("Helvetica", 12)

# ---------------------------
# Backend functions
# ---------------------------
def add_vehicle():
    name = name_entry.get()
    type_ = type_entry.get()
    rent = rent_entry.get()
    if name and type_ and rent:
        try:
            backend.add_vehicle(name, type_, float(rent))
            messagebox.showinfo("Success", "Vehicle added successfully!")
            name_entry.delete(0, END)
            type_entry.delete(0, END)
            rent_entry.delete(0, END)
            update_dashboard()
            view_available()
        except ValueError:
            messagebox.showwarning("Error", "Please enter a valid number for rent.")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

def view_available():
    vehicles = backend.get_available_vehicles()
    listbox.delete(0, END)
    for v in vehicles:
        listbox.insert(END, f"ID:{v[0]} | {v[1]} | {v[2]} | ₹{v[3]}")

def rent_vehicle():
    vehicle_id = rent_id_entry.get()
    customer = customer_entry.get()
    days = days_entry.get()
    if not (vehicle_id and customer and days):
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return
    msg = backend.rent_vehicle(int(vehicle_id), customer, int(days))
    messagebox.showinfo("Info", msg)
    update_dashboard()
    view_available()

def return_vehicle():
    vehicle_id = return_id_entry.get()
    if not vehicle_id:
        messagebox.showwarning("Input Error", "Please enter vehicle ID.")
        return
    msg = backend.return_vehicle(int(vehicle_id))
    messagebox.showinfo("Info", msg)
    update_dashboard()
    view_available()

def view_rentals():
    rentals = backend.get_rental_history()
    listbox.delete(0, END)
    for r in rentals:
        listbox.insert(END, f"ID:{r[0]} | {r[1]} | {r[2]} | {r[3]} days | ₹{r[4]} | {r[5]}")

# ---------------------------
# Dashboard
# ---------------------------
header = Frame(root, bg="#1f3b4d", height=80)
header.pack(fill=X)
Label(header, text="🚗 Vehicle Rental Management System", font=TITLE_FONT, bg="#1f3b4d", fg="white").pack(pady=15)

dashboard = Frame(root, bg="#d7ebf4", height=80)
dashboard.pack(fill=X, pady=5)

Label(dashboard, text="📊 Dashboard Summary", font=SUB_FONT, bg="#d7ebf4", fg="#1f3b4d").pack(pady=5)

summary_frame = Frame(dashboard, bg="#d7ebf4")
summary_frame.pack()

total_lbl = Label(summary_frame, text="Total Vehicles: 0", font=TEXT_FONT, bg="#d7ebf4")
total_lbl.grid(row=0, column=0, padx=60)

rented_lbl = Label(summary_frame, text="Rented: 0", font=TEXT_FONT, bg="#d7ebf4")
rented_lbl.grid(row=0, column=1, padx=60)

available_lbl = Label(summary_frame, text="Available: 0", font=TEXT_FONT, bg="#d7ebf4")
available_lbl.grid(row=0, column=2, padx=60)

def update_dashboard():
    total = backend.get_total_vehicle_count()
    rented = backend.get_rented_vehicle_count()
    available = total - rented
    total_lbl.config(text=f"Total Vehicles: {total}")
    rented_lbl.config(text=f"Rented: {rented}")
    available_lbl.config(text=f"Available: {available}")

# ---------------------------
# Main content area
# ---------------------------
content_frame = Frame(root, bg="#e8f0f2")
content_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

# Left side: Add Vehicle
add_frame = LabelFrame(content_frame, text="➕ Add Vehicle", font=SUB_FONT, bg="#ffffff", padx=20, pady=15, fg="#1f3b4d", bd=2)
add_frame.grid(row=0, column=0, padx=10, pady=5, sticky="n")

Label(add_frame, text="Name:", font=TEXT_FONT, bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
name_entry = Entry(add_frame, font=TEXT_FONT, width=20)
name_entry.grid(row=0, column=1, padx=5, pady=5)

Label(add_frame, text="Type:", font=TEXT_FONT, bg="#ffffff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
type_entry = Entry(add_frame, font=TEXT_FONT, width=20)
type_entry.grid(row=1, column=1, padx=5, pady=5)

Label(add_frame, text="Rent/Day (₹):", font=TEXT_FONT, bg="#ffffff").grid(row=2, column=0, sticky="w", padx=5, pady=5)
rent_entry = Entry(add_frame, font=TEXT_FONT, width=20)
rent_entry.grid(row=2, column=1, padx=5, pady=5)

Button(add_frame, text="Add Vehicle", font=TEXT_FONT, bg="#1f3b4d", fg="white", width=18, command=add_vehicle).grid(row=3, column=0, columnspan=2, pady=10)

# Middle: Rent Vehicle
rent_frame = LabelFrame(content_frame, text="🏁 Rent Vehicle", font=SUB_FONT, bg="#ffffff", padx=20, pady=15, fg="#1f3b4d", bd=2)
rent_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")

Label(rent_frame, text="Vehicle ID:", font=TEXT_FONT, bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
rent_id_entry = Entry(rent_frame, font=TEXT_FONT, width=20)
rent_id_entry.grid(row=0, column=1, padx=5, pady=5)

Label(rent_frame, text="Customer Name:", font=TEXT_FONT, bg="#ffffff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
customer_entry = Entry(rent_frame, font=TEXT_FONT, width=20)
customer_entry.grid(row=1, column=1, padx=5, pady=5)

Label(rent_frame, text="Days:", font=TEXT_FONT, bg="#ffffff").grid(row=2, column=0, sticky="w", padx=5, pady=5)
days_entry = Entry(rent_frame, font=TEXT_FONT, width=20)
days_entry.grid(row=2, column=1, padx=5, pady=5)

Button(rent_frame, text="Rent Vehicle", font=TEXT_FONT, bg="#1f3b4d", fg="white", width=18, command=rent_vehicle).grid(row=3, column=0, columnspan=2, pady=10)

# Right: Return Vehicle
return_frame = LabelFrame(content_frame, text="🔁 Return Vehicle", font=SUB_FONT, bg="#ffffff", padx=20, pady=15, fg="#1f3b4d", bd=2)
return_frame.grid(row=0, column=2, padx=10, pady=5, sticky="n")

Label(return_frame, text="Vehicle ID:", font=TEXT_FONT, bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
return_id_entry = Entry(return_frame, font=TEXT_FONT, width=20)
return_id_entry.grid(row=0, column=1, padx=5, pady=5)

Button(return_frame, text="Return Vehicle", font=TEXT_FONT, bg="#1f3b4d", fg="white", width=18, command=return_vehicle).grid(row=1, column=0, columnspan=2, pady=10)

# Bottom: Display Section
display_frame = LabelFrame(root, text="📋 Available Vehicles / Rental History", font=SUB_FONT, bg="#ffffff", padx=20, pady=15, fg="#1f3b4d", bd=2)
display_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

btn_frame = Frame(display_frame, bg="#ffffff")
btn_frame.pack(pady=5)
Button(btn_frame, text="View Available Vehicles", font=TEXT_FONT, bg="#228B22", fg="white", width=25, command=view_available).grid(row=0, column=0, padx=10)
Button(btn_frame, text="View Rental History", font=TEXT_FONT, bg="#1E90FF", fg="white", width=25, command=view_rentals).grid(row=0, column=1, padx=10)

listbox = Listbox(display_frame, font=("Courier New", 12), width=150, height=10, bg="#f7f7f7", selectmode=SINGLE)
listbox.pack(pady=10)

# ---------------------------
# Initialize data
# ---------------------------
update_dashboard()
view_available()

root.mainloop()
