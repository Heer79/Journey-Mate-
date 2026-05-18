# 🧭 Journey-Mate: Premium Django Travel & Tour Booking Platform

[![Django Version](https://img.shields.io/badge/django-v4.2.7-green.svg?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/python-v3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Razorpay Integrated](https://img.shields.io/badge/payments-Razorpay-orange.svg?style=for-the-badge&logo=razorpay)](https://razorpay.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Journey-Mate** is a responsive, feature-rich travel agency booking platform built on the robust Django framework. It empowers travel companies to showcase dynamic tour packages and offers, while providing travelers with a modern portal to browse destinations, apply coupons, book tickets, verify real-time seat availability, make secure payments through **Razorpay**, and download PDF invoices instantly.

---

## 🌟 Core Highlights & Features

### 🔐 Modern Account & User Management
* **Custom User Model (`CustomUser`):** Extends Django's `AbstractUser` with advanced fields like `phone_number`, `address`, and user type flags (`is_customer`).
* **Authentication Suite:** Out-of-the-box support for user registration, secure login, password resets, and account dashboard.

### 🗺️ Dynamic Tour Packages Showcase
* **Categorized Travel Packages:** Group packages into categories (e.g., Beach, Mountain, Adventure, Heritage).
* **Package Profiles:** Every package features detailed day/night duration tags, pricing, hotel specifics, bus configurations (AC/Non-AC choices), total available seats, and gorgeous media image displays.
* **Instant Booking Flow:** Users can book packages directly with precise passenger count selection and travel date validation.

### 🔍 Advanced Search & Filter Engine
* **Universal Search:** Instantly query package names, descriptions, and hotel specifications using SQL-optimized search views.
* **Smart Filter Bar:** Seamlessly filter the entire tour inventory by category tabs.

### 🎟️ Active Offer & Coupon Engine
* **Promo Code Application:** Fully functional coupon verification system. Users can enter discount codes at checkout.
* **Validation Guards:** The system checks code existence, validation time constraints, and status (active/inactive) automatically.

### 💳 Secure Online Payments with Razorpay
* **Razorpay Payment Gateway Integration:** Complete client-server checkout flow to secure bookings online.
* **Resilient Mock Bypass:** A robust fallback verification routine allows developers to mock payments effortlessly in local testing without needing actual API configurations.
* **Real-time Seat Control:** A dynamic AJAX endpoint keeps track of available seats based on travel date and blocks over-booking.

### 📄 Automated PDF Invoices
* **PDF Document Engine:** Integrates `xhtml2pdf` to transform custom HTML invoices into clean, downloadable PDFs for all approved and paid bookings.

### 🛠️ Developer Utilities
* **Automated Superuser Creation Script:** Spin up an administrator account (`admin` / `admin123`) in seconds using `create_admin.py`.

---

## 🛠️ Technical Architecture & Stack

| Layer | Component | Details |
| :--- | :--- | :--- |
| **Backend Framework** | **Django 4.2.7** | Secure, structured, and fast Python web framework. |
| **Database** | **SQLite3** | Default lightweight database (fully compatible with PostgreSQL/MySQL). |
| **Frontend Style** | **HTML5 / CSS3 / Vanilla JS** | Modern design, using CSS Flexbox/Grid systems and responsive cards. |
| **Payment Gateway** | **Razorpay SDK** | Live payment capture, orders creation, and webhook signature verification. |
| **Document Compiler** | **xhtml2pdf (Pisa)** | Programmatically generates downloadable invoices. |
| **Image Handler** | **Pillow** | Handles travel catalog image uploads securely. |

---

## 📂 Repository Directory Blueprint

A structural overview of the Journey-Mate project codebase:

```bash
journeymate/
│
├── accounts/               # Custom user profile & authentication views/models
│   ├── models.py           # CustomUser definition (phone, address, type)
│   ├── views.py            # Signup, login, profile view handlers
│   └── urls.py             # Authentication routing paths
│
├── bookings/               # Travel booking, Razorpay payment verification
│   ├── models.py           # Booking model with Payment and Approval status
│   ├── views.py            # Checkout, signature validation, PDF invoices
│   └── signals.py          # Auto-signals for seat updates and notifications
│
├── core/                   # Landing page, Feedback & Contact forms
│   ├── models.py           # ContactMessage schema
│   ├── views.py            # Featured packages logic, contact & feedback
│   └── forms.py            # Contact & feedback forms validation
│
├── packages/               # Packages management (Categories, Tours, Offers)
│   ├── models.py           # Package, Category, and Offer schemas
│   ├── views.py            # Dynamic package search, listings, details
│   └── admin.py            # Admin registration for tour assets
│
├── journeymate/            # Core settings directory
│   ├── settings.py         # Main config (apps, DB, Razorpay credentials)
│   ├── urls.py             # Root URL routing configurations
│   └── wsgi.py / asgi.py   # Gateway interface setups
│
├── static/                 # CSS stylesheets, JS scripts, web icons
├── templates/              # Base layouts and individual app template structures
│   ├── base.html           # Master navigation & footer shell
│   ├── core/               # Landing pages and contacts
│   ├── packages/           # Tour listings and details
│   └── bookings/           # Payment gateway frame, user invoices
│
├── create_admin.py         # Superuser creation script
├── manage.py               # Django execution script
├── db.sqlite3              # Relational database (SQLite)
└── .gitignore              # Files to exclude from source control
```

---

## ⚙️ Quick-Start Installation & Setup

Follow these detailed steps to set up and run Journey-Mate on your local environment:

### 1. Clone the Repository
```bash
git clone https://github.com/Heer79/Journey-Mate-.git
cd journeymate
```

### 2. Establish a Virtual Environment
It is highly recommended to isolate dependencies using a Python virtual environment:

**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Ensure you have the required packages installed in your active virtual environment:
```bash
pip install django pillow razorpay xhtml2pdf python-dotenv
```

### 4. Setup Environment Variables
Create a file named `.env` in the root directory of your project (parallel to `manage.py`) to manage sensitive API keys securely. You can use the provided `.env.example` as a starting blueprint:
```env
# General Settings
SECRET_KEY=django-insecure-c7teq%8mrr=mp(!xnb9t83*(5nhw^j+afmh_1skvdnx=g_=7l^
DEBUG=True

# Razorpay Test Credentials (Get these from Razorpay Dashboard > Settings)
RAZORPAY_KEY_ID=rzp_test_YourDummyKeyHere
RAZORPAY_KEY_SECRET=YourDummySecretHere
```

> [!IMPORTANT]
> Keep your `.env` private! It is listed inside `.gitignore` and should never be committed to Git.

### 5. Database Setup & Migrations
Create the SQLite database tables and apply all migration plans:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin Account (Quick Script)
You can set up an instant superuser account for administration access by executing our helper script:
```bash
python create_admin.py
```
* **Default Username:** `admin`
* **Default Password:** `admin123`
* **Default Email:** `admin@journeymate.com`

*Alternatively, create a customized superuser manually:*
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
Fire up the local Django server:
```bash
python manage.py runserver
```

Open your browser and navigate to **`http://127.0.0.1:8000/`** to explore the application! To log into the management console, head to **`http://127.0.0.1:8000/admin/`**.

---

## 💳 Razorpay Payment Configuration & Testing

To configure real money or test-mode transactions:
1. Log in to your [Razorpay Dashboard](https://dashboard.razorpay.com/).
2. Navigate to **Settings** > **API Keys** > **Generate Key**.
3. Copy the **Key ID** and **Key Secret**.
4. Update your `.env` (or `settings.py`) with these live credentials:
   ```env
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxx
   RAZORPAY_KEY_SECRET=yyyyyyyyyyyyyy
   ```

### 🧪 Local Demo Mode (No API Keys needed!)
If you want to quickly demo or test the checkout system without configuring Razorpay keys:
* Keep `RAZORPAY_KEY_ID` set to `'rzp_test_YourDummyKeyHere'` or set it to blank.
* The system detects the dummy state and automatically switches to **Mock Payment Mode**, rendering a secure checkout redirect that processes mock successes and generates the invoices smoothly.

---

## 🤝 Contribution & License

Contributions are welcome! If you'd like to improve Journey-Mate:
1. Fork the Repository.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

This project is open-source, licensed under the **MIT License**.

---
*Developed with ❤️ by Heer Limbachiya. Let's make every journey count!*
