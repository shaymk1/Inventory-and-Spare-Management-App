"""
Spare Management Interface
Add, Edit, Delete, and View spares
"""

import customtkinter as ctk
import os
from tkinter import filedialog

# from PIL import Image, ImageTk  # for image handling
from UI.components.message_dialog import MessageDialog


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

        # Create tabbed interface (ONLY 2 TABS NOW)
        self._create_tabview()

        # Load spares data
        self._load_spares()

    def _create_tabview(self):
        """Create tabbed interface for different functions - EDIT TAB REMOVED"""
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True)

        # Add ONLY 2 tabs now (removed Edit/Delete)
        self.tabview.add("View Spares")
        self.tabview.add("Add New")

        # Setup each tab
        self._setup_view_tab()
        self._setup_add_tab()
        # NO MORE EDIT TAB!

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

        # Instruction label
        instruction_frame = ctk.CTkFrame(view_frame, fg_color="transparent", height=30)
        instruction_frame.pack(fill="x", pady=(5, 10))

        ctk.CTkLabel(
            instruction_frame,
            text="💡 Double-click any spare to edit or delete",
            font=("Arial", 12),
            text_color="#4FC3F7",
        ).pack()

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

    # The _setup_edit_tab method has been REMOVED entirely

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
        category = self.category_var.get()

        # Basic validation
        if not name or not code:
            MessageDialog.show_error(
                self.main_frame, "Error", "Name and Code are required!"
            )
            return

        try:
            quantity = int(quantity) if quantity else 0
            threshold = int(threshold) if threshold else 5
        except ValueError:
            MessageDialog.show_error(
                self.main_frame, "Error", "Quantity and Threshold must be numbers!"
            )
            return

        if quantity < 0 or threshold < 0:
            MessageDialog.show_error(
                self.main_frame, "Error", "Quantity and Threshold cannot be negative!"
            )
            return

        # Prepare image path
        image_path = None
        if self.current_image_path:
            image_path = self.current_image_path

        try:
            from logic.db import db

            # Check if code already exists
            existing = db.execute(
                "SELECT id FROM spares WHERE code = ? AND is_active = 1",
                (code,),
                fetch=True,
            )

            if existing:
                MessageDialog.show_error(
                    self.main_frame, "Error", f"Spare code '{code}' already exists!"
                )
                return

            # Insert into database (add category to notes or create new column?)
            # For now, prepend category to notes
            full_notes = f"[{category}] {notes}" if notes else f"[{category}]"

            db.execute(
                """
                INSERT INTO spares (name, code, quantity, low_stock_threshold, image_path, notes, is_active)
                VALUES (?, ?, ?, ?, ?, ?, 1)  
                """,
                (name, code, quantity, threshold, image_path, full_notes),
            )

            # Clear form but keep category selected
            self.name_entry.delete(0, "end")
            self.quantity_entry.delete(0, "end")
            self.quantity_entry.insert(0, "0")
            self.threshold_entry.delete(0, "end")
            self.threshold_entry.insert(0, "5")
            self.notes_entry.delete(0, "end")
            self.image_label.configure(text="📷 No image selected", text_color="gray")
            self.current_image_path = None

            # Generate next code automatically
            self._generate_code_from_category()

            # Show success message
            MessageDialog.show_success(
                self.main_frame,
                "Success",
                f"Spare '{name}' added successfully!\n\n"
                f"Category: {category}\n"
                f"Code: {code}\n"
                f"Quantity: {quantity}",
            )

            # FIX 2: Switch back to View Spares tab
            self.tabview.set("View Spares")

            # Refresh spares list
            self._load_spares()

            # Clear search entry if it has any text
            if hasattr(self, "search_entry"):
                self.search_entry.delete(0, "end")

        except Exception as e:
            MessageDialog.show_error(
                self.main_frame, "Database Error", f"Failed to add spare:\n{str(e)}"
            )

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
                SELECT id, name, code, quantity, low_stock_threshold, notes 
                FROM spares 
                WHERE is_active = 1 
                AND (LOWER(name) LIKE ? OR LOWER(code) LIKE ?)
                ORDER BY name
                """,
                (f"%{search_term}%", f"%{search_term}%"),
                fetch=True,
            )

            if not spares:
                # Show no results message
                no_results_frame = ctk.CTkFrame(
                    self.spares_table_frame, fg_color="transparent"
                )
                no_results_frame.pack(pady=50, expand=True)

                ctk.CTkLabel(
                    no_results_frame,
                    text=f"🔍 No spares found for '{search_term}'",
                    font=("Arial", 16),
                    text_color="gray",
                ).pack()

                ctk.CTkButton(
                    no_results_frame,
                    text="🔄 Clear Search",
                    width=150,
                    height=35,
                    font=("Arial", 12),
                    command=self._clear_search,
                ).pack(pady=10)
                return

            # Define column widths (same as main view)
            col_widths = [50, 200, 100, 80, 100, 100]

            # Create header row
            headers = ["ID", "Name", "Code", "Qty", "Threshold", "Status"]
            for col, (header, width) in enumerate(zip(headers, col_widths)):
                header_label = ctk.CTkLabel(
                    self.spares_table_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=width,
                    anchor="w",
                    fg_color="#2b2b2b",
                    corner_radius=4,
                )
                header_label.grid(row=0, column=col, padx=2, pady=(0, 10), sticky="w")

            # Add search results (MAKE THEM CLICKABLE)
            for row, spare in enumerate(spares, start=1):
                # Determine status
                quantity = spare["quantity"]
                threshold = spare["low_stock_threshold"]

                if quantity == 0:
                    status = "❌ Out of Stock"
                    status_color = "#F44336"
                elif quantity <= threshold:
                    status = "⚠️ Low Stock"
                    status_color = "#FF9800"
                else:
                    status = "✅ In Stock"
                    status_color = "#4CAF50"

                # Alternate row colors
                row_bg = "#1a1a1a" if row % 2 == 0 else "#2b2b2b"

                data = [
                    str(spare["id"]),
                    spare["name"][:30] + ("..." if len(spare["name"]) > 30 else ""),
                    spare["code"],
                    str(spare["quantity"]),
                    str(spare["low_stock_threshold"]),
                    status,
                ]

                # Create CLICKABLE labels for each column
                for col, (value, width) in enumerate(zip(data, col_widths)):
                    label = ctk.CTkLabel(
                        self.spares_table_frame,
                        text=value,
                        font=("Arial", 11),
                        width=width,
                        height=32,
                        anchor="w",
                        text_color=status_color if col == 5 else "white",
                        fg_color=row_bg,
                        corner_radius=0,
                        cursor="hand2",
                    )
                    label.grid(row=row, column=col, padx=2, pady=1, sticky="w")

                    # Make it clickable
                    label.bind(
                        "<Button-1>", lambda e, s=spare: self._open_edit_dialog(s)
                    )

                    # Hover effect
                    def on_enter(e, lbl=label, bg=row_bg):
                        lbl.configure(fg_color="#3a3a3a")

                    def on_leave(e, lbl=label, bg=row_bg):
                        lbl.configure(fg_color=bg)

                    label.bind("<Enter>", on_enter)
                    label.bind("<Leave>", on_leave)

            # Configure grid columns
            for col, width in enumerate(col_widths):
                self.spares_table_frame.grid_columnconfigure(
                    col, minsize=width, weight=0
                )

            # Add search result count and clear button
            result_frame = ctk.CTkFrame(self.spares_table_frame, fg_color="transparent")
            result_frame.grid(
                row=len(spares) + 1, column=0, columnspan=6, pady=(15, 5), sticky="ew"
            )

            ctk.CTkLabel(
                result_frame,
                text=f"Found {len(spares)} result(s) for '{search_term}'",
                font=("Arial", 11),
                text_color="#888888",
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                result_frame,
                text="✖ Clear Search",
                width=100,
                height=25,
                font=("Arial", 10),
                fg_color="gray",
                command=self._clear_search,
            ).pack(side="right", padx=5)

        except Exception as e:
            print(f"Error searching spares: {e}")
            MessageDialog.show_error(
                self.main_frame, "Search Error", f"Failed to search: {str(e)}"
            )

    def _clear_search(self):
        """Clear search and return to full spare list"""
        # Clear the search entry
        if hasattr(self, "search_entry"):
            self.search_entry.delete(0, "end")

        # Reload all spares
        self._load_spares()

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
                "SELECT id, name, code, quantity, low_stock_threshold, notes FROM spares WHERE is_active = 1 ORDER BY name",
                fetch=True,
            )

            if not spares:
                # No spares message (same as before)
                no_spares_frame = ctk.CTkFrame(
                    self.spares_table_frame, fg_color="transparent"
                )
                no_spares_frame.pack(pady=50, expand=True)

                ctk.CTkLabel(
                    no_spares_frame,
                    text="📦 No spares found",
                    font=("Arial", 16),
                    text_color="gray",
                ).pack()

                ctk.CTkLabel(
                    no_spares_frame,
                    text="Click 'Add New' tab to create your first spare!",
                    font=("Arial", 12),
                    text_color="gray",
                ).pack(pady=10)

                ctk.CTkButton(
                    no_spares_frame,
                    text="➕ Add New Spare",
                    width=150,
                    height=35,
                    font=("Arial", 12),
                    fg_color="#4CAF50",
                    command=lambda: self.tabview.set("Add New"),
                ).pack(pady=10)
                return

            # Define column widths (FIXED widths for alignment)
            col_widths = [50, 200, 100, 80, 100, 100]

            # Create header row IN THE SAME GRID as data rows
            headers = ["ID", "Name", "Code", "Qty", "Threshold", "Status"]
            for col, (header, width) in enumerate(zip(headers, col_widths)):
                header_label = ctk.CTkLabel(
                    self.spares_table_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=width,
                    anchor="w",
                    fg_color="#2b2b2b",
                    corner_radius=4,
                )
                header_label.grid(row=0, column=col, padx=2, pady=(0, 10), sticky="w")

            # Add spares rows
            for row, spare in enumerate(spares, start=1):
                # Determine status color
                quantity = spare["quantity"]
                threshold = spare["low_stock_threshold"]

                if quantity == 0:
                    status = "❌ Out of Stock"
                    status_color = "#F44336"
                elif quantity <= threshold:
                    status = "⚠️ Low Stock"
                    status_color = "#FF9800"
                else:
                    status = "✅ In Stock"
                    status_color = "#4CAF50"

                # Alternate row colors
                row_bg = "#1a1a1a" if row % 2 == 0 else "#2b2b2b"

                # Display data in each column (SAME GRID as headers)
                data = [
                    str(spare["id"]),
                    spare["name"][:30] + ("..." if len(spare["name"]) > 30 else ""),
                    spare["code"],
                    str(spare["quantity"]),
                    str(spare["low_stock_threshold"]),
                    status,
                ]

                # Create clickable labels for each column
                for col, (value, width) in enumerate(zip(data, col_widths)):
                    label = ctk.CTkLabel(
                        self.spares_table_frame,
                        text=value,
                        font=("Arial", 11),
                        width=width,
                        height=32,
                        anchor="w",
                        text_color=status_color if col == 5 else "white",
                        fg_color=row_bg,
                        corner_radius=0,
                        cursor="hand2",
                    )
                    label.grid(row=row, column=col, padx=2, pady=1, sticky="w")

                    # Make label clickable
                    label.bind(
                        "<Button-1>", lambda e, s=spare: self._open_edit_dialog(s)
                    )

                    # Hover effect
                    def on_enter(e, lbl=label, bg=row_bg):
                        lbl.configure(fg_color="#3a3a3a")

                    def on_leave(e, lbl=label, bg=row_bg):
                        lbl.configure(fg_color=bg)

                    label.bind("<Enter>", on_enter)
                    label.bind("<Leave>", on_leave)

            # Configure grid columns to maintain widths
            for col, width in enumerate(col_widths):
                self.spares_table_frame.grid_columnconfigure(
                    col, minsize=width, weight=0
                )

            # Add instruction label
            instruction_label = ctk.CTkLabel(
                self.spares_table_frame,
                text="💡 Double-click any spare to edit or delete",
                font=("Arial", 11),
                text_color="#888888",
            )
            instruction_label.grid(
                row=len(spares) + 1, column=0, columnspan=6, pady=(15, 5)
            )

        except Exception as e:
            print(f"Error loading spares: {e}")
            error_frame = ctk.CTkFrame(self.spares_table_frame, fg_color="transparent")
            error_frame.pack(pady=50)

            ctk.CTkLabel(
                error_frame,
                text=f"❌ Error loading spares: {str(e)}",
                font=("Arial", 14),
                text_color="#F44336",
            ).pack()

            ctk.CTkButton(
                error_frame,
                text="🔄 Try Again",
                width=120,
                height=35,
                command=self._load_spares,
            ).pack(pady=10)

    def _open_edit_dialog(self, spare):
        """Open dialog to edit or delete spare"""
        # Create dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title(f"Edit/Delete: {spare['name']}")
        dialog.geometry("600x650")  # Slightly larger
        dialog.resizable(False, False)
        dialog.transient(self.main_frame)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (650 // 2)
        dialog.geometry(f"+{x}+{y}")

        # === USE SCROLLABLE FRAME ===
        main_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Title with icon
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(pady=(0, 20))

        ctk.CTkLabel(title_frame, text="✏️", font=("Arial", 32)).pack()
        ctk.CTkLabel(title_frame, text=spare["name"], font=("Arial", 20, "bold")).pack(
            pady=(5, 0)
        )
        ctk.CTkLabel(
            title_frame,
            text=f"ID: {spare['id']}",
            font=("Arial", 12),
            text_color="gray",
        ).pack(pady=(5, 0))

        # Edit form
        form_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        form_frame.pack(fill="x", pady=10)

        # Configure grid
        form_frame.grid_columnconfigure(1, weight=1)

        # === ROWS START HERE ===
        row = 0

        # Spare Name
        ctk.CTkLabel(form_frame, text="Spare Name:", font=("Arial", 13, "bold")).grid(
            row=row, column=0, padx=20, pady=15, sticky="w"
        )
        name_var = ctk.StringVar(value=spare["name"])
        name_entry = ctk.CTkEntry(
            form_frame, width=300, textvariable=name_var, font=("Arial", 13)
        )
        name_entry.grid(row=row, column=1, padx=20, pady=15, sticky="w")

        # Spare Code
        row += 1
        ctk.CTkLabel(form_frame, text="Spare Code:", font=("Arial", 13, "bold")).grid(
            row=row, column=0, padx=20, pady=15, sticky="w"
        )
        code_var = ctk.StringVar(value=spare["code"])
        code_entry = ctk.CTkEntry(
            form_frame, width=200, textvariable=code_var, font=("Arial", 13)
        )
        code_entry.grid(row=row, column=1, padx=20, pady=15, sticky="w")

        # Current Quantity
        row += 1
        ctk.CTkLabel(
            form_frame, text="Current Quantity:", font=("Arial", 13, "bold")
        ).grid(row=row, column=0, padx=20, pady=15, sticky="w")
        quantity_var = ctk.StringVar(value=str(spare["quantity"]))
        quantity_entry = ctk.CTkEntry(
            form_frame, width=150, textvariable=quantity_var, font=("Arial", 13)
        )
        quantity_entry.grid(row=row, column=1, padx=20, pady=15, sticky="w")

        # Low Stock Threshold
        row += 1
        ctk.CTkLabel(
            form_frame, text="Low Stock Alert:", font=("Arial", 13, "bold")
        ).grid(row=row, column=0, padx=20, pady=15, sticky="w")
        threshold_var = ctk.StringVar(value=str(spare["low_stock_threshold"]))
        threshold_entry = ctk.CTkEntry(
            form_frame, width=150, textvariable=threshold_var, font=("Arial", 13)
        )
        threshold_entry.grid(row=row, column=1, padx=20, pady=15, sticky="w")

        # Notes
        row += 1
        ctk.CTkLabel(form_frame, text="Notes:", font=("Arial", 13, "bold")).grid(
            row=row, column=0, padx=20, pady=15, sticky="nw"
        )
        notes_text = ctk.CTkTextbox(
            form_frame, width=300, height=80, font=("Arial", 12)
        )
        notes_text.grid(row=row, column=1, padx=20, pady=15, sticky="w")

        # Load existing notes
        if spare.get("notes"):
            notes_text.insert("1.0", spare["notes"])

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=25)

        # Update button
        ctk.CTkButton(
            button_frame,
            text="💾 Update Spare",
            width=150,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#2196F3",
            command=lambda: self._update_spare(
                spare["id"],
                spare["name"],
                spare["code"],
                name_var.get(),
                code_var.get(),
                quantity_var.get(),
                threshold_var.get(),
                notes_text.get("1.0", "end-1c"),
                dialog,
            ),
        ).pack(side="left", padx=10)

        # Delete button
        ctk.CTkButton(
            button_frame,
            text="🗑️ Delete Spare",
            width=150,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=lambda: self._confirm_delete(spare["id"], spare["name"], dialog),
        ).pack(side="left", padx=10)

        # Cancel button
        ctk.CTkButton(
            button_frame,
            text="🔙 Cancel",
            width=100,
            height=45,
            font=("Arial", 14),
            fg_color="gray",
            command=dialog.destroy,
        ).pack(side="left", padx=10)

    def _update_spare(
        self,
        spare_id,
        original_name,
        original_code,
        new_name,
        new_code,
        qty_str,
        threshold_str,
        notes,
        dialog,
    ):
        """Update spare details including name, code, quantity, threshold and notes"""
        try:
            # Validate name
            if not new_name or not new_name.strip():
                MessageDialog.show_error(dialog, "Error", "Spare name cannot be empty")
                return

            # Validate code
            if not new_code or not new_code.strip():
                MessageDialog.show_error(dialog, "Error", "Spare code cannot be empty")
                return

            # Validate quantity
            try:
                quantity = int(qty_str)
                if quantity < 0:
                    MessageDialog.show_error(
                        dialog, "Error", "Quantity cannot be negative"
                    )
                    return
            except ValueError:
                MessageDialog.show_error(dialog, "Error", "Quantity must be a number")
                return

            # Validate threshold
            try:
                threshold = int(threshold_str)
                if threshold < 0:
                    MessageDialog.show_error(
                        dialog, "Error", "Threshold cannot be negative"
                    )
                    return
            except ValueError:
                MessageDialog.show_error(dialog, "Error", "Threshold must be a number")
                return

            # Check if code already exists (only if code was changed)
            from logic.db import db

            if new_code != original_code:
                existing = db.execute(
                    "SELECT id FROM spares WHERE code = ? AND id != ? AND is_active = 1",
                    (new_code.strip(), spare_id),
                    fetch=True,
                )
                if existing:
                    MessageDialog.show_error(
                        dialog,
                        "Error",
                        f"Spare code '{new_code}' already exists!\nPlease use a different code.",
                    )
                    return

            # UPDATE DATABASE
            db.execute(
                """
                UPDATE spares 
                SET name = ?, 
                    code = ?,
                    quantity = ?, 
                    low_stock_threshold = ?, 
                    notes = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    new_name.strip(),
                    new_code.strip(),
                    quantity,
                    threshold,
                    notes,
                    spare_id,
                ),
            )

            # Close dialog
            dialog.destroy()

            # Show success message
            MessageDialog.show_success(
                self.main_frame,
                "Success",
                f"✅ {new_name} updated successfully!\n\n"
                f"Code: {new_code}\n"
                f"Quantity: {quantity}\n"
                f"Alert Threshold: {threshold}",
            )

            # Refresh the spares list
            self._load_spares()

        except Exception as e:
            MessageDialog.show_error(dialog, "Error", f"Failed to update: {str(e)}")

    def _confirm_delete(self, spare_id, spare_name, dialog):
        """Confirm before deleting spare"""
        from UI.components.message_dialog import MessageDialog

        def delete_spare():
            try:
                from logic.db import db

                # Check if spare has any movements
                movements = db.execute(
                    "SELECT COUNT(*) as count FROM movements WHERE spare_id = ?",
                    (spare_id,),
                    fetch=True,
                )

                if movements and movements[0]["count"] > 0:
                    # Soft delete - mark as inactive (preserves history)
                    db.execute(
                        "UPDATE spares SET is_active = 0 WHERE id = ?", (spare_id,)
                    )
                    delete_type = "archived"
                else:
                    # Hard delete - no history, safe to remove
                    db.execute("DELETE FROM spares WHERE id = ?", (spare_id,))
                    delete_type = "deleted"

                # Close both dialogs
                dialog.destroy()

                # Show success message
                MessageDialog.show_success(
                    self.main_frame,
                    "Success",
                    f"✅ {spare_name} has been {delete_type} successfully!",
                )

                # Refresh the spares list
                self._load_spares()

            except Exception as e:
                MessageDialog.show_error(
                    self.main_frame, "Error", f"Failed to delete: {str(e)}"
                )

        MessageDialog.show_confirm(
            dialog,
            "Confirm Delete",
            f"Are you sure you want to delete '{spare_name}'?\n\nThis action cannot be undone.",
            delete_spare,
        )

    def destroy(self):
        """Clean up"""
        self.main_frame.destroy()
