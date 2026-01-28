# app.py
"""
Main application entry point
"""
import customtkinter as ctk
from UI.login import LoginWindow


class SpareManagerApp:
    def __init__(self):
        # Setup appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def show_dashboard(self, user):
        """Show main dashboard after login"""
        print(f"✅ Logged in as: {user['full_name']}")

        # Create dashboard window
        dashboard = ctk.CTk()
        dashboard.title(f"Spare Manager - {user['full_name']}")
        dashboard.state("zoomed")
        # dashboard.geometry("800x600")

        # Center window
        dashboard.update_idletasks()
        width = dashboard.winfo_width()
        height = dashboard.winfo_height()
        x = (dashboard.winfo_screenwidth() // 2) - (width // 2)
        y = (dashboard.winfo_screenheight() // 2) - (height // 2)
        dashboard.geometry(f"{width}x{height}+{x}+{y}")

        # Welcome message
        welcome_frame = ctk.CTkFrame(dashboard, corner_radius=10)
        welcome_frame.pack(pady=50, padx=50, fill="both", expand=True)

        # User info
        role = "👨‍💻 Developer" if user["is_developer"] else "👷 Manager"

        ctk.CTkLabel(
            welcome_frame,
            text=f"🎉 WELCOME, {user['full_name']}!",
            font=("Arial", 24, "bold"),
        ).pack(pady=20)

        ctk.CTkLabel(welcome_frame, text=f"Role: {role}", font=("Arial", 14)).pack(
            pady=10
        )

        ctk.CTkLabel(
            welcome_frame,
            text="Your inventory management system is ready to use.",
            font=("Arial", 12),
            text_color="gray",
        ).pack(pady=30)

        # Status
        info_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        info_frame.pack(pady=20)

        # Get stats from database
        from logic.db import db

        spares = db.execute("SELECT COUNT(*) as count FROM spares", fetch=True)
        users = db.execute(
            "SELECT COUNT(*) as count FROM users WHERE is_active = 1", fetch=True
        )

        stats = [
            ("📦", f"Total Spares: {spares[0]['count'] if spares else 0}"),
            ("👥", f"Active Users: {users[0]['count'] if users else 0}"),
            ("✅", "Database: Connected"),
            ("🔒", "Authentication: Working"),
        ]

        for icon, text in stats:
            item = ctk.CTkFrame(info_frame, fg_color="transparent")
            item.pack(pady=5, anchor="w")

            ctk.CTkLabel(item, text=icon, font=("Arial", 14), width=30).pack(
                side="left"
            )
            ctk.CTkLabel(item, text=text, font=("Arial", 12)).pack(side="left")

        # Quick actions (placeholders for now)
        ctk.CTkLabel(
            welcome_frame,
            text="🚀 Quick actions coming soon...",
            font=("Arial", 12),
            text_color="gray",
        ).pack(pady=40)

        # Exit button
        ctk.CTkButton(
            dashboard,
            text="LOGOUT",
            command=dashboard.destroy,
            fg_color="#F44336",
            hover_color="#D32F2F",
            height=40,
            font=("Arial", 12),
        ).pack(pady=20)

        dashboard.mainloop()

    def run(self):
        """Start application"""
        login = LoginWindow(self.show_dashboard)
        login.run()


if __name__ == "__main__":
    app = SpareManagerApp()
    app.run()
