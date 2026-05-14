# Kawasi Hostels Booking System

A full-stack web application for student hostel booking, built to streamline the accommodation process for university students in Kenya. Students can register, browse available rooms, make payments via M-Pesa, and receive SMS confirmations without visiting the hostel in person.

## Overview

Kawasi was developed as a practical solution to the manual and time-consuming hostel booking processes common at Kenyan universities. The system handles the complete booking workflow from registration through to payment confirmation.

## Features

**Student Portal**
- User registration and login with session management
- Personal profile and booking details capture (name, university, room preferences, contact information)
- Room browsing with property listings and detail views
- M-Pesa STK Push payment integration — payment prompt sent directly to the student's phone
- SMS confirmation sent to the student's phone number on successful registration

**Admin Portal**
- Property and room management (add, edit, remove listings)
- Review and feedback management

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML, Bootstrap 5
- **Payment:** M-Pesa Daraja API (STK Push, sandbox)
- **Notifications:** SMS API

## Project Structure

```
KAWASI_BOOKING_SYSTEM/
├── app.py          # Flask application and all routes
├── sms.py          # SMS notification helper
├── nav.html        # Navigation template
├── static/         # Bootstrap CSS and static assets
└── templates/      # HTML templates (login, register, booknow, houses, reviews, etc.)
```

## Setup

**Prerequisites:** Python 3.8+, MySQL

```bash
git clone https://github.com/melissaangwenyi/KAWASI_BOOKING_SYSTEM.git
cd KAWASI_BOOKING_SYSTEM
pip install flask pymysql requests
```

Create a MySQL database named `project` and set up the required tables (register, booknow, housedetails, reviews).

Configure your credentials in `app.py`:
```python
# Database
connection = pymysql.connect(host="localhost", user="root", password="your_password", database="project")

# M-Pesa (replace with your Daraja API credentials)
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
```

Run the application:
```bash
python app.py
```

Visit `http://localhost:5000`

## Author

Melissa Angwenyi — melissaangwenyi276@gmail.com
