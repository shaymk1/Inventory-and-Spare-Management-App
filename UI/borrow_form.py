"""
Borrow Items Interface
"""

import customtkinter as ctk
from logic.db import db
from UI.components.message_dialog import MessageDialog
from datetime import datetime


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
        
        # Add history button next to other buttons
        ctk.CTkButton(
            button_frame,
            text="📜 View History",
            width=150,
            height=45,
            font=("Arial", 14),
            fg_color="#9C27B0",
            command=self.show_borrow_history
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
            MessageDialog.show_error(self.main_frame, "Error", "No spares available to borrow")
            return
        
        selected_index = self.spare_combo.current()
        if selected_index < 0:
            MessageDialog.show_error(self.main_frame, "Error", "Please select a spare")
            return
        
        spare = self.current_spares[selected_index]
        spare_id = spare['id']
        spare_name = spare['name']
        available_qty = spare['quantity']
        
        # Get quantity to borrow
        qty_text = self.quantity_entry.get().strip()
        if not qty_text:
            MessageDialog.show_error(self.main_frame, "Error", "Please enter quantity to borrow")
            return
        
        try:
            borrow_qty = int(qty_text)
            if borrow_qty <= 0:
                MessageDialog.show_error(self.main_frame, "Error", "Quantity must be greater than 0")
                return
            if borrow_qty > available_qty:
                MessageDialog.show_error(
                    self.main_frame,
                    "Error",
                    f"Cannot borrow more than available!\n\nAvailable: {available_qty}\nRequested: {borrow_qty}"
                )
                return
        except ValueError:
            MessageDialog.show_error(self.main_frame, "Error", "Quantity must be a number")
            return
        
        # Get borrower name
        borrower = self.borrower_entry.get().strip()
        if not borrower:
            MessageDialog.show_error(self.main_frame, "Error", "Please enter borrower name")
            return
        
        # Get notes
        notes = self.notes_text.get("1.0", "end-1c").strip()
        
        # Show confirmation dialog
        MessageDialog.show_confirm(
            self.main_frame,
            "Confirm Borrow",
            f"Borrow {borrow_qty} of {spare_name}?\n\nBorrower: {borrower}\nNotes: {notes[:50]}...",
            lambda: self._execute_borrow(spare_id, spare_name, borrow_qty, borrower, notes)
        )
    
       def _process_borrow(self):
        """Process the borrow request"""
        # Get form values
        if not self.spare_combo:
            MessageDialog.show_error(self.main_frame, "Error", "No spares available to borrow")
            return
        
        selected_index = self.spare_combo.current()
        if selected_index < 0:
            MessageDialog.show_error(self.main_frame, "Error", "Please select a spare")
            return
        
        spare = self.current_spares[selected_index]
        spare_id = spare['id']
        spare_name = spare['name']
        available_qty = spare['quantity']
        
        # Get quantity to borrow
        qty_text = self.quantity_entry.get().strip()
        if not qty_text:
            MessageDialog.show_error(self.main_frame, "Error", "Please enter quantity to borrow")
            return
        
        try:
            borrow_qty = int(qty_text)
            if borrow_qty <= 0:
                MessageDialog.show_error(self.main_frame, "Error", "Quantity must be greater than 0")
                return
            if borrow_qty > available_qty:
                MessageDialog.show_error(
                    self.main_frame,
                    "Error",
                    f"Cannot borrow more than available!\n\nAvailable: {available_qty}\nRequested: {borrow_qty}"
                )
                return
        except ValueError:
            MessageDialog.show_error(self.main_frame, "Error", "Quantity must be a number")
            return
        
        # Get borrower name
        borrower = self.borrower_entry.get().strip()
        if not borrower:
            MessageDialog.show_error(self.main_frame, "Error", "Please enter borrower name")
            return
        
        # Get notes
        notes = self.notes_text.get("1.0", "end-1c").strip()
        
        # Show confirmation dialog
        MessageDialog.show_confirm(
            self.main_frame,
            "Confirm Borrow",
            f"Borrow {borrow_qty} of {spare_name}?\n\nBorrower: {borrower}\nNotes: {notes[:50]}...",
            lambda: self._execute_borrow(spare_id, spare_name, borrow_qty, borrower, notes)
        )
        def _process_borrow(self):
        """Process the borrow request"""
        # Get form values
        if not self.spare_combo:
            MessageDialog.show_error(self.main_frame, "Error", "No spares available to borrow")
            return
        
        selected_index = self.spare_combo.current()
        if selected_index < 0:
            MessageDialog.show_error(self.main_frame, "Error", "Please select a spare")
            return
        
        spare = self.current_spares[selected_index]
        spare_id = spare['id']
        spare_name = spare['name']
        available_qty = spare['quantity']
        
        # Get quantity to borrow
        qty_text = self.quantity_entry.get().strip()
        if not qty_text:
            MessageDialog.show_error(self.main_frame, "Error", "Please enter quantity to borrow")
            return
        
        try:
            borrow_qty = int(qty_text)
            if borrow_qty <= 0:
                MessageDialog.show_error(self.main_frame, "Error", "Quantity must be greater than 0")
                return
            if borrow_qty > available_qty:
                MessageDialog.show_error(
                    self.main_frame,
                    "Error",
                    f"Cannot borrow more than available!\n\nAvailable: {available_qty}\nRequested: {borrow_qty}"
                )
                return
        except ValueError:
            MessageDialog.show_error(self.main_frame, "Error", "Quantity must be a number")
            return
        
        # Get borrower name
        borrower = self.borrower_entry.get().strip()
        if not borrower:
            MessageDialog.show_error(self.main_frame, "Error", "Please enter borrower name")
            return
        
        # Get notes
        notes = self.notes_text.get("1.0", "end-1c").strip()
        
        # Show confirmation dialog
        MessageDialog.show_confirm(
            self.main_frame,
            "Confirm Borrow",
            f"Borrow {borrow_qty} of {spare_name}?\n\nBorrower: {borrower}\nNotes: {notes[:50]}...",
            lambda: self._execute_borrow(spare_id, spare_name, borrow_qty, borrower, notes)
        )
    def _process_borrow(self):
        """Process the borrow request"""
        # Get form values
        if not self.spare_combo:
            MessageDialog.show_error(self.main_frame, "Error", "No spares available to borrow")
            return
        
        selected_index = self.spare_combo.current()
        if selected_index < 0:
            MessageDialog.show_error(self.main_frame, "Error", "Please select a spare")
            return
        
        spare = self.current_spares[selected_index]
        spare_id = spare['id']
        spare_name = spare['name']
        available_qty = spare['quantity']
        
        # Get quantity to borrow
        qty_text = self.quantity_entry.get().strip()
        if not qty_text:
            MessageDialog.show_error(self.main_frame, "Error", "Please enter quantity to borrow")
            return
        try:
            borrow_qty = int(qty_text)
            if borrow_qty <= 0:
                MessageDialog.show_error(self.main_frame, "Error", "Quantity must be greater than 0")
                return
            if borrow_qty > available_qty:
                MessageDialog.show_error(
                    self.main_frame,
                    "Error",
                    f"Cannot borrow more than available!\n\nAvailable: {available_qty}\nRequested: {borrow_qty}"
                )
                return
        except ValueError:
            MessageDialog.show_error(self.main_frame, "Error", "Quantity must be a number")
            return
        
        # Get borrower name
        borrower = self.borrower_entry.get().strip()
        if not borrower:
            MessageDialog.show_error(self.main_frame, "Error", "Please enter borrower name")
            return
        
        # Get notes
        notes = self.notes_text.get("1.0", "end-1c").strip()
        # Show confirmation dialog
        MessageDialog.show_confirm(
            self.main_frame,
            "Confirm Borrow",
            f"Borrow {borrow_qty} of {spare_name}?\n\nBorrower: {borrower}\nNotes: {notes[:50]}...",
            lambda: self._execute_borrow(spare_id, spare_name, borrow_qty, borrower, notes)
        )
    def _execute_borrow(self, spare_id, spare_name, borrow_qty, borrower, notes):
        """Execute the borrow transaction after confirmation"""
        try:
            # 1. Update spare quantity
            db.execute(
                "UPDATE spares SET quantity = quantity - ? WHERE id = ?",
                (borrow_qty, spare_id)
            )
            
            # 2. Log movement
            db.execute(
                """
                INSERT INTO movements (spare_id, user_id, quantity, movement_type, notes)
                VALUES (?, 1, ?, 'borrow', ?)
                """,
                (spare_id, borrow_qty, notes or f"Borrowed by {borrower}")
            )
            
            # Show success message
            MessageDialog.show_success(
                self.main_frame,
                "Success",
                f"✅ Successfully borrowed {borrow_qty} of {spare_name}!\n\nBorrower: {borrower}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            
            # Reset form and reload spares
            self._reset_form()
            self._load_spares()
            
            # Update dropdown if needed
            if self.spare_combo:
                spare_options = [f"{s['name']} ({s['code']}) - Qty: {s['quantity']}" 
                               for s in self.current_spares]
                self.spare_combo.configure(values=spare_options)
            
        except Exception as e:
            MessageDialog.show_error(
                self.main_frame,
                "Database Error",
                f"Failed to process borrow:\n{str(e)}"
            )
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
    def show_borrow_history(self):
        """Show borrow history (optional - can be called from a button)"""
        try:
            # Get borrow history
            history = db.execute(
                """
                SELECT 
                    m.id,
                    s.name as spare_name,
                    s.code as spare_code,
                    m.quantity,
                    m.movement_date,
                    m.notes,
                    m.returned_quantity
                FROM movements m
                JOIN spares s ON m.spare_id = s.id
                WHERE m.movement_type = 'borrow'
                ORDER BY m.movement_date DESC
                LIMIT 50
                """,
                fetch=True
            )
            
            if not history:
                MessageDialog.show_info(self.main_frame, "History", "No borrow history found")
                return
            
            # Create history dialog
            dialog = ctk.CTkToplevel(self.main_frame)
            dialog.title("Borrow History")
            dialog.geometry("800x500")
            dialog.resizable(True, True)
            
            # Center dialog
            dialog.update_idletasks()
            width = dialog.winfo_width()
            height = dialog.winfo_height()
            x = (self.main_frame.winfo_screenwidth() // 2) - (width // 2)
            y = (self.main_frame.winfo_screenheight() // 2) - (height // 2)
            dialog.geometry(f"{width}x{height}+{x}+{y}")
            
            # Title
            ctk.CTkLabel(
                dialog,
                text="📜 Borrow History",
                font=("Arial", 18, "bold")
            ).pack(pady=(15, 10))
            
            # Create scrollable table
            scroll_frame = ctk.CTkScrollableFrame(dialog, height=400)
            scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            # Table headers
            headers = ["Date", "Spare", "Quantity", "Returned", "Status", "Notes"]
            for col, header in enumerate(headers):
                label = ctk.CTkLabel(
                    scroll_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=120
                )
                label.grid(row=0, column=col, padx=5, pady=10, sticky="w")
            
            # Add history rows
            for row, record in enumerate(history, start=1):
                # Format date
                date_str = record['movement_date']
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        display_date = date_obj.strftime('%b %d, %Y %H:%M')
                    except:
                        display_date = date_str
                else:
                    display_date = "N/A"
                
                # Determine status
                returned = record['returned_quantity'] or 0
                borrowed = record['quantity']
                
                if returned >= borrowed:
                    status = "✅ Returned"
                    status_color = "green"
                elif returned > 0:
                    status = "🔄 Partially Returned"
                    status_color = "orange"
                else:
                    status = "⏳ Pending"
                    status_color = "gray"
                
                # Display data
                data = [
                    display_date,
                    f"{record['spare_name']}\n({record['spare_code']})",
                    str(borrowed),
                    str(returned),
                    status,
                    (record['notes'] or "")[:30] + ("..." if len(record['notes'] or "") > 30 else "")
                ]
                
                for col, value in enumerate(data):
                    label = ctk.CTkLabel(
                        scroll_frame,
                        text=value,
                        font=("Arial", 11),
                        width=120,
                        text_color=status_color if col == 4 else "white"
                    )
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            
            # Close button
            ctk.CTkButton(
                dialog,
                text="Close",
                width=100,
                command=dialog.destroy
            ).pack(pady=(0, 15))
            
        except Exception as e:
            MessageDialog.show_error(self.main_frame, "Error", f"Failed to load history:\n{str(e)}")
