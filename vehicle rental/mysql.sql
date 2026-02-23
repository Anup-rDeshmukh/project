--This database will be connected to the fronted by using mysqlconnector
CREATE DATABASE IF NOT EXISTS vehicle_rental_db;
USE vehicle_rental_db;

-- --------------------------------------------------
-- Table: vehicles
-- --------------------------------------------------
CREATE TABLE vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    rent_per_day FLOAT NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

-- --------------------------------------------------
-- Table: rentals
-- --------------------------------------------------
CREATE TABLE rentals (
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    days INT NOT NULL,
    total_cost FLOAT NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);

select* from vehicles;
select* from rentals;
