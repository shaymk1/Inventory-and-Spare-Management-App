"""
Spare Management Interface
Add, Edit, Delete, and View spares
"""

import customtkinter as ctk
import os
from tkinter import filedialog
from PIL import Image, ImageTk


class SpareManagement:
    def __init__(self, parent_frame, user_info):
        """
        Initialize spare management interface

        Args:
            parent_frame: Frame to pack this interface into
            user_info: Current user information
        """
        self.parent = parent_frame
        self.user_info = user_info
        self.current_image_path = None

        # Create main container
        self.main_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create tabbed interface
        self._create_tabview()

        # Load spares data
        self._load_spares()

    def _create_tabview(self):
        """Create tabbed interface for different functions"""
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True)

        # Add tabs
        self.tabview.add("View Spares")
        self.tabview.add("Add New")
        self.tabview.add("Edit/Delete")

        # Setup each tab
        self._setup_view_tab()
        self._setup_add_tab()
        self._setup_edit_tab()

    def _setup_view_tab(self):
        """Setup the 'View Spares' tab"""
        view_frame = self.tabview.tab("View Spares")

        # Search bar
        search_frame = ctk.CTkFrame(view_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(search_frame, text="Search:", font=("Arial", 12)).pack(
            side="left", padx=(0, 10)
        )

        self.search_entry = ctk.CTkEntry(
            search_frame, width=200, placeholder_text="Search by name or code"
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            search_frame, text="🔍 Search", width=80, command=self._search_spares
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            search_frame, text="🔄 Refresh", width=80, command=self._load_spares
        ).pack(side="left")

        # Spares table (using scrollable frame)
        table_frame = ctk.CTkFrame(view_frame)
        table_frame.pack(fill="both", expand=True)

        # Create scrollable frame for table
        self.spares_scroll = ctk.CTkScrollableFrame(table_frame, height=400)
        self.spares_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize table
        self.spares_table_frame = ctk.CTkFrame(
            self.spares_scroll, fg_color="transparent"
        )
        self.spares_table_frame.pack(fill="both", expand=True)

    def _setup_add_tab(self):
        """Setup the 'Add New' tab with scrollbar"""
        add_frame = self.tabview.tab("Add New")
        
        # Create scrollable frame for the entire tab
        scroll_frame = ctk.CTkScrollableFrame(add_frame, label_text="")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Form frame inside scrollable area
        form_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        ctk.CTkLabel(
            form_frame, text="➕ Add New Spare", font=("Arial", 18, "bold")
        ).pack(pady=20)

        # Form container
        fields_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_container.pack(pady=10, padx=20, fill="both", expand=True)

        # Row 0: Spare Name
        row = 0
        ctk.CTkLabel(fields_container, text="Spare Name:*", font=("Arial", 12)).grid(
            row=row, column=0, pady=10, padx=10, sticky="e"
        )
        self.name_entry = ctk.CTkEntry(fields_container, width=300)
        self.name_entry.grid(row=row, column=1, pady=10, padx=10, sticky="w")

        # Row 1: Spare Code
        row += 1
        ctk.CTkLabel(fields_container, text="Spare Code:*", font=("Arial", 12)).grid(
            row=row, column=0, pady=10, padx=10, sticky="e"
        )
        self.code_entry = ctk.CTkEntry(fields_container, width=300)
        self.code_entry.grid(row=row, column=1, pady=10, padx=10, sticky="w")

        # Row 2: Initial Quantity
        row += 1
        ctk.CTkLabel(
            fields_container, text="Initial Quantity:*", font=("Arial", 12)
        ).grid(row=row, column=0, pady=10, padx=10, sticky="e")
        self.quantity_entry = ctk.CTkEntry(fields_container, width=300)
        self.quantity_entry.insert(0, "0")
        self.quantity_entry.grid(row=row, column=1, pady=10, padx=10, sticky="w")

        # Row 3: Low Stock Threshold
        row += 1
        ctk.CTkLabel(
            fields_container, text="Low Stock Alert:*", font=("Arial", 12)
        ).grid(row=row, column=0, pady=10, padx=10, sticky="e")
        self.threshold_entry = ctk.CTkEntry(fields_container, width=300)
        self.threshold_entry.insert(0, "5")
        self.threshold_entry.grid(row=row, column=1, pady=10, padx=10, sticky="w")

        # Row 4: Location/Notes
        row += 1
        ctk.CTkLabel(fields_container, text="Location/Notes:", font=("Arial", 12)).grid(
            row=row, column=0, pady=10, padx=10, sticky="e"
        )
        self.notes_entry = ctk.CTkEntry(fields_container, width=300)
        self.notes_entry.grid(row=row, column=1, pady=10, padx=10, sticky="w")

        # Row 5: Image upload
        row += 1
        ctk.CTkLabel(fields_container, text="Spare Image:", font=("Arial", 12)).grid(
            row=row, column=0, pady=10, padx=10, sticky="e"
        )

        image_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
        image_frame.grid(row=row, column=1, pady=10, padx=10, sticky="w")

        self.image_label = ctk.CTkLabel(
            image_frame,
            text="📷 No image selected",
            font=("Arial", 12),
            text_color="gray",
        )
        self.image_label.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            image_frame, text="📁 Browse", width=80, command=self._browse_image
        ).pack(side="left")

        # Row 6: Add button
        row += 1
        button_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
        button_frame.grid(row=row, column=0, columnspan=2, pady=30)

        ctk.CTkButton(
            button_frame,
            text="✅ Add Spare",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#4CAF50",
            command=self._add_spare,
        ).pack()

        # Configure grid weights
        fields_container.grid_columnconfigure(1, weight=1)

    def _setup_edit_tab(self):
        """Setup the 'Edit/Delete' tab"""
        edit_frame = self.tabview.tab("Edit/Delete")

        ctk.CTkLabel(
            edit_frame, text="Select a spare to edit or delete", font=("Arial", 14)
        ).pack(pady=20)

        # Will implement edit/delete functionality in next step
        placeholder = ctk.CTkLabel(
            edit_frame,
            text="Edit/Delete functionality coming soon...",
            font=("Arial", 12),
            text_color="gray",
        )
        placeholder.pack(pady=100)

    def _browse_image(self):
        """Open file dialog to select image"""
        file_path = filedialog.askopenfilename(
            title="Select Spare Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")],
        )

        if file_path:
            self.current_image_path = file_path
            filename = os.path.basename(file_path)
            self.image_label.configure(
                text=f"📷 {filename[:20]}...", text_color="white"
            )

    def _add_spare(self):
        """Add new spare to database"""
        # Get values from form
        name = self.name_entry.get().strip()
        code = self.code_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        threshold = self.threshold_entry.get().strip()
        notes = self.notes_entry.get().strip()

        # Basic validation
        if not name or not code:
            self._show_message("❌ Error", "Name and Code are required!", "error")
            return

        try:
            quantity = int(quantity) if quantity else 0
            threshold = int(threshold) if threshold else 5
        except ValueError:
            self._show_message(
                "❌ Error", "Quantity and Threshold must be numbers!", "error"
            )
            return

        if quantity < 0 or threshold < 0:
            self._show_message(
                "❌ Error", "Quantity and Threshold cannot be negative!", "error"
            )
            return

        # Prepare image path
        image_path = None
        if self.current_image_path:
            # In production, you'd copy the image to a project folder
            image_path = self.current_image_path

        try:
            # Import database module
            from logic.db import db

            # Insert into database
            db.execute(
                """
                INSERT INTO spares (name, code, quantity, low_stock_threshold, image_path, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
                """,
                (name, code, quantity, threshold, image_path),
            )

            # Clear form
            self.name_entry.delete(0, "end")
            self.code_entry.delete(0, "end")
            self.quantity_entry.delete(0, "end")
            self.quantity_entry.insert(0, "0")
            self.threshold_entry.delete(0, "end")
            self.threshold_entry.insert(0, "5")
            self.notes_entry.delete(0, "end")
            self.image_label.configure(text="📷 No image selected", text_color="gray")
            self.current_image_path = None

            # Show success message
            self._show_message(
                "✅ Success", f"Spare '{name}' added successfully!", "success"
            )

            # Refresh spares list
            self._load_spares()

        except Exception as e:
            self._show_message(
                "❌ Database Error", f"Failed to add spare: {str(e)}", "error"
            )

    def _load_spares(self):
        """Load and display spares from database"""
        try:
            # Clear current table
            for widget in self.spares_table_frame.winfo_children():
                widget.destroy()

            # Import database
            from logic.db import db

            # Query spares
            spares = db.execute(
                "SELECT id, name, code, quantity, low_stock_threshold FROM spares WHERE is_active = 1 ORDER BY name",
                fetch=True,
            )

            if not spares:
                # No spares message
                ctk.CTkLabel(
                    self.spares_table_frame,
                    text="No spares found. Add your first spare!",
                    font=("Arial", 14),
                    text_color="gray",
                ).pack(pady=50)
                return

            # Create table headers
            headers = ["ID", "Name", "Code", "Quantity", "Low Stock", "Status"]
            for col, header in enumerate(headers):
                label = ctk.CTkLabel(
                    self.spares_table_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=100 if col < 2 else 80,
                )
                label.grid(row=0, column=col, padx=5, pady=10, sticky="w")

            # Add spares rows
            for row, spare in enumerate(spares, start=1):
                # Determine status color
                quantity = spare["quantity"]
                threshold = spare["low_stock_threshold"]

                if quantity == 0:
                    status = "❌ Out of Stock"
                    status_color = "red"
                elif quantity <= threshold:
                    status = "⚠️ Low Stock"
                    status_color = "orange"
                else:
                    status = "✅ In Stock"
                    status_color = "green"

                # Display row
                data = [
                    spare["id"],
                    spare["name"][:20] + ("..." if len(spare["name"]) > 20 else ""),
                    spare["code"],
                    str(spare["quantity"]),
                    str(spare["low_stock_threshold"]),
                    status,
                ]

                for col, value in enumerate(data):
                    label = ctk.CTkLabel(
                        self.spares_table_frame,
                        text=value,
                        font=("Arial", 11),
                        width=100 if col < 2 else 80,
                        text_color=status_color if col == 5 else "white",
                    )
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="w")

        except Exception as e:
            print(f"Error loading spares: {e}")
            ctk.CTkLabel(
                self.spares_table_frame,
                text=f"Error loading spares: {str(e)}",
                font=("Arial", 12),
                text_color="orange",
            ).pack(pady=50)

    def _search_spares(self):
        """Search spares by name or code"""
        search_term = self.search_entry.get().strip().lower()

        if not search_term:
            self._load_spares()
            return

        try:
            # Clear current table
            for widget in self.spares_table_frame.winfo_children():
                widget.destroy()

            from logic.db import db

            # Search in database
            spares = db.execute(
                """
                SELECT id, name, code, quantity, low_stock_threshold 
                FROM spares 
                WHERE is_active = 1 
                AND (LOWER(name) LIKE ? OR LOWER(code) LIKE ?)
                ORDER BY name
                """,
                (f"%{search_term}%", f"%{search_term}%"),
                fetch=True,
            )

            if not spares:
                ctk.CTkLabel(
                    self.spares_table_frame,
                    text=f"No spares found for '{search_term}'",
                    font=("Arial", 14),
                    text_color="gray",
                ).pack(pady=50)
                return

            # Create table headers
            headers = ["ID", "Name", "Code", "Quantity", "Low Stock", "Status"]
            for col, header in enumerate(headers):
                label = ctk.CTkLabel(
                    self.spares_table_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=100 if col < 2 else 80,
                )
                label.grid(row=0, column=col, padx=5, pady=10, sticky="w")

            # Add search results
            for row, spare in enumerate(spares, start=1):
                quantity = spare["quantity"]
                threshold = spare["low_stock_threshold"]

                if quantity == 0:
                    status = "❌ Out of Stock"
                    status_color = "red"
                elif quantity <= threshold:
                    status = "⚠️ Low Stock"
                    status_color = "orange"
                else:
                    status = "✅ In Stock"
                    status_color = "green"

                data = [
                    spare["id"],
                    spare["name"][:20] + ("..." if len(spare["name"]) > 20 else ""),
                    spare["code"],
                    str(spare["quantity"]),
                    str(spare["low_stock_threshold"]),
                    status,
                ]

                for col, value in enumerate(data):
                    label = ctk.CTkLabel(
                        self.spares_table_frame,
                        text=value,
                        font=("Arial", 11),
                        width=100 if col < 2 else 80,
                        text_color=status_color if col == 5 else "white",
                    )
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="w")

        except Exception as e:
            print(f"Error searching spares: {e}")

    def _show_message(self, title, message, msg_type="info"):
        """Show message dialog"""
        # For now, just print to console
        print(f"{title}: {message}")

        # In future, implement proper message box
        # You can use: CTkMessagebox or create custom dialog

    def destroy(self):
        """Clean up"""
        self.main_frame.destroy()
