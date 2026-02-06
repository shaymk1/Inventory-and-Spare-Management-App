
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
        ctk.CTkLabel(
            frame,
            text="ℹ️",
            font=("Arial", 32)
        ).pack(pady=(10, 15))
        
        # Message
        ctk.CTkLabel(
            frame,
            text=message,
            font=("Arial", 14),
            wraplength=350,
            justify="center"
        ).pack(pady=(0, 20))
        
        # OK button
        ctk.CTkButton(
            frame,
            text="OK",
            width=100,
            command=dialog.destroy
        ).pack()
        
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
        ctk.CTkLabel(
            frame,
            text="✅",
            font=("Arial", 32)
        ).pack(pady=(10, 15))
        
        # Message
        ctk.CTkLabel(
            frame,
            text=message,
            font=("Arial", 14),
            wraplength=350,
            justify="center"
        ).pack(pady=(0, 20))
        
        # OK button
        ctk.CTkButton(
            frame,
            text="OK",
            width=100,
            command=dialog.destroy
        ).pack()
        
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
        ctk.CTkLabel(
            frame,
            text="❌",
            font=("Arial", 32)
        ).pack(pady=(10, 15))
        
        # Message
        ctk.CTkLabel(
            frame,
            text=message,
            font=("Arial", 14),
            text_color="red",
            wraplength=350,
            justify="center"
        ).pack(pady=(0, 20))
        
        # OK button
        ctk.CTkButton(
            frame,
            text="OK",
            width=100,
            fg_color="red",
            hover_color="darkred",
            command=dialog.destroy
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
        ctk.CTkLabel(
            frame,
            text="❓",
            font=("Arial", 32)
        ).pack(pady=(10, 15))
        
        # Message
        ctk.CTkLabel(
            frame,
            text=message,
            font=("Arial", 14),
            wraplength=350,
            justify="center"
        ).pack(pady=(0, 20))
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack()
        
        ctk.CTkButton(
            btn_frame,
            text="Yes",
            width=100,
            fg_color="#4CAF50",
            command=lambda: [on_confirm(), dialog.destroy()]
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="No",
            width=100,
            fg_color="gray",
            command=dialog.destroy
        ).pack(side="left", padx=5)
        
        return dialog