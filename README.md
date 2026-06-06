# 3-Tier Bus Ticket Booking Application

## Project Overview

This project is a cloud-native 3-tier Bus Ticket Booking Application developed using:

- HTML
- CSS
- JavaScript
- Python Flask
- REST APIs
- Docker
- Kubernetes
- MySQL
- Azure Cloud

---

# Architecture

Frontend Layer
↓
Backend Layer
↓
Database Layer

---

# Frontend Layer

Technologies Used:
- HTML
- CSS
- JavaScript
- Nginx

Frontend Pages:
- register.html
- otp.html
- login.html
- booking.html
- journey.html
- price.html
- payment.html
- ticket.html

Features:
- User Registration
- OTP Verification
- Login
- Multi Passenger Booking
- Seat Selection
- Payment Page
- Ticket Generation

---

# Backend Layer

Technologies Used:
- Python Flask
- Flask REST APIs

APIs Created:
- /send-otp
- /register
- /login
- /book
- /view-bookings

Features:
- Email OTP Generation
- User Authentication
- Ticket Booking
- Ticket Confirmation Email

---

# Database Layer

Database Used:
- MySQL

Database Name:
- busbooking

Tables Created:
- users
- bookings

Users Table Stores:
- Full Name
- Username
- Email
- Phone
- Country
- State
- Password

Bookings Table Stores:
- Booking ID
- Passenger Name
- Age
- Gender
- Seat Number
- From Place
- To Place
- Journey Date
- Payment Status

---

# Docker

Frontend and backend applications were containerized using Docker.

Docker Images:
- bus-frontend
- bus-backend

---

# Kubernetes

Kubernetes YAML files used:
- frontend-deployment.yaml
- frontend-service.yaml
- backend-deployment.yaml
- backend-service.yaml

---

# GitHub Repository

Project Source Code:
- frontend
- backend
- kubernetes

---

# Features

- OTP Verification
- Multi Passenger Booking
- Dynamic Seat Selection
- REST APIs
- Docker Deployment
- Kubernetes Deployment
- Ticket Email Generation


# Setup Secrets

Before deploying the application, create your own Kubernetes secret.

```bash
kubectl apply -f kubernetes/secret.yaml
```

Create `secret.yaml` using `secret-example.yaml` as a reference and replace the placeholder values with your own credentials.

Required values:

* DB_USER
* DB_PASSWORD
* EMAIL_USER
* EMAIL_PASSWORD

```
```


---

# Author

Kiran Kumar
