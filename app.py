# app.py
"""
Main application entry point
"""
import customtkinter as ctk
from UI.login import LoginWindow


# TEMPORARY DEBUG CODE - REMOVE AFTER CHECKING
from logic.db import db

print("=== DATABASE SCHEMA CHECK ===")

# Check movements table
print("\n1. Movements table structure:")
movements_columns = db.execute("PRAGMA table_info(movements)", fetch=True)
if movements_columns:
    for col in movements_columns:
        print(f"  {col['name']} ({col['type']})")
else:
    print("  No movements table found!")

# Check spares table
print("\n2. Spares table structure:")
spares_columns = db.execute("PRAGMA table_info(spares)", fetch=True)
if spares_columns:
    for col in spares_columns:
        print(f"  {col['name']} ({col['type']})")
else:
    print("  No spares table found!")

print("=== END SCHEMA CHECK ===\n")


class SpareManagerApp:
    def __init__(self):
        # Setup appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def show_dashboard(self, user):
        """
        Show main dashboard after login
        """
        print(f"✅ Logged in as: {user['full_name']}")

        # Import and show the dashboard
        from UI.dashboard import Dashboard

        # Create dashboard window
        dashboard = Dashboard(user, self)
        dashboard.mainloop()

    def run(self):
        """Start application"""
        login = LoginWindow(self.show_dashboard)
        login.run()


if __name__ == "__main__":
    app = SpareManagerApp()
    app.run()
