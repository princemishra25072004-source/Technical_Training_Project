# 📦 Stockwise — Inventory and Stock Management System

[![CI Pipeline](https://github.com/princemishra25072004-source/Technical_Training_Project/actions/workflows/ci.yml/badge.svg)](https://github.com/princemishra25072004-source/Technical_Training_Project/actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask_3.x-black.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lightweight, production-grade **Inventory and Stock Management Web Application** designed for technical training demonstrations, college vivas, and real-world warehouse tracking. Built with **Python (Flask)**, **SQLite3**, **Bootstrap 5**, and **JavaScript**.

---

## ✨ Features

- 🔐 **Secure Authentication**: Protected admin routes using Werkzeug PBKDF2 password hashing and secure session cookies.
- 📊 **Real-time Dashboard**:
  - Total catalog product count
  - Overall inventory units in stock
  - Total inventory valuation ($\sum \text{price} \times \text{quantity}$)
  - Low-stock counter with smart warning highlights
- 📦 **Complete Product CRUD**:
  - Add, edit, view, and delete inventory products.
  - Strict validation: unique SKU constraints, non-negative prices, and positive integers for stock quantities.
  - Duplicate SKU detection with descriptive feedback messages.
- ⚡ **Instant Stock Adjustment**:
  - Inline `+` / `-` stock adjustments right from the dashboard table.
  - Automated constraint enforcement preventing inventory levels from falling below zero.
- 🔍 **Search & Multi-Filtering**:
  - Live substring search matching product name, SKU, or supplier.
  - Dynamic category dropdown filter.
  - One-click filter for items below their reorder threshold.
- 🧪 **Automated Testing & CI/CD**:
  - Suite of 12 unit tests covering authentication, database constraints, routes, and business logic.
  - Pre-configured GitHub Actions CI workflow running across Python 3.10, 3.11, 3.12, and 3.13.

---

## 🏗️ Project Architecture

```
inventory_stock_system/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions automated test pipeline
├── static/
│   ├── app.js                 # Frontend interactions (delete confirmations)
│   └── style.css              # Custom styling & responsive UI tokens
├── templates/
│   ├── base.html              # Base Jinja2 layout with navigation & flash alerts
│   ├── dashboard.html         # Main dashboard, metrics cards, table & filters
│   ├── login.html             # Admin authentication form
│   └── product_form.html      # Create & edit product form
├── tests/
│   ├── __init__.py
│   └── test_app.py            # Unit & route test suite with mock DB fixtures
├── .env.example               # Template environment variables
├── .gitignore                 # Standard Python/Flask ignore rules
├── app.py                     # Flask application, routing, SQLite queries & logic
├── LICENSE                    # MIT Open Source License
├── README.md                  # Project documentation & viva guide
└── requirements.txt           # Production dependencies
```

---

## 🗄️ Database Schema

The database utilizes SQLite (`inventory.db`) with two main relations:

### 1. `users` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Autoincrement | Unique user identifier |
| `username` | `TEXT` | Unique, Not Null | Admin username |
| `password_hash`| `TEXT` | Not Null | Werkzeug-generated password hash |

### 2. `products` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Autoincrement | Unique product identifier |
| `name` | `TEXT` | Not Null | Product name |
| `sku` | `TEXT` | Unique, Not Null | Stock Keeping Unit code |
| `category` | `TEXT` | Not Null | Product classification |
| `price` | `REAL` | Not Null, `CHECK(price >= 0)` | Unit selling price (₹) |
| `quantity` | `INTEGER` | Not Null, `CHECK(quantity >= 0)` | Units currently on hand |
| `reorder_level`| `INTEGER` | Default 5, `CHECK(reorder_level >= 0)` | Reorder warning threshold |
| `supplier` | `TEXT` | Default `''` | Vendor or manufacturer |
| `created_at` | `TEXT` | Not Null | ISO-8601 creation date |

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10** or higher
- **Git**

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/princemishra25072004-source/Technical_Training_Project.git
   cd Technical_Training_Project
   ```

2. **Create and activate a virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate.bat
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Configure environment**:
   ```bash
   cp .env.example .env
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open in browser**:
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔑 Default Credentials

| Field | Value |
|---|---|
| **URL** | `http://127.0.0.1:5000/login` |
| **Username** | `admin` |
| **Password** | `admin123` |

> 💡 *Note: The SQLite database (`inventory.db`) and seed demo records are automatically provisioned on the first execution.*

---

## 🧪 Running Automated Tests

Run the full unit test suite without needing third-party testing dependencies:

```bash
python -m unittest discover -s tests -v
```

Expected output:
```text
test_add_product_duplicate_sku (tests.test_app.StockwiseTestCase) ... ok
test_add_product_success (tests.test_app.StockwiseTestCase) ... ok
test_dashboard_metrics (tests.test_app.StockwiseTestCase) ... ok
test_delete_product (tests.test_app.StockwiseTestCase) ... ok
test_edit_product (tests.test_app.StockwiseTestCase) ... ok
test_login_invalid_credentials (tests.test_app.StockwiseTestCase) ... ok
test_login_page_renders (tests.test_app.StockwiseTestCase) ... ok
test_login_valid_credentials (tests.test_app.StockwiseTestCase) ... ok
test_search_and_filter (tests.test_app.StockwiseTestCase) ... ok
test_stock_adjustment_increase_and_decrease (tests.test_app.StockwiseTestCase) ... ok
test_stock_cannot_go_negative (tests.test_app.StockwiseTestCase) ... ok
test_unauthenticated_access_redirects (tests.test_app.StockwiseTestCase) ... ok

----------------------------------------------------------------------
Ran 12 tests in ~3s

OK
```

---

## 🎓 Technical Training Viva Reference

| Concept | Implementation Details |
|---|---|
| **Why SQLite?** | Zero-configuration, serverless, file-backed database ideal for desktop deployments and training demos. Uses SQLite `CHECK` constraints to enforce non-negative prices and quantities directly at the database engine level. |
| **Password Security** | Passwords are never stored in plain text. `generate_password_hash` uses cryptographic PBKDF2 with SHA-256 and unique salting. Verification uses constant-time string comparison via `check_password_hash`. |
| **Session Management** | Protected routes use a custom `@signed_in` Python decorator that inspects `session['user_id']`. Unauthenticated requests are intercepted and redirected to `/login`. |
| **SQL Injection Prevention** | All dynamic values are passed using parameterized queries (`?` placeholders) rather than string interpolation or f-strings. |
| **Resource Management** | Database access uses Python's `@contextmanager` to guarantee connections are cleanly committed and closed on both success and failure, preventing resource leaks. |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — see the LICENSE file for details.

Developed as part of the **Technical Training Project** by [Prince Mishra](https://github.com/princemishra25072004-source).
