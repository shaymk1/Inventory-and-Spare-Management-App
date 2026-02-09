"""
Return Items Interface
"""

import customtkinter as ctk
from logic.db import db


class ReturnForm:
    def __init__(self, parent_frame, user_info):
        """
        Initialize return interface

        Args:
            parent_frame: Frame to pack this interface into
            user_info: Current user information (for logging)
        """
        self.parent = parent_frame
        self.user_info = user_info
        self.borrowed_items = []  # Will store borrowed items

        # Create main container
        self.main_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Load borrowed items
        self._load_borrowed_items()
        self._create_interface()

    def _load_borrowed_items(self):
        """Load items that have been borrowed but not fully returned"""
        try:
            # Get borrowed items with remaining quantity to return
            self.borrowed_items = db.execute(
                """
                SELECT 
                    m.id as movement_id,
                    m.spare_id,
                    m.quantity as borrowed_qty,
                    m.returned_quantity,
                    m.movement_date,
                    m.notes,
                    s.name as spare_name,
                    s.code as spare_code,
                    (m.quantity - COALESCE(m.returned_quantity, 0)) as remaining_qty
                FROM movements m
                JOIN spares s ON m.spare_id = s.id
                WHERE m.movement_type = 'borrow'
                AND (m.returned_quantity IS NULL OR m.returned_quantity < m.quantity)
                ORDER BY m.movement_date DESC
                """,
                fetch=True,
            )
        except Exception as e:
            print(f"Error loading borrowed items: {e}")
            self.borrowed_items = []

    def _create_interface(self):
        """Create the return interface"""
        # Title
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(pady=(0, 20))

        ctk.CTkLabel(
            title_frame, text="⬆️ Return Items", font=("Arial", 22, "bold")
        ).pack()

        ctk.CTkLabel(
            title_frame,
            text="Return borrowed items to inventory",
            font=("Arial", 14),
            text_color="gray",
        ).pack(pady=(5, 0))

        # Refresh button
        refresh_btn = ctk.CTkButton(
            title_frame,
            text="🔄 Refresh List",
            width=120,
            height=35,
            font=("Arial", 12),
            command=self._refresh_list,
        )
        refresh_btn.pack(pady=(10, 0))

        # Main content area
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if not self.borrowed_items:
            # No borrowed items message
            ctk.CTkLabel(
                content_frame,
                text="No items currently borrowed",
                font=("Arial", 16),
                text_color="gray",
            ).pack(expand=True, pady=100)
            return

        # Create scrollable table
        scroll_frame = ctk.CTkScrollableFrame(content_frame, height=400)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Table headers
        headers = ["Spare", "Borrowed", "Returned", "Remaining", "Date", "Action"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                scroll_frame,
                text=header,
                font=("Arial", 12, "bold"),
                width=120 if col < 5 else 100,
            )
            label.grid(row=0, column=col, padx=5, pady=10, sticky="w")

        # Add borrowed items rows
        for row, item in enumerate(self.borrowed_items, start=1):
            # Spare info
            spare_info = f"{item['spare_name']}\n({item['spare_code']})"

            # Quantities
            borrowed_qty = item["borrowed_qty"]
            returned_qty = item["returned_quantity"] or 0
            remaining_qty = item["remaining_qty"]

            # Date
            borrow_date = (
                item["movement_date"].split()[0] if item["movement_date"] else "N/A"
            )

            # Display data
            data = [
                spare_info,
                str(borrowed_qty),
                str(returned_qty),
                str(remaining_qty),
                borrow_date,
            ]

            # Display row
            for col, value in enumerate(data):
                label = ctk.CTkLabel(
                    scroll_frame,
                    text=value,
                    font=("Arial", 11),
                    width=120 if col < 5 else 100,
                )
                label.grid(row=row, column=col, padx=5, pady=5, sticky="w")

            # Return button
            return_btn = ctk.CTkButton(
                scroll_frame,
                text="Return",
                width=80,
                height=30,
                font=("Arial", 11),
                fg_color="#4CAF50",
                command=lambda i=item: self._show_return_dialog(i),
            )
            return_btn.grid(row=row, column=5, padx=5, pady=5)

    def _show_return_dialog(self, item):
        """Show dialog for returning a specific item"""
        # Create dialog window
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title(f"Return {item['spare_name']}")
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Make dialog modal
        dialog.grab_set()

        # Dialog content
        content_frame = ctk.CTkFrame(dialog)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Item info
        ctk.CTkLabel(
            content_frame,
            text=f"Returning: {item['spare_name']}",
            font=("Arial", 16, "bold"),
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            content_frame, text=f"Code: {item['spare_code']}", font=("Arial", 12)
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            content_frame,
            text=f"Borrowed: {item['borrowed_qty']} | Returned: {item['returned_quantity'] or 0} | Remaining: {item['remaining_qty']}",
            font=("Arial", 12),
        ).pack(pady=(0, 20))

        # Quantity to return
        qty_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        qty_frame.pack(pady=10)

        ctk.CTkLabel(
            qty_frame, text="Quantity to Return:", font=("Arial", 12, "bold")
        ).pack(side="left", padx=(0, 10))

        self.return_qty_entry = ctk.CTkEntry(qty_frame, width=100)
        self.return_qty_entry.pack(side="left")
        self.return_qty_entry.insert(0, str(item["remaining_qty"]))

        # Notes
        ctk.CTkLabel(
            content_frame, text="Return Notes (Optional):", font=("Arial", 12, "bold")
        ).pack(pady=(10, 5))

        self.return_notes = ctk.CTkTextbox(content_frame, width=350, height=60)
        self.return_notes.pack(pady=(0, 20))

        # Buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack()

        ctk.CTkButton(
            button_frame,
            text="✅ Confirm Return",
            width=150,
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#4CAF50",
            command=lambda: self._process_return(item, dialog),
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            width=100,
            height=40,
            font=("Arial", 13),
            fg_color="gray",
            command=dialog.destroy,
        ).pack(side="left", padx=5)

    def _process_return(self, item, dialog):
        """Process the return"""
        # Get quantity to return
        qty_text = self.return_qty_entry.get().strip()
        if not qty_text:
            from UI.components.message_dialog import MessageDialog

            MessageDialog.show_error(dialog, "Error", "Please enter quantity to return")
            return

        try:
            return_qty = int(qty_text)
            if return_qty <= 0:
                MessageDialog.show_error(
                    dialog, "Error", "Quantity must be greater than 0"
                )
                return

            remaining_qty = item["remaining_qty"]
            if return_qty > remaining_qty:
                MessageDialog.show_error(
                    dialog,
                    "Error",
                    f"Cannot return more than remaining ({remaining_qty})",
                )
                return
        except ValueError:
            MessageDialog.show_error(dialog, "Error", "Quantity must be a number")
            return

        # Get notes
        notes = self.return_notes.get("1.0", "end-1c").strip()

        try:
            # Get the original borrower name from the borrow movement
            borrow_record = db.execute(
                """
                SELECT borrower_name, notes 
                FROM movements 
                WHERE id = ?
                """,
                (item["movement_id"],),
                fetch=True,
            )

            # Extract borrower name
            borrower_name = "Unknown"
            if borrow_record:
                record = borrow_record[0]
                if record.get("borrower_name"):
                    borrower_name = record["borrower_name"]
                elif record.get("notes"):
                    # Try to parse from old notes format
                    notes_text = record["notes"] or ""
                    if "borrowed by" in notes_text.lower():
                        # Extract from pattern like "Borrowed by John Doe"
                        import re

                        match = re.search(r"[Bb]orrowed by\s+(.+)", notes_text)
                        if match:
                            borrower_name = match.group(1).strip()

            # Start transaction
            # 1. Update spare quantity
            db.execute(
                "UPDATE spares SET quantity = quantity + ? WHERE id = ?",
                (return_qty, item["spare_id"]),
            )

            # 2. Update original borrow movement record
            current_returned = item["returned_quantity"] or 0
            new_returned = current_returned + return_qty

            db.execute(
                """
                UPDATE movements 
                SET returned_quantity = ?,
                    return_date = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (new_returned, item["movement_id"]),
            )

            # 3. Create return movement record
            # Determine if this is full or partial return
            is_full_return = new_returned >= item["borrowed_qty"]
            return_type = "full" if is_full_return else "partial"

            # Create return notes if none provided
            if not notes:
                notes = f"{return_type} return of {item['spare_name']}"
                if not is_full_return:
                    notes += f" ({return_qty} of {item['borrowed_qty']} returned)"

            # Insert return movement
            db.execute(
                """
                INSERT INTO movements 
                (spare_id, user_id, quantity, movement_type, notes, borrower_name, returned_quantity)
                VALUES (?, ?, ?, 'return', ?, ?, ?)
                """,
                (
                    item["spare_id"],
                    self.user_info.get("id", 1),
                    return_qty,
                    notes,
                    borrower_name,  # Store borrower name
                    return_qty,  # For returns, this equals quantity
                ),
            )

            # Show success and close dialog
            dialog.destroy()

            # Refresh the list
            self._refresh_list()

            # Show success message
            MessageDialog.show_success(
                self.main_frame,
                "Success",
                f"✅ Return successful!\n\n"
                f"Item: {item['spare_name']}\n"
                f"Quantity: {return_qty}\n"
                f"Borrower: {borrower_name}\n"
                f"Type: {return_type.title()} Return",
            )

        except Exception as e:
            MessageDialog.show_error(
                dialog, "Database Error", f"Failed to process return:\n{str(e)}"
            )

    def _refresh_list(self):
        """Refresh the borrowed items list"""
        # Clear current interface
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Reload and recreate
        self._load_borrowed_items()
        self._create_interface()

    def _show_message(self, title, message):
        """Show message (placeholder - implement proper dialog later)"""
        print(f"{title}: {message}")
        # TODO: Implement proper message dialog

    def destroy(self):
        """Clean up"""
        self.main_frame.destroy()
