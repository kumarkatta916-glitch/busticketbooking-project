
CREATE DATABASE busbooking;
USE busbooking;


1. users Table

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

2. bookings Table


CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    from_place VARCHAR(100) NOT NULL,
    to_place VARCHAR(100) NOT NULL,
    journey_date DATE NOT NULL,
    bus_type VARCHAR(50) NOT NULL,
    travels_name VARCHAR(100) NOT NULL,
    ticket_count INT NOT NULL,
    base_price DECIMAL(10,2),
    gst DECIMAL(10,2),
    state_tax DECIMAL(10,2),
    toll_fee DECIMAL(10,2),
    total_price DECIMAL(10,2),
    payment_status VARCHAR(20) DEFAULT 'SUCCESS',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

3. passengers Table

CREATE TABLE passengers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id VARCHAR(50) NOT NULL,
    passenger_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    seat_number VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
