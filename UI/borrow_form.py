"""
Borrow Items Interface
"""

import customtkinter as ctk
from logic.db import db


class BorrowForm:
    def __init__(self, parent_frame, user_info):
        """
        Initialize borrow interface

        Args:
            parent_frame: Frame to pack this interface into
            user_info: Current user information (for logging)
        """
        self.parent = parent_frame
        self.user_info = user_info
        self.current_spares = []  # Will store loaded spares

        # Create main container
        self.main_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Load initial data
        self._load_spares()
        self._create_form()

    def _load_spares(self):
        """Load available spares from database"""
        try:
            # Get all active spares with quantity > 0
            self.current_spares = db.execute(
                "SELECT id, name, code, quantity FROM spares WHERE is_active = 1 AND quantity > 0 ORDER BY name",
                fetch=True,
            )
        except Exception as e:
            print(f"Error loading spares: {e}")
            self.current_spares = []

    def _create_form(self):
        """Create the borrow form"""
        # Title
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(pady=(0, 30))

        ctk.CTkLabel(
            title_frame, text="⬇️ Borrow Items", font=("Arial", 22, "bold")
        ).pack()

        ctk.CTkLabel(
            title_frame,
            text="Borrow items from inventory",
            font=("Arial", 14),
            text_color="gray",
        ).pack(pady=(5, 0))

        # Main form container
        form_container = ctk.CTkFrame(self.main_frame, corner_radius=10)
        form_container.pack(fill="both", expand=True, padx=50, pady=10)

        # Use grid for better alignment
        form_container.grid_columnconfigure(1, weight=1)

        # Row 0: Select Spare
        row = 0
        ctk.CTkLabel(
            form_container, text="Select Spare:*", font=("Arial", 14, "bold")
        ).grid(row=row, column=0, padx=20, pady=15, sticky="w")

        # Create spare selection dropdown
        if self.current_spares:
            spare_options = [
                f"{spare['name']} ({spare['code']}) - Qty: {spare['quantity']}"
                for spare in self.current_spares
            ]
            self.spare_var = ctk.StringVar(value="Select a spare...")
            self.spare_combo = ctk.CTkComboBox(
                form_container,
                values=spare_options,
                variable=self.spare_var,
                width=350,
                state="readonly",
            )
            self.spare_combo.grid(row=row, column=1, padx=20, pady=15, sticky="w")

            # Bind selection change to update available quantity
            self.spare_combo.bind("<<ComboboxSelected>>", self._update_quantity_info)
        else:
            ctk.CTkLabel(
                form_container,
                text="No available spares found",
                font=("Arial", 12),
                text_color="orange",
            ).grid(row=row, column=1, padx=20, pady=15, sticky="w")
            self.spare_combo = None

        # Row 1: Available Quantity Info
        row += 1
        self.quantity_info_label = ctk.CTkLabel(
            form_container,
            text="Available quantity: --",
            font=("Arial", 12),
            text_color="gray",
        )
        self.quantity_info_label.grid(
            row=row, column=1, padx=20, pady=(0, 15), sticky="w"
        )

        # Row 2: Quantity to Borrow
        row += 1
        ctk.CTkLabel(
            form_container, text="Quantity to Borrow:*", font=("Arial", 14, "bold")
        ).grid(row=row, column=0, padx=20, pady=15, sticky="w")

        self.quantity_entry = ctk.CTkEntry(
            form_container, width=150, placeholder_text="Enter quantity"
        )
        self.quantity_entry.grid(row=row, column=1, padx=20, pady=15, sticky="w")

        # Row 3: Borrower
        row += 1
        ctk.CTkLabel(
            form_container, text="Borrower Name:*", font=("Arial", 14, "bold")
        ).grid(row=row, column=0, padx=20, pady=15, sticky="w")

        self.borrower_entry = ctk.CTkEntry(
            form_container, width=350, placeholder_text="Enter borrower name"
        )
        self.borrower_entry.grid(row=row, column=1, padx=20, pady=15, sticky="w")

        # Row 4: Purpose/Notes
        row += 1
        ctk.CTkLabel(
            form_container, text="Purpose/Notes:", font=("Arial", 14, "bold")
        ).grid(row=row, column=0, padx=20, pady=15, sticky="nw")

        self.notes_text = ctk.CTkTextbox(form_container, width=350, height=100)
        self.notes_text.grid(row=row, column=1, padx=20, pady=15, sticky="w")

        # Row 5: Buttons
        row += 1
        button_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        button_frame.grid(row=row, column=0, columnspan=2, pady=40)

        ctk.CTkButton(
            button_frame,
            text="✅ Borrow Items",
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#2196F3",
            command=self._process_borrow,
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="🔄 Reset Form",
            width=150,
            height=45,
            font=("Arial", 14),
            fg_color="gray",
            command=self._reset_form,
        ).pack(side="left", padx=10)

    def _update_quantity_info(self, event=None):
        """Update the available quantity display when spare is selected"""
        if not self.spare_combo or not self.current_spares:
            return

        selected_index = self.spare_combo.current()
        if selected_index >= 0 and selected_index < len(self.current_spares):
            spare = self.current_spares[selected_index]
            self.quantity_info_label.configure(
                text=f"Available quantity: {spare['quantity']}", text_color="green"
            )

    def _reset_form(self):
        """Reset the form to initial state"""
        if self.spare_combo:
            self.spare_var.set("Select a spare...")
        self.quantity_entry.delete(0, "end")
        self.borrower_entry.delete(0, "end")
        self.notes_text.delete("1.0", "end")
        self.quantity_info_label.configure(
            text="Available quantity: --", text_color="gray"
        )

    def _process_borrow(self):
        """Process the borrow request"""
        # Get form values
        if not self.spare_combo:
            self._show_error("No spares available to borrow")
            return

        selected_index = self.spare_combo.current()
        if selected_index < 0:
            self._show_error("Please select a spare")
            return

        spare = self.current_spares[selected_index]
        spare_id = spare["id"]
        spare_name = spare["name"]
        available_qty = spare["quantity"]

        # Get quantity to borrow
        qty_text = self.quantity_entry.get().strip()
        if not qty_text:
            self._show_error("Please enter quantity to borrow")
            return

        try:
            borrow_qty = int(qty_text)
            if borrow_qty <= 0:
                self._show_error("Quantity must be greater than 0")
                return
            if borrow_qty > available_qty:
                self._show_error(f"Cannot borrow more than available ({available_qty})")
                return
        except ValueError:
            self._show_error("Quantity must be a number")
            return

        # Get borrower name
        borrower = self.borrower_entry.get().strip()
        if not borrower:
            self._show_error("Please enter borrower name")
            return

        # Get notes
        notes = self.notes_text.get("1.0", "end-1c").strip()

        try:
            # Start transaction
            # 1. Update spare quantity
            db.execute(
                "UPDATE spares SET quantity = quantity - ? WHERE id = ?",
                (borrow_qty, spare_id),
            )

            # 2. Log movement
            db.execute(
                """
                INSERT INTO movements (spare_id, user_id, quantity, movement_type, notes)
                VALUES (?, ?, ?, 'borrow', ?)
                """,
                (
                    spare_id,
                    self.user_info.get("id", 1),
                    borrow_qty,
                    notes or f"Borrowed by {borrower}",
                ),
            )

            # Show success message
            self._show_success(f"Successfully borrowed {borrow_qty} of {spare_name}")

            # Reset form and reload spares
            self._reset_form()
            self._load_spares()

            # Update dropdown if needed
            if self.spare_combo:
                spare_options = [
                    f"{s['name']} ({s['code']}) - Qty: {s['quantity']}"
                    for s in self.current_spares
                ]
                self.spare_combo.configure(values=spare_options)

        except Exception as e:
            self._show_error(f"Database error: {str(e)}")

    def _show_error(self, message):
        """Show error message (placeholder - implement proper dialog later)"""
        print(f"❌ Error: {message}")
        # TODO: Implement proper error dialog

    def _show_success(self, message):
        """Show success message (placeholder)"""
        print(f"✅ Success: {message}")
        # TODO: Implement proper success dialog

    def destroy(self):
        """Clean up"""
        self.main_frame.destroy()
