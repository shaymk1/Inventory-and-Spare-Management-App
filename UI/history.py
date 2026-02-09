# ui/history.py
"""
Movement History Interface
Shows complete audit trail of all borrow/return activities WITH BORROWER NAMES
"""

import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import filedialog
import csv
from logic.db import db
from UI.components.message_dialog import MessageDialog


class MovementHistory:
    def __init__(self, parent_frame, user_info):
        """
        Initialize movement history interface

        Args:
            parent_frame: Frame to pack this interface into
            user_info: Current user information
        """
        self.parent = parent_frame
        self.user_info = user_info
        self.current_filters = {}

        # Create main container
        self.main_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self._create_interface()
        self._load_history()

    def _create_interface(self):
        """Create the history interface with filters"""
        # Title
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(pady=(0, 20))

        ctk.CTkLabel(
            title_frame, text="📜 Complete Movement History", font=("Arial", 22, "bold")
        ).pack()

        ctk.CTkLabel(
            title_frame,
            text="All borrow and return activities with borrower information",
            font=("Arial", 14),
            text_color="gray",
        ).pack(pady=(5, 0))

        # Filter controls
        filter_frame = ctk.CTkFrame(self.main_frame, height=100)
        filter_frame.pack(fill="x", pady=(0, 15))

        # Create two rows for filters
        top_row = ctk.CTkFrame(filter_frame, fg_color="transparent")
        top_row.pack(fill="x", pady=(10, 5), padx=10)

        bottom_row = ctk.CTkFrame(filter_frame, fg_color="transparent")
        bottom_row.pack(fill="x", pady=(5, 10), padx=10)

        # Row 1: Date and Type filters
        # Date Range
        ctk.CTkLabel(top_row, text="Date:", font=("Arial", 12)).pack(
            side="left", padx=(0, 10)
        )

        # Default dates (last 30 days)
        default_start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        default_end = datetime.now().strftime("%Y-%m-%d")

        self.date_start_entry = ctk.CTkEntry(
            top_row, width=120, placeholder_text="Start"
        )
        self.date_start_entry.pack(side="left", padx=5)
        self.date_start_entry.insert(0, default_start)

        ctk.CTkLabel(top_row, text="to", font=("Arial", 12)).pack(side="left", padx=5)

        self.date_end_entry = ctk.CTkEntry(top_row, width=120, placeholder_text="End")
        self.date_end_entry.pack(side="left", padx=5)
        self.date_end_entry.insert(0, default_end)

        # Movement type filter
        ctk.CTkLabel(top_row, text="Type:", font=("Arial", 12)).pack(
            side="left", padx=(20, 5)
        )

        self.type_var = ctk.StringVar(value="All")
        type_combo = ctk.CTkComboBox(
            top_row,
            values=["All", "Borrow", "Return"],
            variable=self.type_var,
            width=100,
            state="readonly",
        )
        type_combo.pack(side="left", padx=5)

        # Status filter
        ctk.CTkLabel(top_row, text="Status:", font=("Arial", 12)).pack(
            side="left", padx=(20, 5)
        )

        self.status_var = ctk.StringVar(value="All")
        status_combo = ctk.CTkComboBox(
            top_row,
            values=["All", "Pending", "Partial", "Complete"],
            variable=self.status_var,
            width=100,
            state="readonly",
        )
        status_combo.pack(side="left", padx=5)

        # Row 2: Spare and Borrower filters
        # Spare filter
        ctk.CTkLabel(bottom_row, text="Spare:", font=("Arial", 12)).pack(
            side="left", padx=(0, 5)
        )

        self.spare_var = ctk.StringVar(value="All")

        # Get spare list for filter
        try:
            spares = db.execute(
                "SELECT DISTINCT name FROM spares WHERE is_active = 1 ORDER BY name",
                fetch=True,
            )
            spare_names = ["All"] + [spare["name"] for spare in spares]
            self.spare_combo = ctk.CTkComboBox(
                bottom_row,
                values=spare_names,
                variable=self.spare_var,
                width=180,
                state="readonly",
            )
            self.spare_combo.pack(side="left", padx=5)
        except Exception as e:
            print(f"Error loading spares: {e}")
            self.spare_combo = ctk.CTkComboBox(
                bottom_row,
                values=["All"],
                variable=self.spare_var,
                width=180,
                state="readonly",
            )
            self.spare_combo.pack(side="left", padx=5)

        # Borrower filter
        ctk.CTkLabel(bottom_row, text="Borrower:", font=("Arial", 12)).pack(
            side="left", padx=(20, 5)
        )

        self.borrower_var = ctk.StringVar(value="All")

        # Get unique borrower names
        try:
            borrowers = db.execute(
                "SELECT DISTINCT borrower_name FROM movements WHERE borrower_name IS NOT NULL AND borrower_name != '' ORDER BY borrower_name",
                fetch=True,
            )
            borrower_names = ["All"] + [
                borrower["borrower_name"]
                for borrower in borrowers
                if borrower["borrower_name"]
            ]
            self.borrower_combo = ctk.CTkComboBox(
                bottom_row,
                values=borrower_names,
                variable=self.borrower_var,
                width=180,
                state="readonly",
            )
            self.borrower_combo.pack(side="left", padx=5)
        except Exception as e:
            print(f"Error loading borrowers: {e}")
            self.borrower_combo = ctk.CTkComboBox(
                bottom_row,
                values=["All"],
                variable=self.borrower_var,
                width=180,
                state="readonly",
            )
            self.borrower_combo.pack(side="left", padx=5)

        # Action buttons
        button_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(5, 0), padx=10)

        # Filter button
        ctk.CTkButton(
            button_frame,
            text="🔍 Apply Filters",
            width=120,
            height=35,
            font=("Arial", 12),
            command=self._apply_filter,
        ).pack(side="left", padx=(0, 10))

        # Clear filter button
        ctk.CTkButton(
            button_frame,
            text="🗑️ Clear All",
            width=100,
            height=35,
            font=("Arial", 12),
            fg_color="gray",
            command=self._clear_filter,
        ).pack(side="left", padx=5)

        # Export button
        ctk.CTkButton(
            button_frame,
            text="📤 Export CSV",
            width=120,
            height=35,
            font=("Arial", 12),
            fg_color="#4CAF50",
            command=self._export_csv,
        ).pack(side="left", padx=5)

        # Refresh button
        ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            width=100,
            height=35,
            font=("Arial", 12),
            command=self._refresh_history,
        ).pack(side="right", padx=5)

        # Create scrollable table area
        table_container = ctk.CTkFrame(self.main_frame)
        table_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Create scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            table_container, height=500, label_text=""
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Statistics frame
        self._create_statistics()

    def _create_statistics(self):
        """Create statistics display"""
        stats_frame = ctk.CTkFrame(self.main_frame, height=80)
        stats_frame.pack(fill="x", pady=(15, 5), padx=10)

        # Will be populated with data
        self.stats_labels = {}

        stats = [
            ("📊", "Total", "total"),
            ("⬇️", "Borrows", "borrows"),
            ("⬆️", "Returns", "returns"),
            ("👥", "Borrowers", "borrowers"),
            ("📦", "Items", "items"),
        ]

        for i, (icon, label, key) in enumerate(stats):
            stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_frame.pack(side="left", expand=True, padx=10)

            ctk.CTkLabel(stat_frame, text=icon, font=("Arial", 14)).pack()

            ctk.CTkLabel(
                stat_frame, text=label, font=("Arial", 10), text_color="gray"
            ).pack()

            value_label = ctk.CTkLabel(stat_frame, text="0", font=("Arial", 16, "bold"))
            value_label.pack()

            self.stats_labels[key] = value_label

    def _load_history(self, filters=None):
        """Load movement history with optional filters"""
        try:
            # Clear current table
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()

            # Store current filters
            if filters is not None:
                self.current_filters = filters
            elif not self.current_filters:
                # Initialize empty filters
                self.current_filters = {}

            # Build query with filters
            query = """
            SELECT 
                m.id,
                m.movement_date,
                m.movement_type,
                m.quantity,
                m.notes,
                m.returned_quantity,
                m.borrower_name,
                s.name as spare_name,
                s.code as spare_code,
                u.full_name as processed_by
            FROM movements m
            JOIN spares s ON m.spare_id = s.id
            JOIN users u ON m.user_id = u.id
            WHERE 1=1
            """
            params = []

            # Apply date range filter
            date_start = self.current_filters.get("date_start")
            date_end = self.current_filters.get("date_end")

            if date_start:
                query += " AND date(m.movement_date) >= ?"
                params.append(date_start)
            if date_end:
                query += " AND date(m.movement_date) <= ?"
                params.append(date_end)

            # Apply movement type filter
            movement_type = self.current_filters.get("movement_type")
            if movement_type and movement_type != "All":
                query += " AND m.movement_type = ?"
                params.append(movement_type.lower())

            # Apply spare name filter
            spare_name = self.current_filters.get("spare_name")
            if spare_name and spare_name != "All":
                query += " AND s.name = ?"
                params.append(spare_name)

            # Apply borrower filter
            borrower_name = self.current_filters.get("borrower_name")
            if borrower_name and borrower_name != "All":
                query += " AND m.borrower_name = ?"
                params.append(borrower_name)

            # Apply status filter (for borrows only)
            status = self.current_filters.get("status")
            if status and status != "All":
                if status == "Pending":
                    query += " AND m.movement_type = 'borrow' AND (m.returned_quantity IS NULL OR m.returned_quantity = 0)"
                elif status == "Partial":
                    query += " AND m.movement_type = 'borrow' AND m.returned_quantity > 0 AND m.returned_quantity < m.quantity"
                elif status == "Complete":
                    query += " AND ((m.movement_type = 'borrow' AND m.returned_quantity >= m.quantity) OR m.movement_type = 'return')"

            query += " ORDER BY m.movement_date DESC"

            # Execute query
            movements = db.execute(query, params, fetch=True)

            if not movements:
                # Show empty message
                empty_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
                empty_frame.pack(pady=100, expand=True)

                ctk.CTkLabel(
                    empty_frame,
                    text="📭 No movement history found",
                    font=("Arial", 16),
                    text_color="gray",
                ).pack()

                if any(self.current_filters.values()):
                    ctk.CTkLabel(
                        empty_frame,
                        text="Try changing your filters",
                        font=("Arial", 12),
                        text_color="gray",
                    ).pack(pady=10)

                # Clear statistics
                for key in self.stats_labels:
                    self.stats_labels[key].configure(text="0")
                return

            # Create table headers
            headers_frame = ctk.CTkFrame(
                self.scroll_frame, fg_color="#2b2b2b", height=40
            )
            headers_frame.grid(
                row=0, column=0, columnspan=8, sticky="ew", padx=5, pady=(0, 10)
            )

            headers = [
                "Date/Time",
                "Type",
                "Spare",
                "Quantity",
                "Borrower",
                "Processed By",
                "Notes",
                "Status",
            ]
            col_widths = [140, 70, 140, 70, 120, 120, 180, 100]

            for col, (header, width) in enumerate(zip(headers, col_widths)):
                label = ctk.CTkLabel(
                    headers_frame,
                    text=header,
                    font=("Arial", 11, "bold"),
                    width=width,
                    anchor="w",
                )
                label.grid(row=0, column=col, padx=5, pady=10, sticky="w")

            # Add movement rows
            for row, movement in enumerate(movements, start=1):
                # Alternate row colors
                row_bg = "#1a1a1a" if row % 2 == 0 else "#2b2b2b"

                # Format date
                date_str = movement["movement_date"]
                if date_str:
                    try:
                        # Try to parse the date string
                        if "T" in date_str:
                            date_obj = datetime.fromisoformat(
                                date_str.replace("T", " ")
                            )
                        else:
                            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]:
                                try:
                                    date_obj = datetime.strptime(date_str, fmt)
                                    break
                                except ValueError:
                                    continue
                            else:
                                date_obj = datetime.now()

                        display_date = date_obj.strftime("%b %d\n%H:%M")
                    except Exception:
                        display_date = date_str
                else:
                    display_date = "N/A"

                # Determine status and color
                movement_type = movement["movement_type"].lower()
                status = ""
                status_color = "white"

                if movement_type == "borrow":
                    returned = movement["returned_quantity"] or 0
                    quantity = movement["quantity"]

                    if returned == 0:
                        status = "⏳ Pending"
                        status_color = "#FF9800"
                    elif returned < quantity:
                        status = f"🔄 {returned}/{quantity}"
                        status_color = "#FFC107"
                    else:
                        status = "✅ Complete"
                        status_color = "#4CAF50"
                elif movement_type == "return":
                    status = "✅ Returned"
                    status_color = "#4CAF50"

                # Get borrower name - for returns, show original borrower
                borrower = movement["borrower_name"] or "N/A"

                # Truncate long text
                spare_name = movement["spare_name"]
                if len(spare_name) > 18:
                    spare_display = spare_name[:16] + "..."
                else:
                    spare_display = spare_name

                spare_text = f"{spare_display}\n({movement['spare_code']})"

                # Display data
                data = [
                    display_date,
                    movement_type.title(),
                    spare_text,
                    str(movement["quantity"]),
                    borrower,
                    movement["processed_by"],
                    (movement["notes"] or "")[:35]
                    + ("..." if len(movement["notes"] or "") > 35 else ""),
                    status,
                ]

                # Create row frame
                row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=row_bg, height=40)
                row_frame.grid(
                    row=row, column=0, columnspan=8, sticky="ew", padx=5, pady=2
                )

                for col, (value, width) in enumerate(zip(data, col_widths)):
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        font=("Arial", 10),
                        width=width,
                        anchor="w",
                        text_color=status_color if col == 7 else "white",
                    )
                    label.grid(row=0, column=col, padx=5, pady=8, sticky="w")

            # Update statistics
            self._update_statistics(movements)

        except Exception as e:
            print(f"Error loading history: {e}")
            MessageDialog.show_error(
                self.main_frame, "Error", f"Failed to load history:\n{str(e)}"
            )

    def _update_statistics(self, movements):
        """Update statistics display"""
        try:
            total = len(movements)
            borrows = sum(
                1 for m in movements if m["movement_type"].lower() == "borrow"
            )
            returns = sum(
                1 for m in movements if m["movement_type"].lower() == "return"
            )

            # Count unique borrowers (excluding returns and empty names)
            borrowers = len(
                set(
                    m["borrower_name"]
                    for m in movements
                    if m["borrower_name"] and m["borrower_name"] != "N/A"
                )
            )

            # Count unique items
            items = len(set(m["spare_name"] for m in movements))

            self.stats_labels["total"].configure(text=str(total))
            self.stats_labels["borrows"].configure(text=str(borrows))
            self.stats_labels["returns"].configure(text=str(returns))
            self.stats_labels["borrowers"].configure(text=str(borrowers))
            self.stats_labels["items"].configure(text=str(items))

        except Exception as e:
            print(f"Error updating statistics: {e}")

    def _apply_filter(self):
        """Apply filters to history"""
        filters = {}

        # Date filters
        start_date = self.date_start_entry.get().strip()
        end_date = self.date_end_entry.get().strip()

        if start_date:
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                filters["date_start"] = start_date
            except ValueError:
                MessageDialog.show_error(
                    self.main_frame,
                    "Invalid Date",
                    "Start date must be in YYYY-MM-DD format",
                )
                return

        if end_date:
            try:
                datetime.strptime(end_date, "%Y-%m-%d")
                filters["date_end"] = end_date
            except ValueError:
                MessageDialog.show_error(
                    self.main_frame,
                    "Invalid Date",
                    "End date must be in YYYY-MM-DD format",
                )
                return

        # Type filter
        movement_type = self.type_var.get()
        if movement_type != "All":
            filters["movement_type"] = movement_type

        # Spare filter
        spare_name = self.spare_var.get()
        if spare_name != "All":
            filters["spare_name"] = spare_name

        # Borrower filter
        borrower_name = self.borrower_var.get()
        if borrower_name != "All":
            filters["borrower_name"] = borrower_name

        # Status filter
        status = self.status_var.get()
        if status != "All":
            filters["status"] = status

        # Load with filters
        self._load_history(filters)

    def _clear_filter(self):
        """Clear all filters"""
        # Reset UI elements
        default_start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        default_end = datetime.now().strftime("%Y-%m-%d")

        self.date_start_entry.delete(0, "end")
        self.date_start_entry.insert(0, default_start)

        self.date_end_entry.delete(0, "end")
        self.date_end_entry.insert(0, default_end)

        self.type_var.set("All")
        self.spare_var.set("All")
        self.borrower_var.set("All")
        self.status_var.set("All")

        # Clear filters and reload
        self.current_filters = {}
        self._load_history()

    def _refresh_history(self):
        """Refresh history with current filters"""
        self._load_history(self.current_filters)

    def _export_csv(self):
        """Export history to CSV"""
        try:
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save History as CSV",
            )

            if not filename:
                return

            # Build query with current filters
            query = """
            SELECT 
                m.movement_date,
                m.movement_type,
                m.quantity,
                m.notes,
                m.returned_quantity,
                m.borrower_name,
                s.name as spare_name,
                s.code as spare_code,
                u.full_name as processed_by
            FROM movements m
            JOIN spares s ON m.spare_id = s.id
            JOIN users u ON m.user_id = u.id
            WHERE 1=1
            """
            params = []

            # Apply current filters
            if self.current_filters.get("date_start"):
                query += " AND date(m.movement_date) >= ?"
                params.append(self.current_filters["date_start"])
            if self.current_filters.get("date_end"):
                query += " AND date(m.movement_date) <= ?"
                params.append(self.current_filters["date_end"])

            movement_type = self.current_filters.get("movement_type")
            if movement_type and movement_type != "All":
                query += " AND m.movement_type = ?"
                params.append(movement_type.lower())

            spare_name = self.current_filters.get("spare_name")
            if spare_name and spare_name != "All":
                query += " AND s.name = ?"
                params.append(spare_name)

            borrower_name = self.current_filters.get("borrower_name")
            if borrower_name and borrower_name != "All":
                query += " AND m.borrower_name = ?"
                params.append(borrower_name)

            status = self.current_filters.get("status")
            if status and status != "All":
                if status == "Pending":
                    query += " AND m.movement_type = 'borrow' AND (m.returned_quantity IS NULL OR m.returned_quantity = 0)"
                elif status == "Partial":
                    query += " AND m.movement_type = 'borrow' AND m.returned_quantity > 0 AND m.returned_quantity < m.quantity"
                elif status == "Complete":
                    query += " AND ((m.movement_type = 'borrow' AND m.returned_quantity >= m.quantity) OR m.movement_type = 'return')"

            query += " ORDER BY m.movement_date DESC"

            # Get data
            movements = db.execute(query, params, fetch=True)

            if not movements:
                MessageDialog.show_info(
                    self.main_frame, "No Data", "No movement history to export"
                )
                return

            # Write to CSV
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = [
                    "Date/Time",
                    "Type",
                    "Spare Name",
                    "Spare Code",
                    "Quantity",
                    "Returned",
                    "Borrower",
                    "Processed By",
                    "Notes",
                    "Status",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for movement in movements:
                    # Determine status
                    movement_type = movement["movement_type"].lower()
                    returned = movement["returned_quantity"] or 0
                    quantity = movement["quantity"]

                    if movement_type == "borrow":
                        if returned == 0:
                            status = "Pending"
                        elif returned < quantity:
                            status = f"Partial ({returned}/{quantity})"
                        else:
                            status = "Complete"
                    else:
                        status = "Returned"

                    writer.writerow(
                        {
                            "Date/Time": movement["movement_date"],
                            "Type": movement_type.title(),
                            "Spare Name": movement["spare_name"],
                            "Spare Code": movement["spare_code"],
                            "Quantity": movement["quantity"],
                            "Returned": returned,
                            "Borrower": movement["borrower_name"] or "",
                            "Processed By": movement["processed_by"],
                            "Notes": movement["notes"] or "",
                            "Status": status,
                        }
                    )

            MessageDialog.show_success(
                self.main_frame,
                "Export Complete",
                f"✅ History exported successfully!\n\nLocation: {filename}\nRecords: {len(movements)}",
            )

        except Exception as e:
            print(f"Error exporting CSV: {e}")
            MessageDialog.show_error(
                self.main_frame, "Export Failed", f"Failed to export CSV:\n{str(e)}"
            )

    def destroy(self):
        """Clean up"""
        self.main_frame.destroy()
