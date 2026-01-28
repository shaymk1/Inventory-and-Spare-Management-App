# gui/login_window.py
"""
Login screen for Spare Manager
"""
import customtkinter as ctk
from logic.db import db


class LoginWindow:
    def __init__(self, on_login_success):
        """
        Initialize login window

        Args:
            on_login_success: Callback function when login succeeds
        """
        self.on_login_success = on_login_success

        # Create window
        self.window = ctk.CTk()
        self.window.title("Spare Manager - Login")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        # Center window
        self._center_window()

        # Create UI
        self._create_ui()

        # Bind Enter key
        self.window.bind("<Return>", lambda event: self.attempt_login())

    def _center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def _create_ui(self):
        """Create all UI elements"""
        # Title
        title = ctk.CTkLabel(
            self.window, text="🔧 SPARE MANAGER", font=("Arial", 24, "bold")
        )
        title.pack(pady=30)

        # Subtitle
        ctk.CTkLabel(
            self.window,
            text="Inventory Management System",
            font=("Arial", 12),
            text_color="gray",
        ).pack(pady=(0, 30))

        # Username
        ctk.CTkLabel(self.window, text="Username:", font=("Arial", 12)).pack()
        self.username_entry = ctk.CTkEntry(self.window, width=200)
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, "store_manager")  # Default

        # Password
        ctk.CTkLabel(self.window, text="Password:", font=("Arial", 12)).pack()
        self.password_entry = ctk.CTkEntry(self.window, width=200, show="•")
        self.password_entry.pack(pady=5)

        # Login button
        self.login_btn = ctk.CTkButton(
            self.window,
            text="LOGIN",
            command=self.attempt_login,
            width=200,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#2E8B57",
        )
        self.login_btn.pack(pady=30)

        # Error label
        self.error_label = ctk.CTkLabel(
            self.window, text="", font=("Arial", 11), text_color="red"
        )
        self.error_label.pack()

        # Hint
        ctk.CTkLabel(
            self.window,
            text="Use: store_manager / boss_backup / dev_admin",
            font=("Arial", 10),
            text_color="gray",
        ).pack(pady=(10, 0))

    def attempt_login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Clear previous error
        self.error_label.configure(text="")

        # Validate
        if not username or not password:
            self.show_error("Please enter username and password")
            return

        # Authenticate
        user = self.authenticate(username, password)

        if user:
            self.show_success(f"Welcome, {user['full_name']}!")
            self.login_btn.configure(state="disabled")
            self.window.after(1000, lambda: self.login_success(user))
        else:
            self.show_error("Invalid username or password")
            self.password_entry.delete(0, "end")

    def authenticate(self, username, password):
        """
        Simple authentication against database
        For now: passwords are stored plain text (we'll hash later)
        """
        try:
            # Query database for user with matching password
            users = db.execute(
                "SELECT username, full_name, is_developer FROM users WHERE username = ? AND password_hash = ? AND is_active = 1",
                (username, password),
                fetch=True,
            )

            if users:
                return users[0]
        except Exception as e:
            print(f"Auth error: {e}")

        return None

    def show_error(self, message):
        """Show error message"""
        self.error_label.configure(text=f"❌ {message}", text_color="red")

    def show_success(self, message):
        """Show success message"""
        self.error_label.configure(text=f"✅ {message}", text_color="green")

    def login_success(self, user_data):
        """Close login and pass user to main app"""
        self.window.destroy()
        self.on_login_success(user_data)

    def run(self):
        """Start the login window"""
        self.window.mainloop()
