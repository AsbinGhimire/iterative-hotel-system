# Hotel Information Management System (IMS)

A modern, visually stunning, and feature-rich Hotel Management System built with Django and Bootstrap 5. It is designed to empower hotel owners and staff with the tools they need to manage their property in a digital-first world while maintaining an incredibly premium and intuitive user experience.

---

## ✨ Features

- **Premium UI/UX:** Completely responsive, aesthetically pleasing frontend using modern CSS techniques, glassmorphism, and Lucide icons.
- **Robust Hotel & Room Management:** Manage multiple hotels, track room availability, define pricing, and add detailed descriptions.
- **Advanced Booking System:** Easily create and manage guest bookings with conflict prevention for overlapping dates.
- **Dynamic Billing & Invoices:** Automatically calculates stay duration and total cost, featuring a beautifully crafted, printable invoice complete with native PDF export support.
- **Interactive Information Pages:** High-end **About Us** and **Contact Us** pages equipped with interactive maps, forms, and value propositions.
- **Role-Based Access Control:** Distinct views and privileges for Staff vs. Guests.

---

## 🛠️ Technology Stack

- **Backend:** Python, Django 3.0.5+ (Compatible up to Django 5.x)
- **Frontend:** HTML5, CSS3, Bootstrap 5.3, Vanilla JavaScript
- **Icons:** Lucide Icons
- **Database:** SQLite (default, production ready for PostgreSQL/MySQL)

---

## 🚀 Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites
- Python 3.9+ installed on your system.
- Git for version control.

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AsbinGhimire/iterative-hotel-system.git
   cd iterative-hotel-system/HotelManagementSystem
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (Admin account):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 📸 Core Flows
- **Guest / Customer Flow:** Register an account -> Browse Hotels -> Book a Room -> Receive digital invoice.
- **Manager / Admin Flow:** Login -> Add/Edit Hotel Details -> Manage Rooms -> Monitor Bookings -> Update checkout status.

---

## 🔮 Future Enhancements
- Integration with live payment gateways (Stripe, PayPal).
- Advanced revenue analytics dashboard for Hotel Managers.
- Guest reviews and ratings per hotel/room.

---

## 📄 License
This iterative project is provided under the MIT License. Feel free to fork, modify, and use it for your own hospitality needs!

*Developed with passion for the hospitality industry by Asbin Ghimire (Nirmit).*
