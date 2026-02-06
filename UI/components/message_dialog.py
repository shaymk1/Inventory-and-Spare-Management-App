"""
Message dialog utility for showing success/error messages
"""

import customtkinter as ctk


class MessageDialog:
    @staticmethod
    def show_info(parent, title, message):
        """Show information dialog"""
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (parent.winfo_screenwidth() // 2) - (width // 2)
        y = (parent.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Content
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Icon
        ctk.CTkLabel(frame, text="ℹ️", font=("Arial", 32)).pack(pady=(10, 15))

        # Message
        ctk.CTkLabel(
            frame, text=message, font=("Arial", 14), wraplength=350, justify="center"
        ).pack(pady=(0, 20))

        # OK button
        ctk.CTkButton(frame, text="OK", width=100, command=dialog.destroy).pack()

        return dialog

    @staticmethod
    def show_success(parent, title, message):
        """Show success dialog"""
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (parent.winfo_screenwidth() // 2) - (width // 2)
        y = (parent.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Content
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Icon
        ctk.CTkLabel(frame, text="✅", font=("Arial", 32)).pack(pady=(10, 15))

        # Message
        ctk.CTkLabel(
            frame, text=message, font=("Arial", 14), wraplength=350, justify="center"
        ).pack(pady=(0, 20))

        # OK button
        ctk.CTkButton(frame, text="OK", width=100, command=dialog.destroy).pack()

        return dialog

    @staticmethod
    def show_error(parent, title, message):
        """Show error dialog"""
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        dialog.geometry("400x220")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (parent.winfo_screenwidth() // 2) - (width // 2)
        y = (parent.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Content
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Icon
        ctk.CTkLabel(frame, text="❌", font=("Arial", 32)).pack(pady=(10, 15))

        # Message
        ctk.CTkLabel(
            frame,
            text=message,
            font=("Arial", 14),
            text_color="red",
            wraplength=350,
            justify="center",
        ).pack(pady=(0, 20))

        # OK button
        ctk.CTkButton(
            frame,
            text="OK",
            width=100,
            fg_color="red",
            hover_color="darkred",
            command=dialog.destroy,
        ).pack()

        return dialog

    @staticmethod
    def show_confirm(parent, title, message, on_confirm):
        """Show confirmation dialog with Yes/No buttons"""
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        dialog.geometry("400x220")
        dialog.resizable(False, False)
        dialog.transient(parent)

        # Bring to front and focus
        dialog.lift()
        dialog.focus_force()
        dialog.attributes("-topmost", True)
        dialog.after(100, lambda: dialog.attributes("-topmost", False))

        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (parent.winfo_screenwidth() // 2) - (width // 2)
        y = (parent.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Content
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Icon
        ctk.CTkLabel(frame, text="❓", font=("Arial", 32)).pack(pady=(10, 15))

        # Message
        ctk.CTkLabel(
            frame, text=message, font=("Arial", 14), wraplength=350, justify="center"
        ).pack(pady=(0, 20))

        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack()

        def handle_confirm():
            """Handle confirm with proper cleanup"""
            try:
                dialog.grab_release()  # Release grab before callback
                on_confirm()
            finally:
                try:
                    dialog.destroy()
                except Exception:
                    pass  # Dialog already destroyed

        def handle_cancel():
            """Handle cancel with proper cleanup"""
            try:
                dialog.grab_release()
                dialog.destroy()
            except Exception:
                pass  # Dialog already destroyed

        ctk.CTkButton(
            btn_frame, text="Yes", width=100, fg_color="#4CAF50", command=handle_confirm
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="No", width=100, fg_color="gray", command=handle_cancel
        ).pack(side="left", padx=5)

        # Handle window close (X button)
        dialog.protocol("WM_DELETE_WINDOW", handle_cancel)

        # Set grab after window is fully set up
        dialog.after(10, dialog.grab_set)

        return dialog
