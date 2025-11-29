# 🌐 Library Service API — Django REST Framework

A comprehensive RESTful API for a modern digital library platform, designed to manage book inventory, handle
user borrowings, process payments via Stripe, and provide real-time updates using Telegram notifications and Celery
asynchronous task management.


## 🚀 Features

The API provides a full suite of features ensuring data integrity, security, and a seamless
user experience across a core library and financial operations.

### 📚 Core Library Management

* ✅ **Book Management (CRUD)**: Full control over book inventory and details.
* ✅ **Inventory Control**: Automatic decrement/increment of book counts upon borrowing/return to maintain accurate stock levels.
* ✅ **Borrowing Lifecycle**: Dedicated endpoints for **creating** and **returning** books.

### 💰 Payments & Fines

* ✅ **Stripe Integration**: Secure payment processing for rental fees using the Stripe API.
* ✅ **Automated Checkout**: Creation of a Stripe checkout session and retrieval of the payment URL upon initiating a new borrowing.
* ✅ **Fine Calculation**: Dynamic assessment and creation of new **FINE** payments for overdue returns.
* ✅ **Payment Callback Handling**: Endpoints for handling successful and canceled Stripe sessions, updating payment status in the database.

### 🔔 Asynchronous Tasks & Notifications

* ✅ **Celery Task Queue**: Utilization of Celery with Redis as a message broker for handling background tasks asynchronously.
* ✅ **Telegram Notifications**: Real-time alerts sent to staff or users via a Telegram Bot upon significant events (e.g., new borrowing creation or fine payment).
* ✅ **Scheduled Tasks (Celery Beat)**: Management of periodic tasks, such as daily checks for overdue borrowings or sending reminders.

### ⚙️ System & Security

* ✅ **User Authentication**: Secure token-based authentication using JSON Web Token Authentication.
* ✅ **Data Validation**: Robust validation ensuring logical integrity (e.g., expected return date is in the future, inventory is non-negative).
* ✅ **API Documentation**: Comprehensive documentation generated via `drf-spectacular`.
* ✅ **Proper Permissions**: Users are restricted to managing their own borrowing and payment data.

## 🧱 Tech Stack

- **Framework**: Django + Django REST Framework
- **Database**: PostgreSQL (or SQLite for development)
- **Authentication**: Token-based (JSON Web Token Authentication)
- **Task Queue**: Celery + Redis
- **Payment Gateway**: Stripe
- **Notifications**: Telegram (via Telegram Bot API)
- **API Documentation**: drf-spectacular (OpenAPI 3.0)
- **Containerization**: Docker + Docker Compose

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/vmyronets/library-service-api.git
````

### 2. Go to the project directory
```bash
cd library-service-api
```

### 3. Copy `.env.sample` to `.env` and fill in the values

### 4. Build and Run Docker Containers

```bash
docker compose up --build
```

This will:
- Build the Django application image
- Start PostgreSQL database
- Start Redis server
- Start Django application
- Start Celery worker
- Start Celery beat scheduler


### 5. Create Superuser
```bash
docker compose exec app python manage.py createsuperuser
```

### 6. Access the Application

Once all services are running:

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/doc/
- **Admin Panel**: http://localhost:8000/admin/

---

## 📚 API Documentation

Swagger UI is automatically generated using `drf-spectacular` and available at:

```
http://localhost:8000/api/v1/doc/
```

---

## 🏁 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute it with attribution.

---
