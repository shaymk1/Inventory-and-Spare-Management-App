# 🧰 Inventory-and-Spare-Management-App

A simple, offline, desktop application to manage spares, stock levels, and daily borrow/return operations for a small internal team.

This app is designed to be easy to understand, easy to maintain, and reliable in real-world daily use — no hosting, no servers, no unnecessary complexity.

## 🎯 Purpose

This project exists to solve a real workshop problem:

- Track available spares and quantities

- Record who borrows and returns items

- Handle partial borrow / partial return

- Keep a movement history (audit trail)

- Trigger alerts when critical spares are low

- Work fully offline

- Be maintainable by a single developer
  
## 🧱 Tech Stack

- Language: Python 3

- UI: CustomTkinter

- Database: SQLite (local file)

- Email Alerts: Python smtplib

- Packaging: PyInstaller

- Hosting: ❌ None (offline-first)
  
## ✅ Key Features

- Admin login + backup users

📦 Spare management (name, code, quantity, image)

🔁 Borrow / Return workflow

- Partial borrow

- Partial return

- Daily usage supported

📜 Movement history (who did what, when)

📧 Low-stock email alerts for critical spares

💾 Automatic and manual backups

📴 Works fully offline

🖥️ Desktop-only (Windows / macOS / Linux)

## 🗂️ Project Structure

inventory_app/
│
├── sql/
│   ├── create_movements.sql
│   ├── create_spares.sql
│   ├── create_users.sql
│
├── ui/
│   ├── login.py
│   ├── dashboard.py
│   ├── spare_form.py
│   ├── borrow_return.py
│   └── history.py
│
├── data/
│   ├── inventory.db       # SQLite database (source of truth)
│   ├── images/            # Spare images
│   └── backups/           # Timestamped backups
│
│
├── logic/
│   ├── auth.py
│   ├── backup.py
│   └── db.py
│   ├── email_alerts.py
│   ├── main.py
│   └── movements.py
│   ├── test_db.py
│   └── utils.py
│
└── requirements.txt
└── app.py                #entry point of the app
└── run_test.py           #test script
└── readme.md

## Application Architecture

### The app follows a simple 3-layer design

UI (CustomTkinter)
        ↓
Application Logic (Python)
        ↓
Data Layer (SQLite + local files)

- UI never talks directly to the database

- All business rules live in Python logic

- Data is stored locally and backed up regularly
  
## 🔄 Core Workflow (Borrow / Return)

### Borrow

- Select spare

- Enter quantity and borrower

- Validate available stock

- Update quantity

- Log movement

- Trigger low-stock alert if needed

### Return

- Select spare

- Enter quantity returned

- Update quantity

- Log movement
  
## 💾 Backup Strategy

### Automatic

- Runs on app startup or once per day

- Copies inventory.db into data/backups/

- Timestamped for safety

### Manual

- “Export Backup” button

- User selects destination (USB, folder, etc.)

🔴 The database and data folders are never overwritten during app updates

## 🚀 Deployment

### Development

- Run directly with Python:
  - python main.py

### Production

- Package with PyInstaller into a standalone executable

- Copy the executable to the target laptop

- No Python installation required on the target machine

### Updating the App

- Replace the executable only

- Keep existing data/ folder

- No data loss
  
## 🏁 Project Philosophy

### This project prioritizes

- Simplicity
  
- Clarity
  
- Maintainability
  
- Real-world usage
  
- ---If this app works reliably every day in the workshop, it is a success
  
## 🛠️ Setup Instructions (Step by Step)

### Python Version

This project is developed and tested with **Python 3.12**.

⚠️ Python 3.13 is not recommended YET due to instability with `venv` on Windows.

- These steps are for development and local testing.
- The final app will later be packaged into a standalone executable.

### 1️⃣ Prerequisites

- Python 3.10+

- python --version

- pip (comes with Python)

- A code editor (VS Code recommended)

- The target/workshop laptop does NOT need Python (after packaging)
  
### 2️⃣ Clone or Create the Project Folder

- Create a project directory:

  - mkdir inventory_app
  - cd inventory_app

- (Optional) Initialize git:

  - git init

### 3️⃣ Create a Virtual Environment (Recommended)

- This keeps dependencies isolated.

- Windows:
  - python -m venv venv
  - venv\Scripts\activate

- macOS / Linux
  - python3 -m venv venv
  - source venv/bin/activate

- You should now see (venv) in your terminal.
  
### 4️⃣ Install Dependencies

- Create a requirements.txt file:

  - customtkinter>=5.2.0
  - pillow>=10.0.0

- Install dependencies:

  - pip install -r requirements.txt

### 5️⃣ Project Folder Structure

- Create the following folders and files:
  
  inventory_app/
│
├── main.py
├── db.py
├── auth.py
├── inventory.py
├── movements.py
├── email_alerts.py
├── backup.py
│
├── UI/
│   ├── login.py
│   ├── dashboard.py
│   ├── spare_form.py
│   ├── borrow_return.py
│   └── history.py
│
├── data/
│   ├── inventory.db
│   ├── images/
│   └── backups/
│
└── requirements.txt

- ✅ data/ holds real data
- ❌ Never overwrite this folder when updating the app
  
### 6️⃣ Initialize the Database

- In db.py:

  - Create SQLite connection

  - Create tables if they don’t exist:

  - users

  - spares

  - movements

- The database file:

  - data/inventory.db

- This file is the single source of truth.

### 7️⃣ Run the App (Development Mode)

- From the project root:

  - python main.py

- Expected result:

  - App window opens

  - Login screen appears

  - Database file is created if missing

### 8️⃣ Test Core Features (Early)

- Before adding UI polish, verify:

  - App starts without errors

  - Database tables are created

  - Login logic works

  - Spares can be added

  - Quantities update correctly

### 9️⃣ Email Configuration (Optional at First)

- In email_alerts.py:

  - Configure SMTP settings

  - Store credentials securely (env vars or config file)

  - Low-stock alerts will trigger when:

  - quantity <= low_stock_threshold

- You can skip this step until later phases.

### 🔟 Packaging the App (Later)

- When ready for deployment:

  - pip install pyinstaller
  - pyinstaller --onefile main.py

- Output:

  - dist/main.exe

- Copy the executable to the target laptop.

- 📌 Do NOT copy your dev database
- The app will create its own data/ folder on first run.
  
### ♻️ Updating the App Safely

- When releasing updates:

  - Replace the executable only

- Keep:

  - data/inventory.db

  - data/images/

  - data/backups/

- This guarantees zero data loss.
  
### 🧠 Common Troubleshooting

- App doesn’t start?

  - Check virtual environment is activated

- UI doesn’t show?

  - Verify main.py imports UI modules correctly

- Database errors?

  - Confirm data/ folder exists

- Email not sending?

  - Check SMTP credentials and firewall rules

### ✅ Setup Complete

- If:

  - The app launches

  - The database exists

  - You can add a spare

- Then your environment is correctly set up.