import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="vehicle_rental_db"
    )
    print(" MySQL connection successful!")
    conn.close()
except mysql.connector.Error as e:
    print(" MySQL Error:", e)
