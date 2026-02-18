import mysql.connector

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def connect():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # your MySQL username
        password="root",   # your MySQL password
        database="vehicle_rental_db"
    )
    return conn

# -----------------------------
# TABLE CREATION
# -----------------------------
def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                        vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100),
                        type VARCHAR(50),
                        rent_per_day FLOAT,
                        available BOOLEAN DEFAULT TRUE
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS rentals (
                        rental_id INT AUTO_INCREMENT PRIMARY KEY,
                        vehicle_id INT,
                        customer_name VARCHAR(100),
                        days INT,
                        total_cost FLOAT,
                        status VARCHAR(20),
                        FOREIGN KEY(vehicle_id) REFERENCES vehicles(vehicle_id)
                    )''')

    conn.commit()
    conn.close()

# -----------------------------
# CRUD OPERATIONS
# -----------------------------
def add_vehicle(name, type_, rent_per_day):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vehicles (name, type, rent_per_day) VALUES (%s, %s, %s)",
                   (name, type_, rent_per_day))
    conn.commit()
    conn.close()

def get_available_vehicles():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles WHERE available=TRUE")
    rows = cursor.fetchall()
    conn.close()
    return rows

def rent_vehicle(vehicle_id, customer_name, days):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT rent_per_day, available FROM vehicles WHERE vehicle_id=%s", (vehicle_id,))
    data = cursor.fetchone()

    if not data:
        conn.close()
        return "Vehicle not found."
    rent_per_day, available = data
    if not available:
        conn.close()
        return "Vehicle already rented."

    total_cost = rent_per_day * days
    cursor.execute("INSERT INTO rentals (vehicle_id, customer_name, days, total_cost, status) VALUES (%s, %s, %s, %s, %s)",
                   (vehicle_id, customer_name, days, total_cost, "Rented"))
    cursor.execute("UPDATE vehicles SET available=FALSE WHERE vehicle_id=%s", (vehicle_id,))
    conn.commit()
    conn.close()
    return f"Vehicle rented successfully for ₹{total_cost}"

def return_vehicle(vehicle_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT rental_id FROM rentals WHERE vehicle_id=%s AND status='Rented'", (vehicle_id,))
    data = cursor.fetchone()
    if not data:
        conn.close()
        return "Vehicle is not currently rented."

    rental_id = data[0]
    cursor.execute("UPDATE rentals SET status='Returned' WHERE rental_id=%s", (rental_id,))
    cursor.execute("UPDATE vehicles SET available=TRUE WHERE vehicle_id=%s", (vehicle_id,))
    conn.commit()
    conn.close()
    return "Vehicle returned successfully."

def get_rental_history():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''SELECT rentals.rental_id, vehicles.name, customer_name, days, total_cost, status
                      FROM rentals JOIN vehicles ON rentals.vehicle_id = vehicles.vehicle_id''')
    rows = cursor.fetchall()
    conn.close()
    return rows

# -----------------------------
# DASHBOARD FUNCTIONS
# -----------------------------
def get_total_vehicle_count():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_rented_vehicle_count():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vehicles WHERE available=0")
    rented = cursor.fetchone()[0]
    conn.close()
    return rented
